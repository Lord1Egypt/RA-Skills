#!/usr/bin/env python3
"""
Generate RIS - Generate RIS file for EndNote import
"""
import argparse
import sys
import urllib.request
import re

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
    author_str = ", ".join([f"{last}, {first[0]}." for last, first in author_list[:10]])
    if len(author_list) > 10:
        author_str += " et al."
    
    doi_match = re.search(r'ArticleId IdType="doi">([^<]+)</ArticleId', content)
    doi = doi_match.group(1).strip() if doi_match else ""
    
    return {
        'title': title,
        'journal': journal,
        'year': year,
        'volume': volume,
        'issue': issue,
        'pages': pages,
        'authors': author_str,
        'doi': doi,
        'pmid': pmid
    }

def generate_ris(papers):
    """Generate RIS format content"""
    ris = ""
    
    for paper in papers:
        ris += "TY  - JOUR\n"
        ris += f"TI  - {paper['title']}\n"
        ris += f"JO  - {paper['journal']}\n"
        ris += f"PY  - {paper['year']}\n"
        if paper['volume']:
            ris += f"VL  - {paper['volume']}\n"
        if paper['issue']:
            ris += f"IS  - {paper['issue']}\n"
        if paper['pages']:
            ris += f"SP  - {paper['pages']}\n"
        if paper['authors']:
            ris += f"AU  - {paper['authors']}\n"
        if paper['doi']:
            ris += f"DO  - {paper['doi']}\n"
        ris += f"AN  - PMID:{paper['pmid']}\n"
        ris += "ER  - \n\n"
    
    return ris

def main():
    parser = argparse.ArgumentParser(description='Generate RIS file for EndNote')
    parser.add_argument('--pmids', required=True, help='Comma-separated list of PMIDs')
    parser.add_argument('--output', default='literature.ris', help='Output RIS file')
    
    args = parser.parse_args()
    
    pmids = [p.strip() for p in args.pmids.split(',') if p.strip()]
    
    print(f"Fetching metadata for {len(pmids)} papers...")
    
    papers = []
    for i, pmid in enumerate(pmids, 1):
        print(f"[{i}/{len(pmids)}] PMID {pmid}...", end=" ")
        try:
            paper = get_paper_metadata(pmid)
            if paper['title']:
                print("✓")
                papers.append(paper)
            else:
                print("✗ Not found")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    if not papers:
        print("No papers found")
        sys.exit(1)
    
    # Generate RIS
    ris_content = generate_ris(papers)
    
    # Write to file
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(ris_content)
    
    print(f"\n✓ Saved to {args.output} ({len(papers)} records)")
    print("\nTo import to EndNote:")
    print("  1. Open EndNote")
    print("  2. File → Import → File...")
    print(f"  3. Select '{args.output}'")
    print("  4. Import Option: Reference Manager (RIS)")
    print("  5. Click Import")

if __name__ == '__main__':
    main()
