import os
import sys
from io import TextIOWrapper
from typing import Any, Dict, List, Optional, Tuple

import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import GTS_AUTHORIZATION, check_version, format_response


HOT_TOPIC_CATEGORY_LABEL = {
    "morningBriefing": "早报",
    "noonBriefing": "午报",
    "afternoonFlash": "盘中快报",
    "eveningBriefing": "晚报",
}

_HOT_TOPIC_CATEGORY_ALIASES = {
    "morning": "morningBriefing",
    "morningbriefing": "morningBriefing",
    "早报": "morningBriefing",
    "noon": "noonBriefing",
    "noonbriefing": "noonBriefing",
    "午报": "noonBriefing",
    "afternoon": "afternoonFlash",
    "afternoonflash": "afternoonFlash",
    "盘中": "afternoonFlash",
    "盘中快报": "afternoonFlash",
    "evening": "eveningBriefing",
    "eveningbriefing": "eveningBriefing",
    "晚报": "eveningBriefing",
}

_VALID_HOT_TOPIC_CATEGORIES = {
    "morningBriefing",
    "noonBriefing",
    "afternoonFlash",
    "eveningBriefing",
}


def normalize_hot_topic_categories(raw: Optional[List[str]]) -> Optional[List[str]]:
    if not raw:
        return None
    out: List[str] = []
    for item in raw:
        s = str(item).strip()
        if not s:
            continue
        mapped: Optional[str] = None
        if s in _VALID_HOT_TOPIC_CATEGORIES:
            mapped = s
        elif s in _HOT_TOPIC_CATEGORY_ALIASES:
            mapped = _HOT_TOPIC_CATEGORY_ALIASES[s]
        else:
            low = s.lower()
            mapped = _HOT_TOPIC_CATEGORY_ALIASES.get(low)
            if not mapped:
                for v in _VALID_HOT_TOPIC_CATEGORIES:
                    if v.lower() == low:
                        mapped = v
                        break
        if not mapped:
            continue
        if mapped not in out:
            out.append(mapped)
    return out or None


def _format_hot_topic_report_date(raw: Any) -> str:
    r = str(raw or "").strip()
    if len(r) == 8 and r.isdigit():
        return f"{r[:4]}-{r[4:6]}-{r[6:8]}"
    return r


def _md_table_cell(val: Any) -> str:
    s = str(val if val is not None else "").replace("|", "\\|")
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = " ".join(s.splitlines())
    return s.strip()


def markdown_hot_topic_list(data: Dict[str, Any]) -> str:
    total = data.get("total", 0)
    reports = data.get("list", [])
    if not isinstance(reports, list):
        reports = []
    lines: List[str] = [
        f"## 热点话题报告（本页 {len(reports)} 篇，接口 total={total}）",
        "",
    ]
    for rep in reports:
        if not isinstance(rep, dict):
            continue
        rid = rep.get("id", "")
        title = rep.get("title", "")
        rdate = _format_hot_topic_report_date(rep.get("reportDate", ""))
        cat = rep.get("category", "")
        cat_label = HOT_TOPIC_CATEGORY_LABEL.get(str(cat), str(cat))
        lines.append(f"### {title}")
        lines.append(f"- **报告 ID**：{rid}")
        lines.append(f"- **报告日期**：{rdate}")
        lines.append(f"- **报告类型**：{cat_label}（`{cat}`）")
        lines.append("")
        topics = rep.get("topics", [])
        if not isinstance(topics, list):
            topics = []
        for ti, topic in enumerate(topics, 1):
            if not isinstance(topic, dict):
                continue
            t_title = topic.get("topicTitle", "")
            lines.append(f"#### {ti}. {t_title}")
            lines.append(f"- **话题 ID**：{topic.get('topicId', '')}")
            lines.append("")
            lines.append("**驱动事件**")
            lines.append("")
            lines.append(str(topic.get("driverEvent", "") or "").strip() or "（无）")
            lines.append("")
            lines.append("**投资逻辑**")
            lines.append("")
            lines.append(str(topic.get("investLogic", "") or "").strip() or "（无）")
            lines.append("")
            rel = topic.get("relatedSecurities")
            if isinstance(rel, list) and len(rel) > 0:
                lines.append("##### 核心标的")
                lines.append("")
                lines.append("| 证券代码 | 证券简称 | 投资理由与逻辑 |")
                lines.append("| --- | --- | --- |")
                for sec in rel:
                    if not isinstance(sec, dict):
                        continue
                    lines.append(
                        "| "
                        + _md_table_cell(sec.get("securityCode", ""))
                        + " | "
                        + _md_table_cell(sec.get("securityName", ""))
                        + " | "
                        + _md_table_cell(sec.get("reason", ""))
                        + " |"
                    )
                lines.append("")
            readings = topic.get("closeReading")
            if isinstance(readings, list) and len(readings) > 0:
                lines.append("##### 话题精读")
                lines.append("")
                for cr in readings:
                    if not isinstance(cr, dict):
                        continue
                    crt = str(cr.get("title", "") or "").strip()
                    crc = str(cr.get("content", "") or "").strip()
                    lines.append(f"###### {crt}" if crt else "###### （无标题）")
                    lines.append("")
                    lines.append(crc if crc else "（无内容）")
                    lines.append("")
            lines.append("---")
            lines.append("")
    while lines and lines[-1].strip() == "":
        lines.pop()
    while lines and lines[-1].strip() == "---":
        lines.pop()
    return "\n".join(lines).strip()


