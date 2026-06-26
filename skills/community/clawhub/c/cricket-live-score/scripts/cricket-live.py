#!/usr/bin/env python3
"""
Generic live cricket score updater.
Scrapes Cricbuzz live score page, sends text + voice memo to Telegram.
Supports both innings with auto-detection.

Usage:
  python3 cricket-live.py --url <cricbuzz_url> --chat-id <id> [--bot-token <token>] [--interval 300] [--voice]

The script auto-detects:
  - Team names (from page data)
  - Which innings (1st or 2nd) based on score structure
  - Target score for 2nd innings chase
  - Match completion (auto-stops)
"""

import json, time, urllib.request, urllib.parse, re, html as htmllib
import sys, os, tempfile, argparse

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# ─── Config ───────────────────────────────────────────────────────────────────

def load_bot_token():
    """Load Telegram bot token from OpenClaw config (fallback when --bot-token not provided)."""
    config_path = os.environ.get("OPENCLAW_CONFIG", os.path.expanduser("~/.openclaw/openclaw.json"))
    try:
        with open(config_path) as f:
            config = json.load(f)
        return config["channels"]["telegram"]["botToken"]
    except (FileNotFoundError, KeyError) as e:
        print(f"Error: Could not load bot token from {config_path}: {e}", file=sys.stderr)
        print("Provide --bot-token explicitly or ensure your OpenClaw config has channels.telegram.botToken", file=sys.stderr)
        sys.exit(1)

# ─── Telegram helpers ─────────────────────────────────────────────────────────

