import argparse
import subprocess
import json
import sys
import os
import datetime

def run_command(cmd, env=None):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Error executing command: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Run eonik Creative Audit Pipeline")
    parser.add_argument("--config", required=True, help="Path to config.json")
    args = parser.parse_args()

    # Load config to get account_id and days
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Failed to load config: {e}", file=sys.stderr)
        sys.exit(1)

    account_id = config.get("meta", {}).get("account_id")
    days = config.get("meta", {}).get("evaluation_days", 30)
    redact = config.get("meta", {}).get("redact_sensitive", True)
    allow_auto_resolve_account = config.get("meta", {}).get("allow_auto_resolve_account", False)

    if isinstance(account_id, str):
        account_id = account_id.strip()
    if account_id == "YOUR_ACCOUNT_ID_OR_LEAVE_BLANK_TO_AUTO_RESOLVE" or account_id == "":
        account_id = None

    if account_id and not str(account_id).startswith("act_"):
        print("Invalid `meta.account_id` in config: must begin with `act_`.", file=sys.stderr)
        sys.exit(1)

    if not account_id and not allow_auto_resolve_account:
        print(
            "Missing `meta.account_id`: set an explicit `act_...` account_id or set "
            "`meta.allow_auto_resolve_account` to true to opt in to auto-resolve.",
            file=sys.stderr,
        )
        sys.exit(1)

    run_date = datetime.datetime.now().strftime("%Y-%m-%d")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f"audit-{run_date}.json")

    # Step 1: Run Audit
    print("=== Stage 1: Running eonik Creative Audit ===")
    audit_cmd = [
        sys.executable, "scripts/audit.py",
        "--days", str(days)
    ]
    if account_id:
        audit_cmd.extend(["--account_id", account_id])
    # Security: Pass only the explicitly required variables to the child process.
    safe_env = {
        "PATH": os.environ.get("PATH", ""),
        "EONIK_API_KEY": os.environ.get("EONIK_API_KEY", "")
    }
    audit_out = run_command(audit_cmd, env=safe_env)    
    with open(report_path, "w") as f:
        f.write(audit_out)
    
    print(f"Audit complete. Report saved to {report_path}")

    # Step 2: Format and Display Report
    print("\n\n=== eonik Creative Audit Report ===")
    try:
        data = json.loads(audit_out)
        if data.get("status") != "success":
            print(f"Audit Status: {data.get('status', 'failed')}")
            sys.exit(1)

        # Currency symbol comes from the backend — no hardcoded fallback
        cs = data.get('currency_symbol', '')
        if not cs:
            cs = '$'  # Absolute last resort only
        
        spent = data.get('total_leaked_spend', 0.0)
        flagged = data.get('flagged_ads_count', 0)

        # --- Account Performance Overview ---
        acct_spend = "***" if redact else f"{cs}{data.get('total_spend', 0.0):,.2f}"
        acct_impressions = "***" if redact else f"{data.get('total_impressions', 0):,}"
        acct_clicks = "***" if redact else f"{data.get('total_clicks', 0):,}"
        acct_ctr = data.get('total_ctr', 0.0)
        acct_cpc = "***" if redact else f"{cs}{data.get('total_cpc', 0.0):,.2f}"
        acct_conversions = "***" if redact else f"{data.get('total_conversions', 0.0):,.0f}"

        print(f"\n📊 Account Performance ({days}d)")
        print(f"   Spend: {acct_spend}")
        print(f"   Impressions: {acct_impressions}")
        print(f"   Clicks: {acct_clicks}")
        print(f"   CTR: {acct_ctr:.2f}%")
        print(f"   CPC: {acct_cpc}")
        print(f"   Conversions: {acct_conversions}")

        # --- Impact Summary ---
        spent_str = "***" if redact else f"{cs}{spent:,.2f}"
        print(f"\n💰 Impact Summary")
        print(f"   Flags Found: {flagged}")
        print(f"   Wasted Spend Detected: {spent_str}")

        # --- Creative Intelligence ---
        insight = data.get("creative_insight")
        if insight:
            print(f"\n🧠 Creative Insight\n   {insight}")

        fatigue_signals = data.get("dna_fatigue", [])
        if fatigue_signals:
            print(f"\n🧬 DNA Fatigue Detected ({len(fatigue_signals)} signals)")
            for sig in fatigue_signals:
                val = sig.get('dna_value', '').capitalize()
                dec = sig.get('decline_pct', 0)
                sev = sig.get('severity', 'high').upper()
                rec = sig.get('recommendation', '')
                print(f"   [{sev}] {val} style is dropping by {dec}% \n     └ {rec}")

        learnings = data.get("creative_learnings", [])
        if learnings:
            print(f"\n🏆 Institutional Memory ({len(learnings)} winners)")
            for learn in learnings:
                msg = learn.get('message', '')
                print(f"   ✓ {msg}")

        preds = data.get("creative_predictions", [])
        if preds:
            print(f"\n🔮 What To Test Next (Predicted Top {len(preds)})")
            for p in preds:
                h = p.get('hook_type', '').capitalize()
                s = p.get('creative_style', '').capitalize()
                conf = p.get('confidence_score', 0)
                print(f"   [{conf}% Match] {h} hook + {s} style")

        win_rate = data.get("win_rate", {})
        if win_rate and win_rate.get('total_tests', 0) > 0:
            rate = win_rate.get('win_rate_pct', 0)
            tests = win_rate.get('total_tests', 0)
            baseline = win_rate.get('baseline_cpc', 0)
            print(f"\n📊 Testing Velocity")
            print(f"   Win Rate: {rate}% ({win_rate.get('winners', 0)} out of {tests} new tests beat the {cs}{baseline:.2f} CPC baseline)")
        # --- Pause / Refresh Recommendations ---
        pauses = data.get("pause_recommendations", [])
        if pauses:
            print(f"\n🚨 Urgent Actions ({len(pauses)} ads)")
            for i, ad in enumerate(pauses, 1):
                _print_ad_detail(ad, cs, is_pause=True, redact=redact)

        # --- Scale Recommendations ---
        scales = data.get("scale_recommendations", [])
        if scales:
            print(f"\n🚀 Scale Opportunities ({len(scales)} ads)")
            for i, ad in enumerate(scales, 1):
                _print_ad_detail(ad, cs, is_pause=False, redact=redact)

        # --- Monitor Recommendations ---
        monitors = data.get("monitor_recommendations", [])
        if monitors:
            print(f"\n👁️ Under Monitoring ({len(monitors)} ads)")
            for i, ad in enumerate(monitors, 1):
                rec = ad.get("recommendation", {})
                reason = rec.get("reason", "")
                ad_name = "[REDACTED]" if redact else ad.get("ad_name", "Unknown")
                category = ad.get("category", "Monitoring")
                spend = "***" if redact else f"{cs}{ad.get('spend', 0):,.2f}"
                ctr = ad.get("ctr", 0)

                print(f"\n   🔍 {ad_name}")
                print(f"     Category: {category}")
                print(f"     Spend: {spend} | CTR: {ctr:.2f}%")
                if reason:
                    print(f"     Note: {reason}")

                for sig in ad.get("signals", []):
                    print(f"     └ {sig.get('label')}: {sig.get('detail')}")

        if not pauses and not scales and not monitors:
            print("\n✅ No critical issues found. All ads are within healthy baselines.")

        print("\n\n✅ Report dispatched to active OpenCLAW channel.")
    except Exception as e:
        print(f"Failed to parse or format the audit report: {e}")
        
    print(f"\nRedaction mode: {'ON' if redact else 'OFF'}")
    print("\nPipeline Complete!")


