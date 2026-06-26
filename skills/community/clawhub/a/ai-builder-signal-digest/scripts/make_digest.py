#!/usr/bin/env python3
"""Make a short, sourced, transparent AI builder signal digest.

Inputs:
- JSONL log with fields like: title, canonical_url, category, day_et, notes/why_edge
- Or a direct list of links.

Outputs:
- Markdown digest with 3–5 items; each item includes: what, why care, maturity, link.

No external deps.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request


def eprint(*a):
    print(*a, file=sys.stderr)


def parse_date(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def is_github(url: str) -> bool:
    return url.startswith("https://github.com/") or url.startswith("http://github.com/")


def github_repo_from_url(url: str) -> str | None:
    # https://github.com/owner/repo[/...]
    try:
        u = urllib.parse.urlparse(url)
    except Exception:
        return None
    if u.netloc not in ("github.com", "www.github.com"):
        return None
    parts = [p for p in u.path.split("/") if p]
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1]
    # Strip .git
    repo = repo[:-4] if repo.endswith(".git") else repo
    return f"{owner}/{repo}"


def fetch_github_repo_info(repo: str, timeout_s: int = 10) -> tuple[int | None, int | None, str | None, str | None]:
    """Return (stars, forks, description, err). Unauthenticated; may rate-limit."""
    api = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(
        api,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "ai-builder-signal-digest/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        stars = data.get("stargazers_count")
        forks = data.get("forks_count")
        desc = data.get("description")
        return (int(stars) if stars is not None else 0,
                int(forks) if forks is not None else 0,
                (desc.strip() if isinstance(desc, str) else ""),
                None)
    except urllib.error.HTTPError as e:
        return None, None, None, f"HTTP {e.code}"
    except Exception as e:
        return None, None, None, str(e)


def summarize_arxiv_abstract(url: str, timeout_s: int = 10) -> str | None:
    """Best-effort: fetch arXiv abs page and extract the first 1–2 sentences of abstract."""
    # Keep very lightweight; regex over HTML.
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ai-builder-signal-digest/1.0"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None

    m = re.search(r"<blockquote class=\"abstract\">\s*<span[^>]*>Abstract:</span>(.*?)</blockquote>", html, re.S)
    if not m:
        return None
    # Strip tags
    abstract = re.sub(r"<[^>]+>", " ", m.group(1))
    abstract = re.sub(r"\s+", " ", abstract).strip()
    if not abstract:
        return None
    # First 1–2 sentences (naive).
    sentences = re.split(r"(?<=[.!?])\s+", abstract)
    out = " ".join(sentences[:2]).strip()
    return out


def why_care_from_record(rec: dict) -> str | None:
    # Prefer notes/why_edge-like fields from the log.
    for k in ("notes", "why_edge", "summary", "reason", "why"):
        v = rec.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def load_candidates(path: str) -> list[dict]:
    out: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def pick_items(records: list[dict], since: dt.date | None, until: dt.date | None, category: str | None, top: int) -> list[dict]:
    filtered: list[dict] = []
    for r in records:
        day = r.get("day_et")
        if isinstance(day, str):
            try:
                d = parse_date(day)
            except Exception:
                d = None
        else:
            d = None

        if since and d and d < since:
            continue
        if until and d and d > until:
            continue
        if category and r.get("category") != category:
            continue

        url = r.get("canonical_url")
        title = r.get("title")
        if not isinstance(url, str) or not url.startswith("http"):
            continue
        if not isinstance(title, str) or not title.strip():
            continue

        filtered.append(r)

    # Sort by score desc if present; else stable.
    def score_key(x: dict):
        s = x.get("score")
        try:
            return float(s)
        except Exception:
            return -1.0

    filtered.sort(key=score_key, reverse=True)
    return filtered[:top]


def format_digest(items: list[dict], title: str) -> str:
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")

    for i, it in enumerate(items, start=1):
        name = it.get("title", "").strip()
        url = it.get("canonical_url", "").strip()
        why = it.get("_why_care") or ""
        maturity = it.get("_maturity") or ""

        lines.append(f"{i}) **{name}**")
        if why:
            lines.append(f"- Why care: {why}")
        if maturity:
            lines.append(f"- Maturity: {maturity}")
        lines.append(f"- Link: {url}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="Path to JSONL log")
    ap.add_argument("--since", help="YYYY-MM-DD (inclusive)")
    ap.add_argument("--until", help="YYYY-MM-DD (inclusive)")
    ap.add_argument("--category", help="Exact category match")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--title", default="AI Builder Signal Digest")
    ap.add_argument("--links", nargs="*", help="Direct links (GitHub/arXiv/etc)")
    ap.add_argument("--out", help="Write output markdown to this path; else stdout")
    args = ap.parse_args()

    if not args.input and not args.links:
        ap.error("Provide --input or --links")

    since = parse_date(args.since) if args.since else None
    until = parse_date(args.until) if args.until else None

    items: list[dict] = []

    if args.links:
        for u in args.links:
            items.append({"title": u, "canonical_url": u})
    else:
        recs = load_candidates(args.input)
        items = pick_items(recs, since, until, args.category, args.top)

    # Enrich each item with why-care and maturity.
    for it in items:
        url = it.get("canonical_url")
        title = it.get("title")
        if not isinstance(url, str):
            continue

        # why-care
        why = why_care_from_record(it)

        gh_desc: str | None = None
        if not why and is_github(url):
            repo = github_repo_from_url(url)
            if repo:
                stars, forks, desc, err = fetch_github_repo_info(repo)
                # stash stats for maturity step to avoid a second call
                it["_gh_stars"], it["_gh_forks"], it["_gh_desc"], it["_gh_err"] = stars, forks, desc, err
                if desc:
                    gh_desc = desc
                    why = desc

        if not why and "arxiv.org/abs/" in url:
            abs_sum = summarize_arxiv_abstract(url)
            if abs_sum:
                why = abs_sum
        if why:
            # Keep as one sentence-ish.
            why = why.strip()
            why = re.sub(r"\s+", " ", why)
            if len(why) > 240:
                why = why[:237].rstrip() + "…"
        it["_why_care"] = why or ""

        # maturity
        maturity = ""
        if is_github(url):
            repo = github_repo_from_url(url)
            if repo:
                stars = it.get("_gh_stars")
                forks = it.get("_gh_forks")
                err = it.get("_gh_err")
                if stars is None or forks is None:
                    stars, forks, desc, err2 = fetch_github_repo_info(repo)
                    err = err or err2
                if stars is not None and forks is not None:
                    maturity = f"GitHub repo (~{stars}★, {forks} forks)."
                    if stars <= 5:
                        maturity += " Very early adoption; treat as a reference implementation."
                else:
                    maturity = f"GitHub stats unavailable ({err or 'blocked'})."
            else:
                maturity = "GitHub link (repo not parsed)."
        elif "arxiv.org/abs/" in url:
            maturity = "Paper (arXiv). Validate claims against your stack before adopting."
        else:
            maturity = "Primary source linked. Adoption unknown."

        it["_maturity"] = maturity

        # title normalization for --links mode
        if args.links and isinstance(title, str) and title == url:
            # If a GitHub repo, use owner/repo; if arXiv, use arXiv id.
            if is_github(url):
                repo = github_repo_from_url(url)
                if repo:
                    it["title"] = repo
            elif "arxiv.org/abs/" in url:
                it["title"] = url.split("/abs/")[-1]

    md = format_digest(items, args.title)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
    else:
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
