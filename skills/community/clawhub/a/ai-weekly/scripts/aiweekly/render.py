"""渲染层：把新闻 / 榜单 / 市场 / 看点数据填进单文件 HTML 模板。

从 generate_site.py 抽出（P1#1 Phase 3），`generate()` 是整条管线的装配点。
外部仍可 `from generate_site import generate`（兼容垫层）。

关键约束：看点卡、「给本周的你」、关键词彩标、趋势洞察「本周印证」四块
**全部在此服务端预渲染为静态 HTML**，禁用 JS 时仍可见。
"""
import html
import json
from datetime import datetime, timedelta
from pathlib import Path

from aiweekly import const as _c
from aiweekly.utils import _parse_date_arg, safe_url
from aiweekly.news import (
    MUSTREAD_TOP_N, format_news_items, _score_news, LEADERBOARD_STALE_DAYS,
)
from aiweekly.translate import Translator
from aiweekly.leaderboard import (
    _apply_profile_as_truth, _leaderboard_freshness,
)
from aiweekly.market import (
    build_charts, build_market_routing_note, BASE_SOURCES,
    DEFAULT_MARKET_SOURCE, DEFAULT_FUNDING_SOURCE,
    DEFAULT_CN_MARKET_SOURCE, DEFAULT_CN_FUNDING_SOURCE,
    _extract_market_signals, _compute_weekly_stats, _lb_name_map,
    _render_market_signals_html_with_theme, _render_trend_insights_html,
    resolve_chart_data, snapshot_status_text,
)
# 服务端 SVG 图表轨：与 Chart.js 轨同源数据，保证 JS / Canvas 被拦时市场图仍可见
from aiweekly.charts_svg import build_svg_charts
from aiweekly.insights import (
    DEFAULT_AUDIENCE_SUMMARY, _auto_insights, _auto_lead, _auto_keywords,
    _normalize_keywords, _is_daily_digest,
    _render_audience_chips_html, _render_keyword_chips_html,
    _render_insight_cards_html,
)

SKILL_DIR = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = SKILL_DIR / "assets" / "news_site_template.html"


# ---------- 排行榜列头 display_name（方向 B 修复：表头动态显示真实数据源）----------
def _attach_leaderboard_display_names(lb: dict) -> None:
    """为每个排行榜槽位计算 display_name，供模板表头动态显示真实数据源（而非写死 "LMArena"）。

    规则：
    - 取 source 中「（」前的真实榜名作为 base；
    - is_cache=True 时追加「（历史对照 <snapshot>）」，明确这是旧数据回退、并非该榜实时值；
    - 否则直接用 base（去掉冗长括号后缀）。
    """
    for group in ("comprehensive", "open_source"):
        for _key, sub in (lb.get(group) or {}).items():
            if not isinstance(sub, dict):
                continue
            src = (sub.get("source") or "").strip()
            base = src.split("（")[0].strip() if src else (_key or "")
            if sub.get("is_cache"):
                snap = (sub.get("snapshot") or "").strip()
                sub["display_name"] = f"{base}（历史对照 {snap}）" if snap else f"{base}（历史快照）"
            else:
                sub["display_name"] = base


def _build_leaderboard_notes(lb: dict) -> dict:
    """生成排行榜区 3 处说明文字（ranking-note / lb-explain 末尾 / 性价比象限），
    全部基于实际可达槽位动态生成，避免写死「LMArena」与真实数据矛盾的误导。

    返回 dict 直接并入 final_leaderboard["meta"]。
    """
    comp = lb.get("comprehensive") or {}
    os_ = lb.get("open_source") or {}
    lm = comp.get("lmarena") or {}
    aa = comp.get("aa") or {}
    ls = os_.get("ls") or {}
    hf = os_.get("hf") or {}
    lab = lambda s: (s.get("display_name") or s.get("source") or "")

    comp_parts = []
    if aa.get("rows"):
        comp_parts.append(lab(aa))
    if lm.get("rows"):
        suffix = "（非 LMArena 实时，系 AA 历史数据回退）" if lm.get("is_cache") else ""
        comp_parts.append(lab(lm) + suffix)
    comp_note = "综合榜：" + " + ".join(comp_parts) if comp_parts else "综合榜：暂无数据"

    os_parts = []
    if ls.get("rows"):
        os_parts.append(lab(ls))
    if hf.get("rows"):
        os_parts.append(lab(hf))
    os_note = "开源模型榜：" + " + ".join(os_parts) if os_parts else "开源模型榜：暂无数据"

    ranking_note = comp_note + " ｜ " + os_note

    lb_explain_note = (
        f"综合榜左列为 {lab(lm) or 'LMArena'}，右列为 {lab(aa) or 'AA 智能指数'}；"
        f"开源榜左列为 {lab(ls) or 'LLM-Stats'}，右列为 {lab(hf) or 'Hugging Face'}。"
    )

    if not lm.get("rows") or lm.get("is_cache"):
        value_chart_note = (
            "纵轴=AA 智能指数（真实指标）；本期限 LMArena 实时源不可达，未引入近似归一名次，避免误导。"
            "未匹配成本家族的模型不计入。"
        )
    else:
        value_chart_note = (
            "横轴=输出单价（$/1M tokens），纵轴=能力指数；圆点大小≈上下文窗口。"
            "AA 智能指数为真实指标，LMArena 名次经近似归一，仅供横向参考。未匹配成本家族的模型不计入。"
        )

    return {
        "ranking_note": ranking_note,
        "lb_explain_note": lb_explain_note,
        "value_chart_note": value_chart_note,
    }

