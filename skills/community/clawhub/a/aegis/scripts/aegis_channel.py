#!/usr/bin/env python3
"""
AEGIS Channel Publisher — Formats and posts alerts to Telegram channel.
Called by the scanner or briefing scripts. Handles all channel formatting.

OPSEC: NO personal info, bot names, system details, or user references.
Cold, impersonal, professional broadcasts only.

Usage:
  python3 aegis_channel.py critical <json_file>   # Post critical alert
  python3 aegis_channel.py briefing <json_file>    # Post formatted briefing
  python3 aegis_channel.py status                  # Post quiet status line

Environment:
  AEGIS_BOT_TOKEN    — Telegram bot token
  AEGIS_CHANNEL_ID   — Telegram channel ID
"""

import json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path


def _load_openclaw_dotenv():
    """Best-effort loader for decrypted secrets from tmpfs.

    Reads from /run/user/<uid>/openclaw-secrets/.env (decrypted by
    openclaw-secrets.service) with fallback to ~/.openclaw/.env for
    development. Also resolves simple ${VAR} and $VAR references.
    """
    import pwd
    uid = os.getuid()
    # Primary: tmpfs-decrypted secrets (production)
    env_path = Path(f'/run/user/{uid}/openclaw-secrets/.env')
    if not env_path.exists():
        # Fallback: direct .env (development only)
        env_path = Path(Path.home() / '.openclaw' / '.env')
    if not env_path.exists():
        return {}
    out = {}
    # first pass: parse
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and v:
            out[k] = v
    # second pass: resolve ${VAR} and $VAR using values from out and os.environ
    import re
    pattern = re.compile(r"\$(?:\{([^}]+)\}|(\w+))")
    def resolve_val(val, depth=0):
        if depth>5 or not isinstance(val,str):
            return val
        def repl(m):
            name = m.group(1) or m.group(2)
            return out.get(name, os.environ.get(name, ''))
        new = pattern.sub(repl, val)
        if new==val:
            return new
        return resolve_val(new, depth+1)
    for k in list(out.keys()):
        out[k]=resolve_val(out[k])
    # do not override existing environment variables
    for k,v in list(out.items()):
        if k not in os.environ:
            # put into os.environ temporarily for other code paths
            os.environ[k]=v
    return out

def load_env():
    """Load bot token and channel from aegis-config or environment."""
    # Load from env first; if missing, best-effort load from ~/.openclaw/.env
    token = os.environ.get("AEGIS_BOT_TOKEN", "")
    channel = os.environ.get("AEGIS_CHANNEL_ID", "")
    if not token or not channel:
        dot = _load_openclaw_dotenv()
        token = token or dot.get("AEGIS_BOT_TOKEN", "")
        channel = channel or dot.get("AEGIS_CHANNEL_ID", "")
    
    config_paths = [
        os.path.expanduser("~/.openclaw/aegis-config.json"),
        os.path.join(os.path.dirname(__file__), "..", "aegis-config.json"),
    ]
    for p in config_paths:
        if os.path.exists(p):
            with open(p) as f:
                cfg = json.load(f)
            if not token:
                token = cfg.get("telegram", {}).get("bot_token", "")
            if not channel:
                channel = cfg.get("telegram", {}).get("channel_id", "")
            break
    
    return token, channel

