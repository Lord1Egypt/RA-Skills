#!/usr/bin/env python3
"""
AI 前沿情报 · v3.0 简报生成器
用法:
  python3 generate-briefing.py --mode full     # 全量简报
  python3 generate-briefing.py --mode quick    # 快速信号检测
  python3 generate-briefing.py --mode arxiv    # 仅 arXiv 论文
  python3 generate-briefing.py --mode github   # 仅 GitHub Trending
"""
import json, sys, argparse, subprocess
from datetime import datetime
from pathlib import Path

# ─── 配置 ───────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent
SKILL_ROOT = SKILL_DIR.parent  # skill root (one level up from scripts/)
DATA_DIR = SKILL_ROOT / "data"
CANDIDATES_DEFAULT = DATA_DIR / "candidates" / "today_candidates.json"
CONFIG_FILE = SKILL_ROOT / "references" / "BRIEFING_CONFIG.md"
ARXIV_SCRIPT = SKILL_DIR / "arxiv-fetch.sh"
GH_SCRIPT = SKILL_DIR / "github-trending-fetch.sh"

# 36氪 API
KR_API = "https://openclaw.36krcdn.com/media/hotlist/{date}/24h_hot_list.json"

# 评分维度权重
SCORE_WEIGHTS = {
    'enterprise_landing': 0.40,
    'data_support': 0.20,
    'learnability': 0.20,
    'novelty': 0.20,
}

# ─── 自动评分关键词 ──────────────────────────────────────────────
ENTERPRISE_KW = [
    'enterprise', 'customer', 'business', 'production', 'deployment', 'case study',
    'company', 'organization', 'roi', 'revenue', 'savings', 'scale',
    'fortune 500', 'fortune500', 'regulated', 'industry', 'copilot',
    'automate', 'automates', 'streamline', 'boost', 'productivity',
    'available on', 'built with', 'powered by', 'how we used',
    '企业', '客户', '落地', '部署', '案例', '行业', '转型', '自动化', '提效'
]
DATA_KW = [
    '%', 'percent', 'x faster', 'x cheaper', 'reduced', 'increased', 'improved',
    'saved', 'cost', 'efficiency', 'accuracy', 'latency', 'benchmark',
    'million', 'billion', 'thousand', '量化', '效率', '成本'
]
LEARN_KW = [
    'how we', 'architecture', 'methodology', 'best practice', 'lesson',
    'framework', 'pattern', 'approach', 'strategy', 'pipeline', 'workflow',
    '方法论', '架构', '最佳实践', '经验', '教训'
]
NOVEL_KW = [
    'first', 'new', 'launch', 'announce', 'breakthrough', 'novel',
    'open source', 'open-source', 'release', 'preview', 'beta',
    'now available', 'come to', 'general availability',
    '首次', '发布', '开源', '突破', '新品'
]

# ─── 工具函数 ────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description='AI 前沿情报简报生成器 v3.0')
    p.add_argument('--candidates', default=str(CANDIDATES_DEFAULT))
    p.add_argument('--output', default='-')
    p.add_argument('--date', default=None)
    p.add_argument('--mode', choices=['full', 'quick', 'arxiv', 'github'], default='full')
    p.add_argument('--config', default=str(CONFIG_FILE))
    return p.parse_args()


def auto_score(item):
    """对无 score 的候选自动评分（0-5）"""
    title = item.get('title', '').lower()
    summary = item.get('summary', '').lower()
    source = item.get('source', '').lower()
    text = f"{title} {summary}"

    # 1. 企业落地 (0-2.5分) — 核心维度，权重最高
    ent_hits = sum(1 for kw in ENTERPRISE_KW if kw.lower() in text)
    ent_score = min(2.5, ent_hits * 0.6)
    # 有真实企业名额外加分
    company_indicators = ['used', 'uses', 'deployed', 'built with', 'powered by', 'case study', 'how we']
    if any(kw in text for kw in company_indicators):
        ent_score += 0.5

    # 2. 数据支撑 (0-1.5分)
    data_hits = sum(1 for kw in DATA_KW if kw.lower() in text)
    data_score = min(1.5, data_hits * 0.4)

    # 3. 可学习性 (0-1分)
    learn_hits = sum(1 for kw in LEARN_KW if kw.lower() in text)
    learn_score = min(1.0, learn_hits * 0.4)

    # 4. 前沿性 (0-1分)
    novel_hits = sum(1 for kw in NOVEL_KW if kw.lower() in text)
    novel_score = min(1.0, novel_hits * 0.4)

    # 来源加权：OpenAI/AWS/Techmeme 权重更高
    source_bonus = 0
    if source in ['openai', 'aws-ml']:
        source_bonus = 1.0  # 官方博客，落地案例多
    elif source in ['techmeme']:
        source_bonus = 0.5  # 聚合新闻
    elif source in ['product-hunt', 'hn-show-hn']:
        source_bonus = 0.3

    raw = ent_score + data_score + learn_score + novel_score + source_bonus
    return round(min(5.0, raw), 1)