__all__ = ["generate", "TEMPLATE_PATH", "SKILL_DIR"]


def _json_text_script_safe(s: str) -> str:
    """把**已是 JSON 文本**的字符串转义到可安全嵌入 ``<script>`` 的程度。

    与 :func:`_json_script_safe` 的分工：本函数**不做序列化**，因此完整保留调用方
    原有的 JSON 格式（含紧凑分隔符），适用于调用方已持有 JSON 文本的场景。
    对合法 JSON 而言 ``<`` ``>`` ``&`` 只可能出现在字符串字面量内部，
    故逐字符替换是安全的。
    """
    if not s:
        return ""
    return (s.replace("<", "\\u003c")
             .replace(">", "\\u003e")
             .replace("&", "\\u0026"))


def _json_script_safe(obj) -> str:
    """把对象序列化为可安全嵌入 <script> 的 JSON 字符串。

    关键安全修复：RSS / 外部新闻内容是不可信输入，若其中含 ``</script>``，
    Python 默认的 ``json.dumps`` 不会转义，会被 HTML 解析器识别为脚本块结束，
    从而突破 <script> 上下文执行任意 JS（存储型 XSS）。这里把 < > & 转义为
    Unicode 形式（\\u003c 等），既阻止 ``</script>`` 突破，又保证之后经
    innerHTML + escapeHtml 渲染时按纯文本显示。
    """
    return _json_text_script_safe(json.dumps(obj, ensure_ascii=False))