def send_telegram(token, channel_id, text, parse_mode="", pin=False):
    """Send message to Telegram channel. Plain text by default for reliability."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": channel_id,
        "text": text,
        "parse_mode": parse_mode if parse_mode else None,
        "disable_web_page_preview": True
    }).encode()
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        
        # Auto-pin if requested
        if pin and result.get("ok"):
            msg_id = result["result"]["message_id"]
            pin_url = f"https://api.telegram.org/bot{token}/pinChatMessage"
            pin_payload = json.dumps({
                "chat_id": channel_id,
                "message_id": msg_id,
                "disable_notification": True
            }).encode()
            pin_req = urllib.request.Request(pin_url, data=pin_payload, headers={"Content-Type": "application/json"})
            try:
                urllib.request.urlopen(pin_req, timeout=10)
            except Exception:
                pass  # Pin failure is non-critical
        
        return result
    except Exception as e:
        # Retry without parse_mode
        try:
            payload2 = json.dumps({
                "chat_id": channel_id,
                "text": text,
                "disable_web_page_preview": True
            }).encode()
            req2 = urllib.request.Request(url, data=payload2, headers={"Content-Type": "application/json"})
            resp2 = urllib.request.urlopen(req2, timeout=15)
            return json.loads(resp2.read())
        except Exception as e2:
            print(f"[AEGIS] Send failed: {e2}", file=sys.stderr)
            return {"ok": False, "error": str(e2)}


def format_critical_alert(scan_data):
    """Format a critical alert. Cold, impersonal, factual."""
    threats = scan_data.get("threats", {}).get("critical", [])
    if not threats:
        return None
    
    now = datetime.now(timezone(timedelta(hours=4)))
    
    lines = []
    lines.append("🚨 CRITICAL ALERT")
    lines.append(f"{now.strftime('%d %b %Y — %H:%M')} GST")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    for t in threats[:5]:
        title = t.get("title", "Unknown threat")
        source = t.get("source_name", "Unknown")
        tier = t.get("source_tier", "?")
        
        lines.append("")
        lines.append(f"🔴 {title}")
        lines.append(f"   Source: {source} (Tier {tier})")
    
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("⚠️ Follow official government guidance")
    lines.append("📞 UAE Emergency: 999 / NCEMA: 800-22-444")
    lines.append("")
    lines.append("AEGIS | Automated Emergency Intelligence")
    
    return "\n".join(lines)


def format_high_alert(scan_data):
    """Format a HIGH-level alert. Professional, factual, no personal info."""
    threats = scan_data.get("threats", {}).get("high", [])
    if not threats:
        return None
    
    now = datetime.now(timezone(timedelta(hours=4)))
    
    lines = []
    lines.append("⚠️ ELEVATED THREAT ALERT")
    lines.append(f"{now.strftime('%d %b %Y — %H:%M')} GST")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    for t in threats[:5]:
        title = t.get("title", "Unknown threat")
        source = t.get("source_name", "Unknown")
        tier = t.get("source_tier", "?")
        
        lines.append("")
        lines.append(f"🟠 {title}")
        lines.append(f"   Source: {source} (Tier {tier})")
    
    if len(threats) > 5:
        lines.append(f"\n   + {len(threats) - 5} additional items tracked")
    
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("Monitor official channels for updates")
    lines.append("")
    lines.append("AEGIS | Automated Emergency Intelligence")
    
    return "\n".join(lines)


def format_situation_update(situation):
    """Format a human-readable situation update.
    
    This is the primary civilian format. Written for a person in the affected area
    who needs to understand: What happened? Am I safe? What should I do?
    
    No military jargon, no source tiers, no pattern matches.
    Written like a knowledgeable friend who happens to have all the intel.
    
    Input: dict with keys:
        summary       - 1-3 sentence plain English summary of what's happening
        status        - current safety status (e.g. "Air defenses active, situation ongoing")
        threat_level  - "critical" | "high" | "elevated" | "guarded" | "low"
        actions       - list of concrete action items for civilians
        daily_impact  - dict with keys like flights, schools, work, supplies, roads
        outlook       - 1-2 sentence near-term outlook
        sources       - list of source URLs for "read more"
        timestamp     - ISO timestamp or will use now
        location      - e.g. "Dubai, UAE"
    """
    now = datetime.now(timezone(timedelta(hours=4)))
    ts = now.strftime("%d %b %Y — %H:%M GST")
    location = situation.get("location", "UAE")
    
    # Threat level header
    level = situation.get("threat_level", "high").lower()
    level_display = {
        "critical": "🔴 CRITICAL — Active threat to life",
        "high":     "🟠 HIGH — Significant ongoing threat",
        "elevated": "🟡 ELEVATED — Heightened risk, stay alert",
        "guarded":  "🔵 GUARDED — General risk, monitor updates",
        "low":      "🟢 LOW — No immediate threat",
    }.get(level, "⚪ UNKNOWN")
    
    lines = []
    
    # === HEADER ===
    lines.append(f"📍 SITUATION UPDATE — {location}")
    lines.append(ts)
    lines.append(f"Status: {level_display}")
    lines.append("")
    
    # === WHAT'S HAPPENING ===
    summary = situation.get("summary", "")
    if summary:
        lines.append(summary)
        lines.append("")
    
    # === CURRENT STATUS ===
    status = situation.get("status", "")
    if status:
        lines.append(f"🛡️ {status}")
        lines.append("")
    
    # === WHAT TO DO ===
    actions = situation.get("actions", [])
    if actions:
        lines.append("📋 What you should do:")
        for a in actions:
            lines.append(f"  → {a}")
        lines.append("")
    
    # === DAILY LIFE IMPACT ===
    impact = situation.get("daily_impact", {})
    if impact:
        lines.append("🏙️ How this affects daily life:")
        for area, status_text in impact.items():
            icon = {
                "flights": "✈️",
                "airports": "✈️",
                "schools": "🏫",
                "work": "💼",
                "supplies": "🛒",
                "roads": "🚗",
                "metro": "🚇",
                "hospitals": "🏥",
                "water": "💧",
                "power": "⚡",
                "internet": "📶",
                "banks": "🏦",
            }.get(area.lower(), "•")
            lines.append(f"  {icon} {area}: {status_text}")
        lines.append("")
    
    # === OUTLOOK ===
    outlook = situation.get("outlook", "")
    if outlook:
        lines.append(f"🔮 Near-term: {outlook}")
        lines.append("")
    
    # === SOURCES ===
    sources = situation.get("sources", [])
    if sources:
        lines.append("📰 Sources:")
        for s in sources[:5]:
            if isinstance(s, dict):
                lines.append(f"  • {s.get('name', '')} — {s.get('url', '')}")
            else:
                lines.append(f"  • {s}")
        lines.append("")
    
    # === FOOTER ===
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("📞 Emergency: 999 | NCEMA: 800-22-444")
    lines.append("AEGIS — Open Source Emergency Intelligence")
    
    return "\n".join(lines)


def format_briefing(briefing_data, scan_data=None):
    """Format morning/evening briefing. Professional, cold, no personal info."""
    btype = briefing_data.get("type", "status")
    location = briefing_data.get("location", {})
    threat = briefing_data.get("threat_assessment", {})
    summary = briefing_data.get("scan_summary", {})
    
    now = datetime.now(timezone(timedelta(hours=4)))
    
    is_morning = btype == "morning"
    header = "MORNING SITUATION REPORT" if is_morning else "EVENING SITUATION REPORT"
    
    lines = []
    lines.append(f"{'☀️' if is_morning else '🌙'} {header}")
    lines.append(f"{now.strftime('%d %b %Y — %H:%M')} GST (UTC+4)")
    lines.append(f"Region: {location.get('country', 'UAE')}")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Threat level
    level = threat.get("level", "unknown").upper()
    emoji = threat.get("emoji", "❓")
    trend = threat.get("trend", "➡️")
    trend_text = threat.get("trend_text", "Stable")
    desc = threat.get("description", "")
    
    lines.append("")
    lines.append(f"THREAT LEVEL: {emoji} {level} {trend} {trend_text}")
    if desc:
        lines.append(f"  {desc}")
    
    # Scan stats
    lines.append("")
    lines.append(f"MONITORING ({summary.get('period_hours', 12)}h window)")
    tc = summary.get('total_critical', 0)
    th = summary.get('total_high', 0)
    tm = summary.get('total_medium', 0)
    lines.append(f"  🔴 Critical: {tc}  |  🟠 High: {th}  |  ℹ️ Medium: {tm}")
    lines.append(f"  Scans: {summary.get('scans_analyzed', 0)}  |  Sources: 23+")
    
    # Key developments
    if scan_data:
        all_threats = []
        for level_name in ["critical", "high", "medium"]:
            for t in scan_data.get("threats", {}).get(level_name, []):
                t["_level"] = level_name
                all_threats.append(t)
        
        if all_threats:
            lines.append("")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append("KEY DEVELOPMENTS")
            
            level_emoji = {"critical": "🔴", "high": "🟠", "medium": "ℹ️"}
            seen_titles = set()
            shown = 0
            
            for t in all_threats:
                if shown >= 10:
                    break
                le = level_emoji.get(t["_level"], "•")
                title = t.get("title", "")[:120]
                source = t.get("source_name", "")
                tier = t.get("source_tier", "")
                
                # Dedup similar titles
                title_key = title[:50].lower()
                if title_key in seen_titles:
                    continue
                seen_titles.add(title_key)
                
                try:
                    tier_int = int(tier)
                    verify = "✓ Official" if tier_int <= 1 else "• Reported"
                except:
                    verify = "• Reported"
                
                lines.append(f"")
                lines.append(f"{le} {title}")
                lines.append(f"   {source} | {verify}")
                shown += 1
            
            remaining = len(all_threats) - shown
            if remaining > 0:
                lines.append(f"")
                lines.append(f"  + {remaining} additional items tracked")
    
    # Guidance — generic, no personal details
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("STANDING GUIDANCE")
    lines.append("• Follow NCEMA / official emergency channels")
    lines.append("• Emergency alerts enabled on mobile devices")
    lines.append("• Maintain situational awareness")
    lines.append("• UAE Emergency: 999 | Police: 901")
    
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("AEGIS | Open Source Emergency Intelligence")
    lines.append("23+ sources | 15-min cycle | Anti-hoax protocol")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: aegis_channel.py <critical|high|situation|briefing|status> [json_file]", file=sys.stderr)
        sys.exit(1)
    
    action = sys.argv[1]
    token, channel = load_env()
    
    if not token or not channel:
        print("[AEGIS] Missing AEGIS_BOT_TOKEN or AEGIS_CHANNEL_ID", file=sys.stderr)
        sys.exit(1)
    
    if action == "critical":
        if len(sys.argv) < 3:
            data = json.load(sys.stdin)
        else:
            with open(sys.argv[2]) as f:
                data = json.load(f)
        
        msg = format_critical_alert(data)
        if msg:
            result = send_telegram(token, channel, msg, pin=True)
            print(json.dumps(result, indent=2))
        else:
            print("[AEGIS] No critical threats to post", file=sys.stderr)
    
    elif action == "high":
        if len(sys.argv) < 3:
            data = json.load(sys.stdin)
        else:
            with open(sys.argv[2]) as f:
                data = json.load(f)
        
        msg = format_high_alert(data)
        if msg:
            result = send_telegram(token, channel, msg)
            print(json.dumps(result, indent=2))
        else:
            print("[AEGIS] No high threats to post", file=sys.stderr)
    
    elif action == "situation":
        if len(sys.argv) < 3:
            data = json.load(sys.stdin)
        else:
            with open(sys.argv[2]) as f:
                data = json.load(f)
        
        msg = format_situation_update(data)
        if msg:
            result = send_telegram(token, channel, msg, pin=True)
            print(json.dumps(result, indent=2))
        else:
            print("[AEGIS] Empty situation data", file=sys.stderr)
    
    elif action == "briefing":
        if len(sys.argv) < 3:
            data = json.load(sys.stdin)
        else:
            with open(sys.argv[2]) as f:
                data = json.load(f)
        
        scan_data = None
        data_dir = Path(os.environ.get("AEGIS_DATA_DIR", os.path.expanduser("~/.openclaw/aegis-data")))
        last_scan = data_dir / "last_scan.json"
        if last_scan.exists():
            with open(last_scan) as f:
                scan_data = json.load(f)
        
        msg = format_briefing(data, scan_data)
        result = send_telegram(token, channel, msg, pin=True)
        print(json.dumps(result, indent=2))
    
    elif action == "status":
        now = datetime.now(timezone(timedelta(hours=4)))
        msg = f"AEGIS — {now.strftime('%H:%M')} GST\n📡 Monitoring active | No critical alerts"
        result = send_telegram(token, channel, msg)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
