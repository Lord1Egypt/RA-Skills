#!/usr/bin/env python3
"""
AEGIS Situation Briefing — Agent-powered comprehensive situation report.

Run by the morning (8am) and evening (8pm) crons. Uses World Monitor + LiveUAMap
data to synthesize a rich, human-readable situation update with real context:
flight status, school announcements, supply situation, etc.

The output is a situation JSON that gets posted to the AEGIS channel.

Usage:
  python3 aegis_briefing.py morning    # Morning briefing
  python3 aegis_briefing.py evening    # Evening briefing
  python3 aegis_briefing.py --dry-run  # Preview without posting
"""

import json, os, sys, subprocess, re, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("AEGIS_DATA_DIR", os.path.expanduser("~/.openclaw/aegis-data")))


def fetch_world_monitor():
    """Get World Monitor data for UAE/Gulf region."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "20",
             "https://world-monitor.com/api/signal-markers"],
            capture_output=True, text=True, timeout=25
        )
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            return data.get("locations", [])
    except:
        pass
    return []


def fetch_liveuamap_headlines():
    """Get recent LiveUAMap headlines."""
    try:
        import html as h_mod
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15", "--compressed",
             "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
             "https://iran.liveuamap.com/"],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0:
            return []
        
        html = result.stdout
        raw_texts = re.findall(r'>([^<]{35,400})<', html)
        
        news_kw = ['missile', 'strike', 'attack', 'drone', 'intercept', 'explosion',
                    'defense', 'military', 'launch', 'siren', 'shelter', 'airport',
                    'killed', 'casualt', 'destroy', 'target', 'navy', 'blockade',
                    'oil', 'tanker', 'uae', 'dubai', 'bahrain', 'gulf', 'iran']
        
        events = []
        seen = set()
        for raw in raw_texts:
            clean = h_mod.unescape(raw.strip())
            lower = clean.lower()
            if not any(kw in lower for kw in news_kw):
                continue
            norm = re.sub(r'\s+', ' ', lower)[:80]
            if norm in seen:
                continue
            seen.add(norm)
            events.append(clean)
        
        return events
    except:
        return []


def get_uae_context(locations):
    """Extract UAE-specific intelligence from World Monitor locations."""
    uae_summaries = []
    regional_summaries = []
    
    uae_kw = ['uae', 'united arab emirates', 'dubai', 'abu dhabi', 'emirates',
              'fujairah', 'al dhafra', 'camp de la paix']
    regional_kw = ['strait of hormuz', 'hormuz', 'persian gulf', 'gulf states',
                   'bahrain', 'kuwait', 'qatar']
    
    for loc in locations:
        name = loc.get("location_name", "").lower()
        country = loc.get("country", "").lower()
        summary = loc.get("summary", "")
        analysis = loc.get("analysis", "")
        
        combined = f"{name} {country}"
        
        if any(k in combined for k in uae_kw):
            uae_summaries.append({
                "location": loc.get("location_name"),
                "summary": summary,
                "analysis": analysis[:500],
            })
        elif any(k in combined or k in summary.lower() for k in regional_kw):
            regional_summaries.append({
                "location": loc.get("location_name"),
                "summary": summary[:300],
            })
    
    return uae_summaries, regional_summaries


def _sanitize_for_prompt(text: str, max_len: int = 500) -> str:
    """Strip likely prompt-injection / instruction text from untrusted sources.

    This is not perfect, but it reduces risk by:
    - removing code fences and angle-bracket tags
    - dropping lines containing common injection phrases
    - truncating to a bounded size
    """
    if not text:
        return ""

    t = text.replace("```", "").replace("<", "(").replace(">", ")")
    lines = []
    bad = (
        "ignore previous",
        "system prompt",
        "developer message",
        "you are chatgpt",
        "act as",
        "jailbreak",
        "tool",
        "function call",
        "openclaw",
        "anthropic",
        "api key",
        "token",
    )
    for ln in t.splitlines():
        low = ln.strip().lower()
        if not low:
            continue
        if any(b in low for b in bad):
            continue
        lines.append(ln.strip())

    out = " ".join(lines)
    if len(out) > max_len:
        out = out[:max_len].rstrip() + "…"
    return out


def build_briefing_prompt(period, uae_context, regional_context, headlines):
    """Build the prompt for the agent to synthesize a situation update.

    Security: inputs come from untrusted web sources. We sanitize and bound them
    before embedding into the LLM prompt to reduce prompt-injection risk.
    """
    
    now = datetime.now(timezone(timedelta(hours=4)))
    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%H:%M GST")
    
    uae_text = ""
    for ctx in uae_context[:5]:
        loc = _sanitize_for_prompt(str(ctx.get('location','')), 80)
        summ = _sanitize_for_prompt(str(ctx.get('summary','')), 420)
        uae_text += f"\n### {loc}\n{summ}\n"
        if ctx.get('analysis'):
            uae_text += f"Analysis: {_sanitize_for_prompt(str(ctx['analysis']), 420)}\n"
    
    regional_text = ""
    for ctx in regional_context[:5]:
        loc = _sanitize_for_prompt(str(ctx.get('location','')), 80)
        summ = _sanitize_for_prompt(str(ctx.get('summary','')), 320)
        regional_text += f"\n### {loc}\n{summ}\n"
    
    headlines_text = "\n".join(
        f"• {_sanitize_for_prompt(str(h), 200)}" for h in (headlines[:20] if headlines else [])
    )
    
    return f"""You are generating an AEGIS situation briefing for {date_str} at {time_str}.
