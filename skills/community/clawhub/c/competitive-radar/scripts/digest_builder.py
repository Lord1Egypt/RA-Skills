#!/usr/bin/env python3
"""
digest_builder.py — Assembles the weekly competitor digest.

Reads results from scrape, diff, jobs, and github_tracker outputs,
then builds a structured Markdown + JSON digest for delivery.

Usage:
  python3 digest_builder.py <slug>          # single competitor
  python3 digest_builder.py --all           # all active competitors
"""

from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
DIGESTS_DIR = DATA_DIR / "digests"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
JOBS_DIR = DATA_DIR / "jobs"
COMPETITORS_FILE = DATA_DIR / "competitors.json"

TODAY = date.today().isoformat()
SCRIPTS_DIR = SKILL_DIR / "scripts"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_competitors() -> dict:
    if not COMPETITORS_FILE.exists():
        return {"competitors": []}
    return json.loads(COMPETITORS_FILE.read_text())


def get_active_competitors() -> list[dict]:
    return [c for c in load_competitors()["competitors"] if c.get("active", True)]


def get_competitor(slug: str) -> dict | None:
    return next((c for c in get_active_competitors() if c["slug"] == slug), None)


def run_script(script: str, *args) -> dict | list | None:
    """Run a sibling script and return its JSON stdout."""
    cmd = ["python3", str(SCRIPTS_DIR / script)] + list(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"[digest] {script} exited {result.returncode}: {result.stderr[:200]}",
                  file=sys.stderr)
            return None
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"[digest] {script} returned non-JSON output", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[digest] Error running {script}: {e}", file=sys.stderr)
        return None


def latest_jobs_snapshot(slug: str) -> list[dict]:
    d = JOBS_DIR / slug
    if not d.exists():
        return []
    files = sorted(d.glob("jobs_*.json"), reverse=True)
    if not files:
        return []
    try:
        return json.loads(files[0].read_text())
    except Exception:
        return []


def latest_rss_posts(slug: str) -> list[dict]:
    d = SNAPSHOTS_DIR / slug
    if not d.exists():
        return []
    files = sorted(d.glob("rss_posts_*.json"), reverse=True)
    if not files:
        return []
    try:
        return json.loads(files[0].read_text())
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Signal-level emoji + label helpers
# ---------------------------------------------------------------------------

LEVEL_EMOJI = {
    "HIGH": "🔴",
    "MEDIUM": "🟡",
    "LOW": "🟢",
    "NONE": "⚪",
}


def signal_emoji(level: str) -> str:
    return LEVEL_EMOJI.get(level, "⚪")


# ---------------------------------------------------------------------------
# Per-competitor digest section builder
# ---------------------------------------------------------------------------

