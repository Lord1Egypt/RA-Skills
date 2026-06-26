"""Typed models for Founder Signal."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class VerifiedEvidenceSnapshot:
    """Verified source text supplied from outside the runtime.

    ``reddit_url`` remains accepted for backward-compatible profile files, but new
    code should prefer ``platform`` and ``source_url``.
    """

    source_url: str
    text_snapshot: str
    platform: str = "reddit"
    verification_method: str = "agent_browser"
    verified_by: str = ""

    @property
    def reddit_url(self) -> str:
        return self.source_url

    @classmethod
    def from_dict(cls, payload: dict) -> "VerifiedEvidenceSnapshot":
        platform = str(payload.get("platform") or "reddit").strip().lower() or "reddit"
        source_url = str(payload.get("source_url") or payload.get("reddit_url") or "").strip()
        return cls(
            platform=platform,
            source_url=source_url,
            text_snapshot=str(payload["text_snapshot"]).strip(),
            verification_method=str(payload.get("verification_method", "agent_browser")).strip(),
            verified_by=str(payload.get("verified_by", "")).strip(),
        )


@dataclass(frozen=True)
class PlatformSourceConfig:
    """Platform-specific discovery/evidence configuration."""

    platform: str
    enabled: bool = True
    communities: list[str] = field(default_factory=list)
    discovery_providers: list[str] = field(default_factory=list)
    seed_urls: list[str] = field(default_factory=list)
    excluded_urls: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, platform: str, payload: dict[str, Any]) -> "PlatformSourceConfig":
        return cls(
            platform=platform.strip().lower(),
            enabled=bool(payload.get("enabled", True)),
            communities=[str(item) for item in payload.get("communities", [])],
            discovery_providers=[str(item) for item in payload.get("discovery_providers", [])],
            seed_urls=[str(item) for item in payload.get("seed_urls", [])],
            excluded_urls=[str(item) for item in payload.get("excluded_urls", [])],
        )


@dataclass(frozen=True)
class FounderSignalConfig:
    profile_id: str
    enabled: bool
    product_name: str
    product_one_liner: str
    target_audience: str
    keywords: list[str]
    subreddits: list[str] = field(default_factory=list)
    seed_reddit_urls: list[str] = field(default_factory=list)
    max_candidates: int = 0
    max_action_cards: int = 0
    discovery_mode: str = "live"
    max_post_age_days: int = 7
    preferred_post_age_hours: int = 72
    min_comment_count: int = 0
    max_comment_count: int = 250
    history_ttl_days: int = 45
    discovery_terms: list[str] = field(default_factory=list)
    live_discovery_terms: list[str] = field(default_factory=list)
    research_terms: list[str] = field(default_factory=list)
    scoring_terms: list[str] = field(default_factory=list)
    negative_scoring_terms: list[str] = field(default_factory=list)
    excluded_reddit_urls: list[str] = field(default_factory=list)
    platforms: dict[str, PlatformSourceConfig] = field(default_factory=dict)
    verified_evidence_snapshots: list[VerifiedEvidenceSnapshot] = field(default_factory=list)

    def __post_init__(self) -> None:
        platforms = dict(self.platforms)
        reddit = platforms.get("reddit")
        if reddit is None and (self.subreddits or self.seed_reddit_urls or self.excluded_reddit_urls):
            platforms["reddit"] = PlatformSourceConfig(
                platform="reddit",
                communities=list(self.subreddits),
                seed_urls=list(self.seed_reddit_urls),
                excluded_urls=list(self.excluded_reddit_urls),
            )
        elif reddit is not None:
            object.__setattr__(self, "subreddits", list(reddit.communities))
            object.__setattr__(self, "seed_reddit_urls", list(reddit.seed_urls))
            object.__setattr__(self, "excluded_reddit_urls", list(reddit.excluded_urls))
        object.__setattr__(self, "platforms", platforms)

    @classmethod
    def from_dict(cls, payload: dict) -> "FounderSignalConfig":
        platforms = _parse_platforms(payload)
        discovery_terms = [str(item) for item in payload.get("discovery_terms", [])]
        scoring_terms = [str(item) for item in payload.get("scoring_terms", [])]
        live_discovery_terms = [
            str(item) for item in payload.get("live_discovery_terms", discovery_terms)
        ]
        research_terms = [
            str(item)
            for item in payload.get(
                "research_terms",
                discovery_terms or scoring_terms,
            )
        ]
        default_mode = "research" if "discovery_mode" not in payload else "live"
        return cls(
            profile_id=str(payload["profile_id"]).strip(),
            enabled=bool(payload.get("enabled", True)),
            product_name=str(payload["product_name"]),
            product_one_liner=str(payload["product_one_liner"]),
            target_audience=str(payload["target_audience"]),
            keywords=[str(item) for item in payload["keywords"]],
            subreddits=platforms.get("reddit", PlatformSourceConfig("reddit")).communities,
            seed_reddit_urls=platforms.get("reddit", PlatformSourceConfig("reddit")).seed_urls,
            max_candidates=int(payload["max_candidates"]),
            max_action_cards=int(payload["max_action_cards"]),
            discovery_mode=str(payload.get("discovery_mode", default_mode)).strip().lower(),
            max_post_age_days=int(payload.get("max_post_age_days", 7)),
            preferred_post_age_hours=int(payload.get("preferred_post_age_hours", 72)),
            min_comment_count=int(payload.get("min_comment_count", 0)),
            max_comment_count=int(payload.get("max_comment_count", 250)),
            history_ttl_days=int(payload.get("history_ttl_days", 45)),
            discovery_terms=discovery_terms,
            live_discovery_terms=live_discovery_terms,
            research_terms=research_terms,
            scoring_terms=scoring_terms,
            negative_scoring_terms=[
                str(item) for item in payload.get("negative_scoring_terms", [])
            ],
            excluded_reddit_urls=platforms.get("reddit", PlatformSourceConfig("reddit")).excluded_urls,
            platforms=platforms,
            verified_evidence_snapshots=[
                VerifiedEvidenceSnapshot.from_dict(item)
                for item in payload.get("verified_evidence_snapshots", [])
            ],
        )


def _parse_platforms(payload: dict[str, Any]) -> dict[str, PlatformSourceConfig]:
    parsed: dict[str, PlatformSourceConfig] = {}
    raw_platforms = payload.get("platforms")
    if isinstance(raw_platforms, dict):
        for name, config_payload in raw_platforms.items():
            if isinstance(config_payload, dict):
                parsed[str(name).strip().lower()] = PlatformSourceConfig.from_dict(
                    str(name), config_payload
                )

    legacy_reddit_present = any(
        key in payload for key in ("subreddits", "seed_reddit_urls", "excluded_reddit_urls")
    )
    if legacy_reddit_present or not parsed:
        existing = parsed.get("reddit", PlatformSourceConfig("reddit"))
        parsed["reddit"] = PlatformSourceConfig(
            platform="reddit",
            enabled=existing.enabled,
            communities=(
                [str(item) for item in payload.get("subreddits", [])]
                if "subreddits" in payload
                else existing.communities
            ),
            discovery_providers=existing.discovery_providers,
            seed_urls=(
                [str(item) for item in payload.get("seed_reddit_urls", [])]
                if "seed_reddit_urls" in payload
                else existing.seed_urls
            ),
            excluded_urls=(
                [str(item) for item in payload.get("excluded_reddit_urls", [])]
                if "excluded_reddit_urls" in payload
                else existing.excluded_urls
            ),
        )
    return {name: config for name, config in parsed.items() if config.enabled}


@dataclass(frozen=True)
class StructuredRedditEvidence:
    post_title: str
    post_body: str
    subreddit: str
    comments_excerpt: str
    extraction_quality: str
    raw_text_snapshot: str
    post_age_days: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceReadResult:
    candidate_id: str
    source_url: str
    evidence_url: str
    status: str
    raw_html_path: Path
    text_snapshot_path: Path
    source_url_path: Path
    evidence_url_path: Path
    platform: str = "reddit"
    structured_evidence_path: Path | None = None
    structured_evidence: StructuredRedditEvidence | None = None


RedditEvidenceReadResult = EvidenceReadResult
