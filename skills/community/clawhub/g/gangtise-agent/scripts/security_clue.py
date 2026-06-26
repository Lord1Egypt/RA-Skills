import os
import re
import sys
from datetime import datetime
from io import TextIOWrapper
from typing import Any, Dict, List, Optional, Tuple

import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import GTS_AUTHORIZATION, check_version, format_response


_VALID_QUERY_MODES = {"bySecurity", "byIndustry"}
_QUERY_MODE_ALIASES = {
    "security": "bySecurity",
    "bysecurity": "bySecurity",
    "证券": "bySecurity",
    "industry": "byIndustry",
    "byindustry": "byIndustry",
    "行业": "byIndustry",
}

SECURITY_CLUE_SOURCE_LABEL = {
    "researchReport": "研报",
    "conference": "电话会议（纪要）",
    "announcement": "公告",
    "view": "观点",
}

_VALID_SOURCES = set(SECURITY_CLUE_SOURCE_LABEL.keys())
_SOURCE_ALIASES = {
    "report": "researchReport",
    "research": "researchReport",
    "researchreport": "researchReport",
    "研报": "researchReport",
    "conference": "conference",
    "meeting": "conference",
    "电话会议": "conference",
    "纪要": "conference",
    "announcement": "announcement",
    "公告": "announcement",
    "view": "view",
    "观点": "view",
}

_DATE_ONLY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATETIME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


