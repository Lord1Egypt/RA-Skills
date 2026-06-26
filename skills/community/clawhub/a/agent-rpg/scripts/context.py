# RPG Context Manager

import json
import os
import argparse
from pathlib import Path
from datetime import datetime

MEMORY_ROOT = Path("memory/rpg")

def get_campaign_path(campaign):
    return MEMORY_ROOT / campaign

def load_json(path):
    if not path.exists():
        return {}
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def init_campaign(campaign, system, setting, tone, char_name, archetype):
    path = get_campaign_path(campaign)
    path.mkdir(parents=True, exist_ok=True)
    
    world = {
        "campaign": campaign,
        "system": system,
        "setting": setting,
        "tone": tone,
        "location": "Starting Area",
        "time": "08:00",
        "weather": "Clear",
        "flags": {}
    }
    save_json(path / "world.json", world)
    
    char = {
        "name": char_name,
        "archetype": archetype,
        "hp": {"current": 20, "max": 20},
        "sanity": {"current": 50, "max": 50},
        "stats": {},
        "inventory": [],
        "quests": []
    }
    save_json(path / "character.json", char)
    
    npcs = {}
    save_json(path / "npcs.json", npcs)
    
    journal_path = path / "journal.md"
    date_str = datetime.now().strftime("%Y-%m-%d")
    with open(journal_path, 'w') as f:
        f.write(f"# {campaign} - Journal\n\n")
        f.write(f"- **Campaign Started**: {date_str}\n")
        f.write(f"- **Setting**: {setting}\n")
        f.write(f"- **Tone**: {tone}\n")
        f.write(f"- **System**: {system}\n")
        f.write(f"- **Protagonist**: {char_name}, {archetype}\n\n## The Story Begins\n")
    
    print(f"Campaign '{campaign}' initialized successfully in {path}")

def get_state(campaign):
    path = get_campaign_path(campaign)
    world = load_json(path / "world.json")
    print(json.dumps(world, indent=2, ensure_ascii=False))

def set_flag(campaign, key, value):
    path = get_campaign_path(campaign) / "world.json"
    world = load_json(path)
    
    if value.lower() == 'true': value = True
    elif value.lower() == 'false': value = False
    
    world.setdefault("flags", {})[key] = value
    save_json(path, world)
    print(f"Set flag '{key}' to {value}")

def update_char(campaign, stat, amount):
    path = get_campaign_path(campaign) / "character.json"
    char = load_json(path)
    
    amount = int(amount)
    
    if stat in ["hp", "sanity"]:
        if stat not in char:
            char[stat] = {"current": 20, "max": 20}
        elif isinstance(char[stat], int):
            # Migrate old format
            char[stat] = {"current": char[stat], "max": char[stat]}
            
        char[stat]["current"] += amount
        if char[stat]["current"] > char[stat].get("max", 999):
            char[stat]["current"] = char[stat]["max"]
        print(f"Updated {stat}: {char[stat]['current']}/{char[stat]['max']}")
    else:
        # Generic stat update
        char.setdefault("stats", {})
        char["stats"][stat] = char["stats"].get(stat, 0) + amount
        print(f"Updated {stat}: {char['stats'][stat]}")
        
    save_json(path, char)

def inventory(campaign, action, item):
    path = get_campaign_path(campaign) / "character.json"
    char = load_json(path)
    
    if "inventory" not in char:
        char["inventory"] = []
        
    if action == "add":
        char["inventory"].append(item)
        print(f"Added to inventory: {item}")
    elif action == "remove":
        if item in char["inventory"]:
            char["inventory"].remove(item)
            print(f"Removed from inventory: {item}")
        else:
            print(f"Item not found in inventory: {item}")
            return
            
    save_json(path, char)

def log_journal(campaign, entry):
    path = get_campaign_path(campaign) / "journal.md"
    world = load_json(get_campaign_path(campaign) / "world.json")
    
    time_str = world.get("time", "")
    weather_str = world.get("weather", "")
    prefix = f"[{time_str} | {weather_str}] " if time_str or weather_str else ""
    
    with open(path, 'a') as f:
        f.write(f"- {prefix}{entry}\n")
    print("Log entry added.")

def main():
    parser = argparse.ArgumentParser(description="RPG Context Manager 2.0")
    subparsers = parser.add_subparsers(dest="command")

    init_p = subparsers.add_parser("init")
    init_p.add_argument("-c", "--campaign", required=True)
    init_p.add_argument("--system", required=True)
    init_p.add_argument("--setting", required=True)
    init_p.add_argument("--tone", required=True)
    init_p.add_argument("--char", required=True)
    init_p.add_argument("--archetype", required=True)

    get_p = subparsers.add_parser("get_state")
    get_p.add_argument("-c", "--campaign", required=True)

    flag_p = subparsers.add_parser("set_flag")
    flag_p.add_argument("-c", "--campaign", required=True)
    flag_p.add_argument("-k", "--key", required=True)
    flag_p.add_argument("-v", "--value", required=True)

    char_p = subparsers.add_parser("update_char")
    char_p.add_argument("-c", "--campaign", required=True)
    char_p.add_argument("-s", "--stat", required=True)
    char_p.add_argument("-a", "--amount", required=True, type=int)

    inv_p = subparsers.add_parser("inventory")
    inv_p.add_argument("-c", "--campaign", required=True)
    inv_p.add_argument("-a", "--action", choices=["add", "remove"], required=True)
    inv_p.add_argument("-i", "--item", required=True)

    log_p = subparsers.add_parser("log")
    log_p.add_argument("-c", "--campaign", required=True)
    log_p.add_argument("-e", "--entry", required=True)

    args = parser.parse_args()

    if args.command == "init":
        init_campaign(args.campaign, args.system, args.setting, args.tone, args.char, args.archetype)
    elif args.command == "get_state":
        get_state(args.campaign)
    elif args.command == "set_flag":
        set_flag(args.campaign, args.key, args.value)
    elif args.command == "update_char":
        update_char(args.campaign, args.stat, args.amount)
    elif args.command == "inventory":
        inventory(args.campaign, args.action, args.item)
    elif args.command == "log":
        log_journal(args.campaign, args.entry)

if __name__ == "__main__":
    main()
