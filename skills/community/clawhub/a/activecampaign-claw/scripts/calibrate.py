#!/usr/bin/env python3
"""
calibrate.py — first-run / monthly calibration for the ActiveCampaign skill.

Builds ~/.activecampaign-skill/state.json by scanning the AC account.

Captures:
  - Account taxonomy (lists, tags, custom fields, pipelines, automations)
  - Performance baselines from last 90 days of campaigns
  - Send-time patterns
  - Subject-line patterns (length, top performers)

Usage:
  python3 calibrate.py              # full calibration
  python3 calibrate.py --quick      # taxonomy only, skip baseline computation
  python3 calibrate.py --validate   # test API connection and exit

Required env:
  AC_API_URL   - https://youraccount.api-us1.com
  AC_API_TOKEN - your API token
"""

from __future__ import annotations

import statistics
import sys
from datetime import datetime, timedelta, timezone

from _ac_client import ACClient, ACClientError, sanitize, save_state, state_age_days
from _ac_client import safe_float as _safe_float


def _normalize_options(opts) -> list:
    if not opts:
        return []
    if isinstance(opts, list):
        return [sanitize(str(o)) for o in opts if o]
    if isinstance(opts, str):
        return [sanitize(o) for o in opts.split("||") if o]
    return []


def fetch_taxonomy(client: ACClient) -> dict:
    print("→ Fetching account taxonomy...")

    print("  • lists")
    lists = client.paginate("lists", "lists")

    print("  • tags")
    tags = client.paginate("tags", "tags")

    print("  • contact custom fields")
    contact_fields = client.paginate("fields", "fields")

    print("  • deal custom fields")
    try:
        deal_fields_resp = client.get("dealCustomFieldMeta")
        deal_fields = deal_fields_resp.get("dealCustomFieldMeta", [])
    except Exception:
        deal_fields = []

    print("  • deal pipelines")
    try:
        pipelines = client.paginate("dealGroups", "dealGroups", max_items=200)
    except ACClientError as e:
        if e.status_code == 403:
            print("    (Deals feature not enabled on this account — skipping)")
            pipelines = []
        else:
            raise

    print("  • deal stages")
    try:
        stages = client.paginate("dealStages", "dealStages", max_items=500)
    except ACClientError as e:
        if e.status_code == 403:
            stages = []
        else:
            raise

    for p in pipelines:
        p["stages"] = [s for s in stages if s.get("group") == p.get("id")]

    print("  • automations")
    automations = client.paginate("automations", "automations", max_items=500)

    return {
        "lists": [
            {"id": lst["id"], "name": sanitize(lst["name"]), "stringid": lst.get("stringid", "")}
            for lst in lists
        ],
        "tags": [
            {"id": t["id"], "name": sanitize(t["tag"]), "tagType": t.get("tagType", "contact")}
            for t in tags
        ],
        "custom_fields": {
            "contacts": [
                {
                    "id": f["id"],
                    "title": sanitize(f["title"]),
                    "type": f["type"],
                    "options": _normalize_options(f.get("options")),
                }
                for f in contact_fields
            ],
            "deals": [
                {
                    "id": f.get("id"),
                    "fieldLabel": sanitize(f.get("fieldLabel", "")),
                    "fieldType": f.get("fieldType"),
                }
                for f in deal_fields
            ],
        },
        "pipelines": [
            {
                "id": p["id"],
                "name": sanitize(p["title"]),
                "stages": [
                    {
                        "id": s["id"],
                        "title": sanitize(s["title"]),
                        "order": s.get("order"),
                    }
                    for s in p.get("stages", [])
                ],
            }
            for p in pipelines
        ],
        "automations": [
            {
                "id": a["id"],
                "name": sanitize(a.get("name", "")),
                "status": a.get("status"),
                "entered": a.get("entered"),
                "exited": a.get("exited"),
            }
            for a in automations
        ],
    }


def _percentile(data: list[float], p: int) -> float:
    if not data:
        return 0.0
    if len(data) == 1:
        return round(data[0], 4)
    return round(
        statistics.quantiles(sorted(data), n=100, method="inclusive")[p - 1], 4
    )