def _js_str(s: str) -> str:
    """转义为 JS 字符串字面量（用于 ``const X = "[...]"`` 上下文）。"""
    if not s:
        return ""
    return (s.replace("\\", "\\\\").replace('"', '\\"')
             .replace("\n", "\\n").replace("\r", "\\r")
             .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def _build_capability_card(translate_en: bool, audience_summary: bool,
                            cn_market_data: bool, leaderboard_data: bool,
                            insights: bool, feishu_push: bool = False) -> str:
    """生成「能力自检卡」HTML（服务端预渲染，禁 JS 也可见）。

    E1（v3.4.7）：让用户在报告顶部一眼看到本期启用了哪些能力、哪些没启用以及
    如何开启——回应评测 completeness 4.7「用户可能遗漏部分高级功能」。
    """
    on, off = [], []
    # 恒定能力
    on.append("RSS 抓取（14 源）")
    if translate_en:
        on.append("英文中译（远程译文源默认开启）")
    else:
        off.append(("英文中译", "--translate-en"))
    if leaderboard_data:
        on.append("模型排行榜（综合+开源）")
    else:
        off.append(("模型排行榜", "--leaderboard-json"))
    if cn_market_data:
        on.append("市场双口径（国内+全球）")
    else:
        off.append(("国内口径市场数据", "--cn-market-data"))
    if insights:
        on.append("本周看点编辑洞察")
    # 受众分角色摘要：render 在 audience_summary 为 None 时回退 _DEFAULT_AUDIENCE_SUMMARY，
    # 始终渲染（开发者/产品/自媒体三视角）。如实标注「已启用」，不依赖显式传入。
    on.append("受众分角色摘要（开发者/产品/自媒体）")
    # 飞书推送：生成阶段由 --feishu-push 声明本报告会走飞书分发。
    # 仅标注「是否启用 + 推送身份类型」，绝不暴露 user_id / token / 群名（开发者隐私）。
    if feishu_push:
        on.append("飞书推送（每周一·应用机器人）")
    else:
        off.append(("飞书推送", "--feishu-push（自动化开启）"))

    def tag(text, cls):
        return f'<span class="cap-tag {cls}">{html.escape(text)}</span>'

    on_html = " ".join(tag(t, "cap-on") for t in on)
    off_html = " ".join(
        f'{tag(t, "cap-off")} <code>{cmd}</code>' for t, cmd in off)
    return (f'<div class="cap-row"><b>本期已启用</b>　{on_html}</div>'
            f'<div class="cap-row"><b>未启用</b>　{off_html}</div>')


# ---------- 页脚「数据来源」拆成两组（HON-1）----------
# 为什么拆：此前 8 家静态引用与本周真实抓取的 RSS 源混在同一段排版里，
# 读者第一眼会把「市场基线的人工誊录」误读成「数据来自这 8 家机构」。
# 两组的性质根本不同，必须各自成块：
#   1. 静态快照引用 —— 人工誊录的历史数字，带 as_of /每家 retrieved_at；
#   2. 本周信号来源   —— 本周真的抓了哪些源，从 news_items 的 source 字段统计得出。
def _build_footer_snapshot_block(snapshot_note: str = "") -> str:
    """页脚第一块：静态快照引用（截止 as_of），每家带 retrieved_at 与被哪张图引用。

    外部可控字段：机构名 / URL / retrieved_at 全部来自外部 JSON 文件，
    按不可信输入处理——转义 + URL 仅放行安全协议（safe_url）。
    """
    rows = []
    for s in BASE_SOURCES:
        name = html.escape(s["name"])
        url = safe_url(s["url"]) if s["url"] else ""
        label = f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">{name}</a>' if url else name
        # used_for 为空 = 该机构没被任何一张图的数字引用，必须说清楚而不是混排
        usage = (f'用于{html.escape(s["used_for"])}' if s["used_for"]
                 else '<span class="src-uncited">未引用其数字</span>')
        got = html.escape(s["retrieved_at"]) if s["retrieved_at"] else "未标注"
        rows.append(f'<li>{label} · {usage} · 誊录于 {got}</li>')
    if not rows:
        return ""
    note_html = f'<p class="src-note">{html.escape(snapshot_note)}</p>' if snapshot_note else ""
    as_of = html.escape(_snapshot_as_of())
    return ('<div class="src-block src-block-snapshot">'
            '<p class="src-head">📌 静态快照引用（人工誊录的历史基线，'
            f'截止 {as_of}；<b>非本周抓取</b>）</p>'
            f'<ul class="src-list">{"".join(rows)}</ul>{note_html}</div>')


def _snapshot_as_of() -> str:
    """快照截止日（as_of），取自快照模块已加载的快照；缺失时返回明确文案。"""
    # 从 market_snapshot（快照状态真身）读，而不是从 market 转出的副本——
    # 后者是 import 期的值拷贝，load_snapshot() 重载后不会同步。
    from aiweekly.market_snapshot import _SNAPSHOT
    return str(_SNAPSHOT.get("as_of") or "未标注")


def _count_weekly_sources(news_items: list) -> list:
    """统计本周新闻实际来自哪些源 -> ``[(源名, 条数), ...]``，按条数降序。

    这是**真实可数**的：直接数news_items 的 source 字段，
    不再像从前那样把「配置里有哪些源」当成「本周抓到了什么」。
    """
    counts = {}
    for it in news_items or []:
        name = (it.get("source") or "").strip()
        if name:
            counts[name] = counts.get(name, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def _build_footer_weekly_block(news_items: list, external_source: tuple = None) -> str:
    """页脚第二块：本周信号来源——这周实际抓到哪些源、各多少条。

    空数据时显式说明「本周无RSS 源」，不静默消失（静默会让读者以为漏了东西）。
    """
    pairs = _count_weekly_sources(news_items)
    if not pairs:
        items_html = '<li>本周未取到任何 RSS 源（--api-json 为空或全部解析失败）</li>'
        total_note = "0 条"
    else:
        items_html = "".join(
            f'<li>{html.escape(name)} · <b>{n}</b> 条</li>' for name, n in pairs)
        total_note = f"{len(pairs)} 个源 / {sum(n for _, n in pairs)} 条"
    ext_html = ""
    if external_source and external_source[0]:
        nm = html.escape(external_source[0])
        eu = safe_url(external_source[1] or "") if external_source[1] else ""
        ext_html = (f'<li>用户补充外部 API：'
                    + (f'<a href="{html.escape(eu, quote=True)}" target="_blank" '
                       f'rel="noopener">{nm}</a>' if eu else nm)
                    + '</li>')
    return ('<div class="src-block src-block-weekly">'
            '<p class="src-head">🛰️ 本周信号来源（本周真实抓取，'
            f'{total_note}）</p>'
            f'<ul class="src-list">{items_html}{ext_html}</ul>'
            '<p class="src-note">市场板块的「实测值」来自这些源的本周报道，'
            '与上方静态快照是两回事。</p></div>')


def generate(api_data: dict, output_path: str = None,
             date_range: str = None, ranking_source: str = "unavailable",
             market_data: list = None, market_labels: list = None,
             funding_data: list = None, funding_labels: list = None,
             market_source: str = None, funding_source: str = None,
             cn_market_data: list = None, cn_market_labels: list = None,
             cn_funding_data: list = None, cn_funding_labels: list = None,
             cn_market_source: str = None, cn_funding_source: str = None,
             external_source: tuple = None,
             insights: list = None, lead: str = None,
             keywords: list = None,
             keyword_search_base: str = "https://www.baidu.com/s?wd=",
             audience_summary: str = None,
             keyword_search_sources: str = None,
             leaderboard_data: dict = None,
             model_profiles: dict = None,
             report_date: str = None,
             data_snapshot: str = None,
             pin_terms: list = None,
             translate_en: bool = False,
             translate_model: str = _c.TRANSLATE_MODEL_DEFAULT,
             translate_workers: int = _c.TRANSLATE_WORKERS_DEFAULT,
             translate_timeout: int = _c.TRANSLATE_TIMEOUT_DEFAULT,
             translate_retries: int = _c.TRANSLATE_RETRIES_DEFAULT,
             translate_num_predict: int = _c.TRANSLATE_NUM_PREDICT_DEFAULT,
             translate_title: bool = True,
             translate_cache: str = None,
             translations_url: str = None,
             feishu_push: bool = False,
             region: str = "auto") -> str:
    """生成完整的新闻网站 HTML。

    Args:
        api_data: 新闻 JSON（RSS 兼容格式，含 items[]）
        output_path: 输出文件路径
        date_range: 日期范围标签
        ranking_source: 排行榜来源标签（live/json/default/unavailable）
        market_data/labels, funding_data/labels: 图表数据，未提供则回退标注清晰的估算值
        market_source, funding_source: 图表数据来源说明（用于页脚/注释）
        ranking_criteria: 排行榜排名标准说明（用于排行榜标题下方）
        external_source: 用户自备外部 API 的来源 (name, url)，用于页脚署名与链接
        insights: 「本周看点」编辑洞察列表（每项含 title/analysis/insight/related/kicker）
        lead: 「本周看点」顶部导语一句话（电梯演讲）
        keywords: 「本周看点」顶部关键词列表（每项 {term, note}），引导读者深挖
        keyword_search_base: 关键词点击后跳转的网页搜索基址（搜索词 = 「词语 AI 行业」）
        audience_summary: 面向受众的一句话结论（JSON 字符串 {开发者, PM, 媱}），渲染在关键词区上方
        keyword_search_sources: 可切换的搜索源 JSON 字符串 {name:url}，供关键词联动筛选
    """
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"模板不存在：{TEMPLATE_PATH}")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Chart.js 内联:优先把本地 chart.umd.min.js 内联进 HTML,实现真正单文件;
    # 缺失时回退到 CDN(仅兜底,正常发布总是内联)。
    chart_lib_path = SKILL_DIR / "assets" / "chart.umd.min.js"
    if chart_lib_path.exists():
        chart_lib = chart_lib_path.read_text(encoding="utf-8")
        template = template.replace("[CHARTJS_LIB_PLACEHOLDER]", f"<script>{chart_lib}</script>")
    else:
        template = template.replace(
            "[CHARTJS_LIB_PLACEHOLDER]",
            '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>')

    # 英文报道中文总结：生成途中遇英文即即时中译（本地 Ollama 服务，best-effort 不阻断）
    if translate_en:
        _tr = Translator(
            enabled=True, model=translate_model,
            timeout=translate_timeout, max_workers=translate_workers,
            retries=translate_retries, num_predict=translate_num_predict,
            translate_title=translate_title, cache_path=translate_cache,
            remote_url=translations_url)
        try:
            n_tr = _tr.translate_items(api_data.get("items", []))
            if n_tr:
                print(f"🌐 英文报道中文总结：本地 Ollama 翻译 {n_tr} 条（模型 {translate_model}）")
        except Exception as e:  # noqa: BLE001  best-effort：任何异常都不阻断报告生成
            print(f"  ⚠️ 英文翻译跳过（Ollama 不可用或异常）：{e}")

    # 格式化新闻数据（含信源/摘要归一化 + cn_summary 透传）
    news_items = format_news_items(api_data)
    # C0：重要度评分 + 🔥必读标记（仅排序/标记，不篡改事实字段）
    _score_news(news_items, report_date=report_date, top_n=MUSTREAD_TOP_N, pin_terms=pin_terms)
    # M1：从本周新闻抽取「资本/模型发布」信号，做成新闻↔宏观图桥接卡（服务端预渲染）
    market_signals = _extract_market_signals(news_items, top_n=5)
    # C2#8：聚合「本周数字看板」指标（总量/国内外比/模型发布/融资事件/在榜模型数/必读Top3）
    weekly_stats = _compute_weekly_stats(news_items, market_signals, leaderboard_data)

    # 排行榜数据（双榜：综合 + 开源）。None -> 空结构，模板渲染"暂无实时数据"
    final_leaderboard = leaderboard_data if leaderboard_data is not None else {
        "comprehensive": {"lmarena": {"rows": []}, "aa": {"rows": []}},
        "open_source": {"hf": {"rows": []}},
    }
    if model_profiles:
        final_leaderboard["model_profiles"] = model_profiles
        # 以资料卡为准：用卡片权威值覆盖排行榜行的描述性字段（成本/上下文/许可证等）
        _apply_profile_as_truth(final_leaderboard, model_profiles)
    # 方向 B：为每个槽位计算 display_name（动态表头真实数据源），并生成 3 处动态说明文字
    _attach_leaderboard_display_names(final_leaderboard)
    # M1：构建 模型名/机构名 -> 名次 映射，供「资本↔能力」联动标注
    _lb_map = _lb_name_map(final_leaderboard)

    # C1#5：排行榜快照时效标注——超龄即告警，并把时效信息注入 meta 供模板渲染
    _lb_fresh = _leaderboard_freshness(final_leaderboard, report_date)
    final_leaderboard.setdefault("meta", {})
    final_leaderboard["meta"]["snapshot_max_age"] = _lb_fresh["max_age"]
    final_leaderboard["meta"]["snapshot_stale"] = _lb_fresh["stale"]
    final_leaderboard["meta"]["snapshot_per_source"] = _lb_fresh["per_source"]
    final_leaderboard["meta"]["snapshot_per_source_age"] = _lb_fresh["per_source_age"]
    final_leaderboard["meta"]["snapshot_stale_threshold"] = LEADERBOARD_STALE_DAYS
    if _lb_fresh["stale"]:
        print(f"  ⚠️ 排行榜快照时效告警：最新快照距本期 {_lb_fresh['worst_age']} 天"
              f"（阈值 {LEADERBOARD_STALE_DAYS} 天），部分榜单为「非本周抓取」——"
              f"建议刷新 cn_leaderboard_snapshot.json 或稍后重跑以获取实时数据。")
    else:
        print(f"  ✅ 排行榜快照时效 OK（最大龄 {_lb_fresh['max_age']} 天）。")
    # 方向 B：把动态生成的排行榜说明文字并入 meta，供模板表头/注释按真实数据渲染
    final_leaderboard["meta"].update(_build_leaderboard_notes(final_leaderboard))

    # 图表代码（Chart.js 轨：环境允许时把服务端 SVG 接管为可交互版本）
    chart_code = build_charts(market_data, market_labels, funding_data, funding_labels,
                             cn_market_data, cn_market_labels, cn_funding_data, cn_funding_labels)

    # 服务端 SVG 轨：同一份数据在服务端画好写进静态 HTML，
    # 保证「JS / Canvas 被查看环境拦掉」时 6 张市场图依然可见（默认显示的就是它）。
    svg_charts = build_svg_charts(resolve_chart_data(
        market_data, market_labels, funding_data, funding_labels,
        cn_market_data, cn_market_labels, cn_funding_data, cn_funding_labels))

    # M0：市场数据来源默认用真实署名（国内源优先），不再回退到「示例/估算」自损式免责
    market_source = market_source or DEFAULT_MARKET_SOURCE
    funding_source = funding_source or DEFAULT_FUNDING_SOURCE
    cn_market_source = cn_market_source or DEFAULT_CN_MARKET_SOURCE
    cn_funding_source = cn_funding_source or DEFAULT_CN_FUNDING_SOURCE

    # 数据充分性提示：真实数据点过少时,来源注释追加「数据不足」,避免把少量点伪装成趋势
    _insuff = "（数据不足，仅展示已核实区间）"
    if market_data is not None and len(market_data) < 3:
        market_source = (market_source or "") + _insuff
    if funding_data is not None and len(funding_data) < 3:
        funding_source = (funding_source or "") + _insuff
    if cn_market_data is not None and len(cn_market_data) < 2:
        cn_market_source = (cn_market_source or "") + _insuff
    if cn_funding_data is not None and len(cn_funding_data) < 2:
        cn_funding_source = (cn_funding_source or "") + _insuff

    # 替换占位符
    template = template.replace("[NEWS_DATA_PLACEHOLDER]",
                                _json_script_safe(news_items))
    template = template.replace("[LEADERBOARD_DATA_PLACEHOLDER]",
                                _json_script_safe(final_leaderboard))
    template = template.replace("[CHART_DATA_PLACEHOLDER]", chart_code)
    # 6 张市场图的服务端 SVG（占位名与 canvas id 一一对应）
    for _cid, _svg in svg_charts.items():
        template = template.replace(f"[CHART_SVG_{_cid}]", _svg)

    if not date_range:
        today = (_parse_date_arg(report_date) if report_date
                 else datetime.now().astimezone())
        week_ago = today - timedelta(days=7)
        date_range = f"{week_ago.year}/{week_ago.month}/{week_ago.day}–{today.month}/{today.day}"
    template = template.replace("[DATE_RANGE]", date_range)
    # 图表来源：提供真实来源则用之，否则标注为估算（全球 + 中国双来源）
    # 四个值均来自 CLI（--market-source / --funding-source / --cn-market-source /
    # --cn-funding-source），属不可信输入。模板中这 6 个占位符**全部落在 HTML 文本
    # 节点内**（:888/:896/:904/:912/:921/:929/:1106 的 <p>/<div> 文本），
    # 无一处位于 <script>，故 html.escape 即为对症解。
    template = template.replace("[MARKET_SOURCE]", html.escape(market_source))
    template = template.replace("[FUNDING_SOURCE]", html.escape(funding_source))
    template = template.replace("[CN_MARKET_SOURCE]", html.escape(cn_market_source))
    template = template.replace("[CN_FUNDING_SOURCE]", html.escape(cn_funding_source))

    # 市场数据来源汇总（章节标题下 + 页脚）：国内 + 国外双来源并列
    _srcs = [s for s in [market_source, funding_source, cn_market_source, cn_funding_source] if s]
    _srcs_e = [html.escape(s) for s in _srcs]
    market_summary = "；".join(_srcs_e) if _srcs_e else "数据快照（静态，非实时）"
    template = template.replace("[MARKET_SOURCE_SUMMARY]", market_summary)
    # E1（v3.4.7）：能力自检卡——服务端预渲染，禁 JS 也可见
    _cap_html = _build_capability_card(
        translate_en=translate_en,
        audience_summary=bool(audience_summary),
        cn_market_data=bool(cn_market_data),
        leaderboard_data=bool(leaderboard_data),
        insights=bool(insights),
        feishu_push=feishu_push,
    )
    template = template.replace("[CAPABILITY_CARD_PLACEHOLDER]", _cap_html)
    template = template.replace("[DATA_STATUS_BAR]",
                                _build_data_status_bar(final_leaderboard))
    if _srcs_e:
        market_footer = "市场数据来源（国内+国外）：" + "；".join(_srcs_e)
    else:
        market_footer = "市场数据来源（静态快照，非实时）"
    template = template.replace("[MARKET_SOURCE_FOOTER]", market_footer)

    # 市场数据快照日期（让读者明确这是静态快照而非实时数据）
    if not data_snapshot:
        data_snapshot = (_parse_date_arg(report_date).strftime("%Y-%m-%d")
                         if report_date else datetime.now().astimezone().strftime("%Y-%m-%d"))
    template = template.replace("[DATA_SNAPSHOT]", data_snapshot)

    # 市场数据口径路由（国内适配性）：说明当前该以哪套口径为主、哪套仅作对照
    template = template.replace("[MARKET_ROUTING_NOTE]", build_market_routing_note(region))

    # 页脚数据来源拆成两组（HON-1）：静态快照引用 / 本周信号来源，各成一块不混排。
    # 旧的单行混排会把「人工誊录的历史基线」伪装成「本周从这些机构抓到的数据」。
    _snapshot_note = snapshot_status_text()
    template = template.replace(
        "[SNAPSHOT_SOURCES_BLOCK]",
        _build_footer_snapshot_block(_snapshot_note))
    template = template.replace(
        "[WEEKLY_SOURCES_BLOCK]",
        _build_footer_weekly_block(news_items, external_source))
    # 兼容旧占位符：仍渲染成「本周真实来源」的一句话摘要（供自定义模板沿用）
    _weekly_pairs = _count_weekly_sources(news_items)
    template = template.replace(
        "[ALL_SOURCES]",
        "、".join(html.escape(n) for n, _ in _weekly_pairs) or "本周未取到 RSS 源")
    news_extra = ""
    if external_source and external_source[0]:
        ext_name_e = html.escape(external_source[0])
        ext_url_safe = safe_url(external_source[1] or "") if external_source[1] else ""
        news_extra = (f' 与 <a href="{html.escape(ext_url_safe, quote=True)}" target="_blank" '
                      f'rel="noopener">{ext_name_e}</a>' if ext_url_safe
                      else f' 与 {ext_name_e}')
    template = template.replace("[NEWS_SOURCE_EXTRA]", news_extra)
    template = template.replace("[GEN_DATE]", datetime.now().astimezone().isoformat(timespec="minutes"))  # P0#16

    # 在排行榜标题旁标注数据来源
    # 「live」= 多源池实时抓取（LMArena / Artificial Analysis / LLM-Stats / HF 等），
    # **不是** LMMarketCap——后者从未提供过任何榜单数字，只作为「未引用」署名条目保留。
    source_label = {
        "live": "多源实时榜单数据（LMArena / Artificial Analysis / LLM-Stats / Hugging Face）",
        "json": "自定义数据",
        "default": "默认数据（可能过时）",
        "unavailable": "暂无实时数据",
    }.get(ranking_source, "暂无实时数据")
    template = template.replace("[RANKING_SOURCE]", source_label)

    # 本周看点（编辑洞察 + 关键词）：注入 JSON；若无 curated 数据则自动派生基线，
    # 确保头版核心区永不静默消失（curated --insights-json 仍优先覆盖）。
    _insights = insights
    if not _insights:
        _insights = _auto_insights(api_data)
        if _insights:
            print(f"📌 未传入 --insights-json，已自动派生 {len(_insights)} 条基线看点")
    # C1#6：看点去注水——过滤纯日报聚合类（如「8点1氪」），无论人工或自动路径
    if _insights:
        before = len(_insights)
        _insights = [it for it in _insights if not _is_daily_digest(it)]
        dropped = before - len(_insights)
        if dropped:
            print(f"  💧 看点去注水：已剔除 {dropped} 条纯日报聚合类看点")
    _lead = lead or _auto_lead(news_items, total_news=len(news_items), insights=_insights)
    # 关键词：优先用 curated；规范化确保每条都带分类标签(tag)，否则从本周新闻自动派生，
    # 保证「本周关键词」区永不空、且每条必有彩色分类标签。
    _kw = _normalize_keywords(keywords)
    if not _kw:
        _kw = _auto_keywords(api_data)
        if _kw:
            print(f"🏷️ 未传入有效关键词，已自动派生 {len(_kw)} 个带标签关键词")
    template = template.replace("[INSIGHTS_KEYWORDS_PLACEHOLDER]",
                                _json_script_safe(_kw or []))
    template = template.replace("[INSIGHTS_DATA_PLACEHOLDER]",
                                _json_script_safe(_insights or []))
    # C2#8：本周数字看板（JSON 注入，模板 JS 渲染；服务端兜底也写入静态 HTML）
    template = template.replace("[WEEKLY_STATS_PLACEHOLDER]",
                                _json_script_safe(weekly_stats or {}))
    template = template.replace("[LEAD]", html.escape(_lead or ""))
    # 受众结论：未传入则回退内置默认三段（开发者/PM/自媒体），确保「给本周的你」始终出现
    template = template.replace("AUDIENCE_SUMMARY_PLACEHOLDER",
                                _json_script_safe(audience_summary or DEFAULT_AUDIENCE_SUMMARY))
    # <script> 上下文（模板 :1127 `const KEYWORD_SEARCH_SOURCES = <裸JSON>;`）：
    # 值来自 --keyword-search-sources，属不可信输入，**必须**转义——否则内容里的
    # </script> 会被 HTML 解析器当作脚本块结束，突破后执行任意 JS。
    # 用 _json_text_script_safe 而非 _json_script_safe：调用方持有的是 JSON **文本**，
    # 不重新序列化才能完整保留原格式（重序列化会改写分隔符，造成无谓的历史输出差异）。
    # 该文本的合法性有两层保障：参数层 resolve_search_sources 当场校验，渲染期 json.loads 再兜底。
    template = template.replace(
        "KEYWORD_SEARCH_SOURCES_PLACEHOLDER",
        _json_text_script_safe(keyword_search_sources or _c.DEFAULT_SEARCH_SOURCES_JSON))
    # 关键词网页搜索基址（默认百度；搜索词 = 「词语 AI 行业」）
    template = template.replace("[KEYWORD_SEARCH_BASE]", _js_str(keyword_search_base))

    # 服务端静态预渲染：把「给本周的你」受众卡 + 关键词（含分类标签）直接写进 HTML，
    # 即使客户端 JS 不执行/出错，这两块也一定出现在页面里（不再依赖 renderInsights）。
    _aud = audience_summary or DEFAULT_AUDIENCE_SUMMARY
    _aud_html = _render_audience_chips_html(_aud)
    _kw_html = _render_keyword_chips_html(_kw, search_sources=json.loads(keyword_search_sources) if keyword_search_sources else None, search_base=keyword_search_base)
    template = template.replace(
        '<div class="insights-audience-chips" id="insightsAudienceChips"><!-- JS generated --></div>',
        f'<div class="insights-audience-chips" id="insightsAudienceChips">{_aud_html}</div>' if _aud_html else
        '<div class="insights-audience-chips" id="insightsAudienceChips"></div>')
    template = template.replace(
        '<div class="insights-keywords-chips" id="insightsKeywordsChips"><!-- JS generated --></div>',
        f'<div class="insights-keywords-chips" id="insightsKeywordsChips">{_kw_html}</div>' if _kw_html else
        '<div class="insights-keywords-chips" id="insightsKeywordsChips"></div>')
    # 看点卡本体也做服务端静态预渲染（与受众/关键词卡同级；此前仅 JSON 注入靠 JS 渲染，
    # 禁 JS 时「本周看点」只剩导语没有卡）。JS renderInsights 仍会在运行时接管交互。
    _ic_html = _render_insight_cards_html(_insights)
    template = template.replace(
        '<div id="insightsList"><!-- JS generated --></div>',
        f'<div id="insightsList">{_ic_html}</div>' if _ic_html else
        '<div id="insightsList"></div>')
    # M1：本周市场信号区块（服务端预渲染，与受众/关键词卡同样不依赖 JS）
    # 新版带「印证趋势」标签，与下方「AI 行业趋势洞察」面板双向桥接
    _ms_html = _render_market_signals_html_with_theme(market_signals, _lb_map)
    template = template.replace(
        '<div class="market-signals" id="marketSignals"><!-- JS generated --></div>',
        f'<div class="market-signals" id="marketSignals">{_ms_html}</div>')
    # 「AI 行业趋势洞察」×「关于本周」合作：宏观趋势面板按周挂「本周印证」证据行
    _ti_html = _render_trend_insights_html(market_signals, news_items)
    template = template.replace("[TREND_INSIGHTS]", _ti_html)
    # 受众块默认改可见（JS 仍会按数据二次管理 display）；无受众数据时回退隐藏
    if _aud_html:
        template = template.replace(
            '<div class="insights-audience" id="insightsAudience" style="display:none;">',
            '<div class="insights-audience" id="insightsAudience">')
    else:
        template = template.replace(
            '<div class="insights-audience" id="insightsAudience" style="display:none;">',
            '<div class="insights-audience" id="insightsAudience" style="display:none;">')

    if output_path:
        Path(output_path).write_text(template, encoding="utf-8")

    return template


def _build_data_status_bar(lb: dict) -> str:
    """服务端预渲染数据状态条（A4，v3.5.1 审计修正）：

    - #1 live 源同样披露抓取日期（原实现丢弃 s["snapshot"]，削弱「数据可信」立项目标）；
    - #2 cache 缺快照日期明确标「未知日期」，不静默隐藏；
    - #3 仅在此处转义一次（原实现 name 已 escape 又二次 escape）。
    """
    comp = (lb or {}).get("comprehensive") or {}
    os_ = (lb or {}).get("open_source") or {}
    slots = [comp.get("lmarena"), comp.get("aa"), os_.get("ls"), os_.get("hf")]
    rows = []  # (name, kind, date)
    for s in slots:
        if not s or not s.get("rows"):
            continue
        raw_name = s.get("display_name") or s.get("source") or "未知榜"
        d = str(s.get("snapshot") or "")[:10]
        kind = "快照" if s.get("is_cache") else "实时"
        # #2: 缺日期明确标未知，不藏
        rows.append((raw_name, kind, d or "未知日期"))
    if not rows:
        return ('<div class="data-status-bar ds-none">'
                '📡 <b>数据状态</b>：本期无排行榜数据（源不可达且本地无快照）</div>')
    live_n = sum(1 for _, k, _ in rows if k == "实时")
    snap_n = sum(1 for _, k, _ in rows if k == "快照")
    # #3: 仅在此处转义一次（name 用原始值，日期纯 ASCII 亦统一转义）
    items = "".join(
        f"<li>{html.escape(n)} · {html.escape(k)} · 抓于 {html.escape(dt)}</li>"
        for n, k, dt in rows
    )
    detail = (f'<details class="ds-detail"><summary>数据源明细（{live_n} 实时 / {snap_n} 快照）</summary>'
              f'<ul>{items}</ul></details>')
    return ('<div class="data-status-bar">'
            f'📡 <b>数据状态</b>：{live_n} 源实时 · {snap_n} 源快照'
            + detail + '</div>')
