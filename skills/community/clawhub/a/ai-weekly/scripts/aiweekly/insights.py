"""本周看点：看点卡 / 导语 / 关键词彩标 / 受众切片 chips。

从 generate_site.py 抽出（P1#1 Phase 2）。
关键约束：三块内容（看点卡、「给本周的你」、关键词彩标）均由本模块**服务端预渲染**为
静态 HTML 片段注入模板，禁用 JS 时仍可见；`insights.json` 的 keywords[].note 受众键
必须与 audience_summary 的键（开发者/PM/自媒体）一致。
"""
import html
import re
import urllib.parse
from collections import Counter, defaultdict

from aiweekly.news import format_news_items
from aiweekly.utils import js_str_in_attr, safe_href, safe_url

__all__ = [
    "_validate_insights", "_AUTO_KICKERS", "_AUTO_SIGNALS", "_DAILY_DIGEST_MARKERS",
    "_is_daily_digest", "_find_related", "_auto_insights", "_EDITORIAL_THEMES",
    "_lead_truncate", "_week_tone", "_auto_lead", "_DEFAULT_AUDIENCE_SUMMARY",
    "_AUTO_TERM_TAGS", "_AUTO_KW_NOTE", "_infer_tag", "_KW_STOP",
    "_tokenize", "_auto_keywords", "_normalize_keywords", "_TAG_COLORS",
    "DEFAULT_ACTIVE_AUDIENCE", "DEFAULT_SEARCH_ENGINE", "GENERIC_AUDIENCE_LABEL", "_pick_preferred_key",
    "_render_audience_chips_html", "_kw_tag_html", "_kw_tier_html", "_kw_note_html",
    "_kw_search_url", "_render_keyword_chips_html",
    # 供其它子模块使用的公共入口（下划线版保留以兼容既有调用点）
    "validate_insights", "DEFAULT_AUDIENCE_SUMMARY",
]


def _validate_insights(data) -> list:
    """校验 insights.json 结构,返回错误字符串列表(空=通过)。"""
    errors = []
    if not isinstance(data, (dict, list)):
        return ["根节点必须是对象或数组"]
    keywords = data.get("keywords", []) if isinstance(data, dict) else []
    insights = data.get("insights", []) if isinstance(data, dict) else data
    if not isinstance(keywords, list):
        errors.append("keywords 必须是数组")
    for i, kw in enumerate(keywords):
        if not isinstance(kw, dict) or not kw.get("term") or not kw.get("note"):
            errors.append(f"keywords[{i}] 缺少 term 或 note")
            continue
        # note 允许字符串或「受众 -> 文案」对象；对象内值必须是字符串
        note = kw.get("note")
        if isinstance(note, dict):
            bad = [k for k, v in note.items() if not isinstance(v, str) or not v.strip()]
            if bad:
                errors.append(f"keywords[{i}].note 的受众项内容为空或非字符串: {', '.join(bad)}")
        elif not isinstance(note, str):
            errors.append(f"keywords[{i}].note 必须是字符串或「受众->文案」对象")
    # audience_summary（可选）：必须是「受众 -> 一句话结论」的对象
    if isinstance(data, dict) and data.get("audience_summary") is not None:
        aud = data.get("audience_summary")
        if not isinstance(aud, dict):
            errors.append("audience_summary 必须是对象（形如 {\"开发者\": \"...\"}）")
        else:
            bad = [k for k, v in aud.items() if not isinstance(v, str) or not v.strip()]
            if bad:
                errors.append(f"audience_summary 的受众项内容为空或非字符串: {', '.join(bad)}")
    if not isinstance(insights, list):
        errors.append("insights 必须是数组")
    else:
        req = ["kicker", "title", "analysis", "insight"]
        for i, ins in enumerate(insights):
            if not isinstance(ins, dict):
                errors.append(f"insights[{i}] 不是对象")
                continue
            missing = [k for k in req if not ins.get(k)]
            if missing:
                errors.append(f"insights[{i}] 缺少字段: {', '.join(missing)}")
    return errors


