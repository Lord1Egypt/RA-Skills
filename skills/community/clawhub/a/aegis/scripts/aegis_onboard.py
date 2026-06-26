#!/usr/bin/env python3
"""
AEGIS Onboarding — Interactive setup for AEGIS skill.
Creates aegis-config.json with user's location, preferences, and alert settings.

Usage:
  python3 aegis_onboard.py              # Interactive setup
  python3 aegis_onboard.py --show       # Show current config
  python3 aegis_onboard.py --reset      # Reset config
"""

import json, os, sys
from pathlib import Path

CONFIG_PATH = Path(os.path.expanduser("~/.openclaw/aegis-config.json"))
SKILL_DIR = Path(__file__).resolve().parent.parent
PROFILES_DIR = SKILL_DIR / "references" / "country-profiles"

# Country code → common name mapping (expandable)
KNOWN_COUNTRIES = {
    "AE": "United Arab Emirates", "IL": "Israel", "LB": "Lebanon",
    "SY": "Syria", "IQ": "Iraq", "IR": "Iran", "YE": "Yemen",
    "SA": "Saudi Arabia", "BH": "Bahrain", "KW": "Kuwait",
    "QA": "Qatar", "OM": "Oman", "JO": "Jordan", "PS": "Palestine",
    "UA": "Ukraine", "RU": "Russia", "PL": "Poland", "RO": "Romania",
    "US": "United States", "GB": "United Kingdom", "DE": "Germany",
    "FR": "France", "TR": "Turkey", "EG": "Egypt", "SD": "Sudan",
    "ET": "Ethiopia", "SO": "Somalia", "LY": "Libya", "TN": "Tunisia",
    "MM": "Myanmar", "AF": "Afghanistan", "PK": "Pakistan",
}

def has_profile(country_code):
    """Check if a country profile exists."""
    cc = country_code.lower()
    profile = PROFILES_DIR / f"{cc}.json"
    if profile.exists():
        return True
    # Check by country_code field
    for f in PROFILES_DIR.glob("*.json"):
        if f.stem.startswith("_"):
            continue
        try:
            data = json.loads(f.read_text())
            if data.get("country_code", "").upper() == country_code.upper():
                return True
        except:
            continue
    return False

