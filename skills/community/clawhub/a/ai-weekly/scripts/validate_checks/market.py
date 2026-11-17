# validate_checks/market.py — 市场板块守护（M0/M1/M2/M3）
import re

def check_market_disclaimer(html_content: str) -> dict:
    """M0 守护：市场板块不得再出现「示例/估算」自损式免责，且四张图均需有真实来源署名。

    - HTML 含「示例/估算」字样 → 不通过（M0 回退 bug 复现）
    - 四张图的「来源：… · 快照」署名缺失或含「示例/估算」→ 不通过
    """
    import re
    has_disclaimer = "示例/估算" in html_content
    notes = re.findall(r"来源：([^<]*?)· 快照", html_content)
    bad = [n for n in notes if (not n.strip()) or ("示例" in n) or ("估算" in n)]
    ok = (not has_disclaimer) and (len(notes) >= 4) and (len(bad) == 0)
    return {
        "ok": ok,
        "warn": False,
        "msg": ("市场数据署名正常，无自损式免责"
                if ok else
                f"市场数据仍含自损式免责或来源缺失（署名 {len(notes)-len(bad)}/{len(notes)} 真实）"),
    }


def check_market_signals(html_content: str) -> dict:
    """M1 守护：市场板块须含「本周市场信号」动态区块，且由本周新闻派生（非静态模板）。

    - 无 marketSignals 区块 → 不通过（M1 未接入）
    - 区块内既无 ms-card（信号卡）也无 ms-empty（诚实空态）→ 不通过（疑似回退/空注入）
    """
    import re
    has_block = "marketSignals" in html_content
    if not has_block:
        return {"ok": False, "warn": False, "msg": "未找到「本周市场信号」区块（M1 未接入）"}
    cards = len(re.findall(r'class="ms-card"', html_content))
    empty = "ms-empty" in html_content
    ok = cards > 0 or empty
    msg = (f"本周市场信号已注入（{cards} 条信号卡，由本周新闻派生）"
           if ok else "marketSignals 区块为空，疑似回退/未注入")
    return {"ok": ok, "warn": False, "msg": msg}


def check_market_structure(html_content: str) -> dict:
    """M2 守护：市场板块须含 6 张图（规模/融资 × 全球/中国 + 中国赛道结构 + 头部集中度），
    且结构图赛道标签已出现、[TREND_INSIGHTS] 占位符已被替换（未残留模板占位）。"""
    import re
    canvases = ["marketSizeChart", "cnMarketChart", "fundingChart",
                "cnFundingChart", "cnStructureChart", "cnConcentrationChart"]
    missing = [c for c in canvases if f'id="{c}"' not in html_content]
    struct_labels = ["大模型", "具身智能", "AIGC 应用"]
    missing_labels = [l for l in struct_labels if l not in html_content]
    placeholder_left = "[TREND_INSIGHTS]" in html_content
    ok = (not missing) and (not missing_labels) and (not placeholder_left)
    if ok:
        msg = "市场板块 6 图齐全（含中国赛道结构 / 头部集中度），结构标签已渲染"
    else:
        bits = []
        if missing:
            bits.append(f"缺图 {missing}")
        if missing_labels:
            bits.append(f"缺结构标签 {missing_labels}")
        if placeholder_left:
            bits.append("趋势洞察占位符未替换")
        msg = "；".join(bits)
    return {"ok": ok, "warn": False, "msg": msg}


def check_trend_evidence(html_content: str) -> dict:
    """「趋势洞察 × 本周」合作守护：宏观趋势面板须挂「本周印证」证据行（来自本周信号/新闻）。"""
    import re
    ev = len(re.findall(r'class="insight-evidence"', html_content))
    ok = ev >= 1
    msg = (f"趋势洞察面板已挂 {ev} 条「本周印证」（宏观趋势↔本周事件联动）"
           if ok else "趋势洞察面板无「本周印证」行，未与本周联动")
    return {"ok": ok, "warn": False, "msg": msg}


def check_market_data(html_content: str) -> dict:
    """M3 守护：图表分析厚度与防回归。

    - 6 张图 canvas 均存在（结构/趋势/集中度齐全）
    - 6 张图的服务端 SVG 兜底就位（JS / Canvas 被查看环境拦掉时仍可见）
    - 每图来源署名已填（无 [xxx_SOURCE] 占位残留）
    - 快照日期已显示（[DATA_SNAPSHOT] 已替换）
    - 无「示例/估算」与真实来源并存的矛盾（自损免责已撤）
    """
    import re
    canvases = ["marketSizeChart", "cnMarketChart", "fundingChart",
                "cnFundingChart", "cnStructureChart", "cnConcentrationChart"]
    missing_canvas = [c for c in canvases if f'id="{c}"' not in html_content]
    # 2026-09-22：图表双轨——服务端 SVG 必须就位，否则受限环境只剩空白 canvas
    svg_n = html_content.count('class="chart-svg"')
    svg_leftover = "[CHART_SVG_" in html_content
    src_placeholders = [p for p in
                        ("[MARKET_SOURCE]", "[FUNDING_SOURCE]", "[CN_MARKET_SOURCE]", "[CN_FUNDING_SOURCE]")
                        if p in html_content]
    snap_left = "[DATA_SNAPSHOT]" in html_content
    disclaimer = "示例/估算" in html_content
    ok = ((not missing_canvas) and svg_n == len(canvases) and not svg_leftover
          and (not src_placeholders) and (not snap_left) and (not disclaimer))
    if ok:
        msg = ("市场图表 6 图齐全（含 6 张服务端 SVG 兜底）、来源署名/快照日期已填、"
               "无自损免责残留（M3 厚度达标）")
    else:
        bits = []
        if missing_canvas:
            bits.append(f"缺图 {missing_canvas}")
        if svg_leftover:
            bits.append("服务端 SVG 占位未替换 [CHART_SVG_*]")
        elif svg_n != len(canvases):
            bits.append(f"服务端 SVG 兜底 {svg_n}/{len(canvases)} 张（JS/Canvas 被拦时市场图会消失）")
        if src_placeholders:
            bits.append(f"来源占位未替换 {src_placeholders}")
        if snap_left:
            bits.append("快照日期占位未替换")
        if disclaimer:
            bits.append("仍存在「示例/估算」自损免责")
        msg = "；".join(bits)
    return {"ok": ok, "warn": False, "msg": msg}


