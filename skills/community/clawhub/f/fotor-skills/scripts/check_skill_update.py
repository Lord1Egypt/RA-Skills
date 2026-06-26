#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
META_PATH = ROOT / "_meta.json"
SKILL_MD_PATH = ROOT / "SKILL.md"
USER_AGENT = "fotor-skills-update-check/1.0"


def http_get_json(url: str, timeout: float = 8.0) -> dict[str, Any]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_get_text(url: str, timeout: float = 8.0) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/plain"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def parse_semver(value: str) -> tuple[Any, ...]:
    value = value.strip().lstrip("v")
    parts = re.split(r"[.+-]", value)
    out: list[Any] = []
    for part in parts:
        if part.isdigit():
            out.append(int(part))
        else:
            out.append(part)
    return tuple(out)


def summarize_changelog(text: str | None, max_items: int = 3, max_chars: int = 240) -> str | None:
    if not text:
        return None
    raw = text.strip()
    if not raw:
        return None

    bullet_items: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(("- ", "* ")):
            bullet_items.append(line[2:].strip())
        elif re.match(r"^\d+[.)]\s+", line):
            bullet_items.append(re.sub(r"^\d+[.)]\s+", "", line).strip())
        if len(bullet_items) >= max_items:
            break

    if bullet_items:
        summary = "; ".join(bullet_items[:max_items])
    else:
        summary = raw.split("\n\n", 1)[0].replace("\n", " ").strip()

    return summary if len(summary) <= max_chars else summary[: max_chars - 1].rstrip() + "…"


def frontmatter_text(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    return text[4:end]


def parse_frontmatter(path: Path) -> dict[str, Any]:
    fm = frontmatter_text(path)
    if not fm:
        return {}

    data: dict[str, Any] = {}
    metadata: dict[str, str] = {}
    in_metadata = False

    for raw_line in fm.splitlines():
        if not raw_line.strip():
            continue

        if re.match(r"^[A-Za-z0-9_-]+:\s*", raw_line) and not raw_line.startswith("  "):
            key, value = raw_line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key == "metadata":
                in_metadata = True
                data.setdefault("metadata", metadata)
                continue
            in_metadata = False
            data[key] = value
            continue

        if in_metadata:
            m = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", raw_line)
            if m:
                k = m.group(1).strip()
                v = m.group(2).strip().strip('"').strip("'")
                metadata[k] = v

    if metadata:
        data["metadata"] = metadata
    return data


def skill_version_from_frontmatter(fm: dict[str, Any]) -> str | None:
    return fm.get("version") or (fm.get("metadata") or {}).get("version")


def read_local_skill_metadata() -> dict[str, Any]:
    fm = parse_frontmatter(SKILL_MD_PATH)
    return {
        "slug": fm.get("name") or ROOT.name,
        "version": skill_version_from_frontmatter(fm),
        "author": (fm.get("metadata") or {}).get("author"),
    }


def read_clawhub_meta() -> dict[str, Any] | None:
    if not META_PATH.exists():
        return None
    return json.loads(META_PATH.read_text(encoding="utf-8"))


def find_skills_lock(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        lock = parent / "skills-lock.json"
        if lock.exists():
            return lock
    return None


def read_skills_lock_entry(slug: str) -> tuple[Path | None, dict[str, Any] | None]:
    lock_path = find_skills_lock(ROOT)
    if not lock_path:
        return None, None
    try:
        data = json.loads(lock_path.read_text(encoding="utf-8"))
    except Exception:
        return lock_path, None
    return lock_path, ((data.get("skills") or {}).get(slug))


def detect_install_source(slug: str) -> tuple[str, dict[str, Any]]:
    clawhub_meta = read_clawhub_meta()
    if clawhub_meta and clawhub_meta.get("version"):
        return "clawhub", {"meta": clawhub_meta}

    lock_path, lock_entry = read_skills_lock_entry(slug)
    if lock_entry and lock_entry.get("sourceType") == "github":
        return "skills-github", {"lock_path": str(lock_path), "lock_entry": lock_entry}

    return "unknown", {}


def default_state_dir(slug: str) -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    return base / slug


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_clawhub_latest(slug: str, timeout: float) -> tuple[str, str | None]:
    cmd = ["clawhub", "inspect", slug, "--json"]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "clawhub inspect failed").strip())
    start = proc.stdout.find("{")
    if start < 0:
        raise RuntimeError("No JSON object found in clawhub inspect output")
    data = json.loads(proc.stdout[start:])
    latest = data.get("latestVersion", {}).get("version") or data.get("skill", {}).get("tags", {}).get("latest")
    if not latest:
        raise RuntimeError("Latest version not found in clawhub inspect output")
    preview = summarize_changelog(data.get("latestVersion", {}).get("changelog"))
    return latest, preview


