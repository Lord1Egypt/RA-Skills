#!/usr/bin/env python3
"""Enrich Apollo search results to get verified emails."""

import argparse, json, csv, subprocess, sys, os, time

APOLLO_KEY = os.environ.get('APOLLO_API_KEY', '')

def enrich_by_id(person_id):
    r = subprocess.run([
        'curl', '-s', '-X', 'POST',
        'https://api.apollo.io/api/v1/people/match',
        '-H', f'X-Api-Key: {APOLLO_KEY}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({'id': person_id})
    ], capture_output=True, text=True)
    return json.loads(r.stdout).get('person', {})

def main():
    parser = argparse.ArgumentParser(description='Enrich Apollo leads with emails')
    parser.add_argument('--input', required=True, help='Input CSV from apollo-search.py')
    parser.add_argument('--output', default='leads-enriched.csv', help='Output CSV')
    parser.add_argument('--max', type=int, default=None, help='Max enrichments (saves credits)')
    args = parser.parse_args()

    if not APOLLO_KEY:
        print("Set APOLLO_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Read input
    leads = []
    with open(args.input) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('has_email', '').lower() == 'true':
                leads.append(row)

    if args.max:
        leads = leads[:args.max]

    print(f"Enriching {len(leads)} leads with email flag...", file=sys.stderr)

    enriched = []
    for i, lead in enumerate(leads):
        person = enrich_by_id(lead['id'])
        email = person.get('email')
        if email:
            enriched.append({
                'name': person.get('name', ''),
                'email': email,
                'title': person.get('title', ''),
                'organization': (person.get('organization') or {}).get('name', ''),
                'city': person.get('city', ''),
                'state': person.get('state', ''),
                'country': person.get('country', '')
            })
        if (i + 1) % 10 == 0:
            print(f"  {i+1}/{len(leads)} processed, {len(enriched)} emails found", file=sys.stderr)

    # Save
    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'email', 'title', 'organization', 'city', 'state', 'country'])
        writer.writeheader()
        writer.writerows(enriched)

    print(f"\n✅ {len(enriched)} verified emails saved to {args.output}", file=sys.stderr)
    print(f"Credits used: ~{len(leads)}", file=sys.stderr)

if __name__ == '__main__':
    main()
