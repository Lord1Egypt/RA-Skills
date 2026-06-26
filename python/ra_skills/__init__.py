"""
ra-skills — search 90,896 Hermes Agent skills offline.

A lightweight, dependency-free search tool over the RA-Skills registry
(https://github.com/Lord1Egypt/RA-Skills). The full skill content (~6.5 GB of
folders) lives in the GitHub repo; this package bundles only the ~45 MB metadata
index so you can search instantly, then fetch a skill's SKILL.md on demand.

API:
    from ra_skills import search, stats, show, fetch_content
    search("github", limit=5)
    stats()
    show("github-pr-workflow")
    fetch_content("aso-playbook")   # downloads SKILL.md from GitHub
"""
import json
import os
import re
import urllib.request
import urllib.parse

__version__ = "1.0.0"

REPO = "Lord1Egypt/RA-Skills"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/master"
GITHUB_API = f"https://api.github.com/repos/{REPO}/contents"

_registry = None


def _registry_path():
    """Bundled registry (in wheel) with a dev fallback to the repo root."""
    here = os.path.dirname(os.path.abspath(__file__))
    bundled = os.path.join(here, "_data", "registry.json")
    if os.path.exists(bundled):
        return bundled
    # dev fallback: <repo>/registry.json (two levels up from python/ra_skills/)
    root = os.path.abspath(os.path.join(here, "..", "..", "registry.json"))
    return root


def _load():
    global _registry
    if _registry is None:
        path = _registry_path()
        if not os.path.exists(path):
            raise FileNotFoundError(
                "registry.json not found. Reinstall ra-skills or run from the repo."
            )
        with open(path, "r", encoding="utf-8") as f:
            _registry = json.load(f)
    return _registry


def all_skills():
    """Return the raw list of all skill metadata dicts."""
    return _load().get("skills", [])


def stats():
    """Return registry totals: total, built_in, optional, community, by_source."""
    data = _load()
    by_source = {}
    for s in data.get("skills", []):
        by_source[s.get("source", "?")] = by_source.get(s.get("source", "?"), 0) + 1
    return {
        "total": data.get("total", len(data.get("skills", []))),
        "built_in": data.get("built_in", 0),
        "optional": data.get("optional", 0),
        "community": data.get("community", 0),
        "by_source": dict(sorted(by_source.items(), key=lambda kv: -kv[1])),
    }


def search(query=None, source=None, category=None, limit=10):
    """Search skills by keyword (name/identifier/description/tags) and filters.

    Returns a list of skill dicts (length capped by `limit`; use limit=0 for all).
    """
    q = query.lower() if query else None
    src = source.lower() if source else None
    cat = category.lower() if category else None
    out = []
    for s in all_skills():
        if src and s.get("source", "").lower() != src:
            continue
        if cat and s.get("category", "").lower() != cat:
            continue
        if q:
            in_name = q in s.get("name", "").lower() or q in s.get("identifier", "").lower()
            in_desc = q in (s.get("description", "") or "").lower()
            in_tags = any(q in str(t).lower() for t in s.get("tags", []) or [])
            if not (in_name or in_desc or in_tags):
                continue
        out.append(s)
    return out if limit in (0, None) else out[:limit]


def show(name_or_id):
    """Return a single skill's metadata by exact name/identifier (or substring)."""
    key = name_or_id.lower()
    for s in all_skills():
        if s.get("name", "").lower() == key or s.get("identifier", "").lower() == key:
            return s
    for s in all_skills():
        if key in s.get("name", "").lower() or key in s.get("identifier", "").lower():
            return s
    return None


def _sanitize(name, maxlen=80):
    return (re.sub(r"[^\w\-]", "_", name).lower() or "unknown")[:maxlen]


def _partition_char(name):
    clean = re.sub(r"[^a-zA-Z0-9]", "", name)
    return clean[0].lower() if clean else "_"


def _source_slug(source):
    return re.sub(r"[^\w]", "_", source).lower()


