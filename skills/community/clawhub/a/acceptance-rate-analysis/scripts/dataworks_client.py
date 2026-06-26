from __future__ import annotations

import json
import os
import time
from typing import Any

import httpx
from loguru import logger


DEFAULT_ENDPOINT = os.getenv(
    "DATAWORKS_METRIC_ENDPOINT",
    "https://dataworks-metric.jirongyunke.net/dataworks-metric/metric/data/query/agent/queryMetricData",
)
DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_ACCESS_TOKEN = os.getenv("BIGDATA_ACCESS_TOKEN")


class DataworksQueryError(RuntimeError):
    def __init__(self, message: str, *, code: str | None = None, payload: Any | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.payload = payload


def json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def metric(name: str, metric_label: str | None = None, metric_type: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"name": name}
    if metric_label:
        payload["metricLabel"] = metric_label
    if metric_type:
        payload["metricType"] = metric_type
    return payload


def dimension(name: str, entity_name: str, time_granularity: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "name": name,
        "dimLabel": name,
        "entityName": entity_name,
    }
    if time_granularity:
        payload["timeGranularity"] = time_granularity
    return payload


def build_time_rule(
    *,
    name: str,
    entity_name: str,
    start: str,
    end: str,
    time_granularity: str = "day",
) -> dict[str, Any]:
    return {
        "id": int(time.time() * 1000),
        "name": name,
        "type": "1",
        "entityName": entity_name,
        "dimensionType": "time",
        "conditions": [
            {
                "operator": "在区间内",
                "symbol": "BETWEEN",
                "value": [start, end],
            }
        ],
        "originalType": "",
        "logicalType": "time",
        "timeGranularity": time_granularity,
    }


def build_equals_rule(*, name: str, entity_name: str, value: str) -> dict[str, Any]:
    return {
        "id": int(time.time() * 1000),
        "name": name,
        "type": "1",
        "entityName": entity_name,
        "dimensionType": "categorical",
        "conditions": [
            {
                "operator": "等于",
                "symbol": "=",
                "value": value,
            }
        ],
        "originalType": "",
        "logicalType": "string",
        "timeGranularity": None,
    }


def build_filter(rules: list[dict[str, Any]]) -> str:
    payload = {
        "logic": "且",
        "symbol": "AND",
        "rules": rules,
    }
    return json.dumps(payload, ensure_ascii=False)


def extract_row_value(row: dict[str, Any], field_name: str) -> Any:
    if field_name in row:
        return row[field_name]

    exact_suffix = f"__{field_name}"
    surrounded = f"__{field_name}__"
    dim_surrounded = f"__dim_{field_name}__"
    candidates: list[str] = []
    for key in row:
        if key.endswith(exact_suffix) or surrounded in key or dim_surrounded in key:
            candidates.append(key)
    if len(candidates) == 1:
        return row[candidates[0]]
    if candidates:
        candidates.sort(key=len)
        return row[candidates[0]]
    return None


def _normalize_metric_list(metric_list: list[str | dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in metric_list:
        if isinstance(item, str):
            normalized.append({"name": item})
        else:
            normalized.append(item)
    return normalized


def _normalize_dimension_list(dimension_list: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    return list(dimension_list or [])


def _map_response_rows(column_head_list: list[Any], data_list: list[Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    headers = [str(item) for item in column_head_list]
    for raw_row in data_list:
        if isinstance(raw_row, dict):
            rows.append(raw_row)
            continue
        if not isinstance(raw_row, list):
            continue
        mapped = {
            headers[index]: raw_row[index]
            for index in range(min(len(headers), len(raw_row)))
        }
        rows.append(mapped)
    return rows


def query_metric_data(
    *,
    access_token: str | None = None,
    data_model_set_name: str,
    metric_list: list[str | dict[str, Any]],
    dimension_list: list[dict[str, Any]] | None = None,
    row_dimension_list: list[dict[str, Any]] | None = None,
    column_dimension_list: list[dict[str, Any]] | None = None,
    filter_payload: str | dict[str, Any] | None = None,
    endpoint: str | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "dataModelSetName": data_model_set_name,
        "metricList": _normalize_metric_list(metric_list),
    }

    if row_dimension_list is not None or column_dimension_list is not None:
        payload["sql"] = ""
        payload["rowDimensionList"] = _normalize_dimension_list(row_dimension_list)
        payload["columnDimensionList"] = _normalize_dimension_list(column_dimension_list)
        payload["isComparison"] = False
    else:
        payload["dimensionList"] = _normalize_dimension_list(dimension_list)

    if filter_payload is not None:
        if isinstance(filter_payload, dict):
            payload["filter"] = json.dumps(filter_payload, ensure_ascii=False)
        else:
            payload["filter"] = filter_payload

    # 请求体 JSON 不含 Cookie/token。默认写入调试文件，便于核对取数参数与原始返回数据。
    # 若需关闭大量输出：DATAWORKS_QUERY_LOG=0
    if os.getenv("DATAWORKS_QUERY_LOG", "1").strip().lower() not in {"0", "false", "no"}:
        logger.info(
            "[query_metric_data] POST {}\n{}",
            endpoint or DEFAULT_ENDPOINT,
            json.dumps(payload, ensure_ascii=False, indent=2),
        )

    response = httpx.post(
        endpoint or DEFAULT_ENDPOINT,
        headers={
            "Cookie": f"bigdata_access_token={access_token or DEFAULT_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout_seconds,
    )
    response.raise_for_status()
    raw_payload = response.json()
    if raw_payload.get("code") != "S200":
        raise DataworksQueryError(
            raw_payload.get("message") or "DataWorks 查询失败",
            code=str(raw_payload.get("code") or ""),
            payload=raw_payload,
        )

    data = raw_payload.get("data") or {}
    column_head_list = list(data.get("columnHeadList") or [])
    data_list = list(data.get("dataList") or [])
    if os.getenv("DATAWORKS_QUERY_LOG", "1").strip().lower() not in {"0", "false", "no"}:
        logger.info(
            "[query_metric_data] 响应摘要 {}",
            json.dumps(
                {
                    "code": raw_payload.get("code"),
                    "row_count": len(data_list),
                    "column_head_list": column_head_list,
                },
                ensure_ascii=False,
                default=str,
            ),
        )
        logger.info(
            "[query_metric_data] 响应原始数据 {}",
            json.dumps(
                {
                    "sql": data.get("sql"),
                    "column_head_list": column_head_list,
                    "data_list": data_list,
                    "rows": _map_response_rows(column_head_list, data_list),
                },
                ensure_ascii=False,
                default=str,
            ),
        )

    return {
        "code": raw_payload.get("code"),
        "message": raw_payload.get("message"),
        "payload": payload,
        "raw": raw_payload,
        "sql": data.get("sql"),
        "column_head_list": column_head_list,
        "rows": _map_response_rows(column_head_list, data_list),
    }