# ── 「本周看点」自动兜底（避免头版核心区静默消失）─────────────────
# 当调用方未传 --insights-json / --lead 时，从本周新闻自动派生基线看点，
# 保证「本周看点」始终有内容；人工 curated 数据仍优先覆盖。
_AUTO_KICKERS = {
    "ai-models": "模型",
    "ai-products": "产品",
    "industry": "行业",
    "paper": "论文",
    "tip": "技巧",
}
# 重要性信号词（命中越多权重越高）
_AUTO_SIGNALS = [
    ("发布", 3), ("开源", 3), ("融资", 3), ("收购", 3), ("登顶", 3), ("夺冠", 3),
    ("超越", 2), ("首发", 3), ("重磅", 3), ("推出", 2), ("基座", 2), ("模型", 1),
    ("agent", 2), ("智能体", 2), ("端侧", 2), ("具身", 2), ("突破", 3), ("论文", 2),
    ("夺冠", 3), ("刷新", 2), ("SOTA", 3), ("开源版", 3), ("上线", 2), ("封测", 2),
    # 民间热度/性价比信号（Market Research 2026-08：实测、调用量与价格是开发者
    # 「用脚投票」的最硬信号——匿名公测揭晓、免费实测、价格屠夫类报道缺位曾致
    # GLM-5.3-Flash/Ox Alpha 这类民间最高热度话题进不了看点）
    ("实测", 3), ("上手", 2), ("免费", 3), ("降价", 3), ("性价比", 3), ("价格", 2),
    ("刷屏", 3), ("爆火", 3), ("揭晓", 3), ("匿名", 3), ("公测", 3), ("下载量", 3),
    ("调用量", 3), ("token", 2), ("复刻", 2), ("网友", 2), ("横评", 2),
]

# 主题实体组（看点多样性去重：同一新闻线的多条报道只占一席，把席位让给不同话题）。
# 组名 -> 该组实体关键词；标题命中任一实体即归入该组。
_TOPIC_ENTITY_GROUPS = [
    ("GLM系", ["GLM", "Ox Alpha", "Ox-Alpha", "牛来", "智谱", "Zhipu"]),
    ("混元", ["Hy4", "Hy3", "混元", "腾讯"]),
    ("千问", ["Qwen", "千问", "阿里"]),
    ("DeepSeek", ["DeepSeek", "深度求索"]),
    ("豆包", ["豆包", "字节"]),
    ("MiniMax", ["MiniMax"]),
    ("Claude", ["Claude", "Anthropic"]),
    ("GPT/OpenAI", ["GPT", "OpenAI"]),
    ("Gemini/谷歌", ["Gemini", "谷歌"]),
    ("Kimi", ["Kimi", "月之暗面"]),
    ("Llama/Meta", ["Llama", "Meta "]),
]


def _topic_keys(title: str) -> set:
    """提取标题所属的主题实体组名集合（未命中任何组的条目返回空集，永不冲突）。"""
    return {name for name, kws in _TOPIC_ENTITY_GROUPS if any(k in title for k in kws)}


# 纯日报聚合类信源/标题特征（C1#6：看点去注水，排除这些条目作为「看点」）
_DAILY_DIGEST_MARKERS = ["8点1氪", "早讯", "早报", "日报", "每日速览", "今日速览",
                         "晚报", "晨读", "周报", "daily brief", "早知道", "三分钟速览",
                         "一氪早讯", "科技早报"]


def _is_daily_digest(item: dict) -> bool:
    """判断一条新闻是否为纯日报聚合类（不宜作为编辑「看点」）。"""
    text = f"{item.get('title', '')} {item.get('source', '')}".lower()
    return any(m.lower() in text for m in _DAILY_DIGEST_MARKERS)


def _find_related(seed: dict, items: list, exclude_titles: set, max_n: int = 2) -> list:
    """为一条看点补充 2 条相关新闻：优先同分类或共享信号词，排除日报聚合类与自身。

    返回 [{title, url, source}]，用于「同源深挖 + 异源佐证」的扩链。
    """
    seed_text = (seed.get("title", "") + " " + seed.get("summary", "")).lower()
    seed_cat = seed.get("category", "")
    scored = []
    for it in items:
        t = (it.get("title", "") or "").strip()
        if not t or t in exclude_titles:
            continue
        if _is_daily_digest(it):
            continue
        it_text = (it.get("title", "") + " " + it.get("summary", "")).lower()
        if it_text == seed_text:
            continue
        w = 0
        if it.get("category") == seed_cat:
            w += 2
        w += sum(1 for sig, _ in _AUTO_SIGNALS
                 if sig.lower() in it_text and sig.lower() in seed_text)
        if w <= 0:
            continue
        scored.append((w, it))
    scored.sort(key=lambda x: x[0], reverse=True)
    out = []
    for _, it in scored[:max_n]:
        url = it.get("url", "")
        if not url:
            continue
        out.append({"title": (it.get("title", "") or "").strip(),
                    "url": url,
                    "source": it.get("source", "")})
    return out


