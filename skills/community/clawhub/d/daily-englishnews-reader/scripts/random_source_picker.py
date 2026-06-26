#!/usr/bin/env python3
import random
import json
import sys
import requests
from typing import List, Dict

def pick_random_sources(rss_config: Dict) -> List[Dict]:
    """
    Pick one random source from each group in the RSS config
    Args:
        rss_config: loaded content from rss_sources.json
    Returns:
        list of selected sources, one per group
    """
    selected = []
    groups = rss_config["groups"]
    
    for group_name, sources in groups.items():
        # Pick a random index from 0 to len(sources)-1
        random_index = random.randint(0, len(sources) - 1)
        picked_source = sources[random_index]
        # Add group name to the picked source info
        picked_source["group"] = group_name
        selected.append(picked_source)
        print(f"Picked source from {group_name}: {picked_source['name']}")
    
    return selected

def test_sources(rss_config: Dict) -> bool:
    """Test if all RSS sources are reachable"""
    all_ok = True
    groups = rss_config["groups"]
    
    for group_name, sources in groups.items():
        print(f"\nTesting {group_name} sources:")
        for source in sources:
            try:
                response = requests.get(source["url"], timeout=10)
                response.raise_for_status()
                print(f"✅ {source['name']}: OK")
            except Exception as e:
                print(f"❌ {source['name']}: Failed - {str(e)}")
                all_ok = False
    return all_ok

if __name__ == "__main__":
    # Load RSS sources config
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rss_config_path = os.path.join(script_dir, "../config/rss_sources.json")
    with open(rss_config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # Check for test flag
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = test_sources(config)
        sys.exit(0 if success else 1)
    
    # Pick random sources
    picked = pick_random_sources(config)
    print("\nAll selected sources for today:")
    for s in picked:
        print(f"- {s['name']} ({s['group']}): {s['url']}")
