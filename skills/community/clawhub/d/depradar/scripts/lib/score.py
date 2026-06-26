"""Scoring engine for /depradar.

PackageUpdate score = severity × recency × impact × community (weighted).
Community signal scores use log1p-based engagement formulas.
"""

from __future__ import annotations

import math
import re
from typing import List, Optional

from schema import (
    DepRadarReport, GithubIssueItem, HackerNewsItem, PackageUpdate,
    RedditItem, StackOverflowItem, SubScores, TwitterItem,
)
from dates import recency_score, days_since


# ── Severity weights by change type ─────────────────────────────────────────

SEVERITY_MAP = {
    "removed":           100,
    "renamed":            80,
    "signature_changed":  70,
    "behavior_changed":   60,
    "type_changed":       50,
    "deprecated":         40,
    "other":              30,
}

IMPACT_CONFIDENCE_BONUS = {
    "high":        100,
    "med":          70,
    "low":          40,
    "not_scanned":  50,   # neutral — we don't know
}

# ── PackageUpdate scoring ─────────────────────────────────────────────────────

def score_package_update(pkg: PackageUpdate) -> PackageUpdate:
    """Compute and assign pkg.score and pkg.subs."""
    if not pkg.has_breaking_changes:
        pkg.score = _minor_update_score(pkg)
        return pkg

    severity  = _pkg_severity_score(pkg)
    recency   = recency_score(pkg.release_date)
    impact    = IMPACT_CONFIDENCE_BONUS.get(pkg.impact_confidence, 50)
    community = 50   # will be enriched after community signals are fetched

    raw = (0.35 * severity + 0.25 * recency + 0.30 * impact + 0.10 * community)

    # Staleness bonus: counteracts recency decay for old-but-unfixed breaks
    stale = staleness_bonus(pkg.release_date)
    raw = min(100.0, raw + stale)

    pkg.subs  = SubScores(severity=severity, recency=recency, impact=impact, community=community)
    pkg.score = min(100, int(round(raw)))
    return pkg


def staleness_bonus(release_date: Optional[str]) -> float:
    """Return an additive score bonus (0–18) for old-but-unfixed breaking changes.

    Partially counteracts recency decay for packages that have been breaking
    for a long time without being upgraded.  Recent packages still score higher
    overall — this bonus narrows the gap to keep old technical debt visible.

    Example: a 7-day-old break gets recency=100 (score ~75); a 365-day-old
    break gets recency=10 + staleness=18 (score ~47) — both stay prominent.

    Capped at 18 so the fundamental recency ordering is preserved.
    """
    if not release_date:
        return 0.0
    try:
        days = days_since(release_date)
    except Exception:
        return 0.0
    if days is None:
        return 0.0
    if days < 30:
        return 0.0    # too new — normal recency applies
    elif days < 90:
        return 3.0    # 1-3 months: slight nudge
    elif days < 180:
        return 8.0    # 3-6 months: moderate urgency
    elif days < 365:
        return 12.0   # 6-12 months: high urgency — technical debt
    else:
        return 18.0   # 1+ year unfixed: critical debt


def enrich_package_community_scores(
    packages: List[PackageUpdate],
    report: "DepRadarReport",
) -> None:
    """Update pkg.subs.community and pkg.score after community signals are available."""
    for pkg in packages:
        if not pkg.has_breaking_changes or pkg.subs is None:
            continue
        pain = _community_pain_count(pkg.package, report, pkg.latest_version)
        community = min(100, int(math.log1p(pain) * 14))
        pkg.subs.community = community
        raw = (
            0.35 * pkg.subs.severity +
            0.25 * pkg.subs.recency  +
            0.30 * pkg.subs.impact   +
            0.10 * community
        )
        stale = staleness_bonus(pkg.release_date)
        pkg.score = min(100, int(round(raw + stale)))


def _pkg_severity_score(pkg: PackageUpdate) -> int:
    """Average severity across all breaking changes; penalise if semver is unknown."""
    if not pkg.breaking_changes:
        return 30 if pkg.semver_type == "major" else 15
    scores = [SEVERITY_MAP.get(bc.change_type, 30) for bc in pkg.breaking_changes]
    avg = sum(scores) / len(scores)
    # Confidence modifiers
    avg_confidence = sum(
        {"high": 1.0, "med": 0.8, "low": 0.6}.get(bc.confidence, 0.7)
        for bc in pkg.breaking_changes
    ) / len(pkg.breaking_changes)
    return min(100, int(round(avg * avg_confidence)))


def _minor_update_score(pkg: PackageUpdate) -> int:
    recency = recency_score(pkg.release_date)
    bump    = {"minor": 30, "patch": 15, "none": 5}.get(pkg.semver_type, 10)
    return min(100, int(round(0.40 * bump + 0.60 * recency * 0.30)))


