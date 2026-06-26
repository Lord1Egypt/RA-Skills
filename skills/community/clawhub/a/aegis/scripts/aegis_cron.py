#!/usr/bin/env python3
"""
AEGIS Cron Runner — 15-min scan cycle.
Posts to the public channel ONLY for CRITICAL (imminent, life-safety) threats.
HIGH/MEDIUM are collected for morning/evening briefings.
Silent when nothing new. Saves scan results for briefings.

Usage:
  python3 aegis_cron.py          # Normal silent scan
  python3 aegis_cron.py --force  # Force output even if no threats

Environment:
  AEGIS_BOT_TOKEN    — Telegram bot token (for channel alerts)
  AEGIS_CHANNEL_ID   — Telegram channel ID
"""

import json, os, sys, subprocess, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
DATA_DIR = Path(os.environ.get("AEGIS_DATA_DIR", os.path.expanduser("~/.openclaw/aegis-data")))
ALERT_COOLDOWN_FILE = DATA_DIR / "last_alert_time.json"

# Cooldown between channel posts (avoid spam)
# Default 4h for single-source CRITICAL; 60min if corroborated by 2+ distinct sources
ALERT_COOLDOWN_MINUTES = 240
ALERT_COOLDOWN_CORROBORATED_MINUTES = 60


def should_alert(corroborated=False):
    """Check if we're past the cooldown period since last alert."""
    cooldown = ALERT_COOLDOWN_CORROBORATED_MINUTES if corroborated else ALERT_COOLDOWN_MINUTES
    try:
        if ALERT_COOLDOWN_FILE.exists():
            data = json.loads(ALERT_COOLDOWN_FILE.read_text())
            last_time = data.get("last_alert_ts", 0)
            elapsed_min = (time.time() - last_time) / 60
            return elapsed_min >= cooldown
    except:
        pass
    return True


def is_corroborated(critical_threats):
    """Check if CRITICAL threats are reported by 2+ distinct sources."""
    sources = set()
    for t in critical_threats:
        sources.add(t.get("source_id", ""))
    return len(sources) >= 2