def _auto_insights(api_data: dict, top_n: int = 6) -> list:
    """从新闻 JSON 自动派生基线「本周看点」列表。无网络依赖。

    truncate=False：看点 analysis 字段须完整呈现摘要原文，用户明确要求
    「看点里的信息可以全部出现，而不是中途被截断」，故不过数据层截断。
    """
    try:
        items = format_news_items(api_data, truncate=False)
    except Exception:
        items = []
    if not items:
        return []

    scored = []
    for it in items:
        title_l = (it.get("title") or "").lower()
        text = f"{title_l} {(it.get('summary') or '').lower()}"
        score = float(it.get("score", 0) or 0)
        title_bonus = 0.0
        for sig, w in _AUTO_SIGNALS:
            if sig.lower() in title_l:
                title_bonus += w
        bonus = title_bonus + sum(
            w for sig, w in _AUTO_SIGNALS if sig.lower() in text and sig.lower() not in title_l
        )
        score += bonus
        # 聚合条轻降权：「A；B；C」清单式日报的信号词是塞多条新闻堆出来的，
        # 价值密度低于单主题深度文。同线竞争时让民间实测/深度文优先占席位。
        if _is_daily_digest(it):
            score -= 2.0
        scored.append((score, title_bonus, it))
    scored.sort(key=lambda x: x[0], reverse=True)

    out = []
    seen_titles = set()
    used_topics = set()  # C-多样性：已入选看点占用的主题实体组
    for score, bonus, it in scored:
        if len(out) >= top_n:
            break
        title = (it.get("title") or "").strip()
        if not title or title in seen_titles:
            continue
        # C1#6：排除纯日报聚合类作为「看点」（去注水）。
        # 高分豁免：聚合条里也可能藏着本周头号民间事件（如「匿名模型身份揭晓」）。
        # 豁免判据用 title_bonus（标题信号词权重）而非全文 bonus——日报聚合的 summary
        # 会堆砌大量信号词导致全文 bonus 虚高；只有标题本身就带强民间信号
        # （title_bonus ≥3）且总分达标（score ≥6）的聚合条才值得入场，避免一刀切陪葬。
        if _is_daily_digest(it) and not (bonus >= 3.0 and score >= 6.0):
            continue
        # 主题去重：同一新闻线（共享模型/公司实体组）的多条报道只占一席，
        # 未命中任何实体组的条目不受影响。
        tkeys = _topic_keys(title)
        if tkeys and (tkeys & used_topics):
            continue
        seen_titles.add(title)
        used_topics |= tkeys
        cat = it.get("category", "industry")
        kicker = _AUTO_KICKERS.get(cat, "行业")
        summary = (it.get("summary") or "").strip()
        # UX: 用户要求「看点」信息全部出现，不做 160 字符截断。summary 本身已是 RSS 摘要，
        # 若原始摘要过长，由模板自然换行即可，不应在数据层人为掐断。
        # 基于类别给一句轻量编辑提示（明确为自动摘要，非人工深度洞察；即「对读者意味着什么」）
        hint = {
            "ai-models": "模型侧变动，往往直接决定你选型与成本。",
            "ai-products": "产品化信号，值得关注能否为你所用。",
            "industry": "行业格局信号，影响机会窗口。",
            "paper": "新方法可能半年内落地为工具链。",
            "tip": "可直接复用的实战经验。",
        }.get(cat, "本周值得追踪的动态。")
        # C1#6：扩链——原文 + 2 条相关（同分类/共享信号词，异源佐证）
        related_url = it.get("url", "")
        related = []
        if related_url:
            related.append({"title": f"原文：{it.get('source', '来源')}", "url": related_url})
        related += _find_related(it, items, seen_titles | {title}, max_n=2)
        out.append({
            "kicker": kicker,
            "title": title,
            "analysis": summary or title,
            "insight": f"（自动摘要）{hint}",
            "related": related,
        })
    return out


