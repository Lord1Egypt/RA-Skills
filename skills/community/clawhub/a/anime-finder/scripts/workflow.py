#!/usr/bin/env python3
"""Single-entry workflow for anime finding, intent resolution, and download."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from functools import lru_cache
from pathlib import Path

from intent import DEFAULT_RESOLUTION_ORDER, parse_intent
from search_nyaa import run_search
from verify import _extract_core_query, verify_anime

ROOT = Path(__file__).resolve().parents[1]
OVERRIDE_PATH = Path(__file__).with_name("data") / "series_overrides.json"
STATE_DIR = ROOT / "state"
PROFILE_PATH = STATE_DIR / "user_profile.json"
LAST_DOWNLOAD_PATH = STATE_DIR / "last_download.json"

DEFAULT_PROFILE = {
    "subtitle_pref": None,
    "resolution_order": list(DEFAULT_RESOLUTION_ORDER),
    "file_size_cap_gb": None,
    "downloader": "transmission",
    "default_action": "search",
    "auto_download_high_confidence": True,
    "preferred_release_groups": [],
    "blocked_release_groups": [],
}

SUBTITLE_KEYWORDS = {
    "simplified": ["简中", "简体", "chs", "simplified", "中字", "中文字幕"],
    "traditional": ["繁中", "繁体", "cht", "traditional"],
}


def _add_unique(items: list[str], value: str | None) -> None:
    if not value:
        return
    value = value.strip()
    if value and value not in items:
        items.append(value)


def _add_reason(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def _normalize_lookup(text: str) -> str:
    text = text.lower()
    text = text.replace("’", "'").replace("'", "")
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", text)


def _normalize_group_text(text: str) -> str:
    return re.sub(r"[^0-9a-z]+", "", text.lower())


def _ordered_resolution(value: str | None) -> list[str]:
    if not value:
        return list(DEFAULT_RESOLUTION_ORDER)
    order = [value]
    for candidate in DEFAULT_RESOLUTION_ORDER:
        if candidate != value:
            order.append(candidate)
    return order


def _resolution_key(title: str) -> str | None:
    lowered = title.lower()
    if "2160p" in lowered or "4k" in lowered or "uhd" in lowered:
        return "2160p"
    if "1080p" in lowered:
        return "1080p"
    if "720p" in lowered:
        return "720p"
    if "480p" in lowered:
        return "480p"
    if "360p" in lowered:
        return "360p"
    return None


def _subtitle_bucket(title: str) -> str | None:
    lowered = title.lower()
    for bucket, keywords in SUBTITLE_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return bucket
    return None


def _size_to_gb(text: str) -> float | None:
    match = re.search(r"([\d.]+)\s*(GiB|MiB|GB|MB|KB)", text, re.IGNORECASE)
    if not match:
        return None

    value = float(match.group(1))
    unit = match.group(2).upper()
    if unit in {"GIB", "GB"}:
        return value
    if unit in {"MIB", "MB"}:
        return value / 1024
    if unit in {"KB"}:
        return value / (1024 * 1024)
    return None


def _ensure_state_dir() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: dict) -> None:
    _ensure_state_dir()
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def _read_json(path: Path, default: dict | None = None) -> dict:
    if not path.exists():
        return dict(default or {})
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def load_series_overrides() -> list[dict]:
    if not OVERRIDE_PATH.exists():
        return []

    with OVERRIDE_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    return data.get("series", [])


def load_user_profile() -> dict:
    profile = dict(DEFAULT_PROFILE)
    profile.update(_read_json(PROFILE_PATH))
    for key in ("preferred_release_groups", "blocked_release_groups", "resolution_order"):
        value = profile.get(key)
        if not isinstance(value, list):
            profile[key] = list(DEFAULT_PROFILE[key])
    return profile


def load_persisted_profile() -> dict:
    profile = _read_json(PROFILE_PATH)
    for key in ("preferred_release_groups", "blocked_release_groups", "resolution_order"):
        if key in profile and not isinstance(profile[key], list):
            profile[key] = list(DEFAULT_PROFILE[key])
    return profile


def save_user_profile(updates: dict) -> dict:
    profile = load_user_profile()
    profile.update(updates)
    _write_json(PROFILE_PATH, profile)
    return profile


def load_last_download_state() -> dict | None:
    data = _read_json(LAST_DOWNLOAD_PATH)
    return data or None


def save_last_download_state(record: dict) -> None:
    _write_json(LAST_DOWNLOAD_PATH, record)


def resolve_series_override(query: str) -> dict | None:
    normalized_query = _normalize_lookup(query)

    for entry in load_series_overrides():
        candidates = [entry.get("id", ""), entry.get("canonical_query", "")]
        candidates.extend(entry.get("match", []))
        for candidate in candidates:
            if _normalize_lookup(candidate) == normalized_query:
                return entry
    return None


def expand_aliases(text: str) -> list[str]:
    aliases: list[str] = []
    if not text:
        return aliases

    _add_unique(aliases, text)
    stripped = text.replace("’", "'").replace("'", "")
    _add_unique(aliases, stripped)
    core = _extract_core_query(text)
    if core != text:
        _add_unique(aliases, core)
    return aliases


def choose_verify_query(query: str, override: dict | None, latest_season: bool) -> str:
    if override and latest_season:
        latest = override.get("latest_season", {})
        if latest.get("bangumi_query"):
            return latest["bangumi_query"]

    if override and override.get("bangumi_query"):
        return override["bangumi_query"]

    return query


def choose_primary_search_query(
    query: str,
    verification: dict,
    override: dict | None,
    latest_season: bool,
) -> str:
    if override and latest_season:
        latest = override.get("latest_season", {})
        if latest.get("primary_query"):
            return latest["primary_query"]

    if override and override.get("canonical_query"):
        return override["canonical_query"]

    match = verification.get("match") or {}
    return match.get("name") or query


def build_search_aliases(
    query: str,
    verification: dict,
    override: dict | None = None,
    latest_season: bool = False,
) -> list[str]:
    aliases: list[str] = []

    if override:
        for candidate in override.get("aliases", []):
            for expanded in expand_aliases(candidate):
                _add_unique(aliases, expanded)

        if latest_season:
            latest = override.get("latest_season", {})
            for candidate in latest.get("aliases", []):
                for expanded in expand_aliases(candidate):
                    _add_unique(aliases, expanded)

    for candidate in expand_aliases(query):
        _add_unique(aliases, candidate)

    match = verification.get("match") or {}
    if verification.get("status") in {"found", "ambiguous", "api_error"}:
        for key in ("name", "name_jp"):
            for candidate in expand_aliases(match.get(key, "")):
                _add_unique(aliases, candidate)
    elif verification.get("status") == "not_found":
        for alternative in verification.get("alternatives", [])[:3]:
            for key in ("name", "name_jp"):
                for candidate in expand_aliases(alternative.get(key, "")):
                    _add_unique(aliases, candidate)

    return aliases


def needs_user_choice(verification: dict) -> bool:
    status = verification.get("status")
    if status == "ambiguous":
        return True
    if status == "not_found" and verification.get("alternatives"):
        return True
    return False


def search_has_consensus(search: dict, episode: int | None, latest_season: bool, season: int | None) -> bool:
    if search.get("error") or not search.get("results"):
        return False

    sample = search["results"][: min(3, len(search["results"]))]
    if not sample:
        return False

    if episode is not None and any(episode not in item.get("episode_numbers", []) for item in sample):
        return False

    if season is not None and any(season not in item.get("season_numbers", []) for item in sample):
        return False

    if latest_season:
        resolved_latest_season = search.get("resolved_latest_season")
        if resolved_latest_season is None:
            return False
        if any(resolved_latest_season not in item.get("season_numbers", []) for item in sample):
            return False

    return True


def _torrent_url(torrent_id: str) -> str:
    return f"https://nyaa.si/download/{torrent_id}.torrent"


def _magnet(infohash: str, name: str) -> str:
    return f"magnet:?xt=urn:btih:{infohash}&dn={name}"


def _download_torrent_file(torrent_id: str, destination: str) -> None:
    req = urllib.request.Request(
        _torrent_url(torrent_id),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        data = response.read()
    with open(destination, "wb") as handle:
        handle.write(data)


def _run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def _ensure_transmission(download_dir: str) -> tuple[bool, str | None]:
    if not shutil.which("transmission-daemon") or not shutil.which("transmission-remote"):
        return False, "Transmission 未安装，已回退到磁力链接模式"

    if _run_command(["pgrep", "-x", "transmission-daemon"]).returncode != 0:
        os.makedirs(os.path.expanduser("~/.transmission"), exist_ok=True)
        subprocess.Popen(
            [
                "transmission-daemon",
                "--config-dir",
                os.path.expanduser("~/.transmission"),
                "--download-dir",
                download_dir,
                "--log-level=error",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(3)

    if _run_command(["pgrep", "-x", "transmission-daemon"]).returncode != 0:
        return False, "transmission-daemon 无法启动，已回退到磁力链接模式"
    return True, None


def _list_transmission_entries() -> list[dict]:
    if not shutil.which("transmission-remote"):
        return []
    result = _run_command(["transmission-remote", "-l"])
    if result.returncode != 0:
        return []

    entries: list[dict] = []
    for line in result.stdout.splitlines():
        if not line.strip() or line.startswith("ID") or line.startswith("Sum:"):
            continue
        parts = line.split(None, 8)
        if len(parts) < 9:
            continue
        entries.append(
            {
                "id": parts[0].rstrip("*"),
                "done": parts[1],
                "status": parts[7],
                "name": parts[8],
            }
        )
    return entries


def _find_transmission_entry(name: str) -> dict | None:
    target = _normalize_group_text(name)
    for entry in _list_transmission_entries():
        current = _normalize_group_text(entry.get("name", ""))
        if not current:
            continue
        if target in current or current in target:
            return entry
    return None


def _parse_transmission_info(output: str) -> dict:
    info: dict = {}
    for line in output.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip().lower().replace(" ", "_")] = value.strip()
    return info


def fetch_download_status(last_state: dict | None) -> dict:
    if not last_state:
        return {
            "status": "blocked",
            "reason": "暂无最近下载记录。",
        }

    if last_state.get("status") == "fallback_to_magnet":
        return {
            "status": "fallback_to_magnet",
            "reason": "最近一次请求只返回了磁力链接，没有可追踪的下载进度。",
            "magnet": last_state.get("magnet"),
            "torrent_url": last_state.get("torrent_url"),
            "name": last_state.get("name"),
        }

    transmission_id = last_state.get("transmission_id")
    if not transmission_id or not shutil.which("transmission-remote"):
        return {
            "status": last_state.get("status", "queued"),
            "name": last_state.get("name"),
            "reason": "缺少 Transmission 任务 ID，返回最近一次已知状态。",
        }

    result = _run_command(["transmission-remote", "-t", str(transmission_id), "-i"])
    if result.returncode != 0:
        return {
            "status": last_state.get("status", "queued"),
            "name": last_state.get("name"),
            "reason": result.stderr.strip() or result.stdout.strip() or "无法读取 Transmission 状态。",
            "transmission_id": transmission_id,
        }

    parsed = _parse_transmission_info(result.stdout)
    progress = parsed.get("percent_done") or parsed.get("percentdone")
    state = parsed.get("state") or parsed.get("status") or "unknown"
    return {
        "status": "queued",
        "name": last_state.get("name"),
        "transmission_id": transmission_id,
        "transmission_state": state,
        "progress": progress,
        "eta": parsed.get("eta"),
        "download_dir": last_state.get("download_dir"),
        "magnet": last_state.get("magnet"),
        "torrent_url": last_state.get("torrent_url"),
    }


def queue_download(best: dict, download_dir: str, downloader: str) -> dict:
    magnet = _magnet(best["infohash"], best["title"])
    torrent_url = _torrent_url(best["torrent_id"])

    if downloader == "cli-only":
        return {
            "status": "fallback_to_magnet",
            "mode": "cli-only",
            "reason": "cli-only 模式按请求直接返回磁力链接",
            "magnet": magnet,
            "torrent_url": torrent_url,
            "name": best["title"],
        }

    ok, reason = _ensure_transmission(download_dir)
    if not ok:
        return {
            "status": "fallback_to_magnet",
            "reason": reason,
            "magnet": magnet,
            "torrent_url": torrent_url,
            "name": best["title"],
        }

    with tempfile.TemporaryDirectory() as temp_dir:
        torrent_path = os.path.join(temp_dir, "download.torrent")
        try:
            _download_torrent_file(best["torrent_id"], torrent_path)
        except Exception as exc:
            return {
                "status": "fallback_to_magnet",
                "reason": f"种子文件下载失败：{exc}",
                "magnet": magnet,
                "torrent_url": torrent_url,
                "name": best["title"],
            }

        result = _run_command(
            [
                "transmission-remote",
                "--add",
                torrent_path,
                "--download-dir",
                download_dir,
            ]
        )

    if result.returncode != 0:
        return {
            "status": "fallback_to_magnet",
            "reason": f"Transmission 添加失败：{result.stderr.strip() or result.stdout.strip()}",
            "magnet": magnet,
            "torrent_url": torrent_url,
            "name": best["title"],
        }

    entry = _find_transmission_entry(best["title"])
    return {
        "status": "queued",
        "downloader": "transmission-daemon",
        "download_dir": download_dir,
        "name": best["title"],
        "infohash": best["infohash"],
        "magnet": magnet,
        "torrent_url": torrent_url,
        "transmission_id": entry.get("id") if entry else None,
        "transmission_status": entry.get("status") if entry else None,
        "progress": entry.get("done") if entry else None,
    }


def _blocked_download(reason: str) -> dict:
    return {
        "status": "blocked",
        "reason": reason,
    }


def apply_explicit_season_filter(search: dict, season: int | None) -> dict:
    if season is None or search.get("error") or not search.get("results"):
        return search

    filtered = [
        result
        for result in search.get("results", [])
        if season in result.get("season_numbers", [])
    ]
    if not filtered:
        warnings = list(search.get("warnings", []))
        warnings.append(f"结果中没有明确命中第 {season} 季的条目。")
        search["warnings"] = warnings
        search["results"] = []
        search["total"] = 0
        return search

    search["results"] = filtered
    search["total"] = len(filtered)
    return search


def apply_result_preferences(search: dict, preferences: dict) -> dict:
    if search.get("error") or not search.get("results"):
        return search

    warnings = list(search.get("warnings", []))
    results = [dict(result) for result in search.get("results", [])]
    filtered_by: list[str] = []
    blocked_groups = [
        _normalize_group_text(value)
        for value in preferences.get("blocked_release_groups", [])
        if value
    ]
    preferred_groups = [
        _normalize_group_text(value)
        for value in preferences.get("preferred_release_groups", [])
        if value
    ]
    file_size_cap = preferences.get("file_size_cap_gb")
    resolution_order = preferences.get("resolution_order") or list(DEFAULT_RESOLUTION_ORDER)
    resolution_rank = {value: index for index, value in enumerate(resolution_order)}
    subtitle_pref = preferences.get("subtitle_pref")

    if blocked_groups:
        kept = [
            result
            for result in results
            if not any(group in _normalize_group_text(result["title"]) for group in blocked_groups)
        ]
        if kept:
            results = kept
            filtered_by.append("blocked_release_groups")

    if file_size_cap is not None:
        kept = [
            result
            for result in results
            if (_size_to_gb(result.get("size", "")) or 0) <= file_size_cap
        ]
        if kept:
            results = kept
            filtered_by.append("file_size_cap_gb")

    for result in results:
        preference_score = 0
        reasons: list[str] = []
        resolution = _resolution_key(result["title"])
        if resolution and resolution in resolution_rank:
            preference_score += max(0, 24 - resolution_rank[resolution] * 6)
            reasons.append(f"resolution:{resolution}")

        subtitle_bucket = _subtitle_bucket(result["title"])
        if subtitle_pref:
            if subtitle_bucket == subtitle_pref:
                preference_score += 18
                reasons.append(f"subtitle:{subtitle_pref}")
            elif subtitle_bucket and subtitle_bucket != subtitle_pref:
                preference_score -= 8

        normalized_title = _normalize_group_text(result["title"])
        if preferred_groups and any(group in normalized_title for group in preferred_groups):
            preference_score += 20
            reasons.append("preferred_group")
        if blocked_groups and any(group in normalized_title for group in blocked_groups):
            preference_score -= 40

        result["preference_score"] = preference_score
        if reasons:
            result["preference_reasons"] = reasons
        result["effective_score"] = result.get("score", 0) + preference_score

    results.sort(key=lambda item: (-item.get("effective_score", item.get("score", 0)), -item["seeders"], item["title"]))
    if filtered_by:
        warnings.append(f"已按偏好过滤：{', '.join(filtered_by)}")

    search["results"] = results
    search["total"] = len(results)
    search["warnings"] = warnings
    search["preferences_applied"] = {
        "subtitle_pref": subtitle_pref,
        "resolution_order": resolution_order,
        "file_size_cap_gb": file_size_cap,
        "preferred_release_groups": preferences.get("preferred_release_groups", []),
        "blocked_release_groups": preferences.get("blocked_release_groups", []),
    }
    return search


def determine_effective_settings(
    intent: dict,
    *,
    episode: int | None,
    latest_season: bool,
    prefer_4k: bool,
    do_download: bool,
    downloader: str,
    explicit_flags: dict,
    profile: dict,
    override: dict | None,
) -> tuple[dict, list[str]]:
    effective = dict(DEFAULT_PROFILE)
    effective["resolution_order"] = list(DEFAULT_PROFILE["resolution_order"])
    source: dict[str, str] = {key: "default" for key in effective}

    def apply_layer(values: dict, source_name: str) -> None:
        for key, value in values.items():
            if value is None:
                continue
            if key in {"preferred_release_groups", "blocked_release_groups", "resolution_order"}:
                effective[key] = list(value)
            else:
                effective[key] = value
            source[key] = source_name

    apply_layer((override or {}).get("default_preferences", {}), "series_override")
    apply_layer(profile, "user_profile")

    if intent.get("subtitle_pref"):
        effective["subtitle_pref"] = intent["subtitle_pref"]
        source["subtitle_pref"] = "intent"
    if intent.get("quality_pref"):
        effective["resolution_order"] = _ordered_resolution(intent["quality_pref"])
        source["resolution_order"] = "intent"
    if intent.get("file_size_cap_gb") is not None:
        effective["file_size_cap_gb"] = intent["file_size_cap_gb"]
        source["file_size_cap_gb"] = "intent"
    if intent.get("downloader_pref"):
        effective["downloader"] = intent["downloader_pref"]
        source["downloader"] = "intent"
    if intent.get("preferred_release_groups"):
        effective["preferred_release_groups"] = list(intent["preferred_release_groups"])
        source["preferred_release_groups"] = "intent"
    if intent.get("blocked_release_groups"):
        effective["blocked_release_groups"] = list(intent["blocked_release_groups"])
        source["blocked_release_groups"] = "intent"

    if prefer_4k:
        effective["resolution_order"] = _ordered_resolution("2160p")
        source["resolution_order"] = "cli"
    if explicit_flags.get("downloader"):
        effective["downloader"] = downloader
        source["downloader"] = "cli"
    if do_download and explicit_flags.get("download"):
        effective["default_action"] = "download"
        source["default_action"] = "cli"

    profile_applied = [key for key, value in source.items() if value == "user_profile"]
    return effective, profile_applied


def determine_effective_action(intent: dict, settings: dict, explicit_flags: dict) -> tuple[str, list[str]]:
    reasons = list(intent.get("reason_codes", []))

    if explicit_flags.get("downloader") and settings.get("downloader") == "cli-only":
        _add_reason(reasons, "cli_only_override")
        return "magnet", reasons

    if explicit_flags.get("download"):
        _add_reason(reasons, "cli_download_override")
        return "download", reasons

    action = intent.get("action", "search")
    if action == "search":
        default_action = settings.get("default_action", "search")
        if (
            default_action in {"download", "magnet"}
            and settings.get("auto_download_high_confidence", True)
            and intent.get("confidence") == "high"
            and intent.get("watch_intent")
        ):
            _add_reason(reasons, "profile_default_action")
            action = default_action

    if action in {"download", "magnet"} and settings.get("auto_download_high_confidence", True):
        _add_reason(reasons, "auto_download_high_confidence")

    return action, reasons


def finalize_status(output: dict, do_download: bool) -> str:
    if output["needs_user_choice"]:
        return "need_disambiguation"

    search = output["search"]
    if search.get("error"):
        return "blocked"

    if not search.get("results"):
        return "no_results"

    if not do_download:
        return "ready"

    download = output.get("download") or {}
    if download.get("status") == "queued":
        return "queued"
    if download.get("status") == "fallback_to_magnet":
        return "fallback_to_magnet"
    return "blocked"


def build_decision(
    *,
    intent: dict,
    profile_applied: list[str],
    reason_codes: list[str],
    status: str,
    confirmation_required: bool,
) -> dict:
    if status == "blocked":
        autonomy_mode = "halt"
    elif confirmation_required:
        autonomy_mode = "ask_once"
    else:
        autonomy_mode = "auto_execute"

    return {
        "confidence": intent.get("confidence", "medium"),
        "confirmation_required": confirmation_required,
        "autonomy_mode": autonomy_mode,
        "profile_applied": profile_applied,
        "reason_codes": reason_codes,
    }


def build_summary(output: dict) -> str:
    status = output["status"]
    if status == "need_disambiguation":
        return output.get("next_question") or "还需要你确认一个关键信息后才能继续。"
    if status == "blocked":
        return output.get("download", {}).get("reason") or output["search"].get("error") or "流程被阻断。"
    if status == "no_results":
        return "没有找到符合当前条件的可下载视频资源。"
    if status == "ready":
        best = output.get("best_result") or {}
        return f"已找到最佳资源：{best.get('title', '未知条目')}。"
    if status == "queued":
        download = output.get("download") or {}
        return f"已将 {download.get('name', '目标资源')} 加入下载队列。"
    if status == "fallback_to_magnet":
        download = output.get("download") or {}
        return download.get("reason") or "已返回磁力链接作为回退结果。"
    return "流程完成。"


def make_status_output(query: str, intent: dict, profile_applied: list[str], reason_codes: list[str]) -> dict:
    last_state = load_last_download_state()
    download = fetch_download_status(last_state)
    status = "queued"
    if download.get("status") == "blocked":
        status = "blocked"
    elif download.get("status") == "fallback_to_magnet":
        status = "fallback_to_magnet"

    output = {
        "query": query,
        "status": status,
        "verification": {"status": "skipped", "reason": "status_query"},
        "search": {"status": "skipped", "results": [], "reason": "status_query"},
        "intent": intent,
        "decision": build_decision(
            intent=intent,
            profile_applied=profile_applied,
            reason_codes=reason_codes,
            status=status,
            confirmation_required=False,
        ),
        "needs_user_choice": False,
        "auto_resolved_by_search": False,
        "download": download,
        "last_download": last_state,
    }
    output["summary"] = "暂无最近下载记录。" if status == "blocked" else (
        f"最近任务 {download.get('name', '未知任务')} 当前状态：{download.get('transmission_state') or download.get('status')}。"
    )
    return output


def _record_download_state(query: str, intent: dict, best_result: dict | None, download: dict) -> None:
    record = {
        "query": query,
        "title": intent.get("title"),
        "action": intent.get("action"),
        "status": download.get("status"),
        "name": download.get("name") or (best_result or {}).get("title"),
        "torrent_id": (best_result or {}).get("torrent_id"),
        "infohash": (best_result or {}).get("infohash") or download.get("infohash"),
        "download_dir": download.get("download_dir"),
        "magnet": download.get("magnet"),
        "torrent_url": download.get("torrent_url"),
        "transmission_id": download.get("transmission_id"),
        "saved_at": int(time.time()),
    }
    save_last_download_state(record)


def workflow(
    query: str,
    *,
    episode: int | None = None,
    latest_season: bool = False,
    prefer_4k: bool = False,
    do_download: bool = False,
    downloader: str = "transmission",
    download_dir: str | None = None,
    episode_explicit: bool = False,
    latest_season_explicit: bool = False,
    prefer_4k_explicit: bool = False,
    download_explicit: bool = False,
    downloader_explicit: bool = False,
) -> dict:
    parsed_intent = parse_intent(query)

    profile_update = None
    if parsed_intent.get("should_persist_profile") and parsed_intent.get("profile_updates"):
        saved_profile = save_user_profile(parsed_intent["profile_updates"])
        profile_update = {
            "saved": True,
            "updates": parsed_intent["profile_updates"],
            "profile_path": str(PROFILE_PATH),
            "profile": saved_profile,
        }

    title = parsed_intent.get("title") or query
    override = resolve_series_override(title)
    explicit_flags = {
        "episode": episode_explicit or episode is not None,
        "latest_season": latest_season_explicit or latest_season,
        "prefer_4k": prefer_4k_explicit or prefer_4k,
        "download": download_explicit or do_download,
        "downloader": downloader_explicit or downloader != "transmission",
    }
    settings, profile_applied = determine_effective_settings(
        parsed_intent,
        episode=episode,
        latest_season=latest_season,
        prefer_4k=prefer_4k,
        do_download=do_download,
        downloader=downloader,
        explicit_flags=explicit_flags,
        profile=load_persisted_profile(),
        override=override,
    )
    action, reason_codes = determine_effective_action(parsed_intent, settings, explicit_flags)

    resolved_intent = dict(parsed_intent)
    resolved_intent["title"] = parsed_intent.get("title")
    resolved_intent["episode"] = episode if explicit_flags.get("episode") else parsed_intent.get("episode")
    resolved_intent["season"] = parsed_intent.get("season")
    resolved_intent["latest_season"] = (
        latest_season if explicit_flags.get("latest_season") else parsed_intent.get("latest_season")
    )
    resolved_intent["quality_pref"] = settings.get("resolution_order", [None])[0]
    resolved_intent["subtitle_pref"] = parsed_intent.get("subtitle_pref") or settings.get("subtitle_pref")
    resolved_intent["downloader_pref"] = "cli-only" if action == "magnet" else settings.get("downloader")
    resolved_intent["action"] = action

    if action == "status":
        output = make_status_output(query, resolved_intent, profile_applied, reason_codes)
        if profile_update:
            output["profile_update"] = profile_update
        return output

    if not resolved_intent.get("title"):
        output = {
            "query": query,
            "status": "need_disambiguation",
            "verification": {"status": "skipped", "reason": "missing_title"},
            "search": {"status": "skipped", "results": [], "reason": "missing_title"},
            "intent": resolved_intent,
            "needs_user_choice": True,
            "auto_resolved_by_search": False,
            "next_question": "你想找哪部番？",
        }
        output["decision"] = build_decision(
            intent=resolved_intent,
            profile_applied=profile_applied,
            reason_codes=reason_codes,
            status=output["status"],
            confirmation_required=True,
        )
        if profile_update:
            output["profile_update"] = profile_update
        output["summary"] = build_summary(output)
        return output

    resolved_episode = resolved_intent.get("episode")
    resolved_season = resolved_intent.get("season")
    resolved_latest_season = bool(resolved_intent.get("latest_season"))
    prefer_4k_final = settings.get("resolution_order", [None])[0] == "2160p"
    do_download_final = action in {"download", "magnet"}
    downloader_final = "cli-only" if action == "magnet" else settings.get("downloader", downloader)

    verify_query = choose_verify_query(resolved_intent["title"], override, resolved_latest_season)
    verification = verify_anime(verify_query, output_json=True)

    primary_search_query = choose_primary_search_query(resolved_intent["title"], verification, override, resolved_latest_season)
    aliases = build_search_aliases(resolved_intent["title"], verification, override, resolved_latest_season)
    alias_list = [candidate for candidate in aliases if candidate != primary_search_query]

    search = run_search(
        primary_search_query,
        aliases=alias_list,
        episode=resolved_episode,
        latest_season=resolved_latest_season,
        prefer_4k=prefer_4k_final,
    )
    search = apply_explicit_season_filter(search, resolved_season)
    search = apply_result_preferences(search, settings)

    auto_resolved_by_search = (
        verification.get("status") == "ambiguous"
        and search_has_consensus(search, resolved_episode, resolved_latest_season, resolved_season)
    )

    output = {
        "query": query,
        "status": "blocked",
        "verification": verification,
        "search": search,
        "intent": resolved_intent,
        "episode": resolved_episode,
        "season": resolved_season,
        "latest_season_requested": resolved_latest_season,
        "prefer_4k": prefer_4k_final,
        "needs_user_choice": needs_user_choice(verification) and not auto_resolved_by_search,
        "auto_resolved_by_search": auto_resolved_by_search,
    }

    if override:
        output["series_override"] = {
            "id": override.get("id"),
            "verify_query": verify_query,
            "primary_search_query": primary_search_query,
        }

    best_result = search.get("results", [])[:1]
    if best_result:
        output["best_result"] = best_result[0]

    if output["needs_user_choice"]:
        output["next_question"] = "Bangumi 返回了多个候选，请先确认具体是哪一部番。"

    if do_download_final:
        if output["needs_user_choice"]:
            output["download"] = _blocked_download("Bangumi 返回了多个可能匹配，先让用户确认番名再下载。")
        elif search.get("error"):
            output["download"] = _blocked_download(search["error"])
        elif not search.get("results"):
            output["download"] = _blocked_download("没有找到可下载的资源。")
        else:
            output["download"] = queue_download(
                search["results"][0],
                download_dir or os.path.expanduser("~/Downloads"),
                downloader_final,
            )
            _record_download_state(query, resolved_intent, output.get("best_result"), output["download"])

    output["status"] = finalize_status(output, do_download_final)
    output["decision"] = build_decision(
        intent=resolved_intent,
        profile_applied=profile_applied,
        reason_codes=reason_codes,
        status=output["status"],
        confirmation_required=output["needs_user_choice"],
    )
    if profile_update:
        output["profile_update"] = profile_update
    output["summary"] = build_summary(output)
    return output


def _print_human(output: dict) -> None:
    print(f"📺 查询：{output['query']}")
    print(f"📌 状态：{output['status']}")
    print(f"🧭 意图：{output['intent'].get('action')} | 置信度：{output['decision'].get('confidence')}")
    print(f"📝 摘要：{output.get('summary')}")

    verification = output["verification"]
    if verification.get("status") and verification.get("status") != "skipped":
        print(f"🔎 番剧确认：{verification.get('status')}")
        if verification.get("match"):
            print(f"   命中：{verification['match'].get('name')}")
    if output.get("next_question"):
        print(f"❓ 下一问：{output['next_question']}")

    search = output["search"]
    if search.get("error"):
        print(f"❌ {search['error']}")
    elif search.get("results"):
        print(f"🔍 搜索查询：{', '.join(search.get('search_queries', []))}")
        print(f"📋 结果数：{search.get('total', 0)}")
        if search.get("resolved_latest_season") is not None:
            print(f"📺 已锁定最新一季：S{search['resolved_latest_season']:02d}")
        best = output.get("best_result")
        if best:
            print(f"✅ 最佳结果：{best['title']}")
            print(f"   大小：{best['size']} | 种子：{best['seeders']} | 评分：{best.get('effective_score', best.get('score'))}")

    if output.get("download"):
        download = output["download"]
        print(f"⬇️  下载状态：{download['status']}")
        if download.get("transmission_state"):
            print(f"   Transmission：{download['transmission_state']} | 进度：{download.get('progress')}")
        if download.get("reason"):
            print(f"   原因：{download['reason']}")
        if download.get("download_dir"):
            print(f"   目录：{download['download_dir']}")
        if download.get("magnet"):
            print(f"   磁力：{download['magnet']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve anime intent, search Nyaa, and optionally queue a download.")
    parser.add_argument("query", help="Anime title, user utterance, or follow-up request")
    parser.add_argument("--episode", type=int, help="Target episode number")
    parser.add_argument("--latest-season", action="store_true", help="Prefer the latest detected season")
    parser.add_argument("--prefer-4k", action="store_true", help="Prefer 4K releases")
    parser.add_argument("--download", action="store_true", help="Queue the best result for download")
    parser.add_argument(
        "--downloader",
        default="transmission",
        choices=["transmission", "transmission-daemon", "cli-only"],
        help="Download mode",
    )
    parser.add_argument("--download-dir", help="Target download directory")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    argv = sys.argv[1:]
    output = workflow(
        args.query,
        episode=args.episode,
        latest_season=args.latest_season,
        prefer_4k=args.prefer_4k,
        do_download=args.download,
        downloader=args.downloader,
        download_dir=args.download_dir,
        episode_explicit="--episode" in argv,
        latest_season_explicit="--latest-season" in argv,
        prefer_4k_explicit="--prefer-4k" in argv,
        download_explicit="--download" in argv,
        downloader_explicit="--downloader" in argv,
    )

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        _print_human(output)

    sys.exit(1 if output["status"] == "blocked" else 0)


if __name__ == "__main__":
    main()
