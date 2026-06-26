#!/usr/bin/env python3
"""Search Apollo for decision-makers by title, keywords, and location."""

import argparse, json, csv, subprocess, sys, os

APOLLO_KEY = os.environ.get('APOLLO_API_KEY', '')

def search(titles, keywords, location, page=1, per_page=100):
    payload = {
        "q_organization_keyword_tags": keywords.split(","),
        "person_titles": titles.split(","),
        "person_locations": [location],
        "per_page": per_page,
        "page": page
    }
    r = subprocess.run([
        'curl', '-s', '-X', 'POST',
        'https://api.apollo.io/api/v1/mixed_people/api_search',
        '-H', f'X-Api-Key: {APOLLO_KEY}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(payload)
    ], capture_output=True, text=True)
    return json.loads(r.stdout)

def main():
    parser = argparse.ArgumentParser(description='Search Apollo for leads')
    parser.add_argument('--titles', required=True, help='Comma-separated job titles')
    parser.add_argument('--keywords', required=True, help='Comma-separated org keywords')
    parser.add_argument('--location', required=True, help='Location string')
    parser.add_argument('--max', type=int, default=100, help='Max results')
    parser.add_argument('--output', default='leads-raw.csv', help='Output CSV')
    args = parser.parse_args()

    if not APOLLO_KEY:
        print("Set APOLLO_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    all_people = []
    pages = (args.max // 100) + 1
    
    for page in range(1, pages + 1):
        data = search(args.titles, args.keywords, args.location, page=page)
        people = data.get('people', [])
        total = data.get('total_entries', 0)
        all_people.extend(people)
        print(f"Page {page}: {len(people)} results (total available: {total})", file=sys.stderr)
        if len(people) < 100:
            break

    # Save to CSV
    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'first_name', 'title', 'organization', 'has_email'])
        writer.writeheader()
        for p in all_people[:args.max]:
            writer.writerow({
                'id': p.get('id', ''),
                'first_name': p.get('first_name', ''),
                'title': p.get('title', ''),
                'organization': (p.get('organization') or {}).get('name', ''),
                'has_email': p.get('has_email', False)
            })

    print(f"Saved {min(len(all_people), args.max)} leads to {args.output}", file=sys.stderr)

if __name__ == '__main__':
    main()