# 编辑视角主线主题（用于「本周看点」导语合成：从全量新闻聚合真实信号，而非仅数分类标签）
_EDITORIAL_THEMES = [
    ("模型军备竞赛", ["万亿", "参数", "大模型", "基座模型", "旗舰", "moe", "gpt", "claude",
                     "gemini", "kimi", "deepseek", "qwen", "智谱", "glm", "混元", "文心",
                     "豆包", "llama", "mistral"]),
    ("产品化与 Agent 落地", ["agent", "智能体", "copilot", "助手", "办公", "应用", "端侧",
                          "插件", "app", "工作流", "落地", "套件"]),
    ("开源生态", ["开源", "开源版", "权重", "开放权重", "llama", "mistral"]),
    ("资本与并购", ["融资", "估值", "亿美元", "收购", "并购", "ipo", "募资", "投资", "独角兽"]),
    ("算力与芯片", ["芯片", "gpu", "算力", "hbm", "英伟达", "nvidia", "自研芯片",
                  "数据中心", "云服务", "云厂商"]),
    ("多模态与具身", ["多模态", "视频生成", "图像", "语音", "具身", "机器人", "世界模型"]),
    ("监管与政策", ["监管", "政策", "合规", "出口管制", "反垄断", "立法", "备案", "安全审查"]),
]


def _lead_truncate(title: str, max_len: int = 20) -> str:
    """把证据标题压到适合导语的长度，超出加省略号。"""
    t = (title or "").strip()
    if len(t) <= max_len:
        return t
    return t[:max_len] + "…"


def _week_tone(top_theme_names: list) -> str:
    """基于 Top 主题构成给出一句宏观基调（纯映射，不编造）。"""
    names = set(top_theme_names)
    if "模型军备竞赛" in names and ("产品化与 Agent 落地" in names or "开源生态" in names):
        return "能力狂奔、落地追赶"
    if "资本与并购" in names and "模型军备竞赛" in names:
        return "资本与模型双线升温"
    if "监管与政策" in names:
        return "狂奔与收紧并行"
    if "算力与芯片" in names:
        return "算力底座持续承压"
    if "模型军备竞赛" in names:
        return "模型迭代明显提速"
    if "产品化与 Agent 落地" in names:
        return "从能力走向场景落地"
    if "资本与并购" in names:
        return "资本加注、整合加速"
    if "开源生态" in names:
        return "开源力量持续壮大"
    return "多线并进、密集发布"


def _auto_lead(news_items: list, total_news: int = 0, insights: list = None) -> str:
    """编辑视角导语：从全量新闻聚合真实主线主题 + 关键证据，合成 2~3 句电梯演讲。

    不编造——主题与证据锚点均来自本周真实新闻数据（标题/摘要/评分）。
    仅当无任何主题信号命中时才退化为旧版分类计数兜底，保证不静默。
    """
    items = news_items or []
    if not items:
        return "本周 AI 行业动态已汇总，详见下方新闻流。"

    # 1) 主题聚合：每条新闻按 score + 命中主题词加权
    theme_scores = {name: 0.0 for name, _ in _EDITORIAL_THEMES}
    theme_anchor = {}  # name -> (hits, score, title)
    for it in items:
        text = ((it.get("title") or "") + " " + (it.get("summary") or "")).lower()
        sc = float(it.get("score", 0) or 0)
        for name, kws in _EDITORIAL_THEMES:
            hits = sum(1 for k in kws if k in text)
            if not hits:
                continue
            theme_scores[name] += hits * (1 + sc * 0.5)
            cur = theme_anchor.get(name)
            # 优先「命中更多主题词、其次评分更高」的新闻作为证据锚点，更贴主题
            if cur is None or (hits, sc) > (cur[0], cur[1]):
                theme_anchor[name] = (hits, sc, it.get("title") or "")

    ranked = sorted(((s, n) for n, s in theme_scores.items() if s > 0), reverse=True)
    if not ranked:
        # 极端兜底：退化为旧版分类计数（保持不静默）
        kickers = {}
        for it in (insights or []):
            k = it.get("kicker", "行业")
            kickers[k] = kickers.get(k, 0) + 1
        top = sorted(kickers.items(), key=lambda x: x[1], reverse=True)[:2]
        theme = "、".join(t for t, _ in top) or "模型、产品"
        n = len(insights or [])
        return f"本周共 {total_news} 条 AI 动态，头号信号集中在「{theme}」——挑 {n} 条最值得你跟进的。"

    # 2) 取 Top 主题（最多 3 个），每条配一句真实证据
    top = ranked[:3]
    clauses = []
    for i, (_, name) in enumerate(top):
        anchor = theme_anchor.get(name)
        ev = _lead_truncate(anchor[2]) if anchor else ""
        num = "①②③"[i]
        clauses.append(f"{num}{name}（{ev}）")

    tone = _week_tone([n for _, n in top])
    if len(top) == 3:
        prefix = f"本周共 {total_news} 条 AI 动态，编辑视角看主线有三——"
    else:
        prefix = f"本周共 {total_news} 条 AI 动态，编辑视角看主线集中在——"
    return prefix + "；".join(clauses) + f"。整体是「{tone}」的一周。"


