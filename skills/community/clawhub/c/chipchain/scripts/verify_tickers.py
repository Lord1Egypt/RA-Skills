#!/usr/bin/env python3
"""
Verify semiconductor supply chain company tickers using yfinance.

Extracts all tickers from the skill's entity files, checks each one
against Yahoo Finance, and produces a verification report.

Usage:
    pip install yfinance
    python verify_tickers.py

Output: verification_report.md in the same directory
"""

import re
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _verify_common import ensure_package, find_skill_dir, write_json

ensure_package("yfinance")
import yfinance as yf  # noqa: E402


def extract_tickers_from_file(filepath: str) -> list[dict]:
    """Extract tickers and company names from a markdown file."""
    results = []
    content = Path(filepath).read_text(encoding="utf-8")

    # Pattern 1: Table rows with tickers like "4063.T", "092070.KQ", "688019.SS", "6488.TW", "002371.SZ"
    # Matches: digits + dot + exchange suffix
    ticker_pattern = re.compile(
        r'(\d{3,6}\.(T|KS|KQ|TW|TWO|SS|SZ|HK|DE))\b'
    )

    # Also capture "Parent: XXXX.T" and "sub. of XXXX" patterns
    parent_pattern = re.compile(
        r'(?:Parent|parent|sub\.|subsidiary)[:\s]+.*?(\d{3,6}\.(T|KS|KQ|TW|TWO|SS|SZ|HK|DE))'
    )

    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Skip header/comment lines and delisted tickers
        if line.strip().startswith('#') or line.strip().startswith('>'):
            continue
        if 'DELISTED' in line.upper() or 'delisted' in line:
            continue

        # Extract Asian exchange tickers
        for match in ticker_pattern.finditer(line):
            ticker = match.group(1)
            # Try to extract company name from the same table row
            company = _extract_company_from_line(line)
            results.append({
                'ticker': ticker,
                'company': company,
                'file': os.path.basename(filepath),
                'line': i + 1,
                'raw_line': line.strip()[:120]
            })

        # Extract parent tickers
        for match in parent_pattern.finditer(line):
            ticker = match.group(1)
            company = _extract_company_from_line(line)
            results.append({
                'ticker': ticker,
                'company': company + ' (parent/sub reference)',
                'file': os.path.basename(filepath),
                'line': i + 1,
                'raw_line': line.strip()[:120]
            })

    # Deduplicate by ticker
    seen = set()
    unique = []
    for r in results:
        if r['ticker'] not in seen:
            seen.add(r['ticker'])
            unique.append(r)
    return unique


def _extract_company_from_line(line: str) -> str:
    """Try to extract company name from a markdown table row."""
    # Split by | for table rows
    parts = [p.strip() for p in line.split('|') if p.strip()]
    if len(parts) >= 2:
        # Usually company name is first or second column
        # Remove markdown bold markers
        name = parts[0].replace('**', '').strip()
        if name and not name.startswith('-') and len(name) > 1:
            return name
        if len(parts) > 1:
            return parts[1].replace('**', '').strip()
    return "Unknown"


def verify_ticker_yfinance(ticker: str) -> dict:
    """Verify a single ticker against Yahoo Finance."""
    result = {
        'ticker': ticker,
        'valid': False,
        'name': None,
        'currency': None,
        'exchange': None,
        'market_cap': None,
        'error': None,
        'source': 'yfinance',
    }

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Check if we got valid data
        if info and info.get('regularMarketPrice') is not None:
            result['valid'] = True
            result['name'] = info.get('longName') or info.get('shortName', 'N/A')
            result['currency'] = info.get('currency', 'N/A')
            result['exchange'] = info.get('exchange', 'N/A')
            mc = info.get('marketCap')
            if mc:
                if mc > 1e12:
                    result['market_cap'] = f"${mc/1e12:.1f}T"
                elif mc > 1e9:
                    result['market_cap'] = f"${mc/1e9:.1f}B"
                elif mc > 1e6:
                    result['market_cap'] = f"${mc/1e6:.0f}M"
                else:
                    result['market_cap'] = f"${mc:,.0f}"
        elif info and info.get('shortName'):
            # Sometimes price is None but company exists (delisted, etc.)
            result['valid'] = False
            result['name'] = info.get('shortName', 'N/A')
            result['error'] = 'No market price (possibly delisted or suspended)'
        else:
            result['error'] = 'No data returned'

    except Exception as e:
        result['error'] = str(e)[:100]

    return result


def verify_ticker_pykrx(ticker: str) -> dict:
    """Verify a Korean ticker (.KS/.KQ) using pykrx as fallback.

    pykrx queries KRX (Korea Exchange) directly and is more reliable
    for Korean tickers than yfinance.
    """
    result = {
        'ticker': ticker,
        'valid': False,
        'name': None,
        'error': None,
        'source': 'pykrx',
    }

    try:
        ensure_package("pykrx")
        from pykrx import stock

        # Extract the numeric code (e.g., '092070' from '092070.KQ')
        code = ticker.split('.')[0]

        # pykrx uses the raw numeric code
        name = stock.get_market_ticker_name(code)
        if name:
            result['valid'] = True
            result['name'] = name
        else:
            result['error'] = 'Ticker not found on KRX'

    except Exception as e:
        result['error'] = f'pykrx error: {str(e)[:80]}'

    return result


def verify_ticker(ticker: str) -> dict:
    """Verify a ticker using yfinance primary, pykrx fallback for Korean tickers."""
    result = verify_ticker_yfinance(ticker)

    # If yfinance failed and it's a Korean ticker, try pykrx
    if not result['valid'] and any(ticker.endswith(s) for s in ('.KS', '.KQ')):
        pykrx_result = verify_ticker_pykrx(ticker)
        if pykrx_result['valid']:
            # Merge pykrx success into result
            result['valid'] = True
            result['name'] = pykrx_result['name']
            result['source'] = 'pykrx (yfinance failed)'
            result['error'] = None

    return result