def check_en_cn_summary(html_content: str) -> dict:
    """英文报道中文总结守护（best-effort / warn 级）。

    新闻卡片由客户端 JS 渲染，静态 HTML 无法直接数徽标，故解析嵌入的 NEWS_DATA：
    统计 lang=en 条目中已带非空 cn_summary 的覆盖情况。
    - 无英文报道 → ok（无需总结）
    - 有英文报道且覆盖 ≥1 → ok；覆盖偏低（<50%）→ warn（建议提高并发/超时或重跑）
    - 有英文报道但 0 覆盖 → warn（建议开启 --translate-en）
    """
    import re, json
    m = re.search(r'const NEWS_DATA\s*=\s*(\[.*?\]);', html_content, re.S)
    if not m:
        return {"ok": True, "warn": False, "msg": "未找到 NEWS_DATA（无法核验，跳过）"}
    try:
        data = json.loads(m.group(1))
    except Exception:
        return {"ok": True, "warn": False, "msg": "NEWS_DATA 解析失败（无法核验，跳过）"}
    en = [x for x in data if isinstance(x, dict) and x.get("lang") == "en"]
    if not en:
        return {"ok": True, "warn": False, "msg": "报告无英文报道，无需中文总结"}
    trans = [x for x in en if (x.get("cn_summary") or "").strip()]
    cov = len(trans) / len(en)
    if len(trans) == 0:
        return {"ok": True, "warn": True,
                "msg": f"报告含 {len(en)} 条英文报道但 0 条中文总结（建议重生成时加 --translate-en）"}
    if cov < 0.5:
        return {"ok": True, "warn": True,
                "msg": f"英文报道中文总结覆盖 {len(trans)}/{len(en)}（{cov*100:.0f}%，偏低，建议提高并发/超时或重跑）"}
    return {"ok": True, "warn": False,
            "msg": f"英文报道中文总结覆盖 {len(trans)}/{len(en)}（{cov*100:.0f}%）"}


def check_market_signals_cn(html_content: str) -> dict:
    """市场信号英文链接中文注解守护（Fix2：与新闻卡一致，方便英文不好的中文读者）。

    英文市场信号卡（链接到英文新闻）须带 .ms-cn 中文注解。
    解析嵌入的 NEWS_DATA 取「英文且含 cn_summary」的 url 集合，再核对其出现在
    市场信号卡（ms-card / ms-title）时是否配套 .ms-cn 注解。
    """
    import re, json
    from json import JSONDecoder
    m = re.search(r'const\s+NEWS_DATA\s*=\s*', html_content)
    if not m:
        return {"ok": True, "warn": False, "msg": "未找到 NEWS_DATA（跳过核验）"}
    try:
        data, _ = JSONDecoder().raw_decode(html_content, m.end())
    except Exception:
        return {"ok": True, "warn": False, "msg": "NEWS_DATA 解析失败（跳过核验）"}
    en_urls = {x.get("url") for x in data
               if isinstance(x, dict) and x.get("lang") == "en"
               and (x.get("cn_summary") or "").strip()}
    if not en_urls:
        return {"ok": True, "warn": False, "msg": "无含中文总结的英文报道，无需市场信号注解"}

    # ms-card 仅出现在市场信号区块，直接全文切分即可
    segs = html_content.split('<div class="ms-card">')[1:]
    checked = 0
    missing = 0
    for seg in segs:
        card = seg.split('<div class="ms-card">')[0]  # 仅本卡内容
        hm = re.search(r'ms-title"\s+href="([^"]*)"', card)
        if not hm:
            continue
        if hm.group(1) in en_urls:
            checked += 1
            if 'class="ms-cn"' not in card:
                missing += 1

    if checked == 0:
        return {"ok": True, "warn": False,
                "msg": "本周市场信号无英文链接卡（无需注解）"}
    if missing == 0:
        return {"ok": True, "warn": False,
                "msg": f"市场信号英文链接卡 {checked} 张均带中文注解（Fix2 达标）"}
    return {"ok": False, "warn": False,
            "msg": f"{missing}/{checked} 张英文市场信号卡缺中文注解"}