# ── 「给本周的你」默认受众结论（确保该区永不静默消失）─────────────────
# 面向三类读者的一句话结论；当 --audience-summary / insights.json 未提供时回退到此。
# 受众结论默认兜底（与关键词 note 的受众键保持一致：开发者 / PM / 自媒体），
# 保证即使不传 --audience-summary，「给本周的你」也始终出现。
_DEFAULT_AUDIENCE_SUMMARY = {
    "开发者": "用开源/免费 API（Hy3、Qwen、DeepSeek）做垂直场景应用，别硬刚 base model；推理成本与端侧化直接关系你的毛利。",
    "PM": "需求在「AI+传统行业」（制造/医疗/金融），用低成本模型快速验证 PMF；国产模型替代叙事持续。",
    "自媒体": "具身智能 + 应用层爆发是 2026 最强叙事；开源 VS 闭源、国产登顶都是高传播选题。",
}

# 公共 API 别名：其它子模块（generate_site / render / publish）应使用无下划线名，
# 以免「私有符号被跨模块穿透」——被引用方就不敢改内部实现了。
validate_insights = _validate_insights
DEFAULT_AUDIENCE_SUMMARY = _DEFAULT_AUDIENCE_SUMMARY

# ── 关键词自动派生 + 分类标签 ───────────────────────────────────────
# 跟踪词 -> 分类标签（复用渲染器的 tag 色板：模型/资本/产品/安全/基建/监管）
_AUTO_TERM_TAGS = [
    ("DeepSeek", "模型"), ("Qwen", "模型"), ("千问", "模型"), ("Claude", "模型"),
    ("GPT", "模型"), ("Gemini", "模型"), ("开源", "模型"), ("多模态", "模型"),
    ("牛来", "模型"), ("Ox Alpha", "模型"), ("智谱", "模型"), ("GLM", "模型"),
    ("端侧", "产品"), ("Agent", "产品"), ("智能体", "产品"), ("应用", "产品"),
    ("具身智能", "资本"), ("融资", "资本"), ("估值", "资本"), ("收购", "资本"),
    ("推理成本", "基建"), ("算力", "基建"), ("芯片", "基建"), ("云", "基建"),
    ("监管", "监管"), ("合规", "监管"), ("政策", "监管"), ("安全", "安全"), ("隐私", "安全"),
]
# P2 (2026-09)：民间绰号 / 关键别名保送名单——出现即进关键词聚类（见 _auto_keywords）。
# 低成本高感知：让「民间怎么叫」直接改变读者对本周议题的感知。
_PRIORITY_ALIASES = {"牛来"}
# 关键词的每受众默认提示（note 为 {受众: 文案} 时渲染彩色受众标签）
_AUTO_KW_NOTE = {
    "开发者": "可作为选型 / 成本 / 落地的跟踪锚点，顺着它做资料搜集。",
    "PM": "反映需求与机会窗口，值得纳入路线图评估。",
    "自媒体": "是本周高热叙事，适合做选题与解读。",
}


def _infer_tag(term: str) -> str:
    """从跟踪词表推断关键词分类标签。"""
    if not term:
        return None
    t = term.lower()
    for cand, tag in _AUTO_TERM_TAGS:
        if cand.lower() in t:
            return tag
    return None


# 轻量 TF 聚类停用词（中英文功能词 + 过于通用的词，避免噪声主题词刷屏）
_KW_STOP = {
    # 中文功能/通用词
    "的", "了", "和", "与", "在", "是", "也", "等", "为", "对", "及", "或", "一个", "一种",
    "我们", "他们", "公司", "如何", "为什么", "什么", "可以", "通过", "使用", "表示", "称",
    "将", "已", "并", "其", "该", "这", "那", "有", "更", "中", "上", "下", "后", "前",
    "年", "月", "日", "周", "本周", "目前", "正在", "一款", "推出", "发布", "这款", "这一",
    "为何", "哪些", "一些", "这些", "那些", "据悉", "获悉", "报道", "消息", "计划", "支持",
    "提供", "显示", "认为", "成为", "可能", "已经", "开始", "继续", "包括", "以及", "研究",
    "团队", "科技", "企业", "平台", "服务", "系统", "能力", "网络", "行业", "技术", "数据",
    "市场", "发展", "方面", "进行", "用户", "今日", "全球", "中国", "美国", "国内", "国外",
    "人工智能", "模型", "智能", "学习", "算法", "宣布", "正式", "最新", "首次", "双方",
    "相关", "问题", "领域", "产品",
    # 英文
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "is", "are",
    "was", "were", "be", "by", "as", "at", "from", "ai", "we", "our", "their", "its",
    "this", "that", "new", "now", "how", "why", "what", "more", "using", "via", "has",
    "have", "will", "can", "not", "but", "they", "you", "your", "it", "if", "so", "than",
    "into", "about", "been", "model", "models", "said", "says",
}


