import os
import sys
import time
from io import TextIOWrapper
from typing import Any, Dict, List, Optional, Tuple

import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import GTS_AUTHORIZATION, GANGTISE_DATA_DOMAIN, check_version, format_response, THEME_NAME_TO_ID

CHAINED_AGENT_PAIRS = {
    "viewpoint-debate": ("viewpoint-debate-getid", "viewpoint-debate-getcontent"),
    "earnings-review": ("earnings-review-getid", "earnings-review-getcontent"),
}

CHAIN_POLL_MAX_SECONDS = 600
CHAIN_POLL_INTERVAL_SECONDS = 3
STEP_AGENT_TYPES = {"earnings-review-getid", "earnings-review-getcontent", "viewpoint-debate-getid", "viewpoint-debate-getcontent"}

AGENT_ENDPOINTS = {
    "one-pager": "/one-pager",
    "investment-logic": "/investment-logic",
    "peer-comparison": "/peer-comparison",
    "earnings-review-getid": "/earnings-review-getid",
    "earnings-review-getcontent": "/earnings-review-getcontent",
    "viewpoint-debate-getid": "/viewpoint-debate-getid",
    "viewpoint-debate-getcontent": "/viewpoint-debate-getcontent",
    "theme-tracking": "/theme-tracking",
    "research-outline": "/research-outline",
}

AGENT_METHOD_NAME_MAP = {
    "one-pager": "one_pager",
    "investment-logic": "investment_logic",
    "peer-comparison": "peer_comparison",
    "earnings-review": "earnings_review",
    "earnings-review-getid": "earnings_review_getid",
    "earnings-review-getcontent": "earnings_review_getcontent",
    "viewpoint-debate": "viewpoint_debate",
    "viewpoint-debate-getid": "viewpoint_debate_getid",
    "viewpoint-debate-getcontent": "viewpoint_debate_getcontent",
    "theme-tracking": "theme_tracking",
    "research-outline": "research_outline",
}
PUBLIC_AGENT_TYPES = sorted([k for k in AGENT_ENDPOINTS.keys() if k not in STEP_AGENT_TYPES] + list(CHAINED_AGENT_PAIRS.keys()))


def _normalize_list(raw: Optional[str]) -> Optional[List[str]]:
    if not raw:
        return None
    result: List[str] = []
    for item in str(raw).replace("，", ",").split(","):
        value = item.strip()
        if value and value not in result:
            result.append(value)
    return result or None


def _resolve_theme_id(theme_input: Optional[str]) -> Optional[str]:
    if theme_input is None:
        return None
    value = str(theme_input).strip()
    if not value:
        return None
    if value.isdigit():
        return value
    return THEME_NAME_TO_ID.get(value)


def _format_payload(
    agent_type: str,
    security_code: Optional[str] = None,
    period: Optional[str] = None,
    data_id: Optional[str] = None,
    viewpoint: Optional[str] = None,
    theme_id: Optional[str] = None,
    date: Optional[str] = None,
    types: Optional[List[str]] = None,
) -> Dict:
    if agent_type == "earnings-review":
        return _format_payload(
            "earnings-review-getid",
            security_code=security_code,
            period=period,
            data_id=data_id,
            viewpoint=viewpoint,
            theme_id=theme_id,
            date=date,
            types=types,
        )
    if agent_type == "viewpoint-debate":
        return _format_payload(
            "viewpoint-debate-getid",
            security_code=security_code,
            period=period,
            data_id=data_id,
            viewpoint=viewpoint,
            theme_id=theme_id,
            date=date,
            types=types,
        )
    if agent_type in {"one-pager", "investment-logic", "peer-comparison", "research-outline"}:
        if not security_code:
            raise ValueError(f"{agent_type} 需要参数 --security-code")
        return {"securityCode": security_code}
    if agent_type == "earnings-review-getid":
        if not security_code:
            raise ValueError("earnings-review-getid 需要参数 --security-code")
        if not period:
            raise ValueError("earnings-review-getid 需要参数 --period（示例：2025q3）")
        return {"securityCode": security_code, "period": period}
    if agent_type == "earnings-review-getcontent":
        if not data_id:
            raise ValueError("earnings-review-getcontent 需要参数 --data-id")
        return {"dataId": data_id}
    if agent_type == "viewpoint-debate-getid":
        if not viewpoint or not str(viewpoint).strip():
            raise ValueError("viewpoint-debate-getid 需要参数 --viewpoint（观点文本，不超过 1000 字）")
        v = str(viewpoint).strip()
        if len(v) > 1000:
            raise ValueError("viewpoint 长度不能超过 1000 字")
        return {"viewpoint": v}
    if agent_type == "viewpoint-debate-getcontent":
        if not data_id:
            raise ValueError("viewpoint-debate-getcontent 需要参数 --data-id")
        return {"dataId": data_id}
    if agent_type == "theme-tracking":
        resolved_theme_id = _resolve_theme_id(theme_id)
        if not resolved_theme_id:
            raise ValueError("theme-tracking 需要参数 --theme-id（支持主题 ID 或中文主题名）")
        if not date:
            raise ValueError("theme-tracking 需要参数 --date（yyyy-MM-dd）")
        if not types:
            raise ValueError("theme-tracking 需要参数 --type（morning/night，可逗号分隔）")
        return {"themeId": resolved_theme_id, "date": date, "type": types}
    raise ValueError(f"不支持的 agent-type: {agent_type}")