def fetch_campaign_baselines(client: ACClient) -> dict:
    print("→ Fetching last 90 days of campaign performance...")

    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    campaigns = client.paginate(
        "campaigns", "campaigns", params={"orders[sdate]": "DESC"}, max_items=200
    )

    recent = []
    for c in campaigns:
        sdate = c.get("sdate")
        if not sdate:
            continue
        try:
            sent_at = datetime.fromisoformat(sdate.replace("Z", "+00:00"))
        except Exception:
            continue
        if sent_at < cutoff:
            continue
        recent.append(c)

    if not recent:
        print("  ⚠ No campaigns sent in last 90 days. Using minimal defaults.")
        return {
            "open_rate_p50": 0.25,
            "open_rate_p90": 0.40,
            "click_rate_p50": 0.03,
            "click_rate_p90": 0.07,
            "bounce_rate_p50": 0.005,
            "unsub_rate_p50": 0.003,
            "best_send_window_utc": ["13:00", "17:00"],
            "best_send_dow": ["Tue", "Wed", "Thu"],
            "campaign_count_90d": 0,
            "_note": "Defaults — no recent campaigns to learn from",
        }

    open_rates = []
    click_rates = []
    bounce_rates = []
    unsub_rates = []
    subject_lengths = []
    subject_data = []

    for c in recent:
        sent = _safe_float(c.get("send_amt"))
        opens = _safe_float(c.get("uniqueopens"))
        clicks = _safe_float(c.get("uniquelinkclicks"))
        bounces = _safe_float(c.get("hardbounces")) + _safe_float(
            c.get("softbounces")
        )
        unsubs = _safe_float(c.get("unsubscribes"))

        if sent < 50:
            continue

        open_rates.append(opens / sent)
        click_rates.append(clicks / sent)
        bounce_rates.append(bounces / sent)
        unsub_rates.append(unsubs / sent)

        subject = sanitize(c.get("subject") or "")
        if subject:
            subject_lengths.append(len(subject))
            subject_data.append({"subject": subject, "open_rate": opens / sent})

    # best send hours by avg open rate
    hour_buckets: dict[int, list[float]] = {}
    dow_buckets: dict[str, list[float]] = {}
    for c in recent:
        sent = _safe_float(c.get("send_amt"))
        opens = _safe_float(c.get("uniqueopens"))
        if sent < 50:
            continue
        try:
            dt = datetime.fromisoformat(c.get("sdate", "").replace("Z", "+00:00"))
            rate = opens / sent
            hour_buckets.setdefault(dt.hour, []).append(rate)
            dow_buckets.setdefault(dt.strftime("%a"), []).append(rate)
        except Exception:
            continue

    hour_avgs = {
        h: statistics.mean(rs) for h, rs in hour_buckets.items() if len(rs) >= 2
    }
    top_hours = sorted(hour_avgs.items(), key=lambda x: -x[1])[:3]

    dow_avgs = {
        d: statistics.mean(rs) for d, rs in dow_buckets.items() if len(rs) >= 2
    }
    top_dows = sorted(dow_avgs.items(), key=lambda x: -x[1])[:3]

    top_subjects = sorted(subject_data, key=lambda x: -x["open_rate"])[:5]

    return {
        "open_rate_p50": _percentile(open_rates, 50),
        "open_rate_p90": _percentile(open_rates, 90),
        "click_rate_p50": _percentile(click_rates, 50),
        "click_rate_p90": _percentile(click_rates, 90),
        "bounce_rate_p50": _percentile(bounce_rates, 50),
        "unsub_rate_p50": _percentile(unsub_rates, 50),
        "best_send_window_utc": [f"{h:02d}:00" for h, _ in top_hours],
        "best_send_dow": [d for d, _ in top_dows],
        "avg_subject_line_length": (
            round(statistics.mean(subject_lengths)) if subject_lengths else 0
        ),
        "top_performing_subjects": top_subjects,
        "campaign_count_90d": len(recent),
    }