def _tokenize(text):
    """抽取候选主题词：英文词元 + 中文 2/3/4 字 n-gram。"""
    toks = []
    for m in re.finditer(r'[A-Za-z][A-Za-z0-9+.\-]{1,}', text or ""):
        toks.append(m.group(0))
    for m in re.finditer(r'[一-鿿]{2,}', text or ""):
        run = m.group(0)
        for n in (4, 3, 2):
            for i in range(len(run) - n + 1):
                toks.append(run[i:i + n])
    return toks


def _apply_priority_alias(ranked, cands, top_n):
    """P2(2026-09)：民间绰号 / 关键别名「保送」进关键词聚类（S1 抽出，可读 + 可测）。

    ``ranked`` 为已排序、可能已截断到 ``top_n`` 的 ``[(term, count), ...]``。
    对每个保送词（``_PRIORITY_ALIASES``）：只要本周确实出现（在 ``cands`` 中）且尚未
    入选，就强制进列表——列表未满则追加，已满则替换末位（不额外撑大版面）。
    多余保送项在末尾截断回 ``top_n``。与旧内联实现逐字节等价。
    """
    present = {t.lower() for t, _ in ranked}
    candidate_terms = {c.lower() for c in cands}
    for pa in _PRIORITY_ALIASES:
        if pa.lower() in candidate_terms and pa.lower() not in present:
            if len(ranked) < top_n:
                ranked.append((pa, cands.get(pa, 1)))
            else:
                ranked[-1] = (pa, cands.get(pa, 1))
            present.add(pa.lower())
    return ranked[:top_n]


def _auto_keywords(api_data: dict, top_n: int = 8) -> list:
    """轻量 TF 聚类：从本周新闻标题/摘要自动派生 5–8 个高频主题词 + 标签。

    设计：
      - 白名单 `_AUTO_TERM_TAGS`（高精实体）优先保留，确保关键议题不漏；
      - 同时做 TF n-gram 发现，补充白名单未覆盖的新兴主题（消除人工偏斜）；
      - 过滤停用词与「出现在 >55% 新闻中」的过度通用词；
      - note 写「本周被 N 条新闻提及（如《…》）…」——是本周相关，而非通用知识。
    """
    items = format_news_items(api_data) or []
    if not items:
        return []
    n_items = len(items)
    uni = Counter()
    term_items = defaultdict(set)
    seed_set = {c.lower() for c, _ in _AUTO_TERM_TAGS}

    for idx, it in enumerate(items):
        blob = f"{it.get('title', '')} {it.get('summary', '')}"
        low = blob.lower()
        # 1) 白名单精确命中（高精，优先）
        for cand, tag in _AUTO_TERM_TAGS:
            c = low.count(cand.lower())
            if c:
                uni[cand] += c
                term_items[cand].add(idx)
        # 2) TF n-gram 发现（去停用词/短词）
        for tk in _tokenize(blob):
            tl = tk.lower()
            if tl in _KW_STOP or len(tk) < 2:
                continue
            uni[tk] += 1
            term_items[tk].add(idx)

    # 过滤：白名单词保留；TF 发现词去掉过度通用（覆盖 >55% 新闻）与低频（<2）
    cands = {}
    for t, c in uni.items():
        is_seed = t.lower() in seed_set
        if not is_seed:
            if len(term_items.get(t, set())) > 0.55 * n_items:
                continue
            if c < 2:
                continue
        cands[t] = c
    if not cands:
        cands = dict(uni.most_common(top_n))

    # 排序：白名单优先，其次词频；取 top_n
    ranked = sorted(cands.items(),
                    key=lambda x: (x[0].lower() in seed_set, x[1]),
                    reverse=True)[:top_n]

    # P2 (2026-09)：民间绰号 / 关键别名「保送」（抽成 _apply_priority_alias，单测覆盖）
    ranked = _apply_priority_alias(ranked, cands, top_n)

    def _tag_for(term):
        tl = term.lower()
        for cand, tag in _AUTO_TERM_TAGS:
            if cand.lower() in tl:
                return tag
        idxs = term_items.get(term, set())
        tagcnt = Counter()
        for idx in idxs:
            b = (items[idx].get("title", "") + " " + items[idx].get("summary", "")).lower()
            for cand, tag in _AUTO_TERM_TAGS:
                if cand.lower() in b:
                    tagcnt[tag] += 1
        return tagcnt.most_common(1)[0][0] if tagcnt else "话题"

    def _note_for(term, cov):
        idxs = sorted(term_items.get(term, set()))
        sample = ""
        if idxs:
            s = items[idxs[0]].get("title", "")
            if len(s) > 20:
                s = s[:20] + "…"
            sample = s
        base = f"本周被 {cov} 条新闻提及"
        if sample:
            base += f"（如《{sample}》等）"
        base += "，是本期高频议题，建议沿它做资料搜集与交叉验证。"
        return {
            "开发者": base + "重点关注选型 / 成本 / 落地影响。",
            "PM": base + "反映需求与机会窗口，纳入路线图评估。",
            "自媒体": base + "是本周高热叙事，适合做选题与解读。",
        }

    out = []
    for t, c in ranked:
        cov = len(term_items.get(t, set()))
        out.append({
            "term": t,
            "tag": _tag_for(t),
            "tier": "主线" if (cov >= 4 or c >= 9) else "延伸",
            "note": _note_for(t, cov),
        })
    return out