def _print_ad_detail(ad, cs, is_pause=True, redact=False):
    """Print a single ad's detail block."""
    rec = ad.get("recommendation", {})
    category = ad.get("category", "Flagged")
    action = rec.get("action", "PAUSE" if is_pause else "SCALE")
    reason = rec.get("reason", "")
    ad_name = "[REDACTED]" if redact else ad.get("ad_name", "Unknown")
    
    if is_pause:
        action_emoji = "⏸️" if action == "PAUSE" else "🔄"
    else:
        action_emoji = "📈"
    
    print(f"\n   {action_emoji} [{action}] {ad_name}")
    print(f"     Category: {category}")
    print(f"     Reason: {reason}")
    
    # Metrics
    spend = "***" if redact else f"{cs}{ad.get('spend', 0):,.2f}"
    cpa = "***" if redact else f"{cs}{ad.get('cpa', 0):,.2f}"
    ctr = ad.get("ctr", 0)
    hook = ad.get("hook_rate", 0)
    roas = "***" if redact else f"{ad.get('roas', 0):.2f}"
    
    metrics_line = f"     Spend: {spend} | CPA: {cpa} | CTR: {ctr:.2f}%"
    if not is_pause:
        metrics_line += f" | ROAS: {roas}"
    if hook > 0:
        metrics_line += f" | Hook Rate: {hook:.1f}%"
    print(metrics_line)

    # Signals
    for sig in ad.get("signals", []):
        print(f"     └ {sig.get('label')}: {sig.get('detail')}")

    # Genome Tags
    genome = ad.get("genome_tags")
    if genome:
        tags = [f"{k}: {v}" for k, v in genome.items() if v and v != "unknown"]
        if tags:
            label = "🧬 Winning DNA" if not is_pause else "🧬 Creative DNA"
            print(f"     {label}: {' | '.join(tags)}")


if __name__ == "__main__":
    main()