def fetch_list_growth(client: ACClient) -> dict:
    print("→ Computing list growth metrics...")

    cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    try:
        recent = client.get("contacts", {"filters[created_after]": cutoff, "limit": 1})
        new_30d = int(recent.get("meta", {}).get("total", 0))

        all_resp = client.get("contacts", {"limit": 1})
        total = int(all_resp.get("meta", {}).get("total", 0))

        return {
            "total_contacts": total,
            "new_30d": new_30d,
            "growth_rate_30d": round(new_30d / total, 4) if total else 0,
        }
    except Exception as e:
        print(f"  ⚠ Could not compute list growth: {e}")
        return {"total_contacts": 0, "new_30d": 0, "growth_rate_30d": 0}


def validate_connection(client: ACClient) -> dict:
    """Test the API connection. Returns the /users/me response or exits."""
    try:
        me = client.get("users/me")
        email = me.get("user", {}).get("email", "unknown")
        print(f"✓ Authenticated as {email}")
        return me
    except Exception as e:
        sys.stderr.write(
            f"ERROR: Authentication failed. Check AC_API_URL and AC_API_TOKEN. ({e})\n"
        )
        sys.exit(1)


_FIRST_RUN_NOTICE = """\
ActiveCampaign skill — first-time setup
========================================

This calibration will read the following from your AC account using the
token you provided:

  - List, tag, automation, custom-field, and pipeline definitions
  - 90-day campaign baselines (open/click rates, send patterns)
  - Account-level counts (no contact PII)

It will write the result to a local JSON file at:

  ~/.activecampaign-skill/state.json   (mode 0600, your user only)

Nothing is sent off your machine. The skill never transmits data to any
third party. To remove all skill-managed local state later:

  rm -rf ~/.activecampaign-skill/

See SKILL.md "Local files and data retention" for the full list of files
this skill may create.
"""


def main():
    quick = "--quick" in sys.argv
    validate_only = "--validate" in sys.argv
    client = ACClient()

    validate_connection(client)

    from _ac_client import STATE_FILE
    if not STATE_FILE.exists() and not validate_only:
        # First-time setup: show the disclosure
        print(_FIRST_RUN_NOTICE)

    if validate_only:
        print("✓ Connection valid. Ready to calibrate.")
        if STATE_FILE.exists():
            age = state_age_days()
            if age is not None:
                print(f"  State file exists ({age:.0f} days old)")
            else:
                print("  State file exists (age unknown)")
        else:
            print("  No state file yet — run without --validate to calibrate.")
        return

    base_url = client.base.replace("/api/3", "")
    host = (
        base_url.replace("https://", "").replace("http://", "").split(".")[1]
        if "." in base_url
        else "unknown"
    )

    state = {
        "schema_version": 1,
        "account": {
            "url": base_url,
            "regional_host": host,
        },
        "taxonomy": fetch_taxonomy(client),
        "last_calibrated": datetime.now(timezone.utc).isoformat(),
    }

    if not quick:
        state["baselines"] = fetch_campaign_baselines(client)
        state["list_growth"] = fetch_list_growth(client)

    save_state(state)

    print()
    print(f"✓ Wrote {state_file_path()}")

    _print_discovery_summary(state, quick)


