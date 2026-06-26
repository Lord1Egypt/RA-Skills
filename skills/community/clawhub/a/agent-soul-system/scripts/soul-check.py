#!/usr/bin/env python3
"""Validate SOUL.md files for all agents."""
import os, sys, json

AGENTS_DIR = os.path.expanduser("~/.openclaw/agents")
REQUIRED = ["人格", "核心特质", "核心职责", "核心原则"]

def check():
    issues = []
    agents = sorted([d for d in os.listdir(AGENTS_DIR)
                     if os.path.isdir(os.path.join(AGENTS_DIR, d))])

    for name in agents:
        soul = os.path.join(AGENTS_DIR, name, "SOUL.md")
        if not os.path.exists(soul):
            issues.append(f"❌ {name}: 缺失 SOUL.md")
            continue

        with open(soul, 'r') as f:
            content = f.read()

        size = os.path.getsize(soul)
        missing = [s for s in REQUIRED if s not in content]
        has_collab = "协作协议" in content or "上级" in content

        if missing:
            issues.append(f"⚠️ {name}: 缺少 [{', '.join(missing)}]")
        elif not has_collab:
            issues.append(f"⚠️ {name}: 缺少协作协议")
        else:
            persona = ""
            for line in content.split('\n'):
                if '## 人格' in line or '## Personality' in line:
                    continue
                if line.strip() and ('人格' in line or 'Personality' in line):
                    persona = line.strip()[:50]
                    break
            issues.append(f"✅ {name} ({size} bytes) | {persona}")

    print(f"\n{'='*50}")
    print(f"Agent Soul Check — {len(agents)} agents scanned")
    print(f"{'='*50}")
    for i in issues:
        print(f"  {i}")

    errors = [i for i in issues if i.startswith("❌")]
    warns = [i for i in issues if i.startswith("⚠️")]
    ok = [i for i in issues if i.startswith("✅")]

    print(f"\n  ✅ {len(ok)} 正常  ⚠️ {len(warns)} 警告  ❌ {len(errors)} 错误")
    print(f"{'='*50}")

    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(check())
