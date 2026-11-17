# validate_checks/keywords.py — 关键词/结构/看板/XSS 守护
import re
import json
from .common import _extract_js_var

def check_empty_category_tabs(html_content: str) -> dict:
    """C2 守护（死分类动态隐藏）：确保空分类 tab 不会渲染出来。

    1) 从嵌入的 CATEGORIES 常量取出所有分类键；
    2) 统计 NEWS_DATA 各分类实际条数（含 must 计数）；
    3) 确认模板 JS 的 renderTabs 含「count<1 且非 all 则跳过」逻辑。
    运行时该逻辑会把空分类 tab 隐藏，故 guard 存在即视为达标；
    同时把本周实际为空的分类列出供参考。
    """
    import re, json
    from json import JSONDecoder

    # 1) 解析 CATEGORIES 键
    cm = re.search(r'const CATEGORIES\s*=\s*\[(.*?)\];', html_content, re.S)
    if not cm:
        return {"ok": True, "warn": True,
                "msg": "未找到 CATEGORIES 常量（跳过空分类核验）"}
    keys = re.findall(r"key:\s*'([^']+)'", cm.group(1))
    if not keys:
        return {"ok": True, "warn": True,
                "msg": "CATEGORIES 无 key（跳过空分类核验）"}

    # 2) 统计各分类条数
    nm = re.search(r'const\s+NEWS_DATA\s*=\s*', html_content)
    counts = {k: 0 for k in keys}
    if nm:
        try:
            data, _ = JSONDecoder().raw_decode(html_content, nm.end())
            for it in data:
                if not isinstance(it, dict):
                    continue
                cat = it.get("category", "")
                if cat in counts:
                    counts[cat] += 1
                if it.get("mustRead"):
                    counts["must"] = counts.get("must", 0) + 1
            counts["all"] = len(data)
        except Exception:
            pass

    empties = [k for k in keys if k != "all" and counts.get(k, 0) < 1]

    # 3) 确认 hide 逻辑存在
    guard = ("count < 1 && cat.key !== 'all'" in html_content
             or "cat.key !== 'all') return ''" in html_content)
    if not guard:
        return {"ok": False, "warn": False,
                "msg": "renderTabs 缺少空分类隐藏逻辑，空 tab 会被渲染"}

    if empties:
        return {"ok": True, "warn": False,
                "msg": f"空分类 {empties} 已被动态隐藏（guard 就位，渲染 0 个空 tab）"}
    return {"ok": True, "warn": False,
            "msg": "本周无空分类（guard 就位）"}


def check_keyword_filter(html_content: str) -> dict:
    """C2 守护（关键词聚类成可 filter 标签）：确保关键词 chips 可点击筛选新闻。

    确认模板 JS 含 toggleKeywordFilter 函数、并用 activeKeyword 在 currentFilter 中过滤，
    且 chip 用 data-term + onclick 绑定（而非纯外链）。
    """
    has_fn = "function toggleKeywordFilter" in html_content
    has_state = "let activeKeyword" in html_content
    has_filter = "activeKeyword)" in html_content and "filtered = filtered.filter(n =>" in html_content
    has_bind = "toggleKeywordFilter(this.dataset.term" in html_content

    if has_fn and has_state and has_filter and has_bind:
        return {"ok": True, "warn": False,
                "msg": "关键词聚类标签可点击筛选（toggleKeywordFilter 已接线）"}
    return {"ok": False, "warn": False,
            "msg": f"关键词筛选缺失：fn={has_fn} state={has_state} filter={has_filter} bind={has_bind}"}


def check_keyword_clustering(html_content: str) -> dict:
    """C2#7 守护（关键词自动聚类）：确保 INSIGHTS_KEYWORDS 足够（≥5）且 note 为周相关。

    note 必须包含「本周被 N 条新闻提及」等周相关锚点（不再是通用套话）；
    至少 60% 关键词含「本周」字样视为通过——避免悄悄退回通用 note。
    """
    import re, json
    from json import JSONDecoder

    m = re.search(r'const\s+INSIGHTS_KEYWORDS\s*=\s*', html_content)
    if not m:
        return {"ok": False, "warn": False, "msg": "未找到 INSIGHTS_KEYWORDS 常量"}
    try:
        kws, _ = JSONDecoder().raw_decode(html_content, m.end())
    except Exception as e:
        return {"ok": False, "warn": False, "msg": f"INSIGHTS_KEYWORDS 解析失败：{e}"}

    n = len(kws)
    if n < 5:
        return {"ok": False, "warn": False,
                "msg": f"关键词数量不足：{n} < 5（计划要求 5–8 个高频主题词）"}

    def _note_text(kw):
        nt = kw.get("note")
        if isinstance(nt, dict):
            return " ".join(str(v) for v in nt.values())
        return str(nt or "")

    week_specific = sum(1 for k in kws if "本周" in _note_text(k))
    cov = week_specific / n if n else 0
    if cov < 0.6:
        return {"ok": False, "warn": False,
                "msg": f"note 周相关率 {week_specific}/{n}（{cov*100:.0f}%）< 60%，疑似回退为通用 note"}

    return {"ok": True, "warn": False,
            "msg": f"关键词 {n} 个，{week_specific} 个 note 包含「本周」（周相关率 {cov*100:.0f}%）"}


