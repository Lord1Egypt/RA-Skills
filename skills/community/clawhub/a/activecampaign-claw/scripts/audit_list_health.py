#!/usr/bin/env python3
"""
audit_list_health.py — List health audit for ActiveCampaign.

Analyzes contacts, bounces, campaign metrics, and domain distribution
to produce a markdown health report with actionable recommendations.

Usage:
  python3 audit_list_health.py                # markdown to stdout
  python3 audit_list_health.py --format json  # JSON output
  python3 audit_list_health.py --output report.md

Required: ~/.activecampaign-skill/state.json (run calibrate.py first)
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from _ac_client import (
    ACClient,
    compare_to_previous,
    detect_patterns,
    emit_files,
    ensure_state,
    load_history,
    log_outcome,
    sanitize,
    write_insight,
    write_report,
)


def collect_domain_distribution(client: ACClient, sample_size: int = 500) -> dict:
    contacts = client.paginate("contacts", "contacts", max_items=sample_size)
    domains: Counter = Counter()
    for c in contacts:
        email = c.get("email", "")
        if "@" in email:
            domain = sanitize(email.split("@")[1].lower(), max_len=253)
            domains[domain] += 1
    total = sum(domains.values())
    if total == 0:
        return {"domains": {}, "total_sampled": 0, "concentration_risk": None}

    top_domains = domains.most_common(10)
    distribution = {d: {"count": n, "pct": round(n / total, 4)} for d, n in top_domains}
    top_domain, top_count = top_domains[0] if top_domains else ("", 0)
    concentration_risk = (
        {"domain": top_domain, "pct": round(top_count / total, 4)}
        if top_count / total > 0.40
        else None
    )

    return {
        "domains": distribution,
        "total_sampled": total,
        "concentration_risk": concentration_risk,
    }


def collect_bounce_data(client: ACClient, contact_ids: list[str]) -> dict:
    hard_bounces = 0
    soft_bounces = 0
    multi_bounce_contacts = []

    for cid in contact_ids[:200]:
        try:
            resp = client.get(f"contacts/{cid}/bounceLogs")
            logs = resp.get("bounceLogs", [])
            if not logs:
                continue
            for bl in logs:
                if bl.get("bouncetype") == "hard":
                    hard_bounces += 1
                else:
                    soft_bounces += 1
            if len(logs) >= 3:
                multi_bounce_contacts.append(cid)
        except Exception:
            continue

    return {
        "hard_bounces": hard_bounces,
        "soft_bounces": soft_bounces,
        "multi_bounce_contacts": multi_bounce_contacts,
    }


def collect_campaign_health(client: ACClient) -> dict:
    campaigns = client.paginate(
        "campaigns", "campaigns", params={"orders[sdate]": "DESC"}, max_items=10
    )
    results = []
    for c in campaigns:
        sent = float(c.get("send_amt", 0) or 0)
        if sent < 50:
            continue
        opens = float(c.get("uniqueopens", 0) or 0)
        clicks = float(c.get("uniquelinkclicks", 0) or 0)
        bounces = float(c.get("hardbounces", 0) or 0) + float(
            c.get("softbounces", 0) or 0
        )
        unsubs = float(c.get("unsubscribes", 0) or 0)
        results.append({
            "name": sanitize(c.get("name", "Untitled")),
            "sent": int(sent),
            "open_rate": round(opens / sent, 4),
            "click_rate": round(clicks / sent, 4),
            "bounce_rate": round(bounces / sent, 4),
            "unsub_rate": round(unsubs / sent, 4),
        })
    return {"recent_campaigns": results}


def generate_report(state: dict, domains: dict, bounces: dict,
                    campaign_health: dict) -> dict:
    baselines = state.get("baselines", {})
    growth = state.get("list_growth", {})

    total = growth.get("total_contacts", 0)
    new_30d = growth.get("new_30d", 0)
    growth_rate = growth.get("growth_rate_30d", 0)

    baseline_open = baselines.get("open_rate_p50", 0.25)

    recent = campaign_health.get("recent_campaigns", [])
    avg_open = (
        sum(c["open_rate"] for c in recent) / len(recent) if recent else 0
    )
    avg_unsub = (
        sum(c["unsub_rate"] for c in recent) / len(recent) if recent else 0
    )

    risks = []
    if avg_open < baseline_open * 0.85 and recent:
        risks.append(
            f"Open rate ({avg_open*100:.1f}%) is significantly below "
            f"your baseline ({baseline_open*100:.1f}%). "
            "Check recent subject lines and audience targeting."
        )
    if avg_unsub > 0.005 and recent:
        risks.append(
            f"Unsubscribe rate ({avg_unsub*100:.2f}%) is above 0.5% threshold. "
            "Review send frequency and content relevance."
        )
    if domains.get("concentration_risk"):
        cr = domains["concentration_risk"]
        risks.append(
            f"Domain concentration: {cr['domain']} represents "
            f"{cr['pct']*100:.0f}% of your list. "
            "Single-domain concentration above 40% is a deliverability risk."
        )
    if bounces["hard_bounces"] > 10:
        risks.append(
            f"{bounces['hard_bounces']} hard bounces detected. "
            "Suppress these contacts to protect sender reputation."
        )

    actions = []
    if bounces["hard_bounces"] > 0 or bounces["multi_bounce_contacts"]:
        suppress_count = bounces["hard_bounces"] + len(bounces["multi_bounce_contacts"])
        actions.append(
            f"Suppress {suppress_count} bounced contacts "
            "(tag with auto-suppress-YYYY-MM)"
        )
    if avg_open < baseline_open * 0.85 and recent:
        actions.append(
            "Investigate open rate decline — compare recent vs. "
            "top-performing subject lines from state.json"
        )
    if domains.get("concentration_risk"):
        actions.append("Diversify list sources to reduce domain concentration risk")
    if avg_unsub > 0.005 and recent:
        actions.append(
            "Reduce send frequency or tighten audience to engaged contacts"
        )

    return {
        "headline": {
            "total_contacts": total,
            "new_30d": new_30d,
            "growth_rate_30d": growth_rate,
            "avg_open_rate": round(avg_open, 4),
            "baseline_open_rate": baseline_open,
            "avg_unsub_rate": round(avg_unsub, 4),
            "hard_bounces": bounces["hard_bounces"],
            "soft_bounces": bounces["soft_bounces"],
        },
        "domain_distribution": domains["domains"],
        "concentration_risk": domains.get("concentration_risk"),
        "suppression_candidates": {
            "hard_bounced": bounces["hard_bounces"],
            "multi_bounce_contacts": len(bounces["multi_bounce_contacts"]),
        },
        "recent_campaigns": recent,
        "risks": risks,
        "actions": actions,
    }


def format_markdown(report: dict, account_url: str) -> str:
    h = report["headline"]
    lines = []

    lines.append("## Headline metrics\n")
    lines.append("| Metric | Value | Baseline | Status |")
    lines.append("|---|---|---|---|")
    lines.append(
        f"| Total contacts | {h['total_contacts']:,} | — | — |"
    )
    lines.append(
        f"| New (30d) | {h['new_30d']:,} | — | "
        f"{h['growth_rate_30d']*100:.1f}% growth |"
    )

    open_status = "✅" if h["avg_open_rate"] >= h["baseline_open_rate"] * 0.85 else "⚠️ Below"
    lines.append(
        f"| Open rate (recent) | {h['avg_open_rate']*100:.1f}% | "
        f"{h['baseline_open_rate']*100:.1f}% | {open_status} |"
    )

    unsub_status = "✅" if h["avg_unsub_rate"] <= 0.005 else "⚠️ High"
    lines.append(
        f"| Unsub rate (recent) | {h['avg_unsub_rate']*100:.2f}% | "
        f"<0.50% | {unsub_status} |"
    )
    lines.append(
        f"| Hard bounces | {h['hard_bounces']} | — | "
        f"{'✅' if h['hard_bounces'] < 10 else '⚠️'} |"
    )

    if report["risks"]:
        lines.append("\n## Risk flags\n")
        for r in report["risks"]:
            lines.append(f"⚠️ **{r}**\n")

    if report["domain_distribution"]:
        lines.append("\n## Domain distribution (top 10)\n")
        lines.append("| Domain | Count | % |")
        lines.append("|---|---|---|")
        for domain, data in report["domain_distribution"].items():
            lines.append(f"| {domain} | {data['count']:,} | {data['pct']*100:.1f}% |")

    if report["suppression_candidates"]["hard_bounced"] > 0 or \
       report["suppression_candidates"]["multi_bounce_contacts"] > 0:
        lines.append("\n## Suppression candidates\n")
        sc = report["suppression_candidates"]
        if sc["hard_bounced"] > 0:
            lines.append(f"- {sc['hard_bounced']} contacts with hard bounces → suppress immediately")
        if sc["multi_bounce_contacts"] > 0:
            lines.append(f"- {sc['multi_bounce_contacts']} contacts with 3+ bounce entries → suppress")

    if report["recent_campaigns"]:
        lines.append("\n## Recent campaign performance\n")
        lines.append("| Campaign | Sent | Open rate | Click rate | Unsub rate |")
        lines.append("|---|---|---|---|---|")
        for c in report["recent_campaigns"][:5]:
            lines.append(
                f"| {c['name']} | {c['sent']:,} | "
                f"{c['open_rate']*100:.1f}% | {c['click_rate']*100:.1f}% | "
                f"{c['unsub_rate']*100:.2f}% |"
            )

    if report["actions"]:
        lines.append("\n## Recommended actions\n")
        for i, a in enumerate(report["actions"], 1):
            lines.append(f"{i}. {a}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="List health audit")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    state = ensure_state()
    client = ACClient()

    print("→ Collecting domain distribution...", file=sys.stderr)
    domains = collect_domain_distribution(client)

    print("→ Collecting bounce data...", file=sys.stderr)
    contacts = client.paginate("contacts", "contacts", max_items=200)
    contact_ids = [c["id"] for c in contacts]
    bounces = collect_bounce_data(client, contact_ids)

    print("→ Collecting campaign metrics...", file=sys.stderr)
    campaign_health = collect_campaign_health(client)

    report = generate_report(state, domains, bounces, campaign_health)

    account_url = state.get("account", {}).get("url", "unknown")

    current_metrics = {
        "total_contacts": report["headline"]["total_contacts"],
        "hard_bounces": report["headline"]["hard_bounces"],
        "risks_count": len(report["risks"]),
        "actions_count": len(report["actions"]),
    }

    if args.format == "json":
        output = json.dumps(report, indent=2)
    else:
        title = f"List Health Audit — {account_url.replace('https://', '')}"
        content = format_markdown(report, account_url)
        trends = compare_to_previous(
            "list-health-audit", current_metrics,
            ["total_contacts", "hard_bounces", "risks_count"],
        )
        if trends:
            content += "\n\n" + trends
        patterns = detect_patterns()
        if patterns:
            content += "\n\n## Proactive suggestions\n"
            for p in patterns:
                content += f"\n- {p}"
            content += "\n"
        output = write_report(title, content)

    if args.output:
        Path(args.output).write_text(output)
        print(f"✓ Report written to {args.output}", file=sys.stderr)
        emit_files(args.output)
    else:
        print(output)

    if report["headline"]["hard_bounces"] > 20:
        write_insight(
            f"Hard bounce count ({report['headline']['hard_bounces']}) exceeds 20. "
            f"Immediate suppression recommended to protect sender reputation.",
            category="risk",
        )
    history = load_history(recipe="list-health-audit", limit=3)
    if len(history) >= 3:
        risk_counts = [h.get("risks_count", 0) for h in history[:3]]
        if all(isinstance(v, (int, float)) for v in risk_counts):
            if risk_counts[0] > risk_counts[1] > risk_counts[2]:
                write_insight(
                    f"Risk flag count increasing 3 runs in a row: "
                    f"{risk_counts[2]} → {risk_counts[1]} → {risk_counts[0]}. "
                    f"List health is deteriorating.",
                    category="trend",
                )

    log_outcome(
        "audit_executed",
        recipe="list-health-audit",
        total_contacts=report["headline"]["total_contacts"],
        hard_bounces=report["headline"]["hard_bounces"],
        risks_count=len(report["risks"]),
        actions_count=len(report["actions"]),
    )


if __name__ == "__main__":
    main()
