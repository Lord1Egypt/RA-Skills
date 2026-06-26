"""
Reference implementation of format_report() for anthropic-report.py.

Requires these imports and functions to exist in the target script:
- datetime, timezone, timedelta (from datetime)
- CET timezone
- get_pricing(model) function
- aggregate() must populate stats["cli_potential"] list
"""

CLI_THRESHOLD = 500

# Language strings — edit this dict to localize
LANG = {
    "total":         "Total",
    "calls":         "calls",
    "errors":        "errors",
    "cache":         "cache",
    "tokens":        "Tokens",
    "cost":          "Cost",
    "total_est":     "Total estimate",
    "cli_potential": "CLI potential",
    "inline_work":   "inline work",
    "standard":      "standard",
    "heartbeat":     "heartbeat",
    "no_calls":      "No API calls today.",
    "no_inline":     "No inline work",
}

L = LANG  # shorthand


def format_report(date_str: str, stats: dict) -> str:
    now = datetime.now(CET).strftime("%H:%M")
    lines = [
        f"Anthropic Usage — {date_str} ({now} CET)",
        f"{'═' * 42}",
    ]

    if stats["total_calls"] == 0:
        lines.append(L["no_calls"])
        return "\n".join(lines)

    # ── Summary ──
    total_api = sum(s["gw"]["calls"] for s in stats["agents"].values())
    total_cli = sum(s["cli"]["calls"] for s in stats["agents"].values())
    total = total_api + total_cli
    cli_pct = round(total_cli / total * 100) if total else 0
    api_pct = 100 - cli_pct
    cli_icon = "✅" if cli_pct >= 50 else "⚠️"

    lines.append(f"{L['total']}: {stats['total_calls']} {L['calls']} ({stats['err']} {L['errors']})")
    lines.append(f"{cli_icon} CLI: {cli_pct}% / API: {api_pct}%")

    # Error breakdown only when errors exist
    if stats["err"] > 0:
        ok_api = sum(s["gw"]["ok"] for s in stats["agents"].values())
        ok_cli = sum(s["cli"]["ok"] for s in stats["agents"].values())
        err_api = sum(s["gw"]["err"] for s in stats["agents"].values())
        err_cli = sum(s["cli"]["err"] for s in stats["agents"].values())
        lines.append(
            f"   API: {total_api} ({ok_api} ok, {err_api} {L['errors']})"
            f" | CLI: {total_cli} ({ok_cli} ok, {err_cli} {L['errors']})"
        )

    total_cost = 0.0

    # ── Per-agent ──
    for agent, sources in sorted(stats["agents"].items()):
        lines.append(f"{agent}:")

        raw_input = 0
        total_output = 0
        total_cache_r = 0
        total_cache_c = 0

        for src_name in ("gw", "cli"):
            s = sources[src_name]
            if s["ok"] > 0:
                raw_input += s["input_tokens"]
                total_output += s["output_tokens"]
                total_cache_r += s["cache_read"]
                total_cache_c += s["cache_create"]

        total_input = raw_input + total_cache_r + total_cache_c

        # Cache (emphasized with icon)
        if total_input > 0:
            cache_pct = round(total_cache_r / total_input * 100, 1)
            lines.append(
                f"  🗄️ {cache_pct}% {L['cache']}"
                f" ({total_cache_r:,} read / {total_cache_c:,} create)"
            )
        else:
            lines.append(f"  🗄️ 0% {L['cache']}")

        # Tokens
        lines.append(
            f"  {L['tokens']}: {total_input:,} in ({raw_input:,} new) / {total_output:,} out"
        )

        # Cost
        p = get_pricing("default")
        cost = (
            raw_input / 1_000_000 * p["input"]
            + total_output / 1_000_000 * p["output"]
            + total_cache_r / 1_000_000 * p["cache_read"]
            + total_cache_c / 1_000_000 * p["cache_create"]
        )
        total_cost += cost
        lines.append(f"  {L['cost']}: ~${cost:.4f}")

    lines.append("──────────────────────────────────────────")

    # ── CLI potential (most important first) ──
    cli_pot = stats.get("cli_potential", [])
    if cli_pot:
        high_output = [
            c for c in cli_pot
            if c["output_tokens"] >= CLI_THRESHOLD and c["ok"]
        ]
        mid = [
            c for c in cli_pot
            if 20 <= c["output_tokens"] < CLI_THRESHOLD and c["ok"]
        ]
        idle = [c for c in cli_pot if c["output_tokens"] < 20]

        lines.append(f"{L['cli_potential']}:")
        if high_output:
            total_high_tok = sum(c["output_tokens"] for c in high_output)
            max_out = max(c["output_tokens"] for c in high_output)
            lines.append(
                f"  ⚠️ {len(high_output)}× {L['inline_work']}"
                f" (>{CLI_THRESHOLD} out, {total_high_tok:,} tok, max {max_out})"
            )
        else:
            lines.append(f"  ✅ {L['no_inline']}")
        lines.append(f"  {len(mid)}× {L['standard']} (20-{CLI_THRESHOLD} out)")
        lines.append(f"  {len(idle)}× {L['heartbeat']} (<20 out)")
        lines.append("──────────────────────────────────────────")

    # ── Models (only if multiple) ──
    if len(stats.get("models", {})) > 1:
        model_parts = [
            f"{m} ({c}×)"
            for m, c in sorted(stats["models"].items(), key=lambda x: -x[1])
        ]
        lines.append(f"🧠 {', '.join(model_parts)}")

    lines.append(f"{L['total_est']}: ~${total_cost:.4f}")

    return "\n".join(lines)