def _normalize_agent_response(agent_type: str, body: Dict) -> Dict:
    ok = str(body.get("code", "")) == "000000" and body.get("status") is True
    if not ok:
        return {
            "state": "error",
            "message": body.get("msg", "请求失败"),
            "data": [],
            "usage": {},
        }

    raw_data = body.get("data")
    rows: List[Dict] = []

    if agent_type in {"earnings-review-getid", "viewpoint-debate-getid"}:
        rows = [{"dataId": body.get("dataId", "")}]
    elif agent_type == "theme-tracking":
        data_list = raw_data if isinstance(raw_data, list) else []
        for item in data_list:
            if not isinstance(item, dict):
                continue
            rows.append(
                {
                    "type": item.get("type", ""),
                    "date": item.get("date", ""),
                    "content": item.get("content", ""),
                }
            )
    elif isinstance(raw_data, dict):
        rows = [
            {
                "date": raw_data.get("date", ""),
                "content": raw_data.get("content", ""),
            }
        ]
    elif isinstance(raw_data, list):
        for item in raw_data:
            if isinstance(item, dict):
                rows.append({"date": item.get("date", ""), "content": item.get("content", "")})
    else:
        rows = [{"content": str(raw_data) if raw_data is not None else ""}]

    return {
        "state": "success",
        "message": body.get("msg", "请求成功"),
        "data": [{"data": rows, "module": "agent", "type": agent_type}],
        "usage": {},
    }


def _raw_post_agent(agent_type: str, payload: Dict) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    url = f"{GANGTISE_DATA_DOMAIN}{AGENT_ENDPOINTS[agent_type]}"
    headers = {"Authorization": GTS_AUTHORIZATION}
    resp = requests.post(url, headers=headers, json=payload, timeout=300)
    if resp.status_code != 200:
        return None, resp.text
    try:
        return resp.json(), None
    except Exception as e:
        return None, str(e)


def _getcontent_response_ready(body: Dict) -> bool:
    if str(body.get("code", "")) != "000000" or body.get("status") is not True:
        return False
    raw = body.get("data")
    if isinstance(raw, dict):
        return bool(str(raw.get("content", "")).strip())
    return False


def _openapi_agent_chained(
    composite_type: str,
    security_code: Optional[str],
    period: Optional[str],
    viewpoint: Optional[str],
    theme_id: Optional[str],
    date: Optional[str],
    types: Optional[List[str]],
    output: Optional[str],
) -> str:
    getid_type, getcontent_type = CHAINED_AGENT_PAIRS[composite_type]
    method = AGENT_METHOD_NAME_MAP.get(composite_type, "agent")

    try:
        payload_getid = _format_payload(
            composite_type,
            security_code=security_code,
            period=period,
            data_id=None,
            viewpoint=viewpoint,
            theme_id=theme_id,
            date=date,
            types=types,
        )
    except Exception as e:
        return format_response({"state": "error", "message": str(e), "data": [], "usage": {}}, method, output=output)

    body, err = _raw_post_agent(getid_type, payload_getid)
    if err is not None:
        return format_response({"state": "error", "message": err, "data": [], "usage": {}}, method, output=output)
    if body is None:
        return format_response({"state": "error", "message": "空响应", "data": [], "usage": {}}, method, output=output)

    if str(body.get("code", "")) != "000000" or body.get("status") is not True:
        return format_response(
            {
                "state": "error",
                "message": body.get("msg", "getId 请求失败"),
                "data": [],
                "usage": {},
            },
            method,
            output=output,
        )

    data_id = body.get("dataId")
    if not data_id:
        return format_response(
            {"state": "error", "message": "getId 响应缺少 dataId", "data": [], "usage": {}},
            method,
            output=output,
        )

    deadline = time.monotonic() + CHAIN_POLL_MAX_SECONDS
    last_detail = ""

    while time.monotonic() < deadline:
        payload_content = {"dataId": data_id}
        cbody, cerr = _raw_post_agent(getcontent_type, payload_content)
        if cerr is not None:
            last_detail = cerr
        elif cbody is not None:
            if _getcontent_response_ready(cbody):
                normalized = _normalize_agent_response(getcontent_type, cbody)
                if normalized["state"] == "success" and normalized.get("data"):
                    normalized["data"][0]["type"] = composite_type
                return format_response(normalized, method, output=output)
            last_detail = cbody.get("msg", "内容未就绪或为空")

        time.sleep(CHAIN_POLL_INTERVAL_SECONDS)

    return format_response(
        {
            "state": "error",
            "message": f"轮询 getContent 超时（{CHAIN_POLL_MAX_SECONDS}s），dataId={data_id}。最后状态：{last_detail}",
            "data": [],
            "usage": {},
        },
        method,
        output=output,
    )


