#!/usr/bin/env python3
"""
简报质量评分函数
维度：Coverage / Freshness / Relevance / Diversity / Signal
"""

from datetime import datetime, timedelta
from typing import NamedTuple


class QualityScore(NamedTuple):
    total: float
    coverage: float   # GitHub/HN 覆盖完整性
    freshness: float  # 内容时效性
    relevance: float  # AI 相关性过滤准确率
    diversity: float  # 类型多样性
    signal: float     # 信号强度（star/points）


def calc_freshness_score(repos: list, hn_hits: list, days: int = 7) -> float:
    """Freshness: 内容有多新鲜。越新的项目/讨论分数越高。"""
    if not repos and not hn_hits:
        return 0.0
    
    now = datetime.utcnow()
    total_score = 0.0
    count = 0

    for repo in repos:
        created = repo.get("created_at", "")[:10]
        try:
            d = datetime.strptime(created, "%Y-%m-%d")
            age_days = (now - d).days
            score = max(0, 1.0 - (age_days / (days * 2)))
            total_score += score
            count += 1
        except Exception:
            pass

    for hit in hn_hits:
        created = hit.get("created_at", "")[:10]
        try:
            d = datetime.strptime(created, "%Y-%m-%d")
            age_days = (now - d).days
            score = max(0, 1.0 - (age_days / (days * 2)))
            total_score += score
            count += 1
        except Exception:
            pass

    return total_score / count if count > 0 else 0.5


def calc_relevance_score(hn_hits: list, ai_keywords: list) -> float:
    """Relevance: AI 相关性过滤准确率。越高说明噪音越少。"""
    if not hn_hits:
        return 1.0
    
    ai_count = sum(1 for h in hn_hits if any(
        kw.lower() in h.get("title", "").lower() for kw in ai_keywords
    ))
    return ai_count / len(hn_hits)


def calc_diversity_score(repos: list) -> float:
    """Diversity: 语言/主题多样性。repo 分布越均匀越高。"""
    if not repos:
        return 0.0
    
    langs = [r.get("language") for r in repos if r.get("language")]
    if not langs:
        return 0.5
    
    # 计算语言分布的香农熵（归一化）
    import math
    from collections import Counter
    freq = Counter(langs)
    total = len(langs)
    # 正确的香农熵: -Σ(p * log2(p))
    entropy = -sum((c / total) * math.log2(c / total) for c in freq.values())
    # 最大熵 = log2(k)，归一化到 [0, 1]
    k = len(freq)
    max_entropy = math.log2(k) if k > 1 else 1.0
    return min(1.0, entropy / max_entropy)


def calc_signal_score(repos: list, hn_hits: list) -> float:
    """Signal: 平均信号强度。star/points 越高分数越高。"""
    if not repos and not hn_hits:
        return 0.0
    
    total_score = 0.0
    count = 0

    for repo in repos:
        stars = repo.get("stargazers_count", 0) or 0
        score = min(1.0, stars / 5000)  # 5000 stars = 满分
        total_score += score
        count += 1

    for hit in hn_hits:
        pts = hit.get("points", 0) or 0
        score = min(1.0, pts / 200)  # 200 points = 满分
        total_score += score
        count += 1

    return total_score / count if count > 0 else 0.0


def score_briefing(gh_repos: list, hn_hits: list, ai_keywords: list) -> QualityScore:
    """
    评估简报整体质量（0~100）
    """
    coverage   = min(1.0, (len(gh_repos) / 10) * 0.4 + (len(hn_hits) / 20) * 0.4 + 0.2)
    freshness  = calc_freshness_score(gh_repos, hn_hits)
    relevance  = calc_relevance_score(hn_hits, ai_keywords)
    diversity  = calc_diversity_score(gh_repos)
    signal     = calc_signal_score(gh_repos, hn_hits)

    # 加权总分
    total = (
        coverage  * 0.20 +
        freshness * 0.30 +
        relevance * 0.20 +
        diversity * 0.10 +
        signal    * 0.20
    ) * 100

    return QualityScore(
        total     = round(total, 1),
        coverage  = round(coverage * 100, 1),
        freshness = round(freshness * 100, 1),
        relevance = round(relevance * 100, 1),
        diversity = round(diversity * 100, 1),
        signal    = round(signal * 100, 1),
    )


if __name__ == "__main__":
    import json, sys
    sys.path.insert(0, '.')

    # 读取上一份简报的数据来测试
    from ai_daily_briefing import fetch_github_trending, fetch_hn_ai, HN_KEYWORDS
    
    print("抓取数据中...")
    repos = fetch_github_trending(days=7, per_page=15)
    hits  = fetch_hn_ai()
    
    score = score_briefing(repos, hits, HN_KEYWORDS)
    print(f"\n📊 简报质量评分: {score.total}/100")
    print(f"  覆盖完整度: {score.coverage}/100")
    print(f"  时效性:     {score.freshness}/100")
    print(f"  AI相关性:   {score.relevance}/100")
    print(f"  多样性:     {score.diversity}/100")
    print(f"  信号强度:   {score.signal}/100")
