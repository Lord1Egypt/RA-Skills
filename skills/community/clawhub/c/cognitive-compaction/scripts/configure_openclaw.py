#!/usr/bin/env python3
import json
import os
from pathlib import Path

OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")

def configure_compaction():
    config = {}
    if os.path.exists(OPENCLAW_CONFIG_PATH):
        try:
            with open(OPENCLAW_CONFIG_PATH, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print("Failed to parse existing openclaw.json. Creating a backup and rebuilding.")
            os.rename(OPENCLAW_CONFIG_PATH, OPENCLAW_CONFIG_PATH + ".bak")

    # Initialize nested dicts 
    if "agents" not in config:
        config["agents"] = {}
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}
    
    # Configure the detailed memory compaction
    config["agents"]["defaults"]["compaction"] = {
        "mode": "safeguard",
        "reserveTokensFloor": 20000,
        "memoryFlush": {
            "enabled": True,
            "softThresholdTokens": 6000,
            "systemPrompt": "Session nearing compaction. Execute the cognitive-compaction skill to summarize state.",
            "prompt": "Invoke the cognitive-compaction skill and summarize progress."
        }
    }
    
    with open(OPENCLAW_CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)
        
    print(f"**Configuration Updated**: Successfully applied cognitive-compaction settings to `{OPENCLAW_CONFIG_PATH}`.")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OPENCLAW_CONFIG_PATH), exist_ok=True)
    configure_compaction()