def _normalize_keywords(keywords) -> list:
    """规范化关键词：保证为 dict 列表且尽量带分类 tag。"""
    out = []
    if not isinstance(keywords, list):
        return out
    for kw in keywords:
        if not isinstance(kw, dict) or not kw.get("term"):
            continue
        kw = dict(kw)
        if not kw.get("tag"):
            kw["tag"] = _infer_tag(kw["term"])
        out.append(kw)
    return out


# ── 服务端静态预渲染：把「给本周的你」与关键词标签直接写进 HTML ──────
# 目的：即使浏览器禁用/未执行 JS，这些核心部分也一定出现在静态页面里，
# 不再依赖客户端 renderInsights()。（renderInsights 仍会在 JS 可用时运行并接管交互）
_TAG_COLORS = {
    "安全": "#e74c3c", "模型": "#3498db", "基建": "#f39c12",
    "产品": "#27ae60", "资本": "#9b59b6", "监管": "#16a085",
    "话题": "#7f8c8d",
}


# 命名常量替代散落的魔法字符串（受众默认激活项 / 默认搜索引擎 / note 通用兜底键）
DEFAULT_ACTIVE_AUDIENCE = "开发者"
DEFAULT_SEARCH_ENGINE = "baidu"
GENERIC_AUDIENCE_LABEL = "通用"


def _pick_preferred_key(d: dict, preferred: str):
    """取 preferred 键的值；缺失或为空则取第一个有值键；用于受众 note 的降级。

    避免散落 `next(iter(d), "")` 这类一次性的兜底写法。
    """
    if not isinstance(d, dict):
        return None
    if d.get(preferred):
        return d[preferred]
    for v in d.values():
        if v:
            return v
    return None


def _render_audience_chips_html(audience_summary, active=DEFAULT_ACTIVE_AUDIENCE) -> str:
    """把受众结论渲染成静态 chips HTML（与 JS renderInsights 输出一致）。"""
    if not isinstance(audience_summary, dict) or not audience_summary:
        return ""
    parts = []
    for key in audience_summary:
        cls = "audience-chip active" if key == active else "audience-chip"
        # data-audience 与文本节点属 HTML 上下文 → html.escape 足够；
        # 但 onclick 内嵌的是 **JS 字符串字面量**，必须走 js_str_in_attr 做两层转义
        # （仅 html.escape 会被浏览器先做实体解码后失效）。
        key_attr = html.escape(key, quote=True)
        parts.append(
            f'<span class="{cls}" data-audience="{key_attr}" '
            f'onclick="switchAudience(\'{js_str_in_attr(key)}\', this)">'
            f"{key_attr}</span>"
        )
    return "\n".join(parts)


def _kw_tag_html(tag: str) -> str:
    """关键词分类彩标 HTML。"""
    if not tag:
        return ""
    color = _TAG_COLORS.get(tag, "#888")
    return (f'<span class="kw-tag" style="background:{color}22;color:{color};">'
            f"{html.escape(tag, quote=True)}</span>")