def main():
    skill_dir = find_skill_dir()

    # Find all entity and skill files
    files_to_scan = []
    for pattern in ['entities/*.md', 'chemistry/*.md', 'SKILL.md', 'queries/bottleneck.md']:
        files_to_scan.extend(skill_dir.glob(pattern))

    print(f"Scanning {len(files_to_scan)} files for tickers...")

    # Extract all tickers
    all_tickers = []
    for filepath in files_to_scan:
        tickers = extract_tickers_from_file(str(filepath))
        all_tickers.extend(tickers)
        if tickers:
            print(f"  {filepath.name}: {len(tickers)} tickers found")

    # Deduplicate across files
    seen = {}
    unique_tickers = []
    for t in all_tickers:
        if t['ticker'] not in seen:
            seen[t['ticker']] = t
            unique_tickers.append(t)
        else:
            # Track which files reference this ticker
            seen[t['ticker']]['file'] += f", {t['file']}"

    print(f"\nTotal unique tickers to verify: {len(unique_tickers)}")
    print("Verifying against Yahoo Finance (this may take a few minutes)...\n")

    # Verify each ticker
    results = []
    valid_count = 0
    invalid_count = 0
    error_count = 0

    for i, t in enumerate(unique_tickers):
        ticker = t['ticker']
        print(f"  [{i+1}/{len(unique_tickers)}] {ticker} ({t['company'][:30]})...", end=" ", flush=True)

        verification = verify_ticker(ticker)
        verification['company_in_file'] = t['company']
        verification['source_file'] = t['file']
        verification['line'] = t['line']

        if verification['valid']:
            print(f"OK — {verification['name']}")
            valid_count += 1
        elif verification['error'] and 'delisted' in str(verification['error']).lower():
            print(f"DELISTED/SUSPENDED — {verification.get('name', 'N/A')}")
            invalid_count += 1
        else:
            print(f"FAILED — {verification['error']}")
            error_count += 1

        results.append(verification)

    # Generate report
    report_path = skill_dir / 'ticker_verification_report.md'
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# Ticker Verification Report\n\n")
        f.write(f"**Generated:** {now}\n")
        f.write(f"**Source:** yfinance (Yahoo Finance)\n")
        f.write(f"**Total tickers checked:** {len(results)}\n\n")
        f.write(f"| Status | Count |\n|---|---|\n")
        f.write(f"| Valid | {valid_count} |\n")
        f.write(f"| Invalid/Delisted | {invalid_count} |\n")
        f.write(f"| Error/Not Found | {error_count} |\n\n")

        # Valid tickers
        f.write(f"## Valid Tickers ({valid_count})\n\n")
        f.write("| Ticker | Yahoo Name | In File As | Market Cap | Source |\n")
        f.write("|---|---|---|---|---|\n")
        for r in sorted(results, key=lambda x: x['ticker']):
            if r['valid']:
                name_match = ""
                if r['name'] and r['company_in_file']:
                    # Simple check if names roughly match
                    ya_lower = (r['name'] or '').lower()
                    file_lower = (r['company_in_file'] or '').lower()
                    if any(w in ya_lower for w in file_lower.split()[:2] if len(w) > 2):
                        name_match = ""
                    else:
                        name_match = " ⚠️"
                f.write(f"| {r['ticker']} | {r['name']}{name_match} | {r['company_in_file'][:40]} | {r['market_cap'] or 'N/A'} | {r['source_file']} |\n")

        # Invalid/problem tickers
        if invalid_count + error_count > 0:
            f.write(f"\n## Problem Tickers ({invalid_count + error_count}) — NEED ATTENTION\n\n")
            f.write("| Ticker | In File As | Issue | Source File | Line |\n")
            f.write("|---|---|---|---|---|\n")
            for r in sorted(results, key=lambda x: x['ticker']):
                if not r['valid']:
                    issue = r['error'] or 'Unknown'
                    f.write(f"| {r['ticker']} | {r['company_in_file'][:40]} | {issue[:60]} | {r['source_file']} | {r['line']} |\n")

        # Name mismatches (valid but possibly wrong company)
        f.write(f"\n## Name Verification (check these manually)\n\n")
        f.write("Tickers where Yahoo Finance name differs significantly from file:\n\n")
        f.write("| Ticker | Yahoo Name | In File As | Source |\n")
        f.write("|---|---|---|---|\n")
        for r in sorted(results, key=lambda x: x['ticker']):
            if r['valid'] and r['name'] and r['company_in_file']:
                ya_words = set((r['name'] or '').lower().split())
                file_words = set((r['company_in_file'] or '').lower().replace('**', '').split())
                # If very few words overlap, flag it
                overlap = ya_words & file_words
                if len(overlap) < 1 and 'Unknown' not in r['company_in_file']:
                    f.write(f"| {r['ticker']} | {r['name']} | {r['company_in_file'][:40]} | {r['source_file']} |\n")

    print(f"\n{'='*60}")
    print(f"VERIFICATION COMPLETE")
    print(f"  Valid:   {valid_count}")
    print(f"  Invalid: {invalid_count}")
    print(f"  Errors:  {error_count}")
    print(f"\nFull report: {report_path}")

    # Also save raw JSON for programmatic use
    json_path = skill_dir / 'ticker_verification.json'
    write_json(json_path, results)
    print(f"Raw JSON:    {json_path}")

    return error_count == 0


if __name__ == '__main__':
    success = main()
    raise SystemExit(0 if success else 1)
