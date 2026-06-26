#!/usr/bin/env python3
import argparse
import json
import requests
from bs4 import BeautifulSoup
import urllib.parse

def search_patents(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://patents.google.com/?q={encoded_query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, 'lxml')
    results = []
    for item in soup.find_all('search-result-item'):
        title_tag = item.select_one('h2')
        title = title_tag.text.strip() if title_tag else 'No title'
        id_tag = item.select_one('div#wrapper a.style-scope.search-result-item')
        patent_id = id_tag.text.strip() if id_tag else 'No ID'
        results.append({"title": title, "id": patent_id})
    return results

def combine_patents(patents1, patents2):
    seen = set()
    all_patents = []
    for p in patents1 + patents2:
        if p['id'] not in seen:
            seen.add(p['id'])
            all_patents.append(p)
    return all_patents

def main():
    parser = argparse.ArgumentParser(description="Patent Scout for molecules")
    parser.add_argument('--candidates', required=True, help='Path to JSON file with list of dicts containing "smiles" and optional "name"')
    parser.add_argument('--target', required=True, help='Target indication, e.g., "painkiller"')
    args = parser.parse_args()

    with open(args.candidates, 'r') as f:
        candidates = json.load(f)

    output = {}
    for cand in candidates:
        mol = cand['smiles']
        name = cand.get('name', '')
        search_term = name if name else mol
        query1 = f"patent {search_term} synthesis"
        query2 = f"{search_term} {args.target}"
        patents1 = search_patents(query1)
        patents2 = search_patents(query2)
        all_patents = combine_patents(patents1, patents2)
        num = len(all_patents)
        novelty_score = max(0, 10 - num)  # Simple: 0 patents =10, 10+ =0
        blocking = num > 0  # Any prior art is potentially blocking for simplicity
        output[mol] = {
            "patents": all_patents,
            "novelty_score": novelty_score,
            "blocking": blocking
        }

    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