def send_telegram(text, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        data = json.dumps({"chat_id": chat_id, "text": text}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)


def send_voice(text, bot_token, chat_id):
    if not GTTS_AVAILABLE:
        print("gTTS not installed — skipping voice memo.", file=sys.stderr)
        return
    try:
        clean = re.sub(r'[*_`]', '', text)
        clean = re.sub(r'[🏏🎉📲📊🤝⚡🎯🏁🔹📈📌·━]', '', clean)
        tts = gTTS(clean, lang='en')
        tmp = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        tts.save(tmp.name)
        tmp.close()

        boundary = '----CricketBoundary'
        body = bytearray()
        body.extend(f'--{boundary}\r\n'.encode())
        body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode())
        with open(tmp.name, 'rb') as f:
            audio_data = f.read()
        body.extend(f'--{boundary}\r\n'.encode())
        body.extend(f'Content-Disposition: form-data; name="voice"; filename="score.mp3"\r\n'.encode())
        body.extend(f'Content-Type: audio/mpeg\r\n\r\n'.encode())
        body.extend(audio_data)
        body.extend(f'\r\n--{boundary}--\r\n'.encode())

        url = f"https://api.telegram.org/bot{bot_token}/sendVoice"
        req = urllib.request.Request(url, data=bytes(body),
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        urllib.request.urlopen(req, timeout=15)
        os.unlink(tmp.name)
    except Exception as e:
        print(f"Voice error: {e}", file=sys.stderr)

# ─── Cricbuzz scraping ────────────────────────────────────────────────────────

def validate_url(url):
    """Ensure the URL is a valid Cricbuzz live score page to prevent SSRF."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        print(f"Error: URL must use http or https (got {parsed.scheme})", file=sys.stderr)
        sys.exit(1)
    if not parsed.hostname or not parsed.hostname.endswith('cricbuzz.com'):
        print(f"Error: URL must be a cricbuzz.com domain (got {parsed.hostname})", file=sys.stderr)
        sys.exit(1)
    return url


def fetch_raw(match_url):
    req = urllib.request.Request(match_url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="ignore")


def extract_match_info(raw):
    """Extract team names, series, format from embedded JSON."""
    info = {}

    # Team names — Cricbuzz uses teamName/teamSName in the header JSON
    t1 = re.search(r'"team1":\{"teamId":\d+,"teamName":"([^"]+)","teamSName":"([^"]+)"', raw)
    t2 = re.search(r'"team2":\{"teamId":\d+,"teamName":"([^"]+)","teamSName":"([^"]+)"', raw)
    # Escaped variant
    if not t1:
        t1 = re.search(r'\\\"team1\\\":\{\\\"teamId\\\":\d+,\\\"teamName\\\":\\\"([^\\\"]+)\\\",\\\"teamSName\\\":\\\"([^\\\"]+)\\\"', raw)
    if not t2:
        t2 = re.search(r'\\\"team2\\\":\{\\\"teamId\\\":\d+,\\\"teamName\\\":\\\"([^\\\"]+)\\\",\\\"teamSName\\\":\\\"([^\\\"]+)\\\"', raw)
    # Fallback: look for team blocks with "name" and "shortName" (other Cricbuzz layouts)
    if not t1:
        t1 = re.search(r'"team1":\{[^}]*"name":"([^"]+)"[^}]*"shortName":"([^"]+)"', raw)
    if not t2:
        t2 = re.search(r'"team2":\{[^}]*"name":"([^"]+)"[^}]*"shortName":"([^"]+)"', raw)

    if t1:
        info['team1_name'] = t1.group(1)
        info['team1_short'] = t1.group(2)
    if t2:
        info['team2_name'] = t2.group(1)
        info['team2_short'] = t2.group(2)

    # Series name
    sm = re.search(r'\\"seriesName\\":\\"([^\\]+)\\"', raw)
    if not sm:
        sm = re.search(r'"seriesName":"([^"]+)"', raw)
    if sm:
        info['series'] = sm.group(1)

    # Match format (T20, ODI, Test)
    fm = re.search(r'\\"matchFormat\\":\\"([^\\]+)\\"', raw)
    if not fm:
        fm = re.search(r'"matchFormat":"([^"]+)"', raw)
    if fm:
        info['format'] = fm.group(1)

    # Total overs for format
    fmt = info.get('format', 'T20')
    if fmt == 'T20':
        info['total_overs'] = 20
        info['total_balls'] = 120
    elif fmt == 'ODI':
        info['total_overs'] = 50
        info['total_balls'] = 300
    else:
        info['total_overs'] = None
        info['total_balls'] = None

    return info


def parse_og_description(raw):
    """Parse the og:description for score and batsmen."""
    desc = re.search(r'og:description[^>]*content="Follow ([^"]+)"', raw)
    if not desc:
        return None
    text = htmllib.unescape(desc.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
    score_part = text.split('|')[0].strip()
    return score_part


def parse_score_line(score_part):
    """
    Parse score like:
      1st inn: "WI 120/3 (15) (Rovman Powell 25(14) Jason Holder 12(8))"
      2nd inn: "IND 146/4 (15) vs WI 195/4 (Tilak Varma 20(15) Sanju Samson 80(40))"
    Returns dict with batting_team_short, runs, wickets, overs, batsmen, and
    optionally bowling_team_short, bowl_runs, bowl_wickets if 2nd innings.
    """
    if not score_part:
        return None

    # 2nd innings pattern: "TEAM1 runs/wkts (overs) vs TEAM2 runs/wkts (batsmen)"
    m2 = re.match(
        r'([A-Z]{2,5})\s+(\d+)/(\d+)\s+\((\d+\.?\d*)\)\s+vs\s+([A-Z]{2,5})\s+(\d+)/(\d+)\s*\((.+)\)',
        score_part
    )
    if m2:
        batsmen = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(\d+)\((\d+)\)', m2.group(8))
        return {
            'innings': 2,
            'bat_short': m2.group(1),
            'runs': int(m2.group(2)),
            'wickets': int(m2.group(3)),
            'overs': m2.group(4),
            'bowl_short': m2.group(5),
            'bowl_runs': int(m2.group(6)),
            'bowl_wickets': int(m2.group(7)),
            'batsmen': batsmen,
        }

    # 1st innings pattern: "TEAM runs/wkts (overs) (batsmen)"
    m1 = re.match(
        r'([A-Z]{2,5})\s+(\d+)/(\d+)\s+\((\d+\.?\d*)\)\s*\((.+)\)',
        score_part
    )
    if m1:
        batsmen = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(\d+)\((\d+)\)', m1.group(5))
        return {
            'innings': 1,
            'bat_short': m1.group(1),
            'runs': int(m1.group(2)),
            'wickets': int(m1.group(3)),
            'overs': m1.group(4),
            'batsmen': batsmen,
        }

    return None


def parse_last_wicket(raw):
    """Extract last wicket from embedded JSON, shorten to last names for fielder/bowler."""
    lw_match = re.search(r'lastWicket\\":\\"(.*?)\\"', raw)
    if not lw_match:
        return None
    lw_text = lw_match.group(1).replace('\\\\', '').strip()
    lw_clean = re.sub(r'\s+', ' ', lw_text).strip()
    # Truncate at score marker
    trunc = re.match(r'(.+?\d+\s*\(\d+\))\s*-\s*\d+/\d+\s+in\s+[\d.]+\s*ov\.?', lw_clean)
    if trunc:
        lw_clean = trunc.group(1)

    # Shorten to last names for fielder and bowler
    # Pattern: "Batsman Full c Fielder Full b Bowler Full 18(16)"
    def last_name(full_name):
        parts = full_name.strip().split()
        return parts[-1] if parts else full_name

    m = re.match(r'(.+?)\s+(c\s+)(.+?)\s+(b\s+)(.+?)\s+(\d+\s*\(\d+\))', lw_clean)
    if m:
        batsman = m.group(1).strip()
        fielder = last_name(m.group(3))
        bowler = last_name(m.group(5))
        score = m.group(6).strip()
        return f"{batsman} c {fielder} b {bowler} {score}"

    # Bowled / LBW (no catcher): "Batsman b Bowler 18(16)"
    m2 = re.match(r'(.+?)\s+(b\s+)(.+?)\s+(\d+\s*\(\d+\))', lw_clean)
    if m2:
        batsman = m2.group(1).strip()
        bowler = last_name(m2.group(3))
        score = m2.group(4).strip()
        return f"{batsman} b {bowler} {score}"

    # Stumped: "Batsman st Keeper b Bowler 18(16)"
    m3 = re.match(r'(.+?)\s+(st\s+)(.+?)\s+(b\s+)(.+?)\s+(\d+\s*\(\d+\))', lw_clean)
    if m3:
        batsman = m3.group(1).strip()
        keeper = last_name(m3.group(3))
        bowler = last_name(m3.group(5))
        score = m3.group(6).strip()
        return f"{batsman} st {keeper} b {bowler} {score}"

    return lw_clean


def parse_match_status(raw, match_info=None):
    """Check for match result using og:title (most reliable, page-specific).
    
    The og:title for a live match shows "RSA 1/0 (0.3)" but when the match
    ends it shows "RSA won by 5 wkts" or similar. This avoids false positives
    from sidebar widgets showing other completed matches.
    """
    # Primary: check og:title — this is always about THIS match
    og_title = re.search(r'property="og:title"\s+content="([^"]+)"', raw)
    if og_title:
        title = htmllib.unescape(og_title.group(1))
        if re.search(r'(?:won|tied|no result|match drawn)', title, re.IGNORECASE):
            return title.strip()
    
    # Fallback: check og:description for result text
    og_desc = re.search(r'property="og:description"\s+content="([^"]+)"', raw)
    if og_desc:
        desc = htmllib.unescape(og_desc.group(1))
        rm = re.search(r'((?:[\w ]+)\s+(?:won by|tied|no result|match drawn)[^,]*)', desc, re.IGNORECASE)
        if rm:
            return rm.group(1).strip()
    
    return None


def overs_to_balls(overs_str):
    ov = float(overs_str)
    full = int(ov)
    part = round((ov - full) * 10)
    return full * 6 + part


# ─── Formatting ───────────────────────────────────────────────────────────────

def format_text(score, last_wkt, match_info, match_status):
    """Format the text message."""
    if match_status:
        return f"🏁 *Match Over*\n{match_status}"

    if score is None:
        return "🏏 Waiting for score data..."

    team_names = {
        match_info.get('team1_short', '???'): match_info.get('team1_name', '???'),
        match_info.get('team2_short', '???'): match_info.get('team2_name', '???'),
    }
    bat_name = team_names.get(score['bat_short'], score['bat_short'])
    total_balls = match_info.get('total_balls')

    lines = []

    # Batting score + batsmen
    lines.append(f"*{bat_name}: {score['runs']}/{score['wickets']} ({score['overs']} ov)*")
    for name, runs, balls in score.get('batsmen', []):
        lines.append(f"  🏏 {name} — {runs} ({balls})")

    lines.append("")  # blank line

    if score['innings'] == 2:
        # Chase format
        target = score['bowl_runs'] + 1
        needed = target - score['runs']
        balls_bowled = overs_to_balls(score['overs'])
        balls_left = total_balls - balls_bowled if total_balls else 0
        overs_left = balls_left / 6 if balls_left > 0 else 0

        if needed > 0:
            rrr = needed / overs_left if overs_left > 0 else 0
            lines.append(f"Need: {needed} runs off {balls_left} balls")
            lines.append(f"RRR: {rrr:.1f} per over with {overs_left:.1f} overs to go")
        else:
            lines.append(f"🎉 {bat_name} have reached the target!")

    else:
        # 1st innings format
        balls_bowled = overs_to_balls(score['overs'])
        innings_complete = (total_balls and balls_bowled >= total_balls) or score['wickets'] >= 10
        current_rr = score['runs'] / (balls_bowled / 6) if balls_bowled > 0 else 0

        if innings_complete:
            # Innings over — derive bowling team (the one NOT batting)
            bat_short = score['bat_short']
            t1s = match_info.get('team1_short', '???')
            t2s = match_info.get('team2_short', '???')
            bowl_short = t2s if bat_short == t1s else t1s
            bowl_name = team_names.get(bowl_short, bowl_short)
            lines.append(f"Innings complete — {bowl_name} need {score['runs'] + 1} to win")
        elif total_balls:
            projected = int(current_rr * match_info['total_overs'])
            lines.append(f"Run rate: {current_rr:.1f} per over")
            lines.append(f"Projected: {projected}")
        else:
            lines.append(f"Run rate: {current_rr:.1f} per over")

    # Last wicket
    if last_wkt:
        lines.append(f"Last wicket: {last_wkt}")

    # 2nd innings: show bowling team's score
    if score['innings'] == 2:
        bowl_name = team_names.get(score['bowl_short'], score['bowl_short'])
        bowl_short = score['bowl_short']
        lines.append(f"\n🔹 {bowl_short} innings: {score['bowl_runs']}/{score['bowl_wickets']} ({match_info.get('total_overs', '?')} ov)")

    # Footer: match info
    lines.append("")  # blank line before footer
    t1s = match_info.get('team1_short', '?')
    t2s = match_info.get('team2_short', '?')
    series = match_info.get('series', 'Cricket')
    lines.append(f"━━━━━━━━━━━━━━━━━")
    lines.append(f"🏏 {t1s} vs {t2s} | {series}")

    return "\n".join(lines)


def format_voice(score, last_wkt, match_info, match_status):
    """Format natural spoken summary."""
    if match_status:
        return match_status

    if score is None:
        return "Waiting for score data."

    team_names = {
        match_info.get('team1_short', '???'): match_info.get('team1_name', '???'),
        match_info.get('team2_short', '???'): match_info.get('team2_name', '???'),
    }
    bat_name = team_names.get(score['bat_short'], score['bat_short'])
    total_balls = match_info.get('total_balls')

    parts = []

    # Score
    parts.append(f"{bat_name} are {score['runs']} for {score['wickets']} in {score['overs']} overs.")

    # Batsmen
    bats = score.get('batsmen', [])
    if len(bats) >= 2:
        parts.append(f"{bats[0][0]} and {bats[1][0]} are batting.")
        parts.append(f"{bats[0][0]} is on {bats[0][1]}, and {bats[1][0]} is on {bats[1][1]}.")
    elif len(bats) == 1:
        parts.append(f"{bats[0][0]} is batting on {bats[0][1]}.")

    if score['innings'] == 2:
        target = score['bowl_runs'] + 1
        needed = target - score['runs']
        balls_bowled = overs_to_balls(score['overs'])
        balls_left = total_balls - balls_bowled if total_balls else 0
        overs_left = balls_left / 6 if balls_left > 0 else 0

        if needed > 0:
            rrr = needed / overs_left if overs_left > 0 else 0
            parts.append(f"{bat_name} need {needed} runs off {balls_left} balls.")
            parts.append(f"Required run rate is {rrr:.1f} per over, with {overs_left:.1f} overs to go.")
        else:
            parts.append(f"{bat_name} have reached the target!")

        # Bowling team score
        bowl_name = team_names.get(score['bowl_short'], score['bowl_short'])
        parts.append(f"{bowl_name} scored {score['bowl_runs']} for {score['bowl_wickets']} in {match_info.get('total_overs', '?')} overs.")
    else:
        balls_bowled = overs_to_balls(score['overs'])
        current_rr = score['runs'] / (balls_bowled / 6) if balls_bowled > 0 else 0
        parts.append(f"Run rate is {current_rr:.1f} per over.")
        if total_balls:
            projected = int(current_rr * match_info['total_overs'])
            parts.append(f"Projected total is {projected}.")

    # Last wicket
    if last_wkt:
        # Parse for voice: "Batsman c Fielder b Bowler 18 (16)"
        lw_m = re.match(r'(.+?)\s+(?:c\s+\w+\s+)?(?:st\s+\w+\s+)?b\s+(\w+)\s+(\d+)\s*\((\d+)\)', last_wkt)
        if lw_m:
            parts.append(f"The last wicket was {lw_m.group(1).strip()}, bowled by {lw_m.group(2)}, on {lw_m.group(3)} runs off {lw_m.group(4)} balls.")
        else:
            parts.append(f"The last wicket was {last_wkt}.")

    return " ".join(parts)

# ─── Main loop ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Live cricket score updater")
    parser.add_argument("--url", required=True, help="Cricbuzz live score URL")
    parser.add_argument("--interval", type=int, default=300, help="Update interval in seconds (default: 300)")
    parser.add_argument("--chat-id", required=True, help="Telegram chat ID")
    parser.add_argument("--bot-token", default=None, help="Telegram bot token (falls back to OpenClaw config if not provided)")
    parser.add_argument("--voice", action="store_true", default=False, help="Send voice memo with each update")
    args = parser.parse_args()

    bot_token = args.bot_token or os.environ.get("TELEGRAM_BOT_TOKEN") or load_bot_token()
    match_url = validate_url(args.url)
    interval = args.interval
    chat_id = args.chat_id
    voice_enabled = args.voice

    print(f"Cricket live score started.")
    print(f"  URL: {match_url}")
    print(f"  Interval: {interval}s")
    print(f"  Chat ID: {chat_id}")

    last_score_key = None
    match_info = None
    i = 0

    while True:
        i += 1
        try:
            raw = fetch_raw(match_url)

            # Extract match info once (or refresh if missing)
            if match_info is None or 'team1_short' not in match_info:
                match_info = extract_match_info(raw)
                print(f"  Teams: {match_info.get('team1_short')} vs {match_info.get('team2_short')}")
                print(f"  Series: {match_info.get('series')}")
                print(f"  Format: {match_info.get('format')}")

            # Check for match result (scoped to our teams to avoid sidebar false positives)
            match_status = parse_match_status(raw, match_info)

            # Parse score
            og = parse_og_description(raw)
            score = parse_score_line(og)
            last_wkt = parse_last_wicket(raw)

            # Build score key for dedup
            if score:
                score_key = f"{score['bat_short']}{score['runs']}/{score['wickets']}"
            elif match_status:
                score_key = f"RESULT:{match_status}"
            else:
                score_key = None

            # Only send if changed
            if score_key and score_key != last_score_key:
                text_msg = format_text(score, last_wkt, match_info, match_status)
                voice_msg = format_voice(score, last_wkt, match_info, match_status)

                # Suppress "next update" only if match is truly over (result or target reached)
                target_reached = (score and score.get('innings') == 2
                                  and score.get('bowl_runs') is not None
                                  and score['runs'] >= score['bowl_runs'] + 1)
                if not match_status and not target_reached:
                    text_msg += f"\n\n· Next update in {interval // 60} min"

                send_telegram(text_msg, bot_token, chat_id)
                if voice_enabled:
                    send_voice(voice_msg, bot_token, chat_id)
                last_score_key = score_key
                print(f"[{i}] Sent: {score_key}", flush=True)

                if match_status or target_reached:
                    print("Match over. Exiting.", flush=True)
                    return
            else:
                print(f"[{i}] No change: {score_key or 'no score'}", flush=True)

        except Exception as e:
            print(f"[{i}] Error: {e}", file=sys.stderr, flush=True)

        time.sleep(interval)


if __name__ == "__main__":
    main()