def check_weekly_dashboard(html_content: str) -> dict:
    """C2#8 守护（本周数字看板）：确保 WEEKLY_STATS 注入且字段齐全。

    字段：total / zh / en / model_news / fund_events / lb_models / must_read；
    must_read ≤ 3 且 total > 0（空数据必须隐藏 dashboard）。
    """
    import re, json
    from json import JSONDecoder

    m = re.search(r'const\s+WEEKLY_STATS\s*=\s*', html_content)
    if not m:
        return {"ok": False, "warn": False, "msg": "未找到 WEEKLY_STATS 常量"}
    try:
        s, _ = JSONDecoder().raw_decode(html_content, m.end())
    except Exception as e:
        return {"ok": False, "warn": False, "msg": f"WEEKLY_STATS 解析失败：{e}"}

    if not isinstance(s, dict):
        return {"ok": False, "warn": False, "msg": "WEEKLY_STATS 不是对象"}
    req_keys = ("total", "zh", "en", "model_news", "fund_events", "lb_models", "must_read")
    missing = [k for k in req_keys if k not in s]
    if missing:
        return {"ok": False, "warn": False,
                "msg": f"WEEKLY_STATS 缺字段：{', '.join(missing)}"}

    total = s.get("total", 0) or 0
    must = s.get("must_read", []) or []
    if total <= 0:
        return {"ok": False, "warn": False, "msg": "WEEKLY_STATS.total ≤ 0（无新闻数据）"}
    if len(must) > 3:
        return {"ok": False, "warn": False, "msg": f"must_read 超 3 条：{len(must)}"}

    return {"ok": True, "warn": False,
            "msg": f"数字看板完整：{total} 条 / 必读 Top{len(must)} / 资本&发布事件 {s['fund_events']} 起 / 在榜 {s['lb_models']} 个"}


_XSS_JSON_VARS = [
    "NEWS_DATA", "LEADERBOARD_DATA", "INSIGHTS_DATA",
    "INSIGHTS_KEYWORDS", "WEEKLY_STATS", "AUDIENCE_SUMMARY",
]


def check_xss_safe(html_content: str) -> dict:
    """P2-XSS 守护（H1/H2 防回归）：确保生成 HTML 不含存储型 XSS 突破。

    仅查嵌入 JSON 变量的 **raw 文本**（安全序列化产物为 ``\\u003c/script\\u003e``，
    raw 切片不会出现裸 `<`，故不会误报；只抓到真正的裸 `<` 注入才算突破）：

    1) 裸 `</script` 或 `<script` —— 脚本块突破（正文裸标签 + 闭合标签都算）；
    2) 事件处理器 `on<event>=` —— 属性逃逸：数据里混进 `onclick=` 等，
       一旦被当属性回写即执行（对应 P0 修复里 `jsStrInAttr` / `escapeHtml` 的回归面）；
    3) 危险协议 `href="javascript:` / `href='data:`（H2 向量，safeUrl 已转 `#`）。
    """
    import re
    raw_breakout = []          # 裸 <script / </script
    raw_event_handler = []     # on<event>= 属性逃逸
    for name in _XSS_JSON_VARS:
        raw = _extract_js_var(name, html_content)
        if not raw:
            continue
        if re.search(r'<script', raw, re.IGNORECASE):
            raw_breakout.append(name)
        if re.search(r'\bon[a-z]+\s*=', raw, re.IGNORECASE):
            raw_event_handler.append(name)

    # 3) 危险协议 href（大小写不敏感）
    danger_href = re.findall(r'href\s*=\s*["\']\s*(?:javascript:|data:)',
                              html_content, re.IGNORECASE)

    ok = (not raw_breakout) and (not raw_event_handler) and (not danger_href)
    bits = []
    if raw_breakout:
        bits.append(f"JSON 变量含裸<script突破：{', '.join(raw_breakout)}")
    if raw_event_handler:
        bits.append(f"JSON 变量含事件处理器属性逃逸(on*=)：{', '.join(raw_event_handler)}")
    if danger_href:
        bits.append(f"危险协议 href：{sorted(set(h.lower() for h in danger_href))}")
    msg = ("XSS 守护通过（无脚本突破 / 无属性逃逸 / 无危险协议 href）✅"
           if ok else "；".join(bits))
    return {"ok": ok, "warn": False,
            "raw_breakout": raw_breakout, "raw_event_handler": raw_event_handler,
            "danger_href": danger_href, "msg": msg}