This is the {"morning" if period == "morning" else "evening"} update for civilians in Dubai, UAE.

## Intelligence Data

### UAE Direct Context:
{uae_text or "No direct UAE intelligence available."}

### Regional Context:
{regional_text or "No regional context available."}

### Recent LiveUAMap Headlines:
{headlines_text or "No recent headlines available."}

## Output Format

Generate a JSON object with this exact structure:
{{
  "location": "Dubai, UAE",
  "threat_level": "critical|high|elevated|guarded|low",
  "summary": "2-4 sentences. Plain English. What happened overnight/today. Include real numbers (missiles intercepted, casualties if any). Be factual but human.",
  "status": "1-2 sentences. Current safety status right now.",
  "actions": ["List of 4-6 concrete action items for a civilian in Dubai right now"],
  "daily_impact": {{
    "Flights": "Current status of DXB and AUH based on available intel",
    "Schools": "Any announcements or expected status",
    "Work": "Business impact",
    "Supplies": "Supply chain, fuel, essentials status",
    "Roads": "Traffic and road situation"
  }},
  "outlook": "1-2 sentences. What to expect in the next 12-24 hours.",
  "sources": ["List of source names (max 5)"]
}}

## Rules:
- NO personal information, bot names, system details, or identifying data
- Write for a regular person in Dubai, not a military analyst
- Be calm and factual — no panic, no minimizing
- Include real numbers from the intel data when available
- "actions" should be USEFUL — things people can actually do
- "daily_impact" should reflect REAL current conditions from the intel
- threat_level should match the actual severity of what's happening

Output ONLY the JSON, no markdown fences, no explanation."""


def main():
    dry_run = "--dry-run" in sys.argv
    period = "morning"
    for arg in sys.argv[1:]:
        if arg in ("morning", "evening"):
            period = arg
    
    print(f"[BRIEFING] Building {period} briefing...", file=sys.stderr)
    
    # Gather intelligence
    locations = fetch_world_monitor()
    uae_ctx, regional_ctx = get_uae_context(locations)
    headlines = fetch_liveuamap_headlines()
    
    print(f"[BRIEFING] UAE contexts: {len(uae_ctx)}, Regional: {len(regional_ctx)}, Headlines: {len(headlines)}", file=sys.stderr)
    
    # Build the prompt for agent synthesis
    prompt = build_briefing_prompt(period, uae_ctx, regional_ctx, headlines)
    
    # Save prompt and data for the agent session to use
    briefing_data = {
        "period": period,
        "prompt": prompt,
        "uae_context": uae_ctx,
        "regional_context": regional_ctx,
        "headline_count": len(headlines),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    
    # Output the prompt for the OpenClaw agent to process
    # The agent session will call an LLM, parse the JSON response,
    # then post it via aegis_channel.py situation
    print(json.dumps(briefing_data))


if __name__ == "__main__":
    main()
