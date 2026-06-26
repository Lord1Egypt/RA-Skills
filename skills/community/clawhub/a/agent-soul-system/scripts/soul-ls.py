#!/usr/bin/env python3
"""List all agents and their SOUL.md status."""
import os

AGENTS_DIR = os.path.expanduser("~/.openclaw/agents")

def list_agents():
    agents = sorted([d for d in os.listdir(AGENTS_DIR)
                     if os.path.isdir(os.path.join(AGENTS_DIR, d))])

    print(f"\n{'Agent':<20} {'SOUL.md':<10} {'大小':<10} {'人格'}")
    print("-" * 80)

    for name in agents:
        soul = os.path.join(AGENTS_DIR, name, "SOUL.md")
        if os.path.exists(soul):
            size = os.path.getsize(soul)
            size_str = f"{size/1024:.1f}KB" if size > 1024 else f"{size}B"
            with open(soul, 'r') as f:
                content = f.read()
            persona = ""
            for line in content.split('\n'):
                if line.strip().startswith('**') and ('人格' in content[max(0,content.index(line)-100):content.index(line)] or 'Personality' in content[max(0,content.index(line)-100):content.index(line)]):
                    persona = line.strip()[:50]
                    break
            print(f"{name:<20} {'✅':<10} {size_str:<10} {persona}")
        else:
            print(f"{name:<20} {'❌ 缺失':<10} {'-':<10}")

    print(f"\n总计: {len(agents)} agents")
    with_soul = sum(1 for n in agents if os.path.exists(os.path.join(AGENTS_DIR, n, "SOUL.md")))
    print(f"有灵魂: {with_soul}/{len(agents)}")

if __name__ == "__main__":
    list_agents()
