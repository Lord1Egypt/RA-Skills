#!/usr/bin/env python3
"""Import enriched leads into a Saleshandy sequence step."""

import argparse, json, csv, subprocess, sys, os, time

SH_API_KEY = os.environ.get('SALESHANDY_API_KEY', '')
BASE = 'https://open-api.saleshandy.com'

def sh_api(method, endpoint, data=None):
    cmd = ['curl', '-s', '-X', method, f'{BASE}{endpoint}',
           '-H', f'x-api-key: {SH_API_KEY}', '-H', 'Accept: application/json']
    if data:
        cmd += ['-H', 'Content-Type: application/json', '-d', json.dumps(data)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(r.stdout)

def list_sequences():
    return sh_api('GET', '/v1/sequences')

def import_prospects(step_id, prospects, verify=True):
    payload = {
        "prospectList": prospects,
        "stepId": step_id,
        "verifyProspects": verify,
        "conflictAction": "noUpdate"
    }
    return sh_api('POST', '/v1/sequences/prospects/import-with-field-name', payload)

def main():
    parser = argparse.ArgumentParser(description='Import leads to Saleshandy')
    parser.add_argument('--csv', required=True, help='CSV with name,email,title,organization columns')
    parser.add_argument('--step-id', help='Saleshandy step ID (omit to list sequences)')
    parser.add_argument('--api-key', help='Saleshandy API key (or set SALESHANDY_API_KEY)')
    parser.add_argument('--batch-size', type=int, default=50, help='Import batch size')
    args = parser.parse_args()

    global SH_API_KEY
    if args.api_key:
        SH_API_KEY = args.api_key
    if not SH_API_KEY:
        print("Set SALESHANDY_API_KEY or use --api-key", file=sys.stderr)
        sys.exit(1)

    if not args.step_id:
        print("Available sequences:", file=sys.stderr)
        data = list_sequences()
        for seq in data.get('payload', []):
            print(f"  {seq['title']} (ID: {seq['id']}, Steps: {len(seq.get('steps', []))})")
            for step in seq.get('steps', []):
                print(f"    Step: {step['name']} (ID: {step['id']})")
        return

    # Read CSV
    prospects = []
    with open(args.csv) as f:
        for row in csv.DictReader(f):
            if row.get('email'):
                name_parts = row.get('name', '').split(' ', 1)
                prospects.append({
                    "First Name": name_parts[0] if name_parts else '',
                    "Last Name": name_parts[1] if len(name_parts) > 1 else '',
                    "Email": row['email'],
                    "Company": row.get('organization', ''),
                    "Job Title": row.get('title', ''),
                })

    print(f"Importing {len(prospects)} prospects...", file=sys.stderr)

    total = 0
    for i in range(0, len(prospects), args.batch_size):
        batch = prospects[i:i + args.batch_size]
        result = import_prospects(args.step_id, batch)
        req_id = result.get('payload', {}).get('requestId', '?')
        total += len(batch)
        print(f"  Batch {i}-{i+len(batch)}: → requestId: {req_id}", file=sys.stderr)
        time.sleep(1)

    print(f"\n✅ {total} prospects imported", file=sys.stderr)

if __name__ == '__main__':
    main()
