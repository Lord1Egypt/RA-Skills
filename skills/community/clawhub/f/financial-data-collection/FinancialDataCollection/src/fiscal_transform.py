from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from .fiscal_parser import build_period_label, is_combined_jan_feb, previous_month


def build_derived_metrics(
    extracted_records: List[dict],
    scope_year: Optional[int] = None,
    scope_month: Optional[str] = None,
    scope_start_month: Optional[str] = None,
    scope_end_month: Optional[str] = None,
) -> Tuple[List[dict], List[dict]]:
    records_by_metric: Dict[str, Dict[str, dict]] = defaultdict(dict)
    records_by_month_metric: Dict[Tuple[str, str], dict] = {}
    for record in extracted_records:
        month = record["metric_month"]
        metric_name = record["standard_metric_name"]
        records_by_metric[metric_name][month] = record
        records_by_month_metric[(month, metric_name)] = record

    derived: List[dict] = []
    issues: List[dict] = []

    target_months = sorted({record["metric_month"] for record in extracted_records})
    if scope_year is not None:
        target_months = [month for month in target_months if month.startswith(f"{scope_year:04d}-")]
    if scope_start_month is not None and scope_end_month is not None:
        target_months = [month for month in target_months if scope_start_month <= month <= scope_end_month]
    if scope_month is not None:
        if scope_month.endswith("-01") or scope_month.endswith("-02"):
            target_year = scope_month.split("-")[0]
            target_months = [month for month in target_months if month == f"{target_year}-02"]
        else:
            target_months = [month for month in target_months if month == scope_month]

    for metric_name, month_map in records_by_metric.items():
        for month in target_months:
            if month not in month_map:
                continue
            current = month_map[month]
            if is_combined_jan_feb(current.get("period_text", ""), month):
                year = month.split("-")[0]
                avg_value = round(current["value"] / 2, 6)
                for split_month in (f"{year}-01", f"{year}-02"):
                    derived.append(
                        _make_derived_record(
                            month=split_month,
                            period_label=split_month,
                            metric_name=metric_name,
                            metric_category=current["metric_category"],
                            source_order=current.get("source_order", 999999),
                            value=avg_value,
                            yoy_growth=current.get("yoy_growth"),
                            formula=f"{year}-01~02={current['value']}/2",
                            source_record_ids=current["record_id"],
                            source_document_ids=current["source_document_id"],
                            derived_type="average_from_jan_feb_combined",
                            is_derived=True,
                            remark="1-2月合并值按平均值拆分为1月和2月",
                        )
                    )
                continue
            prev = previous_month(month)
            if prev is None:
                derived.append(
                    _make_derived_record(
                        month=month,
                        period_label=build_period_label(current.get("period_text", month), month),
                        metric_name=metric_name,
                        metric_category=current["metric_category"],
                        source_order=current.get("source_order", 999999),
                        value=current["value"],
                        yoy_growth=current.get("yoy_growth"),
                        formula=f"{month}={current['value']}",
                        source_record_ids=current["record_id"],
                        source_document_ids=current["source_document_id"],
                        derived_type="single_month_from_january_cumulative",
                        is_derived=False,
                        remark="",
                    )
                )
                continue
            previous = month_map.get(prev)
            if previous is None:
                issues.append(
                    {
                        "metric_month": month,
                        "standard_metric_name": metric_name,
                        "issue_type": "missing_previous_cumulative",
                        "detail": f"缺少上期累计值: {prev}",
                    }
                )
                continue
            value = round(current["value"] - previous["value"], 6)
            derived.append(
                _make_derived_record(
                    month=month,
                    period_label=month,
                    metric_name=metric_name,
                    metric_category=current["metric_category"],
                    source_order=current.get("source_order", 999999),
                    value=value,
                    yoy_growth=None,
                    formula=f"{month}={current['value']}-{previous['value']}",
                    source_record_ids=f"{current['record_id']},{previous['record_id']}",
                    source_document_ids=f"{current['source_document_id']},{previous['source_document_id']}",
                    derived_type="monthly_from_cumulative_difference",
                    is_derived=True,
                    remark="",
                )
            )

    derived_by_month_metric = {(item["metric_month"], item["standard_metric_name"]): item for item in derived}
    deficit_months = sorted({item["metric_month"] for item in derived})
    for month in deficit_months:
        narrow = _compute_deficit(
            month,
            derived_by_month_metric,
            "全国一般公共预算收入",
            "全国一般公共预算支出",
            "窄口径赤字",
            "一般公共预算赤字",
        )
        if narrow:
            derived.append(narrow)
        wide = _compute_wide_deficit(month, derived_by_month_metric)
        if wide:
            derived.append(wide)
    return derived, issues