# Words that strongly indicate a signal is off-topic (content/platform noise)
_UNRELATED_TITLE_WORDS: frozenset = frozenset({
    "checklist", "tutorial", "introduction", "overview", "summary",
    "interview", "jobs", "hiring", "newsletter", "weekly", "monthly",
    "roundup", "digest", "awesome", "curated", "collection",
    "flutter", "android", "ios", "swift", "kotlin",
    "podcast", "youtube", "video", "course", "workshop",
})

# Words that indicate a signal is technically relevant
_TECHNICAL_TITLE_WORDS: frozenset = frozenset({
    "breaking", "error", "crash", "migration", "upgrade",
    "deprecated", "removed", "api", "import", "require",
    "version", "release", "changelog", "update",
})


def _title_is_probably_relevant(title: str, package: str) -> bool:
    """Return True if a version-free signal title is likely relevant to the package.

    Used as a secondary filter when a signal mentions no version number.
    Accepts if:
    - Package base name is directly in the title (clear reference), OR
    - Title has a technical relevance word AND no known-unrelated platform words.
    Rejects "Flutter Pre-Launch Checklist" for commander.js, etc.
    """
    title_lower = title.lower()
    # Strip scope prefix and sub-path for comparison: @angular/core → core
    pkg_base = package.lower().lstrip("@").split("/")[-1].split(".")[0]

    if pkg_base and pkg_base in title_lower:
        return True

    has_technical = any(w in title_lower for w in _TECHNICAL_TITLE_WORDS)
    has_unrelated = any(w in title_lower for w in _UNRELATED_TITLE_WORDS)
    return has_technical and not has_unrelated


def _community_pain_count(
    package: str,
    report: "DepRadarReport",
    version_range: Optional[str] = None,
) -> float:
    """Count weighted community signals for a package, filtered to version range.

    Uses quality_weight (closed+answered = 2.0, open+no comments = 0.8, default 1.0)
    to weigh signals. Version-filters to avoid old signals for different major versions.
    For signals with no version mentioned, applies title relevance filter to reject
    off-topic noise (e.g. "Flutter Pre-Launch Checklist" for commander.js).
    Returns a weighted float count used as input to log1p formula.
    """
    major = None
    if version_range:
        m = re.match(r"v?(\d+)", version_range)
        if m:
            major = int(m.group(1))

    def _version_relevant(text: str) -> bool:
        """Return True if the text mentions the relevant major version (or passes relevance filter)."""
        if major is None:
            return True
        # Match "v8.0", "8.0.0" AND bare "v8" (major-only version references)
        versions_mentioned = [
            g1 or g2
            for g1, g2 in re.findall(r"v?(\d+)\.\d+|(?<!\d)v(\d+)\b", text or "")
        ]
        if not versions_mentioned:
            # No version mentioned — apply secondary relevance filter instead of blindly accepting
            return _title_is_probably_relevant(text, package)
        return any(int(v) == major for v in versions_mentioned)

    count: float = 0.0

    for x in report.github_issues:
        if x.package == package:
            combined = f"{x.title} {x.body_snippet or ''}"
            if _version_relevant(combined):
                count += getattr(x, "quality_weight", 1.0)

    for x in report.stackoverflow:
        if x.package == package:
            combined = x.question_title
            if _version_relevant(combined):
                count += getattr(x, "quality_weight", 1.0)

    for x in report.reddit:
        if x.package == package:
            if _version_relevant(x.title):
                count += 1.0

    for x in report.hackernews:
        if x.package == package:
            if _version_relevant(x.title):
                count += 1.0

    # Twitter/X signals come from the xAI Grok LLM (not live search).
    # Engagement metrics (likes, reposts, replies) are recalled from training
    # data and may be approximate or fabricated. We display the signals for
    # context but exclude them from the community pain count to avoid inflating
    # package scores with potentially unreliable data.

    return count


# ── Community signal scoring ──────────────────────────────────────────────────

def score_github_issue(item: GithubIssueItem) -> GithubIssueItem:
    """
    severity : "breaking-change" label → 80, "bug" → 50, else 40
    recency  : recency_score(created_at)
    impact   : min(100, comments * 3)   — comment count as pain proxy
    community: 50 flat
    score    = 0.30*sev + 0.30*rec + 0.25*imp + 0.15*community

    quality_weight: 2.0 if closed+accepted, 1.5 if closed, 0.8 if open+no comments, else 1.0
    """
    label_names = [l.lower() for l in item.labels]
    if any("breaking" in l for l in label_names):
        severity = 80
    elif "bug" in label_names:
        severity = 50
    else:
        severity = 40

    recency  = recency_score(item.created_at)
    impact   = min(100, item.comments * 3)
    community = 50

    # Quality weight: closed+answered signals are more valuable
    if item.state == "closed":
        item.quality_weight = 2.0 if item.has_accepted_answer else 1.5
    elif item.comments == 0:
        item.quality_weight = 0.8  # unanswered open issue — may be noise
    elif item.comments > 10:
        item.quality_weight = 1.2  # actively discussed
    else:
        item.quality_weight = 1.0

    raw = 0.30 * severity + 0.30 * recency + 0.25 * impact + 0.15 * community
    item.subs  = SubScores(severity=severity, recency=recency, impact=impact, community=community)
    item.score = min(100, int(round(raw)))
    return item