def _kw_tier_html(tier: str) -> str:
    """关键词层级（主线/延伸）标签 HTML。"""
    if not tier:
        return ""
    tier_cls = "kw-tier-main" if tier == "主线" else "kw-tier-ext"
    return f'<span class="kw-tier {tier_cls}">{html.escape(tier, quote=True)}</span>'


def _kw_note_html(note, active: str) -> str:
    """关键词面向当前受众的注释 HTML。"""
    if not note:
        return ""
    note_obj = note if isinstance(note, dict) else {GENERIC_AUDIENCE_LABEL: note}
    note_text = _pick_preferred_key(note_obj, active)
    if not note_text:
        return ""
    return (f'<div class="kw-note" style="margin-top:6px;font-size:12px;'
            f'line-height:1.5;color:var(--text-secondary);">'
            f'<b style="color:var(--accent);">{html.escape(active, quote=True)}：</b>'
            f"{html.escape(note_text, quote=True)}</div>")


def _kw_search_url(k: dict, active: str, base: str) -> str:
    """关键词点击跳转的网页搜索 URL。"""
    search = k.get("search")
    if isinstance(search, dict):
        q = _pick_preferred_key(search, active) or k.get("term", "")
        q = f"{q} AI"
    else:
        q = f"{k.get('term', '')} AI 行业"
    return base + urllib.parse.quote(q)


def _render_keyword_chips_html(keywords, active=DEFAULT_ACTIVE_AUDIENCE,
                               search_sources=None,
                               search_base="https://www.baidu.com/s?wd=") -> str:
    """把关键词渲染成静态 chips HTML（含彩色分类标签 tag），与 JS 输出一致。"""
    if not keywords:
        return ""
    src = search_sources or {"baidu": "https://www.baidu.com/s?wd="}
    base = src.get(DEFAULT_SEARCH_ENGINE) or search_base
    parts = []
    for k in keywords:
        if not isinstance(k, dict):
            k = {"term": k}
        term = k.get("term") or ""
        if not term:
            continue
        parts.append(
            f'<div class="kw-item" style="margin-bottom:12px;">\n'
            f'  <a class="kw-chip" href="{safe_href(_kw_search_url(k, active, base))}" '
            f'target="_blank" rel="noopener" '
            f'title="在网页中搜索「{html.escape(term, quote=True)} AI」" '
            f'style="display:flex;align-items:center;gap:8px;">\n'
            f'    <span class="kw-term" style="font-weight:600;">'
            f'{html.escape(term, quote=True)} <span class="kw-go">↗</span></span>\n'
            f"    {_kw_tag_html(k.get('tag'))}\n    {_kw_tier_html(k.get('tier'))}\n  </a>\n"
            f"  {_kw_note_html(k.get('note'), active)}\n</div>"
        )
    return "\n".join(parts)


def _render_insight_cards_html(insights) -> str:
    """把看点列表渲染成静态卡片 HTML，与模板 JS renderInsights 输出结构一致
    （insight-card / 看点 NN / insight-kicker / insight-title / insight-analysis /
    insight-editorial / insight-related）。禁 JS 时看点卡依然可见。"""
    if not insights:
        return ""
    parts = []
    for i, it in enumerate(insights, 1):
        if not isinstance(it, dict):
            continue
        title = (it.get("title") or "").strip()
        if not title:
            continue
        num = f"{i:02d}"
        kicker = (f'<span class="insight-kicker">{html.escape(it["kicker"])}</span>'
                  if it.get("kicker") else "")
        analysis = (f'<p class="insight-analysis">{html.escape(it["analysis"])}</p>'
                    if it.get("analysis") else "")
        editorial = (f'<div class="insight-editorial"><b>编辑洞察</b>'
                     f'{html.escape(it["insight"])}</div>'
                     if it.get("insight") else "")
        related_items = []
        for r in (it.get("related") or []):
            if not isinstance(r, dict) or not r.get("title"):
                continue
            url = safe_url(r.get("url") or "")
            related_items.append(
                f'<a href="{html.escape(url, quote=True)}" target="_blank" '
                f'rel="noopener">{html.escape(r["title"])} →</a>')
        related = (f'<div class="insight-related">{"".join(related_items)}</div>'
                   if related_items else "")
        parts.append(
            f'<article class="insight-card">\n'
            f'      <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">\n'
            f'        <span style="font-size:13px;font-weight:600;color:var(--accent);">看点 {num}</span>\n'
            f'        {kicker}\n      </div>\n'
            f'      <h3 class="insight-title">{html.escape(title)}</h3>\n'
            f'      {analysis}\n      {editorial}\n      {related}\n    </article>'
        )
    return "\n".join(parts)

