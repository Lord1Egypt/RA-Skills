#!/usr/bin/env python3
"""Prepare for upcoming call."""
import json
import os
import argparse

CALLS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/calls")

def load_calls():
    calls_file = os.path.join(CALLS_DIR, "calls.json")
    if os.path.exists(calls_file):
        with open(calls_file, 'r') as f:
            return json.load(f)
    return {"calls": []}

def main():
    parser = argparse.ArgumentParser(description='Prepare for call')
    parser.add_argument('--contact', required=True, help='Contact name/company')
    parser.add_argument('--purpose', help='Call purpose')
    
    args = parser.parse_args()
    
    print(f"\n📞 CALL PREPARATION: {args.contact}")
    print("=" * 60)
    
    if args.purpose:
        print(f"Purpose: {args.purpose}")
        print()
    
    # Load previous calls
    data = load_calls()
    previous_calls = [c for c in data.get('calls', []) if c.get('contact') == args.contact]
    
    if previous_calls:
        print(f"PREVIOUS CALLS: {len(previous_calls)}")
        print("-" * 40)
        
        # Show last 3 calls
        for call in sorted(previous_calls, key=lambda x: x.get('date', ''), reverse=True)[:3]:
            print(f"\nDate: {call.get('date', 'Unknown')}")
            if call.get('summary'):
                print(f"Summary: {call['summary'][:100]}...")
            if call.get('commitments'):
                print("Commitments:")
                for c in call['commitments']:
                    print(f"  • {c}")
    else:
        print("No previous calls found with this contact.")
    
    print("\n" + "=" * 60)
    print("PREPARATION CHECKLIST:")
    print("☐ Review previous call notes")
    print("☐ Check open commitments")
    print("☐ Define what you want to accomplish")
    print("☐ Prepare 2-3 key questions")
    print("☐ Have relevant documents ready")

if __name__ == '__main__':
    main()
