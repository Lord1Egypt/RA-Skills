#!/usr/bin/env python3
"""Check warmup status and health scores for all Saleshandy email accounts."""

import json, subprocess, sys, os

SH_API_KEY = os.environ.get('SALESHANDY_API_KEY', '')
BASE = 'https://open-api.saleshandy.com'

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Check email account warmup status')
    parser.add_argument('--api-key', help='Saleshandy API key')
    args = parser.parse_args()

    global SH_API_KEY
    if args.api_key:
        SH_API_KEY = args.api_key
    if not SH_API_KEY:
        print("Set SALESHANDY_API_KEY or use --api-key", file=sys.stderr)
        sys.exit(1)

    r = subprocess.run([
        'curl', '-s', '-X', 'POST', f'{BASE}/v1/email-accounts',
        '-H', f'x-api-key: {SH_API_KEY}',
        '-H', 'Accept: application/json',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({"page": 1, "pageSize": 50})
    ], capture_output=True, text=True)

    data = json.loads(r.stdout)
    emails = data.get('payload', {}).get('emails', [])

    ready_count = 0
    print(f"{'Email':45s} | {'Score':>5s} | {'Status':>12s} | Provider")
    print("-" * 85)

    for e in emails:
        score = e.get('healthScore', 0)
        status = 'CONNECTED' if e['status'] == 1 else 'DISCONNECTED'
        provider = e.get('emailServiceProvider', '?')
        ready = '✅' if score >= 85 else '⏳'
        if score >= 85:
            ready_count += 1
        print(f"{e['fromEmail']:45s} | {score:>5} | {status:>12s} | {provider} {ready}")

    print(f"\n{ready_count}/{len(emails)} accounts ready for sending (score >= 85)")
    
    if ready_count < len(emails):
        print("\n⚠️  Wait for all accounts to reach 85+ before activating sequences.")
        print("   Warmup typically takes 7-14 days from account creation.")
    else:
        print("\n🚀 All accounts ready! Safe to activate sequences.")

if __name__ == '__main__':
    main()
