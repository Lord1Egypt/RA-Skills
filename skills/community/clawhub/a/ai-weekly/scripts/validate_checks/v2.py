# validate_checks/v2.py — v2.0 周刊兼容检查
import re

PLACE_HOLDER_PATTERNS = [
    r"\$XXX", r"(?<!\w)XXX(?!\w)", r"N/A", r"待填充", r"示例数据",
    r"\[PLACE.*?\]", r"\[KPI_.*?\]", r"\[CHART_.*?\]", r"\[NEWS_.*?\]",
]


TEMPLATE_CHART_DATA = [
    "[327, 390.9, 514.5, 680, 890, 1150, 1450, 3500]",
    "[17.4, 13.1, 16.2, 14.9, 13.8, 25.6, 23.5, 47.2, 62.2, 41.8, 45.1, 83.2]",
    "[56, 51, 47, 46, 40, 35, 33, 30, 30, 26]",
    "[46.4, 27.7, 10.3, 15.6]",
]


def _extract_body_html(html_content: str) -> str:
    cleaned = re.sub(r"<style\b[^>]*>.*?</style\b[^>]*>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"<script\b[^>]*>.*?</script\b[^>]*>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
    m = re.search(r"<body[^>]*>(.*?)</body>", cleaned, flags=re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else cleaned


def check_charts_v2(html_content: str) -> dict:
    charts = [
        ("marketSizeChart",   "市场规模柱状图"),
        ("fundingChart",      "AI融资折线图"),
        ("adoptionChart",     "企业AI采用饼图"),
        ("marketShareChart",  "市场份额饼图"),
        ("maChart",           "并购交易柱状图"),
        ("agentMarketChart",  "AI智能体市场预测"),
    ]
    details = []
    for chart_id, chart_name in charts:
        init_pattern = rf"getElementById\(['\"]{chart_id}['\"]\)"
        has_init = re.search(init_pattern, html_content) is not None
        if not has_init:
            details.append({"id": chart_id, "ok": False, "msg": f"{chart_name}：未找到"})
            continue
        init_match = re.search(init_pattern, html_content)
        block = html_content[init_match.start():init_match.start() + 3000] if init_match else ""
        data_arrays = re.findall(r"data:\s*(\[[\d\s,\.\-eE+]+\])", block)
        if not data_arrays:
            details.append({"id": chart_id, "ok": False, "msg": f"{chart_name}：数据缺失"})
            continue
        arr_normalized = data_arrays[0].replace(" ", "")
        is_template = any(arr_normalized == t.replace(" ", "") for t in TEMPLATE_CHART_DATA)
        if is_template:
            details.append({"id": chart_id, "ok": False, "msg": f"{chart_name}：模板数据未替换"})
        else:
            n = data_arrays[0].count(",") + 1 if "," in data_arrays[0] else 1
            details.append({"id": chart_id, "ok": True, "msg": f"{chart_name}：正常（{n} 点）"})
    ok = all(d["ok"] for d in details)
    return {"ok": ok, "details": details}


def check_news_v2(html_content: str) -> dict:
    count = len(re.findall(r'class="news-item"', html_content))
    if count == 0:
        count = len(re.findall(r'class="news-title"', html_content))
    return {"ok": count >= 5, "count": count, "msg": f"找到 {count} 条新闻" + (" ✅" if count >= 5 else " ⚠️")}


def check_kpi_v2(html_content: str) -> dict:
    body_html = _extract_body_html(html_content)
    kpi_section = ""
    m = re.search(r'class="kpi-section"', html_content)
    if m:
        kpi_section = html_content[m.start():m.start() + 3000]
    else:
        for kw in ["KPI", "kpi-value", "kpi-label", "核心数据"]:
            idx = body_html.find(kw)
            if idx >= 0:
                kpi_section = body_html[idx:idx + 3000]
                break
        if not kpi_section:
            kpi_section = body_html

    issues = []
    for pattern in PLACE_HOLDER_PATTERNS:
        matches = re.findall(pattern, kpi_section)
        if matches:
            issues.extend(list(set(matches))[:3])

    return {
        "ok": len(issues) == 0,
        "msg": "KPI 数据正常" if not issues else f"KPI 含占位符：{issues[:3]}"
    }
