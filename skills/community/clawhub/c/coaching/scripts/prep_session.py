#!/usr/bin/env python3
"""Prepare for coaching session."""
import json
import os
import uuid
import argparse
from datetime import datetime

COACHING_DIR = os.path.expanduser("~/.openclaw/workspace/memory/coaching")

def ensure_dir():
    os.makedirs(COACHING_DIR, exist_ok=True)

def load_client_data(client_name):
    """Load client data from isolated storage."""
    client_file = os.path.join(COACHING_DIR, f"{client_name.lower().replace(' ', '_')}.json")
    if os.path.exists(client_file):
        with open(client_file, 'r') as f:
            return json.load(f)
    return {"sessions": [], "goals": [], "commitments": []}

def main():
    parser = argparse.ArgumentParser(description='Prepare coaching session')
    parser.add_argument('--client', required=True, help='Client name')
    parser.add_argument('--session', type=int, help='Session number')
    
    args = parser.parse_args()
    
    print(f"\n🎯 SESSION PREP: {args.client}")
    print("=" * 60)
    
    # Load client data
    client_data = load_client_data(args.client)
    
    # Show previous session summary
    if client_data.get('sessions'):
        last_session = client_data['sessions'][-1]
        print("\nPREVIOUS SESSION:")
        print(f"Date: {last_session.get('date', 'Unknown')}")
        print(f"Key Insights: {last_session.get('insights', 'N/A')}")
        print()
    
    # Show commitments
    if client_data.get('commitments'):
        print("COMMITMENTS CHECK:")
        for commitment in client_data['commitments']:
            status = commitment.get('status', 'pending')
            print(f"  [{'✓' if status == 'complete' else '○'}] {commitment.get('action', '')}")
        print()
    
    # Generate questions
    print("POWERFUL QUESTIONS TO CONSIDER:")
    questions = [
        "What's the real challenge here for you?",
        "What would you do if you knew you couldn't fail?",
        "What has held you back from addressing this before?",
        "What would success look like in this area?",
        "Who do you need to become to achieve this?"
    ]
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
    
    print("\n💡 Remember: Hold space. Listen deeply. Trust the process.")

if __name__ == '__main__':
    main()