def normalize_query_mode(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    s = str(raw).strip()
    if not s:
        return None
    if s in _VALID_QUERY_MODES:
        return s
    low = s.lower()
    if low in _QUERY_MODE_ALIASES:
        return _QUERY_MODE_ALIASES[low]
    for v in _VALID_QUERY_MODES:
        if v.lower() == low:
            return v
    return None


def normalize_security_clue_sources(raw: Optional[List[str]]) -> Optional[List[str]]:
    if not raw:
        return None
    out: List[str] = []
    for item in raw:
        s = str(item).strip()
        if not s:
            continue
        mapped: Optional[str] = None
        if s in _VALID_SOURCES:
            mapped = s
        else:
            low = s.lower()
            mapped = _SOURCE_ALIASES.get(low)
            if not mapped:
                for v in _VALID_SOURCES:
                    if v.lower() == low:
                        mapped = v
                        break
        if mapped and mapped not in out:
            out.append(mapped)
    return out or None


def _validate_time(value: Optional[str], field_name: str) -> Optional[str]:
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    try:
        if _DATE_ONLY_PATTERN.match(s):
            datetime.strptime(s, "%Y-%m-%d")
            return s
        if _DATETIME_PATTERN.match(s):
            datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
            return s
    except ValueError:
        return None
    raise ValueError(f"{field_name} 格式错误，仅支持 yyyy-MM-dd 或 yyyy-MM-dd HH:mm:ss")


def _normalize_codes(raw: Optional[List[str]]) -> List[str]:
    if not raw:
        return []
    out: List[str] = []
    for item in raw:
        s = str(item).strip()
        if s and s not in out:
            out.append(s)
    return out


def _md_cell(value: Any) -> str:
    s = str(value if value is not None else "").replace("|", "\\|")
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = " ".join(s.splitlines())
    return s.strip()


def markdown_security_clue_list(data: Dict[str, Any]) -> str:
    total = data.get("total", 0)
    rows = data.get("list", [])
    if not isinstance(rows, list):
        rows = []
    lines: List[str] = [
        f"## 投研线索列表（本页 {len(rows)} 条，接口 total={total}）",
        "",
        "| 来源 | 发布时间 | 标题 | 证券线索 | 行业线索 | 发布者 | 代码 | 名称 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        if not isinstance(row, dict):
            continue
        source = str(row.get("source", "") or "")
        source_label = SECURITY_CLUE_SOURCE_LABEL.get(source, source)
        party = str(row.get("partyName", "") or "")
        party_id = str(row.get("partyId", "") or "")
        publisher = f"{party}（{party_id}）" if party_id else party
        lines.append(
            "| "
            + _md_cell(source_label)
            + " | "
            + _md_cell(row.get("publishTime", ""))
            + " | "
            + _md_cell(row.get("title", ""))
            + " | "
            + _md_cell(row.get("securityContent", ""))
            + " | "
            + _md_cell(row.get("industryContent", ""))
            + " | "
            + _md_cell(publisher)
            + " | "
            + _md_cell(row.get("gtsCode", ""))
            + " | "
            + _md_cell(row.get("gtsName", ""))
            + " |"
        )
    return "\n".join(lines).strip()


def format_security_clue_payload(
    page_from: int = 0,
    page_size: int = 500,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    query_mode: str = "bySecurity",
    gts_code_list: Optional[List[str]] = None,
    source: Optional[List[str]] = None,
) -> Dict[str, Any]:
    size = int(page_size) if page_size is not None else 500
    if size < 1:
        size = 1
    if size > 500:
        size = 500

    frm = int(page_from) if page_from is not None else 0
    if frm < 0:
        frm = 0

    normalized_mode = normalize_query_mode(query_mode)
    if not normalized_mode:
        raise ValueError("queryMode 无效，仅支持 bySecurity 或 byIndustry")

    codes = _normalize_codes(gts_code_list)
    if not codes:
        raise ValueError("gtsCodeList 不能为空，请至少传入一个证券/行业代码，或传入 all")

    payload: Dict[str, Any] = {
        "from": frm,
        "size": size,
        "queryMode": normalized_mode,
        "gtsCodeList": codes,
    }

    start = _validate_time(start_time, "startTime")
    end = _validate_time(end_time, "endTime")
    if start:
        payload["startTime"] = start
    if end:
        payload["endTime"] = end

    normalized_source = normalize_security_clue_sources(source)
    if normalized_source:
        payload["source"] = normalized_source
    return payload


def normalize_security_clue_response(body: Dict[str, Any]) -> Dict[str, Any]:
    ok = str(body.get("code", "")) == "000000" and body.get("status") is True
    if not ok:
        return {
            "state": "error",
            "message": body.get("msg", "请求失败"),
            "data": [],
            "usage": {},
        }

    raw_data = body.get("data")
    if isinstance(raw_data, dict):
        rows = [{"markdown": markdown_security_clue_list(raw_data), "type": "security-clue-list"}]
        points_cost = len(raw_data.get("list", [])) if isinstance(raw_data.get("list"), list) else 0
        extra_message = f"提示：本次成功返回 {points_cost} 条线索，按 1 积分/条计费。"
    else:
        rows = [{"markdown": "（无数据）", "type": "security-clue-list"}]
        extra_message = ""

    return {
        "state": "success",
        "message": (body.get("msg", "请求成功") + ("\n" + extra_message if extra_message else "")).strip(),
        "data": [{"data": rows, "module": "agent", "type": "security-clue-list"}],
        "usage": {},
    }


def post_security_clue_list(
    openai_root: str,
    payload: Dict[str, Any],
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    url = f"{openai_root.rstrip('/')}/security-clue/getList"
    headers = {"Authorization": GTS_AUTHORIZATION}
    resp = requests.post(url, headers=headers, json=payload, timeout=300)
    if resp.status_code != 200:
        return None, resp.text
    try:
        return resp.json(), None
    except Exception as e:
        return None, str(e)


def run_security_clue_list(
    page_from: int = 0,
    page_size: int = 500,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    query_mode: str = "bySecurity",
    gts_code_list: Optional[List[str]] = None,
    source: Optional[List[str]] = None,
    output: Optional[str] = None,
    openai_root: Optional[str] = None,
) -> str:
    if not openai_root:
        openai_root = os.getenv("GANGTISE_OPENAI_ROOT", "https://open.gangtise.com/application/open-ai")

    try:
        payload = format_security_clue_payload(
            page_from=page_from,
            page_size=page_size,
            start_time=start_time,
            end_time=end_time,
            query_mode=query_mode,
            gts_code_list=gts_code_list,
            source=source,
        )
    except ValueError as e:
        return format_response(
            {"state": "error", "message": str(e), "data": [], "usage": {}},
            "security_clue_list",
            output=output,
        )

    body, err = post_security_clue_list(openai_root=openai_root, payload=payload)
    if err is not None:
        return format_response(
            {"state": "error", "message": err, "data": [], "usage": {}},
            "security_clue_list",
            output=output,
        )
    if body is None:
        return format_response(
            {"state": "error", "message": "空响应", "data": [], "usage": {}},
            "security_clue_list",
            output=output,
        )
    normalized = normalize_security_clue_response(body)
    return format_response(normalized, "security_clue_list", output=output)


def _normalize_list(raw: Optional[str]) -> Optional[List[str]]:
    if not raw:
        return None
    result: List[str] = []
    for item in str(raw).replace("，", ",").split(","):
        value = item.strip()
        if value and value not in result:
            result.append(value)
    return result or None


def main():
    import argparse

    try:
        if not check_version():
            update_sh = os.path.join(script_dir, "update.sh")
            print(f"[WARNING] 存在 Gangtise agent 版本更新，可以执行 {update_sh} 更新，请与用户确认是否更新\n")
    except Exception:
        print("[WARNING] 检查 Gangtise agent 版本失败\n")

    parser = argparse.ArgumentParser(
        description="Gangtise Security Clue OpenAPI 调用入口",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--page-from", type=int, default=0, help="分页 from（从 0 开始）")
    parser.add_argument("--page-size", type=int, default=500, help="分页 size（最大 500）")
    parser.add_argument("-st", "--start-time", default=None, help="开始时间 yyyy-MM-dd 或 yyyy-MM-dd HH:mm:ss")
    parser.add_argument("-et", "--end-time", default=None, help="结束时间 yyyy-MM-dd 或 yyyy-MM-dd HH:mm:ss")
    parser.add_argument(
        "-q",
        "--query-mode",
        default="bySecurity",
        help="查询方式：bySecurity(证券) 或 byIndustry(行业)",
    )
    parser.add_argument(
        "-g",
        "--gts-code-list",
        default=None,
        help="证券/行业代码列表，逗号分隔；如 000001.SZ,000063.SH 或 888888.CI,999999.CI 或 all",
    )
    parser.add_argument(
        "--source",
        default=None,
        help="来源筛选多选，逗号分隔：researchReport,conference,announcement,view",
    )
    parser.add_argument("-o", "--output", default=None, help="结果保存路径")
    args = parser.parse_args()

    out = run_security_clue_list(
        page_from=args.page_from,
        page_size=args.page_size,
        start_time=args.start_time,
        end_time=args.end_time,
        query_mode=args.query_mode,
        gts_code_list=_normalize_list(args.gts_code_list),
        source=_normalize_list(args.source),
        output=args.output,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors="ignore")
    main()
