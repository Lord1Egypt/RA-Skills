"""Configuration loading for Founder Signal."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .models import FounderSignalConfig
from .platforms.v2ex import (
    canonicalize_v2ex_topic_url,
    is_placeholder_v2ex_url,
    validate_config_urls as validate_v2ex_config_urls,
)
from .reddit_fetcher import is_placeholder_reddit_url, to_eddrit_url

_PROFILE_ID_PATTERN = re.compile(r"^[a-z0-9_-]+$")


def load_profiles(
    root_dir: Path,
    *,
    selected_profile_id: str | None = None,
    include_disabled: bool = False,
) -> list[tuple[FounderSignalConfig, Path]]:
    profiles_dir = root_dir / "profiles"
    if not profiles_dir.exists():
        raise FileNotFoundError(f"Profiles directory not found: {profiles_dir}")

    profile_paths = sorted(
        path
        for path in profiles_dir.glob("*.json")
        if path.is_file() and not path.name.endswith(".example.json")
    )
    if not profile_paths:
        raise FileNotFoundError(f"No profile files found in {profiles_dir}")

    profiles: list[tuple[FounderSignalConfig, Path]] = []
    seen_ids: set[str] = set()
    for profile_path in profile_paths:
        payload = json.loads(profile_path.read_text(encoding="utf-8"))
        config = FounderSignalConfig.from_dict(payload)
        _validate_profile(config=config, profile_path=profile_path)
        if config.profile_id in seen_ids:
            raise ValueError(f"Duplicate profile_id '{config.profile_id}' found in {profile_path}")
        seen_ids.add(config.profile_id)
        profiles.append((config, profile_path))

    if selected_profile_id:
        matching = [
            item for item in profiles if item[0].profile_id == selected_profile_id
        ]
        if not matching:
            raise ValueError(f"Profile '{selected_profile_id}' was not found in {profiles_dir}")
        return matching

    if include_disabled:
        return profiles

    enabled_profiles = [item for item in profiles if item[0].enabled]
    if not enabled_profiles:
        raise ValueError(f"No enabled profiles found in {profiles_dir}")
    return enabled_profiles


def _validate_profile(*, config: FounderSignalConfig, profile_path: Path) -> None:
    if not config.profile_id:
        raise ValueError(f"profile_id is required in {profile_path}")
    if not _PROFILE_ID_PATTERN.match(config.profile_id):
        raise ValueError(
            f"profile_id '{config.profile_id}' in {profile_path} must use lowercase letters, digits, '-' or '_'."
        )
    if config.max_action_cards != 1:
        raise ValueError(
            f"max_action_cards for profile '{config.profile_id}' must be 1 in this phase."
        )
    if config.discovery_mode not in {"live", "research"}:
        raise ValueError(
            f"discovery_mode for profile '{config.profile_id}' must be 'live' or 'research'."
        )
    if config.max_post_age_days < 0:
        raise ValueError(
            f"max_post_age_days for profile '{config.profile_id}' must be 0 or greater."
        )
    if config.preferred_post_age_hours < 0:
        raise ValueError(
            f"preferred_post_age_hours for profile '{config.profile_id}' must be 0 or greater."
        )
    if config.min_comment_count < 0:
        raise ValueError(
            f"min_comment_count for profile '{config.profile_id}' must be 0 or greater."
        )
    if config.max_comment_count < 0:
        raise ValueError(
            f"max_comment_count for profile '{config.profile_id}' must be 0 or greater."
        )
    if config.min_comment_count > config.max_comment_count:
        raise ValueError(
            f"comment count bounds for profile '{config.profile_id}' must have min_comment_count <= max_comment_count."
        )
    if config.history_ttl_days <= 0:
        raise ValueError(
            f"history_ttl_days for profile '{config.profile_id}' must be greater than 0."
        )
    _validate_reddit_urls(config)
    validate_v2ex_config_urls(config)
    for snapshot in config.verified_evidence_snapshots:
        if snapshot.platform == "reddit":
            if is_placeholder_reddit_url(snapshot.source_url):
                raise ValueError(
                    f"profile '{config.profile_id}' contains a placeholder verified snapshot URL: "
                    f"{snapshot.source_url}"
                )
            if snapshot.source_url.strip() and not to_eddrit_url(snapshot.source_url):
                raise ValueError(
                    f"profile '{config.profile_id}' contains a non-comments verified snapshot URL: "
                    f"{snapshot.source_url}"
                )
        elif snapshot.platform == "v2ex":
            if is_placeholder_v2ex_url(snapshot.source_url):
                raise ValueError(
                    f"profile '{config.profile_id}' contains a placeholder verified snapshot URL: "
                    f"{snapshot.source_url}"
                )
            if snapshot.source_url.strip() and not canonicalize_v2ex_topic_url(snapshot.source_url):
                raise ValueError(
                    f"profile '{config.profile_id}' contains a non-topic verified snapshot URL: "
                    f"{snapshot.source_url}"
                )
        if not snapshot.text_snapshot.strip():
            raise ValueError(
                f"profile '{config.profile_id}' contains an empty verified evidence snapshot."
            )


def _validate_reddit_urls(config: FounderSignalConfig) -> None:
    for reddit_url in [*config.seed_reddit_urls, *config.excluded_reddit_urls]:
        if is_placeholder_reddit_url(reddit_url):
            raise ValueError(
                f"profile '{config.profile_id}' contains a placeholder Reddit URL: {reddit_url}"
            )
        if reddit_url.strip() and not to_eddrit_url(reddit_url):
            raise ValueError(
                f"profile '{config.profile_id}' contains a non-comments Reddit URL: {reddit_url}"
            )
