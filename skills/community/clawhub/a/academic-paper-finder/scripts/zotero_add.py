#!/usr/bin/env python3
"""
Zotero Add - Add papers to Zotero by PMID or DOI
"""
import argparse
import os
import sys
import urllib.request
import urllib.parse
import json
import re

# Zotero API configuration
API_KEY = os.environ.get('ZOTERO_API_KEY')
USER_ID = os.environ.get('ZOTERO_USER_ID')
API_BASE = "https://api.zotero.org"

def get_paper_metadata(pmid):
    """Fetch paper metadata from PubMed"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
    
    with urllib.request.urlopen(url, timeout=30) as response:
        content = response.read().decode('utf-8')
    
    # Parse XML
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

def search_doi_to_pmid(doi):
    """Convert DOI to PMID"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(doi)}&retmode=json"
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        results = data.get('esearchresult', {}).get('idlist', [])
        return results[0] if results else None

def check_duplicate(doi, pmid):
    """Check if paper already exists in Zotero library"""
    if not (API_KEY and USER_ID):
        return False
    
    # Search by DOI or PMID
    query = f"doi:{doi}" if doi else f"pmid:{pmid}"
    url = f"{API_BASE}/users/{USER_ID}/items?q={urllib.parse.quote(query)}"
    
    req = urllib.request.Request(url)
    req.add_header('Zotero-API-Key', API_KEY)
    req.add_header('Zotero-API-Version', '3')
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
            return len(data) > 0
    except:
        return False

def add_to_zotero(metadata):
    """Add paper to Zotero library"""
    if not (API_KEY and USER_ID):
        print("Error: ZOTERO_API_KEY and ZOTERO_USER_ID not set", file=sys.stderr)
        sys.exit(1)
    
    # Build item data
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
    
    # Remove empty fields
    item = {k: v for k, v in item.items() if v}
    
    url = f"{API_BASE}/users/{USER_ID}/items"
    
    req = urllib.request.Request(url, data=json.dumps([item]).encode('utf-8'))
    req.add_header('Zotero-API-Key', API_KEY)
    req.add_header('Zotero-API-Version', '3')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
            if data.get('successful'):
                key = list(data['successful'].keys())[0]
                print(f"✓ Added to Zotero: {metadata['title'][:50]}...")
                print(f"  Key: {key}")
                return True
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode()}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
    
    return False

def main():
    parser = argparse.ArgumentParser(description='Add paper to Zotero')
    parser.add_argument('--pmid', help='PubMed ID')
    parser.add_argument('--doi', help='DOI (will lookup PMID)')
    parser.add_argument('--force', action='store_true', help='Skip duplicate check')
    
    args = parser.parse_args()
    
    pmid = args.pmid
    
    # If DOI provided, get PMID
    if args.doi:
        print(f"Looking up PMID for DOI: {args.doi}")
        pmid = search_doi_to_pmid(args.doi)
        if not pmid:
            print("Error: Could not find PMID for DOI", file=sys.stderr)
            sys.exit(1)
        print(f"Found PMID: {pmid}")
    
    if not pmid:
        print("Error: Please specify --pmid or --doi", file=sys.stderr)
        sys.exit(1)
    
    # Check for duplicates
    if not args.force:
        metadata = get_paper_metadata(pmid)
        if check_duplicate(metadata.get('doi'), pmid):
            print(f"Paper already in Zotero library (PMID: {pmid})")
            sys.exit(0)
    
    # Get metadata
    print(f"Fetching metadata for PMID: {pmid}")
    metadata = get_paper_metadata(pmid)
    
    if not metadata['title']:
        print("Error: Could not fetch paper metadata", file=sys.stderr)
        sys.exit(1)
    
    # Add to Zotero
    add_to_zotero(metadata)

if __name__ == '__main__':
    main()
