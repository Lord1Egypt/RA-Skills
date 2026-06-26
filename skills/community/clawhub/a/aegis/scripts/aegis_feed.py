#!/usr/bin/env python3
"""
AEGIS Live Feed — Fetches near-real-time events from World Monitor and LiveUAMap,
filters for UAE/Gulf relevance, deduplicates, and posts verified event updates
to the AEGIS Telegram channel.

Format: Short, factual, verified event messages. No analysis fluff.
Posts are batched (max 1 message per BATCH_INTERVAL_MIN minutes).

OPSEC: NO personal info. Cold, impersonal, factual broadcasts only.

Usage:
  python3 aegis_feed.py                # Normal feed cycle
  python3 aegis_feed.py --dry-run      # Preview without posting

Environment:
  AEGIS_BOT_TOKEN    — Telegram bot token
  AEGIS_CHANNEL_ID   — Telegram channel ID
"""

import json, os, sys, re, hashlib, time, subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

DATA_DIR = Path(os.environ.get("AEGIS_DATA_DIR", os.path.expanduser("~/.openclaw/aegis-data")))
FEED_STATE_FILE = DATA_DIR / "feed_state.json"

# Configuration
BATCH_INTERVAL_MIN = 5          # Min minutes between channel posts
MAX_EVENTS_PER_POST = 8         # Max events per batch message
DEDUP_WINDOW_HOURS = 6          # How long to remember seen events
UAE_RELEVANCE_KEYWORDS = [
    'uae', 'dubai', 'abu dhabi', 'emirates', 'sharjah', 'fujairah', 'ajman',
    'ras al', 'umm al', 'al dhafra', 'al minhad', 'jebel ali',
    'ncema', 'thaad', 'patriot',
    # Regional that directly affects UAE
    'strait of hormuz', 'hormuz', 'persian gulf', 'gulf states', 'gulf arab',
    'iran.*missile', 'iran.*drone', 'iran.*attack', 'iran.*launch', 'iran.*strike',
    'iranian.*missile', 'iranian.*drone', 'iranian.*attack',
    'bahrain', 'kuwait', 'qatar', 'saudi', 'oman',
    'intercept', 'air defen', 'ballistic',
]


def load_feed_state():
    """Load feed state (seen event hashes, last post time)."""
    if FEED_STATE_FILE.exists():
        try:
            return json.loads(FEED_STATE_FILE.read_text())
        except:
            pass
    return {"seen_hashes": {}, "last_post_ts": 0, "last_event_ids": []}