def github_repo_default_branch(source: str, timeout: float) -> str:
    data = http_get_json(f"https://api.github.com/repos/{source}", timeout=timeout)
    return data.get("default_branch") or "main"


def github_remote_skill_version(source: str, slug: str, timeout: float) -> str:
    branch = github_repo_default_branch(source, timeout)
    candidates = [
        f"skills/{slug}/SKILL.md",
        f"{slug}/SKILL.md",
        "SKILL.md",
    ]
    last_error: str | None = None
    for rel in candidates:
        url = f"https://raw.githubusercontent.com/{source}/{branch}/{rel}"
        try:
            text = http_get_text(url, timeout=timeout)
        except (HTTPError, URLError) as exc:
            last_error = str(exc)
            continue
        tmp = ROOT / ".__remote_skill_tmp__.md"
        try:
            tmp.write_text(text, encoding="utf-8")
            fm = parse_frontmatter(tmp)
            version = skill_version_from_frontmatter(fm)
            if version:
                return version
        finally:
            try:
                tmp.unlink()
            except Exception:
                pass
    raise RuntimeError(last_error or "Unable to locate remote SKILL.md with a version field")


def extract_changelog_section(text: str, version: str) -> str | None:
    lines = text.splitlines()
    version_patterns = [
        re.compile(rf"^##\s+v?{re.escape(version)}\b", re.IGNORECASE),
        re.compile(rf"^#\s+v?{re.escape(version)}\b", re.IGNORECASE),
    ]

    start = None
    for idx, line in enumerate(lines):
        if any(p.search(line.strip()) for p in version_patterns):
            start = idx + 1
            break
    if start is None:
        return None

    collected: list[str] = []
    for line in lines[start:]:
        if re.match(r"^##\s+", line.strip()) or re.match(r"^#\s+", line.strip()):
            break
        collected.append(line)

    section = "\n".join(collected).strip()
    return section or None


def github_changelog_preview(source: str, version: str, timeout: float) -> str | None:
    branch = github_repo_default_branch(source, timeout)
    url = f"https://raw.githubusercontent.com/{source}/{branch}/CHANGELOG.md"
    try:
        text = http_get_text(url, timeout=timeout)
    except Exception:
        return None

    section = extract_changelog_section(text, version)
    if section:
        return summarize_changelog(section)
    return summarize_changelog(text)