def _print_discovery_summary(state: dict, quick: bool) -> None:
    """Print a rich account discovery summary for first-run narration."""
    tax = state["taxonomy"]
    account_url = state.get("account", {}).get("url", "")
    account_name = account_url.replace("https://", "").split(".")[0] if account_url else "your account"

    print()
    print(f"  === Account Discovery: {account_name} ===")
    print()

    lists = tax.get("lists", [])
    tags = tax.get("tags", [])
    contact_fields = tax.get("custom_fields", {}).get("contacts", [])
    deal_fields = tax.get("custom_fields", {}).get("deals", [])
    pipelines = tax.get("pipelines", [])
    automations = tax.get("automations", [])

    print("  Taxonomy:")
    print(f"    {len(lists)} list{'s' if len(lists) != 1 else ''}: {', '.join(lst['name'] for lst in lists[:5])}")
    print(f"    {len(tags)} tag{'s' if len(tags) != 1 else ''}{': ' + ', '.join(t['name'] for t in tags[:8]) if tags else ''}")
    print(f"    {len(contact_fields)} contact field{'s' if len(contact_fields) != 1 else ''}, {len(deal_fields)} deal field{'s' if len(deal_fields) != 1 else ''}")
    if pipelines:
        for p in pipelines[:3]:
            stages = p.get("stages", [])
            stage_names = " → ".join(s["title"] for s in sorted(stages, key=lambda s: s.get("order", 0)))
            print(f"    Pipeline \"{p['name']}\": {stage_names}")
    active_autos = [a for a in automations if str(a.get("status")) == "1"]
    print(f"    {len(automations)} automation{'s' if len(automations) != 1 else ''} ({len(active_autos)} active)")
    if active_autos:
        top_autos = sorted(active_autos, key=lambda a: int(a.get("entered", 0) or 0), reverse=True)[:3]
        for a in top_autos:
            entered = int(a.get("entered", 0) or 0)
            exited = int(a.get("exited", 0) or 0)
            print(f"      \"{a['name']}\" — {entered:,} entered, {exited:,} exited")

    if not quick and state.get("baselines"):
        b = state["baselines"]
        g = state.get("list_growth", {})
        print()
        print(f"  Performance (last 90 days, {b.get('campaign_count_90d', 0)} campaigns):")
        print(f"    Open rate median:  {b['open_rate_p50']*100:.1f}%  (top 10%: {b.get('open_rate_p90', 0)*100:.1f}%)")
        print(f"    Click rate median: {b['click_rate_p50']*100:.1f}%  (top 10%: {b.get('click_rate_p90', 0)*100:.1f}%)")
        if b.get("bounce_rate_p50", 0) > 0:
            print(f"    Bounce rate:       {b['bounce_rate_p50']*100:.2f}%")
        if b.get("unsub_rate_p50", 0) > 0:
            print(f"    Unsub rate:        {b['unsub_rate_p50']*100:.2f}%")
        if b.get("best_send_dow"):
            print(f"    Best send days:    {', '.join(b['best_send_dow'])}")
        if b.get("best_send_window_utc"):
            print(f"    Best send hours:   {', '.join(b['best_send_window_utc'])} UTC")
        if b.get("avg_subject_line_length"):
            print(f"    Avg subject length: {b['avg_subject_line_length']} chars")

        if g.get("total_contacts"):
            print()
            print("  List size:")
            print(f"    {g['total_contacts']:,} total contacts")
            print(f"    {g.get('new_30d', 0):,} new in last 30 days ({g.get('growth_rate_30d', 0)*100:.1f}% growth)")

        print()
        print("  Quick observations:")
        obs_count = 0
        if b["open_rate_p50"] >= 0.25:
            print(f"    ✅ Open rate is healthy ({b['open_rate_p50']*100:.1f}% — industry avg ~21%)")
            obs_count += 1
        elif b["open_rate_p50"] > 0:
            print(f"    ⚠️  Open rate ({b['open_rate_p50']*100:.1f}%) is below industry average (~21%)")
            obs_count += 1
        if b.get("unsub_rate_p50", 0) > 0.005:
            print(f"    ⚠️  Unsub rate ({b['unsub_rate_p50']*100:.2f}%) is above 0.5% threshold")
            obs_count += 1
        if g.get("growth_rate_30d", 0) > 0.03:
            print(f"    ✅ Strong list growth ({g['growth_rate_30d']*100:.1f}% in 30 days)")
            obs_count += 1
        elif g.get("growth_rate_30d", 0) > 0:
            print(f"    📊 Moderate list growth ({g['growth_rate_30d']*100:.1f}% in 30 days)")
            obs_count += 1
        if not active_autos:
            print("    💡 No active automations — a welcome series could work on autopilot")
            obs_count += 1
        if obs_count == 0:
            print("    📊 Baselines captured — ready for analysis")

    print()


def state_file_path():
    from _ac_client import STATE_FILE
    return STATE_FILE


if __name__ == "__main__":
    main()