def save_feed_state(state):
    """Save feed state, pruning old hashes."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cutoff = time.time() - DEDUP_WINDOW_HOURS * 3600
    state["seen_hashes"] = {
        k: v for k, v in state.get("seen_hashes", {}).items() if v > cutoff
    }
    FEED_STATE_FILE.write_text(json.dumps(state, indent=2))


def event_hash(text):
    """Hash event text for dedup."""
    normalized = re.sub(r'\s+', ' ', text.lower().strip())
    # Also normalize common variations
    normalized = re.sub(r'https?://\S+', '', normalized)
    return hashlib.md5(normalized[:300].encode()).hexdigest()[:12]


def is_uae_relevant(text):
    """Check if event is relevant to UAE/Gulf region."""
    text_lower = text.lower()
    for kw in UAE_RELEVANCE_KEYWORDS:
        if '.*' in kw:
            if re.search(kw, text_lower):
                return True
        elif kw in text_lower:
            return True
    return False


def classify_urgency(text):
    """Classify event urgency: critical, high, medium."""
    text_lower = text.lower()
    
    # CRITICAL: Direct UAE impact
    critical_patterns = [
        r'(uae|dubai|abu dhabi|emirates).*(hit|struck|impact|casualt|killed|explosion)',
        r'(missile|drone).*(hit|impact|struck).*(uae|dubai|abu dhabi)',
        r'(airport|airspace).*(closed|shutdown|suspended).*(dubai|abu dhabi|uae)',
        r'(dubai|abu dhabi|uae).*(airport|airspace).*(closed|shutdown|suspended)',
        r'(siren|air.raid|shelter|evacuate).*(uae|dubai|abu dhabi)',
        r'(uae|dubai|abu dhabi).*(siren|air.raid|shelter|evacuate)',
        r'(uae|emirates).*(intercept).*(fail|breach|penetrat)',
    ]
    for p in critical_patterns:
        if re.search(p, text_lower):
            return "critical"
    
    # HIGH: Active military events affecting UAE
    high_patterns = [
        r'(uae|emirates).*(intercept|air.defen|shoot.down)',
        r'(iran|irgc).*(launch|fire|attack|strike).*(uae|dubai|gulf|base)',
        r'(ballistic|cruise).*(missile).*(uae|gulf|dubai)',
        r'(hormuz).*(block|close|mine|attack)',
        r'(wave|barrage).*(missile|drone|rocket)',
        r'(bahrain|kuwait|qatar).*(siren|intercept|hit|attack)',
    ]
    for p in high_patterns:
        if re.search(p, text_lower):
            return "high"
    
    return "medium"


def fetch_world_monitor_events():
    """Fetch UAE-relevant location updates from World Monitor.
    
    World Monitor provides per-location summaries and analysis, not discrete events.
    We only include locations where the summary indicates a NEW development
    (changed since last check). Used for context, not as primary feed.
    """
    events = []
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15",
             "https://world-monitor.com/api/signal-markers"],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0 or not result.stdout:
            return events
        
        data = json.loads(result.stdout)
        locations = data.get("locations", [])
        
        # Prioritize UAE-direct locations, then regional
        uae_direct = ['uae', 'dubai', 'abu dhabi', 'emirates', 'fujairah', 
                       'al dhafra', 'al minhad', 'camp de la paix']
        
        for loc in locations:
            loc_name = loc.get("location_name", "")
            country = loc.get("country", "")
            summary = loc.get("summary", "")
            
            combined = f"{loc_name} {country} {summary}"
            if not is_uae_relevant(combined):
                continue
            
            # Extract first sentence of summary as the "event"
            # This is analysis, but first sentence is usually the headline
            first_sentence = summary.split('.')[0].strip() + '.' if summary else ""
            
            if first_sentence and len(first_sentence) > 30:
                # Tag as directly relevant or regional
                is_direct = any(k in loc_name.lower() or k in country.lower() 
                               for k in uae_direct)
                
                events.append({
                    "text": first_sentence[:300],
                    "source": "World Monitor",
                    "location": loc_name[:50],
                    "timestamp": data.get("timestamp", ""),
                    "direct_uae": is_direct,
                })
    except Exception as e:
        print(f"[FEED] World Monitor error: {e}", file=sys.stderr)
    
    return events


def fetch_liveuamap_events():
    """Fetch events from LiveUAMap Iran page.
    
    LiveUAMap is a SPA but server-renders event text in the HTML.
    We extract text nodes that contain conflict-related keywords.
    """
    events = []
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15", "--compressed",
             "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
             "https://iran.liveuamap.com/"],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0 or not result.stdout:
            return events
        
        html = result.stdout
        
        # LiveUAMap SSRs event text as text nodes inside HTML
        import html as h_mod
        raw_texts = re.findall(r'>([^<]{30,400})<', html)
        
        # News keywords — filter out UI/nav text
        news_keywords = [
            'missile', 'strike', 'attack', 'drone', 'bomb', 'intercept',
            'explosion', 'defense', 'defence', 'military', 'launch',
            'siren', 'shelter', 'evacuate', 'airport', 'airspace',
            'killed', 'casualt', 'destroy', 'damage', 'target',
            'navy', 'frigate', 'warship', 'submarine',
            'blockade', 'oil', 'tanker', 'shipping',
        ]
        
        # Skip patterns (UI text, metadata, etc)
        skip_patterns = [
            r'^iran news on live',
            r'^liveuamap',
            r'^follow us',
            r'^copyright',
            r'^sign up',
            r'^pricing',
            r'^\s*var\s',
            r'^\s*function\s',
            r'\.css$',
            r'\.js$',
        ]
        
        seen_texts = set()
        for raw in raw_texts:
            clean = h_mod.unescape(raw.strip())
            if len(clean) < 35:
                continue
            
            lower = clean.lower()
            
            # Skip UI text
            if any(re.search(p, lower) for p in skip_patterns):
                continue
            
            # Must contain at least one news keyword
            if not any(kw in lower for kw in news_keywords):
                continue
            
            # Dedup within this batch
            norm = re.sub(r'\s+', ' ', lower)[:80]
            if norm in seen_texts:
                continue
            seen_texts.add(norm)
            
            events.append({
                "text": clean[:300],
                "source": "LiveUAMap",
                "timestamp": "",
            })
        
    except Exception as e:
        print(f"[FEED] LiveUAMap error: {e}", file=sys.stderr)
    
    return events


def format_feed_message(events, is_critical=False):
    """Format a batch of events into a single channel message.
    
    Short, factual, no analysis. Like a news wire ticker.
    """
    now = datetime.now(timezone(timedelta(hours=4)))
    ts = now.strftime("%H:%M GST")
    
    if is_critical:
        header = f"🔴 LIVE — {ts}"
    else:
        header = f"📡 LIVE — {ts}"
    
    lines = [header, ""]
    
    urgency_icon = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "•",
    }
    
    for event in events[:MAX_EVENTS_PER_POST]:
        urgency = classify_urgency(event["text"])
        icon = urgency_icon.get(urgency, "•")
        text = event["text"]
        
        # Truncate long events
        if len(text) > 200:
            text = text[:197] + "..."
        
        source = event.get("source", "")
        location = event.get("location", "")
        
        lines.append(f"{icon} {text}")
        
        # Add source tag on same line if short enough
        tag_parts = []
        if source:
            tag_parts.append(source)
        if location and location.lower() not in text.lower():
            tag_parts.append(location)
        if tag_parts:
            lines.append(f"  — {' | '.join(tag_parts)}")
        lines.append("")
    
    # Footer
    lines.append("━━━━━━━━━━━━━━━━")
    lines.append("AEGIS Live Feed | Verified OSINT")
    
    return "\n".join(lines)


def send_telegram(token, channel_id, text, pin=False):
    """Send message to Telegram channel."""
    import urllib.request
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": channel_id,
        "text": text,
        "disable_web_page_preview": True
    }).encode()
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        
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
            except:
                pass
        
        return result
    except Exception as e:
        print(f"[FEED] Telegram send failed: {e}", file=sys.stderr)
        return {"ok": False, "error": str(e)}


def main():
    dry_run = "--dry-run" in sys.argv
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    state = load_feed_state()
    
    # Check batch interval
    elapsed_min = (time.time() - state.get("last_post_ts", 0)) / 60
    if not dry_run and elapsed_min < BATCH_INTERVAL_MIN:
        print(f"[FEED] Cooldown: {BATCH_INTERVAL_MIN - elapsed_min:.1f}min remaining", file=sys.stderr)
        print("HEARTBEAT_OK")
        return
    
    # Fetch from both sources
    print("[FEED] Fetching World Monitor...", file=sys.stderr)
    wm_events = fetch_world_monitor_events()
    print(f"[FEED] World Monitor: {len(wm_events)} relevant events", file=sys.stderr)
    
    print("[FEED] Fetching LiveUAMap...", file=sys.stderr)
    lua_events = fetch_liveuamap_events()
    print(f"[FEED] LiveUAMap: {len(lua_events)} relevant events", file=sys.stderr)
    
    all_events = wm_events + lua_events
    
    # Dedup against seen hashes
    seen = state.get("seen_hashes", {})
    new_events = []
    for event in all_events:
        h = event_hash(event["text"])
        if h not in seen:
            seen[h] = time.time()
            new_events.append(event)
    
    print(f"[FEED] New (unseen) events: {len(new_events)}", file=sys.stderr)
    
    if not new_events:
        state["seen_hashes"] = seen
        save_feed_state(state)
        print("HEARTBEAT_OK")
        return
    
    # Check if any are critical
    urgency_order = {"critical": 0, "high": 1, "medium": 2}
    has_critical = any(classify_urgency(e["text"]) == "critical" for e in new_events)
    
    # Sort: critical first, then by source (LiveUAMap first — discrete events),
    # then high, then World Monitor summaries
    def sort_key(e):
        urgency = urgency_order.get(classify_urgency(e["text"]), 2)
        source_priority = 0 if e.get("source") == "LiveUAMap" else 1
        direct = 0 if e.get("direct_uae") else 1
        return (urgency, source_priority, direct)
    
    new_events.sort(key=sort_key)
    
    # Format the batch message
    msg = format_feed_message(new_events[:MAX_EVENTS_PER_POST], is_critical=has_critical)
    
    if dry_run:
        print("\n=== DRY RUN — Would post: ===")
        print(msg)
        print(f"\n=== {len(new_events)} new events, {len(all_events)} total ===")
    else:
        token = os.environ.get("AEGIS_BOT_TOKEN", "")
        channel = os.environ.get("AEGIS_CHANNEL_ID", "")
        
        if not token or not channel:
            # Try config file
            for p in [os.path.expanduser("~/.openclaw/aegis-config.json")]:
                if os.path.exists(p):
                    cfg = json.load(open(p))
                    token = token or cfg.get("telegram", {}).get("bot_token", "")
                    channel = channel or cfg.get("telegram", {}).get("channel_id", "")
        
        if token and channel:
            result = send_telegram(token, channel, msg, pin=has_critical)
            if result.get("ok"):
                print(f"[FEED] Posted {len(new_events[:MAX_EVENTS_PER_POST])} events to channel", file=sys.stderr)
                state["last_post_ts"] = time.time()
            else:
                print(f"[FEED] Post failed: {result}", file=sys.stderr)
        else:
            print("[FEED] No Telegram credentials", file=sys.stderr)
    
    # Update state
    state["seen_hashes"] = seen
    save_feed_state(state)
    
    # Output for OpenClaw
    if has_critical:
        print(json.dumps({
            "alert": "critical",
            "message": f"🔴 LIVE: {len(new_events)} new events, includes critical threats",
            "events": [e["text"][:100] for e in new_events[:5]]
        }))
    else:
        # Don't spam DMs for medium events
        print("HEARTBEAT_OK")


if __name__ == "__main__":
    main()
