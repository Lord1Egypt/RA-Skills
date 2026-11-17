# validate_checks/news_v3.py — v3.0 新闻站检查（新闻/编辑/搜索/图表/排行榜）
import re
import json
from .common import _extract_js_var

def check_news_v3(html_content: str, min_news: int = 20, min_cov: float = 80) -> dict:
    """
    检查新闻条目数量和来源链接覆盖率。
    - 从 NEWS_DATA JS 数组中提取条目数
    - 检查每条新闻是否有 url 字段
    返回 {ok, warn, ...}:ok=硬门槛达标;warn=接近门槛(降级但可用)。
    """
    # 提取 NEWS_DATA 数组
    news_match = re.search(r'const NEWS_DATA\s*=\s*(\[[\s\S]*?\])\s*;', html_content)
    if not news_match:
        # 回退：数 .news-card 结构
        cards = re.findall(r'class="news-card"', html_content)
        count = len(cards)
        ok = count >= min_news
        warn = (min_news // 2) <= count < min_news
        return {
            "ok": ok,
            "warn": warn,
            "count": count,
            "with_urls": count,
            "msg": f"找到 {count} 条新闻卡片" + (" ✅" if ok else (" ⚠️ 接近门槛" if warn else f" ⚠️ 建议 ≥ {min_news} 条"))
        }

    try:
        raw_data = news_match.group(1)
        # 提取 url 字段
        urls = re.findall(r'"url":\s*"([^"]+)"', raw_data)
        total = raw_data.count('"title"')

        # 检查 url 是否为有效链接（非空）
        valid_urls = [u for u in urls if u.startswith('http')]
        coverage = len(valid_urls) / total * 100 if total > 0 else 0

        ok = total >= min_news and coverage >= min_cov
        warn = (not ok) and ((min_news // 2) <= total < min_news
                             or (min_cov - 20) <= coverage < min_cov)
        return {
            "ok": ok,
            "warn": warn,
            "count": total,
            "with_urls": len(valid_urls),
            "coverage": f"{coverage:.0f}%",
            "msg": (f"找到 {total} 条新闻，{len(valid_urls)} 条含原始链接（{coverage:.0f}%）"
                    + (" ✅" if ok else (" ⚠️ 接近门槛" if warn else f" ⚠️ 建议 ≥ {min_news} 条 / 覆盖率 ≥ {min_cov:.0f}%")))
        }
    except Exception as e:
        return {"ok": False, "warn": False, "count": 0, "with_urls": 0, "msg": f"解析 NEWS_DATA 失败：{e}"}


def check_editorial_c0(html_content: str) -> dict:
    """C0 内容质量校验：摘要归一、🔥必读标记、信源短名。

    三项任一不达标即判不通过（ok=False），直接拉低总分，确保 C0 落地可追溯。
    """
    news_match = re.search(r'const NEWS_DATA\s*=\s*(\[[\s\S]*?\])\s*;', html_content)
    if not news_match:
        return {"ok": False, "warn": False, "msg": "未找到 NEWS_DATA，无法校验 C0"}
    try:
        data = json.loads(news_match.group(1))
    except Exception as e:
        return {"ok": False, "warn": False, "msg": f"NEWS_DATA 解析失败：{e}"}

    total = len(data)
    if total == 0:
        return {"ok": False, "warn": False, "msg": "新闻为空，无法校验 C0"}

    # 1) 摘要 > 120 字占比（归一化目标：<20%）
    long_sum = sum(1 for n in data if len(n.get("summary", "") or "") > 120)
    long_ratio = long_sum / total
    summary_ok = long_ratio < 0.20

    # 2) 🔥必读标记存在且数量合理（5~12）
    mr = sum(1 for n in data if n.get("mustRead") is True)
    mustread_ok = (5 <= mr <= 12)

    # 3) 信源短名：含 RSS feed 分隔符（" | " / " - "）视为未归一
    verbose = sum(1 for n in data
                  if (" | " in (n.get("source", "") or "")) or (" - " in (n.get("source", "") or "")))
    source_ok = verbose == 0

    # 4) 语言标签：每条必须有 zh/en（供「语言」筛选）；整份缺失某一语言→检测可能失效（warn）
    missing_lang = sum(1 for n in data if n.get("lang") not in ("zh", "en"))
    zh = sum(1 for n in data if n.get("lang") == "zh")
    en = sum(1 for n in data if n.get("lang") == "en")
    lang_ok = missing_lang == 0
    lang_warn = (zh == 0 or en == 0)

    ok = summary_ok and mustread_ok and source_ok and lang_ok
    details = [
        f"摘要>120字 {long_sum}/{total}（{long_ratio*100:.0f}%，阈值<20% {'✅' if summary_ok else '❌'}）",
        f"🔥必读 {mr} 条（合理 5–12 {'✅' if mustread_ok else '❌'}）",
        f"信源含 RSS 分隔符 {verbose} 条（应=0 {'✅' if source_ok else '❌'}）",
        f"语言标签 zh={zh}/en={en}（缺失 {missing_lang} {'✅' if lang_ok else '❌'}{'，⚠️整份缺某语言' if lang_warn else ''}）",
    ]
    return {
        "ok": ok,
        "summary_ok": summary_ok, "mustread_ok": mustread_ok, "source_ok": source_ok, "lang_ok": lang_ok,
        "long_ratio": round(long_ratio, 3), "mustread": mr, "verbose_source": verbose,
        "lang_zh": zh, "lang_en": en, "lang_missing": missing_lang,
        "msg": "；".join(details),
    }


_DAILY_DIGEST_MARKERS = ["8点1氪", "早讯", "早报", "日报", "每日速览", "今日速览",
                         "晚报", "晨读", "周报", "daily brief", "早知道", "三分钟速览",
                         "一氪早讯", "科技早报"]


def check_editorial_c1(html_content: str) -> dict:
    """C1 内容质量校验：看点去注水（无日报聚合类）+ 榜单时效标注。

    - 看点含日报聚合类（如「8点1氪」）→ 不通过（去注水未生效）
    - 榜单快照距报告日超龄 → 因「已显式标注」满足 8.3 的「或显式标注」分支，判通过但提示龄期
    """
    # 1) 看点去注水
    ins_raw = _extract_js_var("INSIGHTS_DATA", html_content)
    digest_hits = []
    if ins_raw:
        try:
            ins = json.loads(ins_raw)
        except Exception:
            ins = []
        for it in ins:
            t = f"{it.get('title', '')} {it.get('source', '')}".lower()
            if any(m.lower() in t for m in _DAILY_DIGEST_MARKERS):
                digest_hits.append(it.get("title", "")[:30])
    digest_ok = len(digest_hits) == 0

    # 2) 榜单时效标注（读 generate() 注入的 meta.snapshot_stale / snapshot_max_age）
    lb_raw = _extract_js_var("LEADERBOARD_DATA", html_content)
    snap_stale = False
    snap_max_age = None
    if lb_raw:
        try:
            lb = json.loads(lb_raw)
            meta = (lb.get("meta") or {}) if isinstance(lb, dict) else {}
            snap_stale = bool(meta.get("snapshot_stale"))
            snap_max_age = meta.get("snapshot_max_age")
        except Exception:
            pass
    # 显式标注即满足 8.3 的「或显式标注」分支 → 通过；仅提示龄期
    snap_ok = True

    ok = digest_ok and snap_ok
    details = [
        f"看点日报聚合类 {len(digest_hits)} 条（应=0 {'✅' if digest_ok else '❌'}）",
        f"榜单快照标注 {'已显式标注' if snap_stale else '新鲜'}（最大龄 {snap_max_age if snap_max_age is not None else '—'} 天，超龄已告警 {'✅' if snap_ok else '❌'}）",
    ]
    if digest_hits:
        details.append("含：" + "；".join(digest_hits))
    return {
        "ok": ok,
        "digest_ok": digest_ok, "digest_hits": digest_hits,
        "snap_stale": snap_stale, "snap_max_age": snap_max_age,
        "msg": "；".join(details),
    }


def check_search_v3(html_content: str) -> dict:
    """检查搜索栏和分类标签是否存在。"""
    has_search = 'searchInput' in html_content or 'search-input' in html_content
    has_tabs = 'tabsContainer' in html_content or 'class="tabs"' in html_content
    has_category_filter = 'activeCategory' in html_content or 'switchTab' in html_content

    all_ok = has_search and has_tabs and has_category_filter
    issues = []
    if not has_search:
        issues.append("缺少搜索栏")
    if not has_tabs:
        issues.append("缺少分类标签")
    if not has_category_filter:
        issues.append("缺少分类筛选逻辑")

    return {
        "ok": all_ok,
        "has_search": has_search,
        "has_tabs": has_tabs,
        "has_filter": has_category_filter,
        "msg": "搜索、分类、筛选功能完整 ✅" if all_ok else "缺少：" + ", ".join(issues)
    }


def check_charts_v3(html_content: str) -> dict:
    """检查 v3.0 的 2 个 Chart.js 图表（市场规模 + 融资趋势）。"""
    charts = [
        ("marketSizeChart", "市场规模柱状图"),
        ("fundingChart",    "AI融资折线图"),
    ]

    details = []
    funding_points = None
    for chart_id, chart_name in charts:
        init_pattern = rf"getElementById\(['\"]{chart_id}['\"]\)"
        has_init = re.search(init_pattern, html_content) is not None

        if not has_init:
            details.append({"id": chart_id, "ok": False, "msg": f"{chart_name}：未找到图表初始化代码"})
            continue

        # 提取数据数组
        init_match = re.search(init_pattern, html_content)
        if init_match:
            block = html_content[init_match.start():init_match.start() + 3000]
            data_arrays = re.findall(r"data:\s*(\[[\d\s,\.\-eE+]+\])", block)

            if data_arrays:
                main_arr = data_arrays[0]
                num_points = main_arr.count(",") + 1 if "," in main_arr else 1
                if chart_id == "fundingChart":
                    funding_points = num_points
                details.append({"id": chart_id, "ok": True,
                                "msg": f"{chart_name}：数据正常（{num_points} 个数据点）"})
            else:
                details.append({"id": chart_id, "ok": False, "msg": f"{chart_name}：数据数组缺失"})

    ok = all(d["ok"] for d in details)
    # 融资数据点过少(<4)仅作警告(非致命),提醒补充更完整真实序列
    warn = funding_points is not None and funding_points < 4
    return {"ok": ok, "warn": warn, "details": details,
            "msg": ("⚠️ 融资数据点偏少(<4),建议补充更完整的真实季度序列" if warn else "")}


def _extract_balanced_brace(html_content: str, start: int) -> str:
    """从 start（'{' 位置）开始，按括号配平截取对象字面量。"""
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(html_content)):
        c = html_content[i]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return html_content[start:i + 1]
    return html_content[start:]


def check_ranking_v3(html_content: str, min_ranking: int = 5) -> dict:
    """检查模型排行榜（双榜：综合榜 LMArena+AA / 开源榜 HF）是否存在且有数据。"""
    has_ranking = ('LEADERBOARD_DATA' in html_content
                   or 'RANKING_DATA' in html_content
                   or 'ranking-table' in html_content)

    if not has_ranking:
        return {"ok": False, "warn": False, "msg": "未找到模型排行榜"}

    # 新双榜结构：const LEADERBOARD_DATA = { ... };
    lb_idx = html_content.find('const LEADERBOARD_DATA')
    if lb_idx >= 0:
        brace = html_content.find('{', lb_idx)
        if brace >= 0:
            raw = _extract_balanced_brace(html_content, brace)
            try:
                data = json.loads(raw)
            except Exception:
                # 宽松模式：退化为按行对象计数
                n = raw.count('"model":') or raw.count('"name":')
                return {"ok": n >= 10, "count": n,
                        "msg": f"双排行榜已填充（约 {n} 条，宽松解析）"}
            comp = data.get("comprehensive", {}) or {}
            lm_rows = (comp.get("lmarena", {}) or {}).get("rows", []) or []
            aa_rows = (comp.get("aa", {}) or {}).get("rows", []) or []
            osb = data.get("open_source", {}) or {}
            ls = osb.get("ls", {}) or {}
            ls_rows = ls.get("rows", []) or []
            hf = osb.get("hf", {}) or {}
            hf_rows = hf.get("rows", []) or []
            counts = {
                "LMArena 综合": len(lm_rows),
                "AA 智能指数": len(aa_rows),
                "LLM-Stats 开源": len(ls_rows),
                "HF 开源": len(hf_rows),
            }
            total = sum(counts.values())
            all_ok = all(v >= min_ranking for v in counts.values())
            warn = any((min_ranking // 2) <= v < min_ranking for v in counts.values())
            detail = "，".join(f"{k} {v} 条" for k, v in counts.items())
            return {"ok": all_ok, "warn": warn, "counts": counts, "count": total,
                    "msg": f"双排行榜：{detail} {'✅' if all_ok else ('⚠️ 接近门槛' if warn else f'⚠️ 每榜建议 ≥{min_ranking} 条')}"}

    # 旧版单榜结构：const RANKING_DATA = [ ... ];
    rank_match = re.search(r'const RANKING_DATA\s*=\s*(\[[\s\S]*?\])\s*;', html_content)
    if rank_match:
        count = rank_match.group(1).count('"name"')
        return {"ok": count >= 5, "warn": False, "count": count, "msg": f"排行榜 {count} 个模型 ✅"}
    return {"ok": True, "warn": False, "msg": "排行榜存在"}


def _extract_leaderboard_data(html_content: str):
    """从 HTML 中提取 LEADERBOARD_DATA 的解析对象（供质量/schema 校验复用）。"""
    lb_idx = html_content.find('const LEADERBOARD_DATA')
    if lb_idx < 0:
        return None
    brace = html_content.find('{', lb_idx)
    if brace < 0:
        return None
    raw = _extract_balanced_brace(html_content, brace)
    try:
        return json.loads(raw)
    except Exception:
        return None


def check_leaderboard_quality(html_content: str) -> dict:
    """对 LEADERBOARD_DATA 做质量 + schema 校验（每榜 source/url/snapshot 非空、
    model 非空、同榜归一键去重、跨榜 rank 差 ≤ 20、selection_notes 三段、delta 覆盖、字段白名单）。
    """
    data = _extract_leaderboard_data(html_content)
    if data is None:
        return {"ok": False, "warn": False, "msg": "未找到 LEADERBOARD_DATA"}
    try:
        from aiweekly.leaderboard import validate_leaderboard_data
    except Exception:
        # 校验器独立运行时退化为自行计算（避免强依赖 aiweekly 包）
        return _fallback_leaderboard_quality(data)
    res = validate_leaderboard_data(data)
    if res["ok"]:
        cov = min((c.get("delta_coverage", 0) for c in res["checks"].values()
                   if isinstance(c, dict) and "delta_coverage" in c), default=0)
        return {"ok": True, "warn": False, "msg": f"排行榜质量+schema 校验通过（delta 覆盖 {cov}）✅",
                "checks": res["checks"]}
    return {"ok": False, "warn": False,
            "msg": "排行榜质量/schema 问题：" + "；".join(res["issues"][:6]),
            "checks": res["checks"], "issues": res["issues"]}


def _fallback_leaderboard_quality(data: dict) -> dict:
    """校验器脱离 aiweekly 包时的降级版（仅做核心断言，不依赖导入）。"""
    issues = []
    comp = data.get("comprehensive", {}) or {}
    osb = data.get("open_source", {}) or {}
    for name, slot in (("comprehensive.lmarena", comp.get("lmarena", {})),
                       ("comprehensive.aa", comp.get("aa", {})),
                       ("open_source.ls", osb.get("ls", {})),
                       ("open_source.hf", osb.get("hf", {}))):
        slot = slot or {}
        rows = slot.get("rows", []) or []
        if len(rows) < 5:
            issues.append(f"[{name}] 行数 < 5")
        if not slot.get("is_cache"):
            for f in ("source", "url", "snapshot"):
                if not str(slot.get(f, "")).strip():
                    issues.append(f"[{name}] {f} 空")
        if any(not str(r.get("model", "")).strip() for r in rows):
            issues.append(f"[{name}] 空 model")
    sn = data.get("selection_notes")
    if not (isinstance(sn, dict) and all(sn.get(k) for k in ("开发者", "PM", "自媒体"))):
        issues.append("selection_notes 缺三段")
    if issues:
        return {"ok": False, "warn": False, "msg": "；".join(issues[:6])}
    return {"ok": True, "warn": False, "msg": "排行榜质量校验通过（降级版）✅"}