def build_competitor_section(
    slug: str,
    diff_result: dict,
    jobs_result: dict,
    github_result: dict | None,
    rss_posts: list[dict],
) -> str:
    """Build the Markdown section for one competitor."""
    name = diff_result.get("name", slug.replace("-", " ").title())
    lines: list[str] = []

    lines.append(f"\n━━ {name.upper()} {'━' * max(0, 38 - len(name))}\n")

    has_anything = False

    # --- Pricing ---
    pricing = diff_result.get("signals", {}).get("pricing", {})
    if pricing.get("changed"):
        has_anything = True
        emoji = signal_emoji("HIGH")
        lines.append(f"💰 PRICING  {emoji} [CHANGED]")
        for plan in pricing.get("removed_plans", []):
            lines.append(f"  → Removed plan: {plan.title()}")
        for plan in pricing.get("added_plans", []):
            lines.append(f"  → New plan: {plan.title()}")
        for price in pricing.get("new_price_points", []):
            lines.append(f"  → New price point: ${price}")
        for price in pricing.get("removed_price_points", []):
            lines.append(f"  → Removed price: ${price}")
        if pricing.get("word_change_pct", 0) > 15:
            lines.append(f"  → Overall page changed significantly "
                         f"({pricing['word_change_pct']}% of words differ)")
        # The LLM prompt is embedded here — OpenClaw agent will expand it
        if pricing.get("llm_prompt"):
            lines.append(f"\n  [AGENT: {pricing['llm_prompt'][:300]}]")
        lines.append("")
    elif pricing.get("note") != "first_run_no_baseline":
        lines.append("💰 PRICING  ⚪ [no change]")
        lines.append("")

    # --- Homepage positioning ---
    hero = diff_result.get("signals", {}).get("homepage_hero", {})
    if hero.get("changed"):
        has_anything = True
        lines.append(f"🏠 POSITIONING  {signal_emoji('MEDIUM')} [CHANGED]")
        lines.append(f"  Old: {hero.get('old_hero', '')[:120]}")
        lines.append(f"  New: {hero.get('new_hero', '')[:120]}")
        if hero.get("llm_prompt"):
            lines.append(f"\n  [AGENT: {hero['llm_prompt'][:300]}]")
        lines.append("")

    # --- Blog / RSS posts ---
    if rss_posts:
        has_anything = True
        lines.append(f"📝 CONTENT  🟡 [{len(rss_posts)} new post{'s' if len(rss_posts) != 1 else ''}]")
        for post in rss_posts[:4]:
            title = post.get("title", "untitled")
            pub = post.get("published", "")[:10] if post.get("published") else ""
            summary = post.get("summary", "")[:150].replace("\n", " ")
            date_str = f" ({pub})" if pub else ""
            lines.append(f"  → \"{title}\"{date_str}")
            if summary:
                lines.append(f"    {summary}")
        lines.append("")

    # --- Jobs ---
    if jobs_result.get("new_roles_this_week", 0) > 0:
        has_anything = True
        new_count = jobs_result["new_roles_this_week"]
        lines.append(f"👷 HIRING  🟡 [+{new_count} new role{'s' if new_count != 1 else ''} vs last week]")
        for role in jobs_result.get("new_roles", [])[:8]:
            loc = role.get("location", "")
            loc_str = f" ({loc})" if loc else ""
            lines.append(f"  → {role['title']}{loc_str}")
        signals = jobs_result.get("signal_summary", {}).get("signals", [])
        if signals:
            lines.append("  Signal:")
            for sig in signals[:3]:
                lines.append(f"    • {sig['category']} ({sig['role_count']} roles): "
                              f"{sig['interpretation']}")
        lines.append("")

    # --- GitHub ---
    if github_result and not github_result.get("skipped") and not github_result.get("error"):
        delta = github_result.get("star_delta_week", 0)
        releases = github_result.get("new_releases", [])
        new_repos = github_result.get("new_repos_this_week", [])

        if delta != 0 or releases or new_repos:
            has_anything = True
            delta_str = f"{'+' if delta >= 0 else ''}{delta:,}"
            total_str = f"{github_result.get('total_stars', 0):,}"
            lines.append(f"⭐ GITHUB  [{total_str} stars | {delta_str} this week]")

            for release in releases[:3]:
                lines.append(f"  → Release {release.get('tag', '')} "
                              f"({release.get('repo', '')}): "
                              f"{release.get('name', '')}")
                body_preview = release.get("body", "")[:120].replace("\n", " ")
                if body_preview:
                    lines.append(f"    {body_preview}")

            for repo in new_repos[:3]:
                lines.append(f"  → New repo: {repo.get('name', '')} — "
                              f"{repo.get('description', '')[:80]}")
            lines.append("")

    if not has_anything:
        lines.append("  No significant changes this week.")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Cross-competitor summary
# ---------------------------------------------------------------------------