def openapi_agent(
    agent_type: str,
    security_code: Optional[str] = None,
    period: Optional[str] = None,
    data_id: Optional[str] = None,
    viewpoint: Optional[str] = None,
    theme_id: Optional[str] = None,
    date: Optional[str] = None,
    types: Optional[List[str]] = None,
    output: Optional[str] = None,
):
    if GTS_AUTHORIZATION is None:
        return format_response(
            {"state": "error", "message": "未配置 gangtise 授权，无法调用 open 接口", "data": [], "usage": {}},
            "agent",
            output=output,
        )

    if agent_type in STEP_AGENT_TYPES:
        return format_response(
            {
                "state": "error",
                "message": f"{agent_type} 仅支持内部串联调用，请使用 earnings-review 或 viewpoint-debate",
                "data": [],
                "usage": {},
            },
            "agent",
            output=output,
        )

    if agent_type not in AGENT_ENDPOINTS and agent_type not in CHAINED_AGENT_PAIRS:
        return format_response(
            {"state": "error", "message": f"不支持的 agent-type: {agent_type}", "data": [], "usage": {}},
            "agent",
            output=output,
        )

    if agent_type in CHAINED_AGENT_PAIRS:
        return _openapi_agent_chained(
            composite_type=agent_type,
            security_code=security_code,
            period=period,
            viewpoint=viewpoint,
            theme_id=theme_id,
            date=date,
            types=types,
            output=output,
        )

    try:
        payload = _format_payload(
            agent_type=agent_type,
            security_code=security_code,
            period=period,
            data_id=data_id,
            viewpoint=viewpoint,
            theme_id=theme_id,
            date=date,
            types=types,
        )
    except Exception as e:
        return format_response(
            {"state": "error", "message": str(e), "data": [], "usage": {}},
            AGENT_METHOD_NAME_MAP.get(agent_type, "agent"),
            output=output,
        )

    try:
        body, err = _raw_post_agent(agent_type, payload)
        if err is not None:
            return format_response(
                {"state": "error", "message": err, "data": [], "usage": {}},
                AGENT_METHOD_NAME_MAP.get(agent_type, "agent"),
                output=output,
            )
        if body is None:
            return format_response(
                {"state": "error", "message": "空响应", "data": [], "usage": {}},
                AGENT_METHOD_NAME_MAP.get(agent_type, "agent"),
                output=output,
            )
        normalized = _normalize_agent_response(agent_type, body)
        return format_response(normalized, AGENT_METHOD_NAME_MAP.get(agent_type, "agent"), output=output)
    except Exception as e:
        return format_response(
            {"state": "error", "message": str(e), "data": [], "usage": {}},
            AGENT_METHOD_NAME_MAP.get(agent_type, "agent"),
            output=output,
        )


def main():
    import argparse

    try:
        if not check_version():
            update_sh = os.path.join(script_dir, "update.sh")
            print(f"[WARNING] 存在 Gangtise agent 版本更新，可以执行 {update_sh} 更新，请与用户确认是否更新\n")
    except Exception:
        print("[WARNING] 检查 Gangtise agent 版本失败\n")

    parser = argparse.ArgumentParser(
        description="Gangtise Agent OpenAPI 统一调用入口",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-a",
        "--agent-type",
        required=True,
        choices=PUBLIC_AGENT_TYPES,
        help="接口类型：含 earnings-review / viewpoint-debate 时为 getId 后轮询 getContent（最长 600s）",
    )
    parser.add_argument("-s", "--security-code", default=None, help="证券代码，如 600519.SH")
    parser.add_argument(
        "-p",
        "--period",
        default=None,
        help="报告期（earnings-review），如 2025q3",
    )
    parser.add_argument("-d", "--data-id", default=None, help="内容 dataId（保留参数，当前无对外场景）")
    parser.add_argument(
        "--viewpoint",
        default=None,
        help="观点文本（viewpoint-debate），不超过 1000 字",
    )
    parser.add_argument("-t", "--theme-id", default=None, help="主题 ID 或中文主题名（仅 theme-tracking）")
    parser.add_argument("--date", default=None, help="日期（仅 theme-tracking），格式 yyyy-MM-dd")
    parser.add_argument("--type", default=None, help="资讯类型（仅 theme-tracking），morning/night，逗号分隔")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="结果保存路径（当前版本由后端统一管理，本参数暂不生效）",
    )
    args = parser.parse_args()

    out = openapi_agent(
        agent_type=args.agent_type,
        security_code=args.security_code,
        period=args.period,
        data_id=args.data_id,
        viewpoint=args.viewpoint,
        theme_id=args.theme_id,
        date=args.date,
        types=_normalize_list(args.type),
        output=args.output,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors="ignore")
    main()