def load_candidates(path, auto_score_enabled=True):
    """加载 RSS 候选数据，自动评分"""
    # 尝试按日期查找最新候选文件
    p = Path(path)
    if not p.exists():
        # 尝试 candidates 目录下最新的日期文件
        candidates_dir = p.parent if p.parent.exists() else DATA_DIR / 'candidates'
        if candidates_dir.exists():
            json_files = sorted(candidates_dir.glob('*_candidates.json'), reverse=True)
            if json_files:
                p = json_files[0]
                print(f'📋 使用候选文件: {p.name}', file=sys.stderr)
    try:
        with open(p) as f:
            candidates = json.load(f)
    except FileNotFoundError:
        return []

    # 自动评分：对没有 score 的条目补充评分
    if auto_score_enabled:
        for c in candidates:
            if 'score' not in c or c['score'] is None:
                c['score'] = auto_score(c)

    return candidates


def run_script(script_path, *args, timeout=30):
    """运行 shell 脚本并返回 JSON"""
    try:
        result = subprocess.run(
            ['bash', str(script_path)] + list(args),
            capture_output=True, text=True, timeout=timeout
        )
        # 尝试直接解析整个 stdout 为 JSON
        stdout = result.stdout.strip()
        if stdout:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                pass
        # 如果整块不是 JSON，可能是 stderr 混入了，尝试找第一个 { 开始
        combined = result.stdout + result.stderr
        start = combined.find('{')
        if start >= 0:
            try:
                return json.loads(combined[start:])
            except json.JSONDecodeError:
                pass
        print(f"⚠️ 脚本输出无法解析为 JSON: {script_path}", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print(f"⚠️ 脚本超时 {script_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"⚠️ 脚本执行失败 {script_path}: {e}", file=sys.stderr)
        return None


def fetch_36kr_hotlist(target_date=None):
    """抓取36氪热榜 API"""
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')
    url = KR_API.format(date=target_date)
    try:
        result = subprocess.run(
            ['curl', '-sL', '--max-time', '10', url],
            capture_output=True, text=True, timeout=15
        )
        data = json.loads(result.stdout)
        return data.get('data', [])
    except Exception:
        return []


def fetch_arxiv(category="cs.AI", days=7, max_results=10):
    """抓取 arXiv 最新论文"""
    result = run_script(ARXIV_SCRIPT, '--category', category, '--days', str(days), '--max', str(max_results))
    if result and 'papers' in result:
        return result['papers']
    return []


def fetch_github_trending(period="daily"):
    """抓取 GitHub Trending"""
    result = run_script(GH_SCRIPT, '--period', period, timeout=60)
    if result and 'ai_repos' in result:
        return result['ai_repos'], result.get('other_notable', [])
    return [], []


def detect_signals(candidates, hotlist=None, arxiv_papers=None, gh_repos=None):
    """
    从所有候选数据中提取技术/产品/资本信号
    返回: {'tech': [], 'product': [], 'funding': []}
    每条信号包含 title + source + link
    """
    signals = {'tech': [], 'product': [], 'funding': []}

    funding_kw = ['series', 'funding', 'raised', 'invest', '投资', '融资', 'million', 'billion',
                  '估值', '融资轮', '收购', 'acquire', 'merger', '并购', 'IPO', '上市',
                  'seed', 'round', 'valuation', 'capital']
    product_kw = ['launch', 'release', 'announce', 'general availability', 'GA',
                  'preview', 'beta', 'open source', 'open-source',
                  '产品', '发布', '上线', '开源', '首发', '推出', '大模型', 'model']
    tech_kw = ['model', 'architecture', 'training', 'inference', 'benchmark',
               'framework', 'sota', 'state-of-the-art', 'breakthrough',
               'fine-tun', 'rag', 'agent', 'mcp', 'tool use', 'reasoning',
               'multimodal', 'diffusion', 'transformer', 'rlhf', 'dpo',
               'spec', 'protocol', 'standard',
               '技术', '架构', '推理', '微调', '多模态']

    # 汇总所有可搜索文本
    all_items = []
    for item in (candidates or []):
        all_items.append({
            'title': item.get('title', ''),
            'source': item.get('source', 'rss'),
            'link': item.get('link', item.get('source', '')),
        })
    for h in (hotlist or []):
        all_items.append({
            'title': h.get('title', ''),
            'source': '36kr',
            'link': h.get('url', ''),
        })
    for p in (arxiv_papers or []):
        all_items.append({
            'title': p.get('title', ''),
            'source': 'arxiv',
            'link': p.get('abs_url', ''),
        })
    for r in (gh_repos or []):
        all_items.append({
            'title': f"{r.get('name', '')} - {r.get('description', '')}",
            'source': 'github',
            'link': r.get('url', ''),
        })

    for item in all_items:
        t = item['title'].lower()
        if any(k.lower() in t for k in funding_kw):
            signals['funding'].append(item)
        if any(k.lower() in t for k in product_kw):
            signals['product'].append(item)
        if any(k.lower() in t for k in tech_kw):
            signals['tech'].append(item)

    # 去重（按 title 前40字符）
    for k in signals:
        seen = set()
        unique = []
        for s in signals[k]:
            key = s['title'][:40]
            if key not in seen:
                seen.add(key)
                unique.append(s)
        signals[k] = unique[:5]

    return signals


def format_link(url, title=None):
    t = title or url
    return f'[{t}]({url})'


def render_arxiv_only(papers):
    """仅渲染 arXiv 论文模块"""
    if not papers:
        return "📚 暂无 arXiv 新论文"

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "📚 arXiv 论文追踪 · AI/ML 最新",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    for i, p in enumerate(papers[:5], 1):
        lines.append(f"**{i}. {p.get('title', '?')}**")
        lines.append(f"👤 {p.get('authors', '?')} | 📅 {p.get('published', '?')}")
        lines.append(f"🏷 {' '.join(p.get('categories', []))}")
        abstract = p.get('abstract', '')[:200]
        if abstract:
            lines.append(f"📝 {abstract}...")
        lines.append(f"🔗 {p.get('abs_url', '')}")
        lines.append("")

    lines += ["━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
    return '\n'.join(lines)


def render_github_only(ai_repos, other_notable=None):
    """仅渲染 GitHub Trending 模块"""
    if not ai_repos:
        return "🔥 暂无 AI 相关 GitHub Trending 项目"

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🔥 GitHub Trending · AI 热榜",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    for i, r in enumerate(ai_repos[:8], 1):
        name = r.get('name', '?')
        lang = r.get('language', '?')
        today = r.get('today_stars', 0)
        total = r.get('total_stars', 0)
        desc = r.get('description', '')[:80]
        url = r.get('url', '')

        lines.append(f"**{i}. [{name}]({url})** ({lang}) +{today}⭐ today")
        if desc:
            lines.append(f"   {desc}")
        lines.append(f"   ⭐ {total:,} total")
        lines.append("")

    lines += ["━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
    return '\n'.join(lines)


def render_full(candidates, hotlist, arxiv_papers, gh_ai_repos, signals, date_str):
    """渲染完整简报 v3.0"""
    # 分层
    # 动态分层：基于实际分数分布调整阈值
    scores = sorted([c.get('score', 0) for c in candidates], reverse=True)
    max_score = scores[0] if scores else 0

    # 动态阈值：核心情报 = top 10% or ≥3.5, 值得关注 = top 30% or ≥2.5
    top_threshold = max(3.5, max_score * 0.8) if max_score >= 3 else max_score * 0.85
    mid_threshold = max(2.5, max_score * 0.5) if max_score >= 3 else max_score * 0.5

    top  = [c for c in candidates if c.get('score', 0) >= top_threshold][:3]
    mid  = [c for c in candidates if mid_threshold <= c.get('score', 0) < top_threshold][:5]
    fast = [c for c in candidates if 1.0 <= c.get('score', 0) < mid_threshold][:5]

    total_candidates = len(candidates)
    high_quality = len(top) + len(mid)

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🤖 AI 前沿情报 · {date_str}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "📡 数据源：11 RSS + 36氪热榜 + arXiv + GitHub Trending + Anthropic补漏",
        f"   候选：{total_candidates} 条 | 高质量：{high_quality} 条 | 评分阈值：核心≥{top_threshold:.1f} / 关注≥{mid_threshold:.1f}",
        "",
    ]

    # ── 核心情报 ──
    if top:
        lines += ["## 🔴 核心情报（{} 条）".format(len(top)), ""]
        for i, c in enumerate(top, 1):
            lines.append(f"### {i}. {c.get('title','?')}")
            meta = [c.get(k, '') for k in ['company', 'industry', 'scenario'] if c.get(k)]
            if meta:
                lines.append(' | '.join(meta))
            if c.get('key_data'):
                lines.append(f"📊 {c['key_data']}")
            link = c.get('link', c.get('source', ''))
            if link:
                lines.append(f"🔗 {format_link(link)}")
            # 自动生成启示：基于标题和来源
            if c.get('insight'):
                lines.append(f"💡 启示：{c['insight']}")
            else:
                # 简单的启示生成逻辑
                title_lower = c.get('title', '').lower()
                if 'agent' in title_lower:
                    lines.append("💡 启示：AI Agent 正在从原型走向生产环境，关注企业级部署模式")
                elif 'case' in title_lower or 'how' in title_lower:
                    lines.append("💡 启示：真实案例值得深入研究，可提取方法论")
                elif 'deploy' in title_lower or 'production' in title_lower:
                    lines.append("💡 启示：生产部署经验是最佳学习材料")
                else:
                    lines.append("💡 启示：关注行业落地趋势，寻找可复用模式")
            lines.append("")

    # ── 值得关注 ──
    if mid:
        lines += ["## 🟡 值得关注（{} 条）".format(len(mid)), ""]
        for i, c in enumerate(mid, 1):
            title = c.get('title', '?')
            link = c.get('link', c.get('source', ''))
            lines.append(f"{i}. **{title}**")
            if link and link.startswith('http'):
                lines.append(f"   🔗 {link}")
            else:
                lines.append(f"   🔗 [{c.get('source', '')}]")
        lines.append("")

    # ── 快速浏览（含36氪）──
    # 合并快速浏览：RSS 低分 + 36氪热榜
    combined_fast = []
    # 先加36氪（国内视角优先）
    if hotlist:
        for h in hotlist[:3]:
            combined_fast.append({
                'title': f"36氪 · {h.get('title','')[:50]}",
                'source': h.get('url', ''),
                'score': 2.5
            })
    # 再加 RSS 低分
    combined_fast.extend(fast)
    # 总数上限 8 条
    combined_fast = combined_fast[:8]

    if combined_fast:
        lines += ["## 🟢 快速浏览（{} 条）".format(len(combined_fast)), ""]
        for c in combined_fast:
            title = c.get('title', '?')[:60]
            link = c.get('link', c.get('source', ''))
            if link and link.startswith('http'):
                lines.append(f"• [{title}]({link})")
            else:
                lines.append(f"• {title}")
        lines.append("")

    # ── arXiv 论文追踪 ──
    if arxiv_papers:
        lines += ["## 📚 技术前沿 · 论文追踪（{} 篇）".format(len(arxiv_papers[:3])), ""]
        for i, p in enumerate(arxiv_papers[:3], 1):
            lines.append(f"**{i}. {p.get('title','?')}**")
            lines.append(f"arXiv | {p.get('authors','?')} | {p.get('published','?')}")
            abstract = p.get('abstract', '')[:150]
            if abstract:
                lines.append(f"摘要：{abstract}...")
            lines.append(f"🔗 {p.get('abs_url','')}")
            lines.append("")

    # ── GitHub Trending ──
    if gh_ai_repos:
        lines += ["## 🔥 GitHub Trending · AI 热榜（{} 个）".format(len(gh_ai_repos[:3])), ""]
        for i, r in enumerate(gh_ai_repos[:3], 1):
            name = r.get('name', '?')
            lang = r.get('language', '?')
            today = r.get('today_stars', 0)
            total = r.get('total_stars', 0)
            desc = r.get('description', '')[:60]
            url = r.get('url', '')
            lines.append(f"**{i}. [{name}]({url})** ({lang}) +{today}⭐ today")
            if desc:
                lines.append(f"   {desc}")
            lines.append(f"   ⭐ {total:,} total")
            lines.append("")

    # ── 今日信号 ──
    lines += [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "", "📊 今日信号", ""
    ]

    tech = signals.get('tech', [])
    prod = signals.get('product', [])
    fund = signals.get('funding', [])

    lines.append(f"🛠 技术趋势：{tech[0]['title'] if tech else '暂无显著信号'}")
    for t in tech[1:3]:
        lines.append(f"   - {t['title']}")

    lines.append(f"🏢 产品发布：{prod[0]['title'] if prod else '暂无显著信号'}")
    for p in prod[1:3]:
        lines.append(f"   - {p['title']}")

    lines.append(f"💰 资本动向：{fund[0]['title'] if fund else '暂无显著信号'}")
    for f in fund[1:3]:
        lines.append(f"   - {f['title']}")

    lines += [
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ 生成时间：{datetime.now().strftime('%H:%M')} | ai-frontier-monitor v3.0"
    ]

    return '\n'.join(lines)


def render_quick(candidates, hotlist, arxiv_papers, gh_ai_repos, signals):
    """快速信号检测模式"""
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🔍 AI 信号快检 · {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    fund = signals.get('funding', [])
    prod = signals.get('product', [])
    tech = signals.get('tech', [])

    if fund:
        lines += ["💰 资本信号", ""]
        for f in fund[:5]:
            lines.append(f"• {f['title']}")
        lines.append("")

    if prod:
        lines += ["🏢 产品发布", ""]
        for p in prod[:5]:
            lines.append(f"• {p['title']}")
        lines.append("")

    if tech:
        lines += ["🛠 技术趋势", ""]
        for t in tech[:5]:
            lines.append(f"• {t['title']}")
        lines.append("")

    # 补充：arXiv + GitHub 摘要
    if arxiv_papers:
        lines += ["📚 arXiv 新论文：{} 篇".format(len(arxiv_papers)), ""]
        for p in arxiv_papers[:2]:
            lines.append(f"• {p.get('title', '?')[:60]}")
        lines.append("")

    if gh_ai_repos:
        lines += ["🔥 GitHub AI 项目：{} 个".format(len(gh_ai_repos)), ""]
        for r in gh_ai_repos[:2]:
            lines.append(f"• {r.get('name', '?')} +{r.get('today_stars', 0)}⭐")
        lines.append("")

    if not (fund or prod or tech or arxiv_papers or gh_ai_repos):
        lines.append("⚠️ 暂无显著信号，候选数据不足")

    lines += ["", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
    return '\n'.join(lines)


def main():
    args = parse_args()
    target_date = args.date or datetime.now().strftime('%Y-%m-%d')

    # ── 仅 arXiv 模式 ──
    if args.mode == 'arxiv':
        papers = fetch_arxiv(category="cs.AI", days=7, max_results=10)
        # 也获取 cs.LG 和 cs.CL
        papers_lg = fetch_arxiv(category="cs.LG", days=7, max_results=5)
        papers_cl = fetch_arxiv(category="cs.CL", days=7, max_results=5)
        # 合并去重
        seen = set()
        all_papers = []
        for p in (papers + papers_lg + papers_cl):
            aid = p.get('arxiv_id', '')
            if aid not in seen:
                seen.add(aid)
                all_papers.append(p)
        report = render_arxiv_only(all_papers)

    # ── 仅 GitHub 模式 ──
    elif args.mode == 'github':
        ai_repos, other = fetch_github_trending(period="daily")
        report = render_github_only(ai_repos, other)

    # ── 快速信号模式 ──
    elif args.mode == 'quick':
        candidates = load_candidates(args.candidates)
        hotlist = fetch_36kr_hotlist(target_date)
        arxiv_papers = fetch_arxiv(category="cs.AI", days=7, max_results=5)
        gh_ai_repos, _ = fetch_github_trending(period="daily")
        signals = detect_signals(candidates, hotlist, arxiv_papers, gh_ai_repos)
        report = render_quick(candidates, hotlist, arxiv_papers, gh_ai_repos, signals)

    # ── 全量模式 ──
    else:
        candidates = load_candidates(args.candidates)
        hotlist = fetch_36kr_hotlist(target_date)
        arxiv_papers = fetch_arxiv(category="cs.AI", days=7, max_results=10)
        # 补充 cs.LG
        papers_lg = fetch_arxiv(category="cs.LG", days=7, max_results=5)
        seen = set(p.get('arxiv_id', '') for p in arxiv_papers)
        for p in papers_lg:
            if p.get('arxiv_id', '') not in seen:
                arxiv_papers.append(p)
                seen.add(p.get('arxiv_id', ''))

        gh_ai_repos, _ = fetch_github_trending(period="daily")
        signals = detect_signals(candidates, hotlist, arxiv_papers, gh_ai_repos)

        weekday = datetime.now().strftime('%A %Y-%m-%d')
        report = render_full(candidates, hotlist, arxiv_papers, gh_ai_repos, signals, weekday)

    # 输出
    if args.output == '-':
        print(report)
    else:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w') as f:
            f.write(report)
        print(f'✅ 简报已写入 {args.output}', file=sys.stderr)


if __name__ == '__main__':
    main()