def _community_folder(skill):
    san = _sanitize(skill.get("identifier", ""))
    return f"skills/community/{_source_slug(skill.get('source', ''))}/{_partition_char(san)}/{san}"


def _candidate_folders(skill):
    """Repo-relative folder paths to try for a skill, most-likely first."""
    source = skill.get("source", "")
    name = skill.get("name", "")
    ident = skill.get("identifier", "")
    cat = skill.get("category", "")
    if source in ("built-in", "optional"):
        base = f"skills/{source}"
        cands = []
        for leaf in (name, ident):
            if cat:
                cands.append(f"{base}/{cat}/{leaf}")
            cands.append(f"{base}/{leaf}")
        return cands
    return [_community_folder(skill)]


def content_url(skill):
    """Build the GitHub raw URL of a community skill's SKILL.md (fast path)."""
    if skill.get("source", "") in ("built-in", "optional"):
        return None
    return f"{RAW_BASE}/{_community_folder(skill)}/SKILL.md"


def _http_json(url, timeout=20):
    headers = {"User-Agent": "ra-skills/1.0", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception:
        return None


def _http_bytes(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ra-skills/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception:
        return None


def fetch_content(name_or_id, timeout=20):
    """Return a community skill's SKILL.md text (fast single-file fetch)."""
    skill = show(name_or_id)
    if not skill:
        return None
    url = content_url(skill)
    if url:
        data = _http_bytes(url, timeout)
        if data is not None:
            return data.decode("utf-8", errors="replace")
    # built-in/optional or fallback: locate the folder and read SKILL.md
    files = _list_skill_files(skill)
    for rel, dl in files:
        if rel.lower() == "skill.md":
            data = _http_bytes(dl)
            return data.decode("utf-8", errors="replace") if data is not None else None
    return None


def _list_folder(path, timeout=20):
    """List a repo folder via the GitHub contents API -> list of items or None."""
    data = _http_json(f"{GITHUB_API}/{urllib.parse.quote(path)}", timeout)
    return data if isinstance(data, list) else None


def _collect(path, root=None, depth=0):
    """Recursively yield (relpath_under_root, download_url) for files in a folder."""
    if root is None:
        root = path
    if depth > 8:
        return []
    items = _list_folder(path)
    out = []
    if not items:
        return out
    for it in items:
        full = it.get("path", "")
        rel = full[len(root):].lstrip("/")
        if it.get("type") == "file" and it.get("download_url"):
            out.append((rel, it["download_url"]))
        elif it.get("type") == "dir":
            out.extend(_collect(full, root, depth + 1))
    return out


def _list_skill_files(skill):
    """Find the skill's folder in the repo and return its file list."""
    for folder in _candidate_folders(skill):
        files = _collect(folder)
        if any(rel.lower() == "skill.md" for rel, _ in files):
            return files
    return []


def download(name_or_id, dest=".", timeout=30):
    """Download a skill's COMPLETE folder (every file) from the GitHub repo.

    Saves into <dest>/<name>/...  Returns the output directory path, or None.
    Works for any skill — community (deterministic path) and built-in/optional.
    Set GITHUB_TOKEN to raise the API rate limit.
    """
    skill = show(name_or_id)
    if not skill:
        return None
    files = _list_skill_files(skill)
    if not files:
        return None
    out_dir = os.path.join(dest, _sanitize(skill.get("name") or skill.get("identifier")))
    written = 0
    for rel, url in files:
        data = _http_bytes(url, timeout)
        if data is None:
            continue
        safe = "/".join(re.sub(r"[^\w.\-]", "_", p)[:80] for p in rel.split("/") if p not in ("", ".", ".."))
        target = os.path.join(out_dir, safe)
        os.makedirs(os.path.dirname(target) or out_dir, exist_ok=True)
        with open(target, "wb") as f:
            f.write(data)
        written += 1
    return out_dir if written else None