def mark_alerted():
    """Record that we just sent an alert."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ALERT_COOLDOWN_FILE.write_text(json.dumps({"last_alert_ts": time.time()}))


def build_situation_from_scan(scan_data, level):
    """Build a human-readable situation dict from raw scan data.
    
    This is template-based for speed. The morning/evening briefings
    use the full agent-powered synthesis for richer content.
    """
    threats = scan_data.get("threats", {})
    critical_threats = threats.get("critical", [])
    high_threats = threats.get("high", [])
    all_significant = critical_threats + high_threats
    
    # Extract key info from threat titles
    titles = [t.get("title", "")[:150] for t in all_significant[:10]]
    title_text = "; ".join(t for t in titles if t)
    
    # Determine what kind of threats we're seeing
    has_missile = any("missile" in t.lower() or "ballistic" in t.lower() for t in titles)
    has_drone = any("drone" in t.lower() for t in titles)
    has_airport = any("airport" in t.lower() or "airspace" in t.lower() or "flight" in t.lower() for t in titles)
    has_intercept = any("intercept" in t.lower() or "air defen" in t.lower() for t in titles)
    has_strait = any("hormuz" in t.lower() or "strait" in t.lower() for t in titles)
    
    # Build summary
    projectile_types = []
    if has_missile:
        projectile_types.append("ballistic missiles")
    if has_drone:
        projectile_types.append("drones")
    projectile_str = " and ".join(projectile_types) if projectile_types else "projectiles"
    
    if level == "critical":
        if has_intercept:
            summary = f"UAE air defenses are actively intercepting incoming {projectile_str}. This is a live situation — take cover if you hear sirens or receive phone alerts."
        elif has_airport:
            summary = f"Dubai/Abu Dhabi airports reporting disruptions. Airspace may be restricted due to active air defense operations."
        else:
            summary = f"Critical security event detected. Multiple sources reporting active threats against UAE. Follow NCEMA guidance immediately."
        
        status = "Active threat. Air defense systems engaged. Stay indoors, away from windows."
        actions = [
            "If you hear sirens or explosions: move to interior room immediately, away from windows",
            "Do NOT go outside to watch or film",
            "Keep phone charged, emergency alerts ON",
            "Stay away from windows, glass facades, and exterior walls",
            "If driving: pull over safely and get inside nearest building",
            "Check on neighbors, especially elderly and those living alone",
        ]
    else:
        # HIGH
        if has_intercept:
            summary = f"New reports of {projectile_str} targeting UAE territory. Air defenses responding. No immediate action required but stay alert."
        elif has_strait:
            summary = f"Tensions at Strait of Hormuz — potential impact on shipping, fuel, and regional stability."
        else:
            summary = f"Elevated security situation. Regional military activity detected that could affect UAE."
        
        status = "Air defenses on high alert. Situation being monitored. No immediate danger reported."
        actions = [
            "Keep phone charged and emergency alerts ON",
            "Know your nearest shelter (parking garage, basement, interior room)",
            "Have a go-bag ready: water, docs, phone charger, medications, cash",
            "Check on flight status if traveling today",
            "Follow @ABORWAIS (NCEMA) and @modgovae for official updates",
        ]
    
    # Daily impact (template — updated in morning/evening briefings with real data)
    impact = {}
    if has_airport:
        impact["Flights"] = "Check airline status before travel. Expect possible diversions and delays."
    if has_missile or has_drone:
        impact["General"] = "Stay alert. Most daily life continues but be prepared to shelter at any moment."
    if has_strait:
        impact["Fuel & shipping"] = "Possible disruptions to fuel supply and shipping routes. No immediate shortages expected."
    
    return {
        "location": "Dubai, UAE",
        "threat_level": level,
        "summary": summary,
        "status": status,
        "actions": actions,
        "daily_impact": impact if impact else {"General": "Daily life continues with heightened caution. Follow official channels."},
        "outlook": "Situation ongoing and fluid. Monitor AEGIS and official channels for updates.",
        "sources": [t.get("source_name", "OSINT") for t in all_significant[:5]]
    }


def main():
    force = "--force" in sys.argv
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run the scanner
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "aegis_scanner.py"), "--cron"],
        capture_output=True, text=True, timeout=120
    )
    
    if result.returncode != 0:
        print(f"[AEGIS] Scanner error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    try:
        scan_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"[AEGIS] Invalid scanner output", file=sys.stderr)
        sys.exit(1)
    
    # Save scan results for briefings
    (DATA_DIR / "last_scan.json").write_text(json.dumps(scan_data, indent=2))
    
    counts = scan_data.get("threat_counts", {})
    critical = counts.get("critical", 0)
    high = counts.get("high", 0)
    medium = counts.get("medium", 0)
    
    now = datetime.now(timezone(timedelta(hours=4)))
    timestamp = now.strftime("%H:%M Dubai")
    
    # Log to scan history
    log_line = f"[{timestamp}] Items: {scan_data.get('total_items', 0)} | 🔴{critical} 🟠{high} ℹ️{medium}"
    
    history_file = DATA_DIR / "scan_history.log"
    with open(history_file, "a") as f:
        f.write(log_line + "\n")
    
    # Keep history file manageable (last 500 lines)
    try:
        lines = history_file.read_text().strip().split("\n")
        if len(lines) > 500:
            history_file.write_text("\n".join(lines[-500:]) + "\n")
    except:
        pass
    
    token = os.environ.get("AEGIS_BOT_TOKEN", "")
    channel = os.environ.get("AEGIS_CHANNEL_ID", "")
    
    # CRITICAL ONLY: Post situation update to channel
    # HIGH/MEDIUM are collected silently for morning/evening briefings
    if critical > 0:
        critical_threats = scan_data.get("threats", {}).get("critical", [])
        
        # INCIDENT-LEVEL DEDUP: Filter to only genuinely NEW incidents
        # Prevents spam when multiple key_points describe the same event
        try:
            from incident_tracker import filter_new_incidents
            new_incidents = filter_new_incidents(critical_threats)
            if not new_incidents:
                print(f"[AEGIS] {critical} CRITICAL threats but all belong to known incidents — suppressing", file=sys.stderr)
                # Still log but don't alert
                print("HEARTBEAT_OK")
                return
            critical_threats = new_incidents
            print(f"[AEGIS] {len(new_incidents)} NEW incidents out of {critical} CRITICAL threats", file=sys.stderr)
        except ImportError:
            print("[AEGIS] incident_tracker not available — falling back to cooldown only", file=sys.stderr)
        
        corroborated = is_corroborated(critical_threats)
        source_count = len(set(t.get("source_id", "") for t in critical_threats))

        label = "CORROBORATED" if corroborated else "single-source"
        print(f"[AEGIS] 🔴 {critical} CRITICAL threats ({label}, {source_count} sources)", file=sys.stderr)

        # Check cooldown — corroborated threats get shorter cooldown
        if should_alert(corroborated=corroborated) and token and channel:
            # Post a cold, factual CRITICAL ALERT to the public channel
            # Use the pre-saved last_scan.json as file arg (avoids stdin pipe issues)
            scan_file = str(DATA_DIR / "last_scan.json")
            result_post = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "aegis_channel.py"), "critical", scan_file],
                capture_output=True, text=True, timeout=30,
                env={**os.environ, "AEGIS_BOT_TOKEN": token, "AEGIS_CHANNEL_ID": channel}
            )
            if result_post.returncode == 0:
                mark_alerted()
                print(f"[AEGIS] Critical alert posted to channel.", file=sys.stderr)
            else:
                print(f"[AEGIS] Channel post failed (rc={result_post.returncode}): {result_post.stderr}", file=sys.stderr)
        else:
            print(f"[AEGIS] Cooldown active or no credentials — skipping channel post.", file=sys.stderr)

        # Also DM the user for critical
        titles = [t.get("title", "?")[:80] for t in critical_threats[:3]]
        print(json.dumps({
            "alert": "critical",
            "corroborated": corroborated,
            "source_count": source_count,
            "message": f"🚨 CRITICAL ({label}): {critical} threat(s):\n" + "\n".join(f"• {t}" for t in titles),
            "threats": critical_threats[:5]
        }))
    elif force:
        print(json.dumps({"status": "ok", "counts": counts}))
    else:
        # Silent — nothing to report
        print(f"[AEGIS] {log_line}", file=sys.stderr)
        print("HEARTBEAT_OK")


if __name__ == "__main__":
    main()
