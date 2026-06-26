#!/usr/bin/env python3
"""Scope new consulting engagement."""
import json
import os
import uuid
import argparse
from datetime import datetime

CONSULTING_DIR = os.path.expanduser("~/.openclaw/workspace/memory/consulting")

def ensure_dir():
    os.makedirs(CONSULTING_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Scope engagement')
    parser.add_argument('--client', required=True, help='Client name')
    parser.add_argument('--presenting', required=True, help='Presenting problem')
    
    args = parser.parse_args()
    
    engagement_id = f"ENG-{str(uuid.uuid4())[:6].upper()}"
    
    print(f"\n📋 ENGAGEMENT SCOPING: {args.client}")
    print("=" * 60)
    print(f"Presenting Problem: {args.presenting}")
    print()
    
    print("DISCOVERY QUESTIONS:")
    print("-" * 40)
    print("1. What have you tried so far?")
    print("2. What happened when you tried that?")
    print("3. What would success look like in specific terms?")
    print("4. What is the cost of not solving this?")
    print("5. Who else is affected by this problem?")
    print("6. What has prevented you from solving this already?")
    print()
    
    print("REAL PROBLEM ANALYSIS:")
    print("-" * 40)
    print("Consider:")
    print("• Is this a symptom of a deeper issue?")
    print("• What organizational dynamics are at play?")
    print("• What is the client actually committed to changing?")
    print()
    
    # Save engagement
    engagement = {
        "id": engagement_id,
        "client": args.client,
        "presenting_problem": args.presenting,
        "real_problem": "",
        "status": "scoping",
        "created_at": datetime.now().isoformat()
    }
    
    engagements_file = os.path.join(CONSULTING_DIR, "engagements.json")
    data = {"engagements": []}
    if os.path.exists(engagements_file):
        with open(engagements_file, 'r') as f:
            data = json.load(f)
    
    data['engagements'].append(engagement)
    
    ensure_dir()
    with open(engagements_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Engagement created: {engagement_id}")

if __name__ == '__main__':
    main()
