#!/usr/bin/env python3
"""
Batch Import - Batch add multiple papers to Zotero
"""
import argparse
import os
import sys
import urllib.request
import urllib.parse
import json
import re
import time

# Zotero API configuration
API_KEY = os.environ.get('ZOTERO_API_KEY')
USER_ID = os.environ.get('ZOTERO_USER_ID')
API_BASE = "https://api.zotero.org"

def get_paper_metadata(pmid):
    """Fetch paper metadata from PubMed"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
    
    with urllib.request.urlopen(url, timeout=30) as response:
        content = response.read().decode('utf-8')
    
    title_match = re.search(r'<ArticleTitle>([^<]+)</ArticleTitle>', content)
    title = title_match.group(1).strip() if title_match else ""
    
    journal_match = re.search(r'<Journal><Title>([^<]+)</Title>', content)
    journal = journal_match.group(1).strip() if journal_match else ""
    
    year_match = re.search(r'<PubDate>\s*<Year>(\d{4})</Year>', content)
    year = year_match.group(1) if year_match else ""
    
    vol_match = re.search(r'<JournalIssue[^>]*>\s*<Volume>([^<]+)</Volume>', content)
    volume = vol_match.group(1).strip() if vol_match else ""
    
    issue_match = re.search(r'<JournalIssue[^>]*>\s*<Issue>([^<]+)</Issue>', content)
    issue = issue_match.group(1).strip() if issue_match else ""
    
    pages_match = re.search(r'<Pagination>\s*<MedlinePgn>([^<]+)</MedlinePgn>', content)
    pages = pages_match.group(1).strip() if pages_match else ""
    
    author_list = re.findall(r'<Author[^>]*>.*?<LastName>([^<]+)</LastName>.*?<ForeName>([^<]+)</ForeName>', content, re.DOTALL)
    authors = [{"lastName": last, "firstName": first} for last, first in author_list]
    
    doi_match = re.search(r'ArticleId IdType="doi">([^<]+)</ArticleId', content)
    doi = doi_match.group(1).strip() if doi_match else ""
    
    return {
        'title': title,
        'journal': journal,
        'year': year,
        'volume': volume,
        'issue': issue,
        'pages': pages,
        'authors': authors,
        'doi': doi,
        'pmid': pmid
    }

def add_to_zotero(metadata):
    """Add paper to Zotero library"""
    if not (API_KEY and USER_ID):
        return False
    
    item = {
        'itemType': 'journalArticle',
        'title': metadata['title'],
        'creators': metadata['authors'],
        'publicationTitle': metadata['journal'],
        'date': metadata['year'],
        'volume': metadata['volume'],
        'issue': metadata['issue'],
        'pages': metadata['pages'],
        'DOI': metadata['doi'],
        'accessionNumber': metadata['pmid'],
        'libraryCatalog': 'PubMed'
    }
    
    item = {k: v for k, v in item.items() if v}
    
    url = f"{API_BASE}/users/{USER_ID}/items"
    
    req = urllib.request.Request(url, data=json.dumps([item]).encode('utf-8'))
    req.add_header('Zotero-API-Key', API_KEY)
    req.add_header('Zotero-API-Version', '3')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
            return data.get('successful', {}) != {}
    except:
        return False

def main():
    parser = argparse.ArgumentParser(description='Batch add papers to Zotero')
    parser.add_argument('--pmids', required=True, help='Comma-separated list of PMIDs')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    
    args = parser.parse_args()
    
    pmids = [p.strip() for p in args.pmids.split(',') if p.strip()]
    
    print(f"Adding {len(pmids)} papers to Zotero...")
    
    added = 0
    failed = 0
    
    for i, pmid in enumerate(pmids, 1):
        print(f"[{i}/{len(pmids)}] Processing PMID {pmid}...", end=" ")
        
        try:
            metadata = get_paper_metadata(pmid)
            if metadata['title']:
                if add_to_zotero(metadata):
                    print("✓ Added")
                    added += 1
                else:
                    print("✗ Failed")
                    failed += 1
            else:
                print("✗ Not found")
                failed += 1
        except Exception as e:
            print(f"✗ Error: {e}")
            failed += 1
        
        if i < len(pmids):
            time.sleep(args.delay)
    
    print(f"\nDone: {added} added, {failed} failed")

if __name__ == '__main__':
    main()