def interactive_setup():
    """Run interactive onboarding."""
    print("\n" + "="*60)
    print("  ⚡ AEGIS — Automated Emergency Intelligence System")
    print("  Setup Wizard")
    print("="*60)
    
    print("\n📍 LOCATION")
    print("  Your location determines which sources AEGIS monitors.")
    country = input("  Country code (e.g. AE, IL, UA, US): ").strip().upper()
    country_name = KNOWN_COUNTRIES.get(country, country)
    city = input(f"  City in {country_name}: ").strip()
    
    if has_profile(country):
        print(f"  ✅ Country profile found for {country_name}")
    else:
        print(f"  ⚠️  No country profile for {country_name} yet.")
        print(f"     AEGIS will use global sources. Consider contributing a profile!")
    
    # Timezone
    tz_default = {
        "AE": "Asia/Dubai", "IL": "Asia/Jerusalem", "UA": "Europe/Kiev",
        "US": "America/New_York", "GB": "Europe/London", "SA": "Asia/Riyadh",
    }.get(country, "UTC")
    tz = input(f"  Timezone [{tz_default}]: ").strip() or tz_default
    
    print("\n🌐 LANGUAGE")
    lang = input("  Preferred language for briefings [en]: ").strip().lower() or "en"
    
    print("\n🔔 ALERTS")
    print("  How should AEGIS deliver alerts?")
    print("  AEGIS uses your OpenClaw messaging channel (Telegram, WhatsApp, etc.)")
    print("  🔴 CRITICAL = instant push")
    print("  🟠 HIGH = batched every 30 min")
    print("  ℹ️  MEDIUM = digest every 6 hours")
    
    batch_min = input("  HIGH alert batch interval (minutes) [30]: ").strip() or "30"
    digest_hrs = input("  MEDIUM digest interval (hours) [6]: ").strip() or "6"
    
    print("\n📋 BRIEFINGS")
    morning = input("  Morning briefing time (local, HH:MM) [07:00]: ").strip() or "07:00"
    evening = input("  Evening briefing time (local, HH:MM) [22:00]: ").strip() or "22:00"
    
    print("\n⏱️  MONITORING")
    interval = input("  Scan interval (minutes) [15]: ").strip() or "15"
    
    print("\n🧠 LLM VERIFICATION (optional — improves CRITICAL alert accuracy)")
    print("  AEGIS can use an LLM to verify CRITICAL alerts and reduce false positives.")
    print("  Without LLM: regex + negative pattern filtering (good, but less precise)")
    print("  With LLM: adds semantic verification (best accuracy)")
    print()
    print("  Options:")
    print("    1. ollama  — Local Ollama instance (free, private, recommended)")
    print("    2. openai  — Any OpenAI-compatible API (OpenRouter, Together, vLLM, etc.)")
    print("    3. none    — No LLM, regex-only mode (works fine, slightly more false positives)")
    llm_choice = input("  LLM provider [1/2/3, default=3 (none)]: ").strip() or "3"

    llm_config = {"enabled": False, "provider": "none"}
    if llm_choice == "1":
        llm_endpoint = input("  Ollama endpoint [http://localhost:11434]: ").strip() or "http://localhost:11434"
        llm_model = input("  Ollama model [qwen3:8b]: ").strip() or "qwen3:8b"
        llm_config = {"enabled": True, "provider": "ollama", "endpoint": llm_endpoint, "model": llm_model}
    elif llm_choice == "2":
        llm_endpoint = input("  API base URL (e.g. https://openrouter.ai/api): ").strip()
        llm_model = input("  Model name (e.g. meta-llama/llama-3-8b-instruct): ").strip()
        llm_key = input("  API key: ").strip()
        if llm_endpoint and llm_model:
            llm_config = {"enabled": True, "provider": "openai", "endpoint": llm_endpoint, "model": llm_model, "api_key": llm_key}
        else:
            print("  ⚠️  Missing endpoint or model — LLM disabled.")

    print("\n🔑 API KEYS (optional — press Enter to skip)")
    newsapi_key = input("  NewsAPI.org key (free at newsapi.org/register): ").strip() or None

    config = {
        "version": "1.1.0",
        "location": {
            "country": country,
            "country_name": country_name,
            "city": city,
            "timezone": tz
        },
        "language": lang,
        "alerts": {
            "critical_instant": True,
            "high_batch_minutes": int(batch_min),
            "medium_digest_hours": int(digest_hrs)
        },
        "briefings": {
            "morning": morning,
            "evening": evening
        },
        "scan_interval_minutes": int(interval),
        "llm": llm_config,
        "api_keys": {}
    }

    if newsapi_key:
        config["api_keys"]["newsapi"] = newsapi_key
    
    # Save
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to {CONFIG_PATH}")
    print(f"\n📋 Next steps:")
    print(f"  1. Test a scan:  python3 {SKILL_DIR}/scripts/aegis_scanner.py")
    print(f"  2. List sources: python3 {SKILL_DIR}/scripts/aegis_scanner.py --sources")
    print(f"  3. Set up cron monitoring via OpenClaw:")
    print(f'     openclaw cron add --every {interval}m --message "Run AEGIS scan"')
    print(f"\n⚡ AEGIS is ready. Stay safe.")
    
    return config

def show_config():
    """Display current configuration."""
    if not CONFIG_PATH.exists():
        print("No AEGIS configuration found. Run setup first.")
        return
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    print(json.dumps(config, indent=2))

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AEGIS Onboarding")
    parser.add_argument("--show", action="store_true", help="Show current config")
    parser.add_argument("--reset", action="store_true", help="Delete config and re-setup")
    args = parser.parse_args()
    
    if args.show:
        show_config()
        return
    
    if args.reset and CONFIG_PATH.exists():
        CONFIG_PATH.unlink()
        print("Config reset.")
    
    interactive_setup()

if __name__ == "__main__":
    main()