def format_hot_topic_payload(
    page_from: int = 0,
    page_size: int = 20,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category_list: Optional[List[str]] = None,
    with_related_securities: bool = False,
    with_close_reading: bool = False,
) -> Dict[str, Any]:
    size = int(page_size) if page_size is not None else 20
    if size < 1:
        size = 1
    if size > 20:
        size = 20
    frm = int(page_from) if page_from is not None else 0
    if frm < 0:
        frm = 0
    payload: Dict[str, Any] = {
        "from": frm,
        "size": size,
        "withRelatedSecurities": bool(with_related_securities),
        "withCloseReading": bool(with_close_reading),
    }
    if start_date:
        payload["startDate"] = str(start_date).strip()
    if end_date:
        payload["endDate"] = str(end_date).strip()
    cats = normalize_hot_topic_categories(category_list)
    if cats:
        payload["categoryList"] = cats
    return payload


def normalize_hot_topic_response(body: Dict[str, Any]) -> Dict[str, Any]:
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
        rows = [{"markdown": markdown_hot_topic_list(raw_data), "type": "hot-topic-list"}]
    else:
        rows = [{"markdown": "（无数据）", "type": "hot-topic-list"}]

    return {
        "state": "success",
        "message": body.get("msg", "请求成功"),
        "data": [{"data": rows, "module": "agent", "type": "hot-topic-list"}],
        "usage": {},
    }


def post_hot_topic_list(
    openai_root: str,
    payload: Dict[str, Any],
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    url = f"{openai_root.rstrip('/')}/hot-topic/getList"
    headers = {"Authorization": GTS_AUTHORIZATION}
    resp = requests.post(url, headers=headers, json=payload, timeout=300)
    if resp.status_code != 200:
        return None, resp.text
    try:
        return resp.json(), None
    except Exception as e:
        return None, str(e)


def run_hot_topic_list(
    page_from: int = 0,
    page_size: int = 20,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category_list: Optional[List[str]] = None,
    with_related_securities: bool = False,
    with_close_reading: bool = False,
    output: Optional[str] = None,
    openai_root: Optional[str] = None,
) -> str:
    if not openai_root:
        openai_root = os.getenv("GANGTISE_OPENAI_ROOT", "https://open.gangtise.com/application/open-ai")

    payload = format_hot_topic_payload(
        page_from=page_from,
        page_size=page_size,
        start_date=start_date,
        end_date=end_date,
        category_list=category_list,
        with_related_securities=with_related_securities,
        with_close_reading=with_close_reading,
    )
    body, err = post_hot_topic_list(openai_root=openai_root, payload=payload)
    if err is not None:
        return format_response(
            {"state": "error", "message": err, "data": [], "usage": {}},
            "hot_topic_list",
            output=output,
        )
    if body is None:
        return format_response(
            {"state": "error", "message": "空响应", "data": [], "usage": {}},
            "hot_topic_list",
            output=output,
        )
    normalized = normalize_hot_topic_response(body)
    return format_response(normalized, "hot_topic_list", output=output)


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
        description="Gangtise Hot Topic OpenAPI 调用入口",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--page-from", type=int, default=0, help="分页 from（从 0 开始）")
    parser.add_argument("--page-size", type=int, default=20, help="分页 size（最大 20）")
    parser.add_argument("-sd", "--start-date", default=None, help="起始日期 yyyy-MM-dd")
    parser.add_argument("-ed", "--end-date", default=None, help="结束日期 yyyy-MM-dd")
    parser.add_argument(
        "--hot-category",
        default=None,
        help="报告类型多选，逗号分隔。可写 morningBriefing 或 morning/noon/afternoon/evening 等",
    )
    parser.add_argument("--with-securities", action="store_true", help="返回是否包含核心标的")
    parser.add_argument("--with-close-reading", action="store_true", help="返回是否包含话题精读")
    parser.add_argument("-o", "--output", default=None, help="结果保存路径")
    args = parser.parse_args()

    out = run_hot_topic_list(
        page_from=args.page_from,
        page_size=args.page_size,
        start_date=args.start_date,
        end_date=args.end_date,
        category_list=_normalize_list(args.hot_category),
        with_related_securities=args.with_securities,
        with_close_reading=args.with_close_reading,
        output=args.output,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors="ignore")
    main()