def _compute_deficit(month: str, derived_by_month_metric: Dict[Tuple[str, str], dict], income_metric: str, spend_metric: str, name: str, category: str) -> Optional[dict]:
    income = derived_by_month_metric.get((month, income_metric))
    spend = derived_by_month_metric.get((month, spend_metric))
    if not income or not spend:
        return None
    period_label = spend.get("period_label") or income.get("period_label") or month
    return _make_derived_record(
        month=month,
        period_label=period_label,
        metric_name=name,
        metric_category=category,
        source_order=min(spend.get("source_order", 999999), income.get("source_order", 999999)),
        value=round(spend["value"] - income["value"], 6),
        yoy_growth=None,
        formula=f"{name}={spend_metric}-{income_metric}",
        source_record_ids=f"{spend['source_record_ids']},{income['source_record_ids']}",
        source_document_ids=f"{spend['source_document_ids']},{income['source_document_ids']}",
        derived_type="deficit_metric",
        is_derived=True,
        remark="",
    )


def _compute_wide_deficit(month: str, derived_by_month_metric: Dict[Tuple[str, str], dict]) -> Optional[dict]:
    metrics = {
        "g_income": derived_by_month_metric.get((month, "全国一般公共预算收入")),
        "g_spend": derived_by_month_metric.get((month, "全国一般公共预算支出")),
        "f_income": derived_by_month_metric.get((month, "全国政府性基金预算收入")),
        "f_spend": derived_by_month_metric.get((month, "全国政府性基金预算支出")),
    }
    if any(value is None for value in metrics.values()):
        return None
    period_label = next((item.get("period_label") for item in metrics.values() if item and item.get("period_label")), month)
    value = round(metrics["g_spend"]["value"] + metrics["f_spend"]["value"] - metrics["g_income"]["value"] - metrics["f_income"]["value"], 6)
    return _make_derived_record(
        month=month,
        period_label=period_label,
        metric_name="宽口径赤字",
        metric_category="合并口径赤字",
        source_order=1000000,
        value=value,
        yoy_growth=None,
        formula="宽口径赤字=(全国一般公共预算支出+全国政府性基金预算支出)-(全国一般公共预算收入+全国政府性基金预算收入)",
        source_record_ids=",".join(item["source_record_ids"] for item in metrics.values()),
        source_document_ids=",".join(item["source_document_ids"] for item in metrics.values()),
        derived_type="deficit_metric",
        is_derived=True,
        remark="",
    )


def _make_derived_record(
    month: str,
    period_label: str,
    metric_name: str,
    metric_category: str,
    source_order: int,
    value: float,
    yoy_growth: Optional[float],
    formula: str,
    source_record_ids: str,
    source_document_ids: str,
    derived_type: str,
    is_derived: bool,
    remark: str,
) -> dict:
    return {
        "metric_month": month,
        "period_label": period_label,
        "standard_metric_name": metric_name,
        "metric_category": metric_category,
        "source_order": source_order,
        "value": value,
        "unit": "亿元",
        "yoy_growth": yoy_growth,
        "derived_type": derived_type,
        "formula": formula,
        "source_record_ids": source_record_ids,
        "source_document_ids": source_document_ids,
        "is_derived_metric": is_derived,
        "remark": remark,
    }
