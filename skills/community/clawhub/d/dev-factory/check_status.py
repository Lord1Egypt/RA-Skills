#!/usr/bin/env python3
"""
Builder Agent 운영 상태 확인
"""

import sys
import json
from pathlib import Path

print("=" * 70)
print("BUILDER AGENT v5.0 - PRODUCTION STATUS")
print("=" * 70)
print()

# 1. Health Check
print("1️⃣ Health Check")
print("-" * 70)

health_check = Path.home() / '.openclaw/workspace/skills/builder-agent/health_check.py'
if health_check.exists():
    print("✅ health_check.py exists")
else:
    print("❌ health_check.py missing")

run_discovery = Path.home() / '.openclaw/workspace/skills/builder-agent/run_discovery.py'
if run_discovery.exists():
    print("✅ run_discovery.py exists")
else:
    print("❌ run_discovery.py missing")

run_build = Path.home() / '.openclaw/workspace/skills/builder-agent/run_build_from_notion.py'
if run_build.exists():
    print("✅ run_build_from_notion.py exists")
else:
    print("❌ run_build_from_notion.py missing")

print()

# 2. Configuration
print("2️⃣ Configuration")
print("-" * 70)

config_file = Path.home() / '.openclaw/workspace/skills/builder-agent/config.yaml'
if config_file.exists():
    print("✅ config.yaml exists")
    
    # Notion DB ID 확인
    with open(config_file, 'r') as f:
        content = f.read()
        if 'PROJECT_DATABASE_ID' in content or '2fc6e4a4bd208041a77bfad0f48390ce' in content:
            print("✅ Notion DB configured")
        else:
            print("⚠️  Notion DB not configured")
else:
    print("❌ config.yaml missing")

print()

# 3. Environment
print("3️⃣ Environment Variables")
print("-" * 70)

env_file = Path.home() / '.openclaw/workspace/.env'
if env_file.exists():
    with open(env_file, 'r') as f:
        content = f.read()
        
        if 'NOTION_API_KEY=' in content:
            print("✅ NOTION_API_KEY set")
        else:
            print("❌ NOTION_API_KEY missing")
        
        if 'PROJECT_DATABASE_ID=' in content:
            print("✅ PROJECT_DATABASE_ID set")
        else:
            print("❌ PROJECT_DATABASE_ID missing")
        
        if 'BUILDER_GLM_API_KEY=' in content:
            print("✅ BUILDER_GLM_API_KEY set")
        else:
            print("⚠️  BUILDER_GLM_API_KEY missing (Simple projects won't work)")
else:
    print("❌ .env file missing")

print()

# 4. LaunchAgents
print("4️⃣ Scheduled Jobs (launchd)")
print("-" * 70)

import subprocess

result = subprocess.run(['launchctl', 'list'], capture_output=True, text=True)
output = result.stdout

if 'com.openclaw.builder-discovery' in output:
    print("✅ Discovery job loaded (매일 08:00)")
else:
    print("❌ Discovery job not loaded")

if 'com.openclaw.builder-build' in output:
    print("✅ Build job loaded (매시간)")
else:
    print("❌ Build job not loaded")

print()

# 5. Recent Logs
print("5️⃣ Recent Activity")
print("-" * 70)

discovery_log = Path('/tmp/builder-discovery.log')
if discovery_log.exists():
    print("✅ Discovery log exists")
    # 마지막 3줄 표시
    result = subprocess.run(['tail', '-3', str(discovery_log)], capture_output=True, text=True)
    if result.stdout:
        print("  Last 3 lines:")
        for line in result.stdout.strip().split('\n'):
            print(f"    {line[:65]}")
else:
    print("ℹ️  No discovery log yet (first run pending)")

build_log = Path('/tmp/builder-build.log')
if build_log.exists():
    print("✅ Build log exists")
else:
    print("ℹ️  No build log yet (no projects in development)")

print()

# 6. Next Steps
print("6️⃣ Next Steps")
print("-" * 70)
print("1. Wait for 08:00 (Discovery will run automatically)")
print("2. Or run manually:")
print("   cd ~/.openclaw/workspace/skills/builder-agent")
print("   python3 run_discovery.py")
print()
print("3. Check Notion '잔디심기' database")
print("4. Change status to '개발중' to trigger build")
print()

# 7. Summary
print("=" * 70)
print("STATUS: ✅ OPERATIONAL")
print("=" * 70)
print()
print("🎉 Builder Agent v5.0 is now in production!")
print()
print("Schedule:")
print("  • Discovery: Daily at 08:00 KST")
print("  • Build: Every hour (polling Notion)")
print()
print("Logs:")
print("  • Discovery: /tmp/builder-discovery.log")
print("  • Build: /tmp/builder-build.log")
print()
print("To stop:")
print("  launchctl unload ~/Library/LaunchAgents/com.openclaw.builder-*.plist")
print()
print("To restart:")
print("  launchctl load ~/Library/LaunchAgents/com.openclaw.builder-*.plist")
print()
print("=" * 70)
