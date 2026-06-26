#!/usr/bin/env python3
"""
PubMed Search - Search PubMed by DOI, title, or author with citation counts
"""
import argparse
import json
import sys
import urllib.request
import urllib.parse
import re

def search_by_doi(doi):
    """Search PubMed by DOI"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(doi)}&retmode=json"
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        return data.get('esearchresult', {}).get('idlist', [])

def search_by_title(title, retmax=20):
    """Search PubMed by title"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(title)}&retmode=json&retmax={retmax}&sort=relevance"
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        return data.get('esearchresult', {}).get('idlist', [])

def search_by_author(author, year=None, retmax=20):
    """Search PubMed by author"""
    query = f"{author}[Author]"
    if year:
        query += f" AND {year}[DP]"
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(query)}&retmode=json&retmax={retmax}"
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        return data.get('esearchresult', {}).get('idlist', [])

def get_paper_details(pmids):
    """Get paper details by PMIDs including citation counts"""
    if not pmids:
        return []
    
    ids = ','.join(pmids)
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids}&retmode=json"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.load(response)
            results = data.get('result', {})
            papers = []
            for pmid in pmids:
                if pmid in results:
                    info = results[pmid]
                    # Get authors
                    authors = info.get('authors', [])[:5]
                    author_names = ', '.join([a.get('name', '') for a in authors])
                    if len(info.get('authors', [])) > 5:
                        author_names += ' et al.'
                    
                    papers.append({
                        'pmid': pmid,
                        'title': info.get('title', ''),
                        'journal': info.get('source', ''),
                        'year': info.get('pubdate', '').split()[0] if info.get('pubdate') else '',
                        'authors': author_names,
                        'doi': info.get('doi', ''),
                        'pubmed_url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    })
            return papers
    except Exception as e:
        print(f"Error fetching details: {e}", file=sys.stderr)
        return []

def get_citation_counts(pmids):
    """Get citation counts from OpenAlex"""
    if not pmids:
        return {}
    
    citation_counts = {}
    
    # OpenAlex API - free, no key needed
    for pmid in pmids:
        try:
            url = f"https://api.openalex.org/works?filter=pmid:{pmid}"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'OpenClaw/1.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.load(response)
                if data.get('results'):
                    work = data['results'][0]
                    citation_counts[pmid] = work.get('cited_by_count', 0)
                else:
                    citation_counts[pmid] = 0
        except:
            citation_counts[pmid] = 0
    
    return citation_counts

def main():
    parser = argparse.ArgumentParser(description='Search PubMed for papers')
    parser.add_argument('--doi', help='Search by DOI')
    parser.add_argument('--title', help='Search by title/keywords')
    parser.add_argument('--author', help='Search by author name')
    parser.add_argument('--year', help='Filter by year')
    parser.add_argument('--retmax', type=int, default=15, help='Max results (default: 15)')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    
    args = parser.parse_args()
    
    pmids = []
    
    if args.doi:
        pmids = search_by_doi(args.doi)
    elif args.title:
        pmids = search_by_title(args.title, args.retmax)
    elif args.author:
        pmids = search_by_author(args.author, args.year, args.retmax)
    else:
        print("Error: Please specify --doi, --title, or --author", file=sys.stderr)
        sys.exit(1)
    
    if not pmids:
        print("No results found")
        sys.exit(0)
    
    # Get paper details
    papers = get_paper_details(pmids)
    
    # Get citation counts
    print("Fetching citation counts...")
    citation_counts = get_citation_counts(pmids)
    
    # Add citation counts to papers
    for paper in papers:
        paper['citations'] = citation_counts.get(paper['pmid'], 0)
    
    # Sort by citations (descending)
    papers.sort(key=lambda x: x['citations'], reverse=True)
    
    if args.json:
        print(json.dumps(papers, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*80}")
        print(f"Found {len(papers)} results (sorted by citations):")
        print(f"{'='*80}\n")
        
        for i, paper in enumerate(papers, 1):
            citations = paper['citations']
            # Add star for highly cited papers
            stars = "⭐⭐⭐" if citations > 500 else "⭐⭐" if citations > 100 else "⭐" if citations > 10 else ""
            
            print(f"{i}. PMID: {paper['pmid']}  |  Citations: {citations} {stars}")
            print(f"   Title: {paper['title']}")
            print(f"   Journal: {paper['journal']} ({paper['year']})")
            print(f"   Authors: {paper['authors']}")
            if paper['doi']:
                print(f"   DOI: {paper['doi']}")
            print(f"   🔗 https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']}/")
            print()

if __name__ == '__main__':
    main()