def maybe_use_cached(state: dict[str, Any], now: int, interval_seconds: int) -> bool:
    last_checked_at = int(state.get("last_checked_at", 0) or 0)
    return bool(last_checked_at and (now - last_checked_at) < interval_seconds)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether this installed skill has a newer version available.")
    parser.add_argument("--mark-notified", action="store_true", help="Record the latest version as already notified when an update is available.")
    parser.add_argument("--state-file", help="Optional custom state file path.")
    parser.add_argument("--check-interval-hours", type=float, default=24.0, help="Minimum hours between network version checks (default: 24).")
    parser.add_argument("--timeout-seconds", type=float, default=8.0, help="Timeout for remote checks (default: 8).")
    parser.add_argument("--install-source", choices=["auto", "clawhub", "skills-github"], default="auto", help="Override install-source detection.")
    parser.add_argument("--slug", help="Optional slug override for development/testing.")
    parser.add_argument("--current-version", help="Optional current version override for development/testing.")
    parser.add_argument("--github-source", help="Optional GitHub owner/repo override for development/testing.")
    args = parser.parse_args()

    local = read_local_skill_metadata()
    slug = args.slug or local.get("slug") or ROOT.name
    current_version = args.current_version or local.get("version")

    detected_source, detected_info = detect_install_source(slug)
    install_source = args.install_source if args.install_source != "auto" else detected_source

    github_source = args.github_source
    if install_source == "skills-github" and not github_source:
        github_source = (detected_info.get("lock_entry") or {}).get("source")

    if install_source == "clawhub" and not current_version:
        meta = (detected_info.get("meta") or {})
        current_version = meta.get("version")
        slug = meta.get("slug", slug)

    result: dict[str, Any] = {
        "ok": False,
        "install_source": install_source,
        "slug": slug,
        "current_version": current_version,
        "latest_version": None,
        "update_available": False,
        "should_notify": False,
        "message": None,
        "changelog_preview": None,
        "error": None,
        "checked_live": False,
        "used_cache": False,
    }

    if install_source == "unknown":
        result["error"] = "Unable to detect install source. Supported sources: clawhub, skills-github."
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if not slug or not current_version:
        result["error"] = "Missing slug/current version. For skills-github installs, ensure SKILL.md has a top-level version field or legacy metadata.version."
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if install_source == "skills-github" and not github_source:
        result["error"] = "Missing GitHub source. Ensure skills-lock.json is discoverable or pass --github-source owner/repo."
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    state_file = Path(args.state_file) if args.state_file else default_state_dir(slug) / f"update-check-{install_source}.json"
    state = load_state(state_file)
    now = int(time.time())
    interval_seconds = max(0, int(args.check_interval_hours * 3600))
    last_notified_version = state.get("last_notified_version")

    latest_version: str | None = None
    changelog_preview: str | None = None
    update_available = False

    if maybe_use_cached(state, now, interval_seconds):
        latest_version = state.get("last_latest_version")
        changelog_preview = state.get("last_changelog_preview")
        if latest_version:
            update_available = parse_semver(latest_version) > parse_semver(current_version)
        else:
            update_available = False
        state["last_current_version"] = current_version
        state["last_update_available"] = update_available
        save_state(state_file, state)
        result["used_cache"] = True
    else:
        try:
            if install_source == "clawhub":
                latest_version, changelog_preview = check_clawhub_latest(slug, args.timeout_seconds)
            elif install_source == "skills-github":
                latest_version = github_remote_skill_version(github_source, slug, args.timeout_seconds)
                changelog_preview = github_changelog_preview(github_source, latest_version, args.timeout_seconds)
            else:
                raise RuntimeError(f"Unsupported install source: {install_source}")
        except Exception as exc:
            result["error"] = str(exc)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0

        update_available = parse_semver(latest_version) > parse_semver(current_version)
        state["last_checked_at"] = now
        state["last_current_version"] = current_version
        state["last_latest_version"] = latest_version
        state["last_changelog_preview"] = changelog_preview
        state["last_update_available"] = update_available
        save_state(state_file, state)
        result["checked_live"] = True

    should_notify = bool(update_available and latest_version and latest_version != last_notified_version)

    if update_available:
        highlights = f" Highlights: {changelog_preview}" if changelog_preview else ""
        message = (
            f"{slug} has an update available via {install_source}: current {current_version}, latest {latest_version}.{highlights} "
            f"If the user wants to update, suggest the updater that matches the install source."
        )
    else:
        message = f"{slug} is up to date for install source {install_source} (current {current_version})."

    if args.mark_notified and should_notify:
        state["last_notified_version"] = latest_version
        save_state(state_file, state)

    result.update(
        {
            "ok": True,
            "latest_version": latest_version,
            "update_available": update_available,
            "should_notify": should_notify,
            "message": message,
            "changelog_preview": changelog_preview,
            "error": None,
        }
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
