#!/usr/bin/env python3
"""
verify.py — Fact-check podcast script against research sources

Cross-references every claim in the script against research sources.
Blocks audio generation if unverified claims are found.

Usage:
    verify.py --script script.txt --research research.json --output verification.json
"""
import sys
import os
import json
import re
import argparse
from pathlib import Path


def extract_citations(script_text: str) -> set:
    """Extract all [Source: URL] citations from script"""
    citations = re.findall(r'\[Source:\s*(https?://[^\]]+)\]', script_text)
    unique = set()
    for url in citations:
        unique.add(url)
        # Also add without query params for matching
        unique.add(url.split('?')[0])
    return unique


def extract_research_urls(research: dict) -> set:
    """Extract all source URLs from research JSON"""
    urls = set()
    for source in research.get("sources", []):
        url = source.get("url", "")
        if url:
            urls.add(url)
            urls.add(url.split('?')[0])  # Add without query params
    
    # Also check other fields
    for stat in research.get("key_statistics", []):
        url = stat.get("source_url", "")
        if url:
            urls.add(url)
            urls.add(url.split('?')[0])
    
    for event in research.get("timeline", []):
        url = event.get("source_url", "")
        if url:
            urls.add(url)
            urls.add(url.split('?')[0])
    
    return urls


def extract_claims(script_text: str) -> list:
    """Extract factual claims (sentences with numbers, stats, dates)"""
    claim_patterns = [
        r'[^.]*\$[\d,]+[^.]*\.',                          # Dollar amounts
        r'[^.]*\d+%[^.]*\.',                               # Percentages
        r'[^.]*\d{4}[^.]*\.',                              # Years
        r'[^.]*\d+\s*(billion|million|thousand|trillion)[^.]*\.',  # Large numbers
        r'[^.]*according to[^.]*\.',                       # Attribution
        r'[^.]*research\s+(shows|found|suggests)[^.]*\.', # Research claims
        r'[^.]*study\s+(found|shows|published)[^.]*\.',   # Study claims
    ]
    
    claims = []
    for pattern in claim_patterns:
        matches = re.findall(pattern, script_text, re.IGNORECASE)
        if isinstance(matches, list):
            for m in matches:
                if isinstance(m, str) and len(m) > 20:
                    claims.append(m.strip())
    
    return list(set(claims))  # Deduplicate


def check_nearby_citations(script_text: str, claims: list) -> list:
    """Check if claims have nearby citations"""
    uncited = []
    for claim in claims:
        pos = script_text.find(claim)
        if pos == -1:
            continue
        
        # Check 500 chars after claim for citation
        nearby = script_text[pos:pos + len(claim) + 500]
        if "[Source:" not in nearby:
            uncited.append(claim[:200])  # Truncate for report
    
    return uncited


def main():
    """Main entry point for fact verification"""
    parser = argparse.ArgumentParser(description="Verify podcast script facts")
    parser.add_argument("--script", required=True, help="Script text file")
    parser.add_argument("--research", required=True, help="Research JSON file")
    parser.add_argument("--output", required=True, help="Verification report JSON")
    args = parser.parse_args()
    
    print(f"=== FACT VERIFICATION ===")
    print(f"Script: {args.script}")
    print(f"Research: {args.research}")
    print()
    
    # Load files
    with open(args.script) as f:
        script_text = f.read()
    
    with open(args.research) as f:
        research = json.load(f)
    
    # Extract data
    script_citations = extract_citations(script_text)
    research_urls = extract_research_urls(research)
    claims = extract_claims(script_text)
    
    print(f"Script citations: {len(script_citations)}")
    print(f"Research URLs: {len(research_urls)}")
    print(f"Factual claims found: {len(claims)}")
    print()
    
    # Verify citations
    verified_cites = []
    unverified_cites = []
    
    for cite in script_citations:
        cite_base = cite.split('?')[0]
        if cite in research_urls or cite_base in research_urls:
            verified_cites.append(cite)
        else:
            unverified_cites.append(cite)
    
    # Check claims have nearby citations
    uncited_claims = check_nearby_citations(script_text, claims)
    
    # Build report
    report = {
        "date": Path(args.script).stem,
        "script_file": args.script,
        "research_file": args.research,
        "total_citations": len(script_citations),
        "verified_citations": len(verified_cites),
        "unverified_citations": unverified_cites,
        "total_factual_claims": len(claims),
        "uncited_claims": uncited_claims[:20],  # Cap at 20
        "pass": len(unverified_cites) == 0 and len(uncited_claims) == 0,
        "summary": ""
    }
    
    if report["pass"]:
        report["summary"] = f"✅ PASSED: {len(verified_cites)} citations verified, {len(claims)} claims all sourced"
        print(report["summary"])
    else:
        issues = []
        if unverified_cites:
            issues.append(f"{len(unverified_cites)} citations not in research")
        if uncited_claims:
            issues.append(f"{len(uncited_claims)} claims without nearby citations")
        report["summary"] = f"❌ FAILED: {'; '.join(issues)}"
        print(report["summary"])
        
        if unverified_cites:
            print("\n⚠️  UNVERIFIED CITATIONS:")
            for cite in unverified_cites[:5]:
                print(f"  - {cite}")
        
        if uncited_claims:
            print("\n⚠️  UNCITED CLAIMS (first 5):")
            for claim in uncited_claims[:5]:
                print(f"  - {claim[:100]}...")
    
    # Save report
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Verification report saved to: {args.output}")
    
    # Exit code
    sys.exit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()