def build_summary_section(competitor_data: list[dict]) -> str:
    lines = ["\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
             "📊 SUMMARY ACROSS ALL COMPETITORS\n"]

    # Pricing changes
    pricing_changers = [
        d["name"] for d in competitor_data
        if d.get("diff", {}).get("signals", {}).get("pricing", {}).get("changed")
    ]
    if pricing_changers:
        lines.append(f"  → Pricing changed: {', '.join(pricing_changers)}")

    # Hiring leaders
    hiring = sorted(
        competitor_data,
        key=lambda d: d.get("jobs", {}).get("new_roles_this_week", 0),
        reverse=True
    )
    if hiring and hiring[0].get("jobs", {}).get("new_roles_this_week", 0) > 0:
        top_hirer = hiring[0]
        lines.append(
            f"  → Most active hiring: {top_hirer['name']} "
            f"(+{top_hirer['jobs'].get('new_roles_this_week', 0)} roles)"
        )

    # GitHub growth
    gh_data = [d for d in competitor_data
               if d.get("github") and not d["github"].get("skipped")]
    if gh_data:
        top_gh = max(gh_data, key=lambda d: d["github"].get("star_delta_week", 0))
        delta = top_gh["github"].get("star_delta_week", 0)
        if delta > 0:
            lines.append(
                f"  → Fastest GitHub growth: {top_gh['name']} "
                f"(+{delta:,} stars this week)"
            )

    if len(lines) == 2:
        lines.append("  → No standout signals across competitors this week.")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Full digest builder
# ---------------------------------------------------------------------------

def build_digest_for_competitor(slug: str) -> dict:
    """Run all signal collectors and return raw data dict for one competitor."""
    competitor = get_competitor(slug)
    if not competitor:
        return {"error": f"Competitor '{slug}' not found"}

    print(f"[digest] Building signals for {competitor['name']}...")

    # Run scrape
    run_script("scrape.py", "--weekly", slug)

    # Run diff
    diff_output = run_script("diff.py", slug)
    diff_result = diff_output[0] if isinstance(diff_output, list) else (diff_output or {})

    # Run jobs
    jobs_output = run_script("jobs.py", slug)
    jobs_result = jobs_output[0] if isinstance(jobs_output, list) else (jobs_output or {})

    # Run github
    github_output = run_script("github_tracker.py", slug)
    github_result = (
        github_output[0] if isinstance(github_output, list) else (github_output or {})
    )

    # Read RSS posts from snapshot (scrape already ran)
    rss_posts = latest_rss_posts(slug)

    return {
        "slug": slug,
        "name": competitor["name"],
        "diff": diff_result,
        "jobs": jobs_result,
        "github": github_result,
        "rss_posts": rss_posts,
    }


def build_full_digest(slugs: list[str]) -> str:
    """Build the full weekly digest Markdown for all given slugs."""
    all_data = [build_digest_for_competitor(s) for s in slugs]

    header = (
        f"🦞 Competitor Radar — Week of {TODAY}\n"
        f"{'═' * 42}\n"
        f"Tracking {len(all_data)} competitor{'s' if len(all_data) != 1 else ''}\n"
    )

    sections = [header]
    for d in all_data:
        if d.get("error"):
            sections.append(f"\n━━ {d.get('slug', 'unknown').upper()} — ERROR: {d['error']}\n")
            continue
        section = build_competitor_section(
            slug=d["slug"],
            diff_result=d.get("diff", {}),
            jobs_result=d.get("jobs", {}),
            github_result=d.get("github"),
            rss_posts=d.get("rss_posts", []),
        )
        sections.append(section)

    sections.append(build_summary_section(all_data))

    digest = "\n".join(sections)

    # Save to digests archive
    DIGESTS_DIR.mkdir(parents=True, exist_ok=True)
    digest_file = DIGESTS_DIR / f"{TODAY}.md"
    digest_file.write_text(digest, encoding="utf-8")
    print(f"[digest] Saved to {digest_file}")

    # Also save raw data as JSON for programmatic use
    data_file = DIGESTS_DIR / f"{TODAY}.json"
    data_file.write_text(json.dumps(all_data, indent=2, default=str), encoding="utf-8")

    return digest


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="competitor-radar digest builder")
    parser.add_argument("slug", nargs="?", help="Competitor slug")
    parser.add_argument("--all", action="store_true", help="Run for all competitors")
    args = parser.parse_args()

    competitors = get_active_competitors()
    if args.all:
        slugs = [c["slug"] for c in competitors]
    elif args.slug:
        slugs = [args.slug]
    else:
        parser.print_help()
        sys.exit(1)

    if not slugs:
        print("[digest] No active competitors found. Add one with /competitor-radar setup")
        sys.exit(0)

    digest = build_full_digest(slugs)
    print("\n" + "=" * 42)
    print(digest)


if __name__ == "__main__":
    main()