def score_stackoverflow_item(item: StackOverflowItem) -> StackOverflowItem:
    """
    0.40*log1p(so_score)*12 + 0.30*log1p(answer_count)*20
    + 0.20*log1p(view_count/100)*15 + 0.10*recency

    quality_weight: 2.0 if answered+accepted, 0.8 if unanswered, else 1.0
    """
    vote_component   = min(100, math.log1p(max(0, item.so_score)) * 12)
    answer_component = min(100, math.log1p(item.answer_count) * 20)
    view_component   = min(100, math.log1p(item.view_count / 100 + 1) * 15)
    recency          = recency_score(item.created_at)

    # Quality weight: answered questions are more valuable
    if item.is_answered and item.accepted_answer_snippet:
        item.quality_weight = 2.0   # accepted answer — proof of solution
    elif item.is_answered:
        item.quality_weight = 1.5   # answered but no accepted
    elif item.answer_count == 0:
        item.quality_weight = 0.8   # unanswered — uncertain value
    else:
        item.quality_weight = 1.0

    raw = (0.40 * vote_component + 0.30 * answer_component +
           0.20 * view_component + 0.10 * recency)
    item.subs  = SubScores(
        severity  = int(vote_component),
        recency   = int(recency),
        impact    = int(answer_component),
        community = int(view_component),
    )
    item.score = min(100, int(round(raw)))
    return item


def score_reddit_item(item: RedditItem) -> RedditItem:
    """0.50*log1p(reddit_score)*8 + 0.35*log1p(num_comments)*10 + 0.15*recency"""
    vote_c    = min(100, math.log1p(max(0, item.reddit_score)) * 8)
    comment_c = min(100, math.log1p(item.num_comments) * 10)
    recency   = recency_score(item.date)

    raw = 0.50 * vote_c + 0.35 * comment_c + 0.15 * recency
    item.subs  = SubScores(severity=0, recency=int(recency),
                           impact=int(comment_c), community=int(vote_c))
    item.score = min(100, int(round(raw)))
    return item


def score_hackernews_item(item: HackerNewsItem) -> HackerNewsItem:
    """0.55*log1p(points)*10 + 0.45*log1p(num_comments)*12"""
    points_c  = min(100, math.log1p(item.points) * 10)
    comment_c = min(100, math.log1p(item.num_comments) * 12)
    recency   = recency_score(item.date)

    raw = 0.55 * points_c + 0.45 * comment_c
    # small recency blend
    raw = 0.80 * raw + 0.20 * recency
    item.subs  = SubScores(severity=0, recency=int(recency),
                           impact=int(comment_c), community=int(points_c))
    item.score = min(100, int(round(raw)))
    return item


def score_twitter_item(item: TwitterItem) -> TwitterItem:
    """0.55*log1p(likes)*8 + 0.25*log1p(reposts)*10 + 0.20*log1p(replies)*8"""
    like_c    = min(100, math.log1p(item.likes) * 8)
    repost_c  = min(100, math.log1p(item.reposts) * 10)
    reply_c   = min(100, math.log1p(item.replies) * 8)
    recency   = recency_score(item.date)

    raw = 0.55 * like_c + 0.25 * repost_c + 0.20 * reply_c
    raw = 0.80 * raw + 0.20 * recency
    item.subs  = SubScores(severity=0, recency=int(recency),
                           impact=int(reply_c), community=int(like_c + repost_c))
    item.score = min(100, int(round(raw)))
    return item


# ── Convenience: score everything in a report ─────────────────────────────────

def score_all(report: "DepRadarReport") -> "DepRadarReport":
    """Apply all scoring functions to all items in the report."""
    for pkg in report.packages_with_breaking_changes:
        score_package_update(pkg)
    for pkg in report.packages_with_minor_updates:
        score_package_update(pkg)
    for item in report.github_issues:
        score_github_issue(item)
    for item in report.stackoverflow:
        score_stackoverflow_item(item)
    for item in report.reddit:
        score_reddit_item(item)
    for item in report.hackernews:
        score_hackernews_item(item)
    for item in report.twitter:
        score_twitter_item(item)
    # Enrich community scores after all signals are scored
    enrich_package_community_scores(report.packages_with_breaking_changes, report)
    # Sort descending by score
    report.packages_with_breaking_changes.sort(key=lambda x: x.score, reverse=True)
    report.packages_with_minor_updates.sort(key=lambda x: x.score, reverse=True)
    return report
