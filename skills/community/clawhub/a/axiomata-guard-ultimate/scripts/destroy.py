#!/usr/bin/env python3
"""
Axioma Guard Ultimate - Destroy Dangerous Skill
Rejects and destroys dangerous skills
"""

import sys
import os
import shutil
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 destroy.py <skill-path> --confirm")
        sys.exit(1)
    
    if "--confirm" not in sys.argv:
        print("⚠️ WARNING: This will DESTROY the skill!")
        print("Add --confirm to proceed")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    skill_name = os.path.basename(skill_path)
    
    print("=" * 60)
    print("🚨 AXIOMA GUARD ULTIMATE - DESTROY PROTOCOL")
    print("=" * 60)
    print(f"\n⚠️ SKILL: {skill_name}")
    print("⚠️ ACTION: REJECT AND DESTROY")
    print("⚠️ REASON: Dangerous skill detected")
    
    # Quarantine
    quarantine_dir = "/tmp/quarantine/axiomata-guard-ultimate"
    os.makedirs(quarantine_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    quarantine_path = f"{quarantine_dir}/{skill_name}_{timestamp}"
    
    print(f"\n[1] Moving to quarantine: {quarantine_path}")
    shutil.move(skill_path, quarantine_path)
    
    # Log
    threat_log = os.path.expanduser("~/axiomata-guard-ultimate-threats.log")
    with open(threat_log, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] THREAT DETECTED: {skill_name} | DESTROYED\n")
    
    print(f"[2] Logged to: {threat_log}")
    
    # Destroy
    print(f"\n[3] Destroying...")
    shutil.rmtree(quarantine_path)
    
    print("\n" + "=" * 60)
    print("✅ DESTROY COMPLETE")
    print(f"✅ Skill {skill_name} has been destroyed")
    print("=" * 60)

if __name__ == "__main__":
    main()
