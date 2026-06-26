#!/usr/bin/env python3
"""
Contract Analyzer — Extract key terms, red flags, and risk assessment from legal documents.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path


RED_FLAGS = {
    'auto_renewal': {
        'patterns': [
            r'auto(?:matic)?(?:ally)?\s*renew',
            r'shall\s*renew\s*unless',
            r'renew(?:s|ed|al)?\s*for\s*successive',
            r'continue\s*in\s*effect\s*unless',
            r'term\s*shall\s*be\s*extended',
        ],
        'severity': 'MEDIUM',
        'label': 'Auto-Renewal Clause',
        'advice': 'Ensure you can cancel before renewal. Set a calendar reminder before the opt-out deadline.'
    },
    'unlimited_liability': {
        'patterns': [
            r'without\s*limit(?:ation)?',
            r'unlimited\s*(?:liability|indemnit)',
            r'no\s*cap\s*on\s*(?:liability|damages)',
            r'notwithstanding\s*any\s*limitation',
            r'consequential\s*(?:,?\s*indirect\s*)?(?:and\s*)?special\s*damages',
        ],
        'severity': 'HIGH',
        'label': 'Unlimited Liability Exposure',
        'advice': 'Negotiate a liability cap. Standard is 12 months of fees paid.'
    },
    'one_sided_termination': {
        'patterns': [
            r'(?:company|party\s*a|licensor|provider)\s*(?:may|shall\s*have\s*the\s*right\s*to)\s*terminat',
            r'terminat\w*\s*(?:at\s*)?(?:its|their|sole|absolute)\s*(?:sole\s*)?discretion',
            r'without\s*cause\s*upon\s*\d+\s*days',
            r'immediately\s*terminat',
            r'terminate\s*at\s*any\s*time\s*without',
        ],
        'severity': 'MEDIUM',
        'label': 'One-Sided Termination Rights',
        'advice': 'Both parties should have equal termination rights. Negotiate mutual termination clauses.'
    },
    'broad_noncompete': {
        'patterns': [
            r'non[\s-]compet\w*\s*for\s*(?:a\s*)?(?:period\s*of\s*)?(?:two|2|three|3|five|5)\s*year',
            r'shall\s*not\s*(?:engage|participate|compete)\s*(?:in\s*any\s*)?(?:business|activity|venture)',
            r'restrict(?:ed|s|ion)?\s*(?:from|on)\s*(?:any|all)\s*(?:compet(?:ing|itive)|similar)',
            r'anywhere\s*in\s*(?:the\s*)?world',
        ],
        'severity': 'HIGH',
        'label': 'Broad Non-Compete',
        'advice': 'Non-competes should be limited in time (6-12 months), geography, and scope. This one may be unenforceable.'
    },
    'unilateral_modification': {
        'patterns': [
            r'(?:may|reserves?\s*the\s*right\s*to)\s*(?:modify|amend|change|update)\s*(?:this|the)\s*(?:agreement|terms)',
            r'without\s*(?:prior\s*)?notice',
            r'sole\s*discretion',
            r'at\s*any\s*time\s*(?:,?\s*with\s*or\s*without\s*notice)?',
        ],
        'severity': 'MEDIUM',
        'label': 'Unilateral Modification Rights',
        'advice': 'Contracts should require mutual consent for changes. Ask for notice period and right to terminate if terms change.'
    },
    'broad_ip_assignment': {
        'patterns': [
            r'all\s*(?:rights?\s*(?:,?\s*titles?\s*)?(?:,?\s*and\s*)?interests?\s*(?:,?\s*including\s*intellectual\s*property)?)\s*(?:shall|will)\s*(?:be|become|vest)\s*(?:the\s*property\s*of|owned\s*by)',
            r'assign(?:s|ed|ment)?\s*(?:all|any)\s*(?:right|title|interest|ip|intellectual\s*property)',
            r'work[\s-]for[\s-]hire',
            r'(?:irrevocably|perpetually)\s*assign',
        ],
        'severity': 'MEDIUM',
        'label': 'Broad IP Assignment',
        'advice': 'Ensure IP assignment is limited to work done under the contract. Protect pre-existing IP and side projects.'
    },
    'arbitration_only': {
        'patterns': [
            r'binding\s*arbitration',
            r'waiv\w*\s*(?:the\s*)?right\s*to\s*(?:a\s*)?(?:jury\s*trial|class\s*action|court)',
            r'sole\s*(?:and\s*)?exclusive\s*remedy\s*(?:shall\s*be)?\s*arbitrat',
            r'no\s*class\s*action',
        ],
        'severity': 'LOW',
        'label': 'Mandatory Arbitration',
        'advice': 'Arbitration limits your ability to go to court. Consider if this is acceptable for the value of the agreement.'
    },
    'penalty_clauses': {
        'patterns': [
            r'liquidated\s*damage',
            r'penalty\s*of\s*\$?\d',
            r'forfeit\w*\s*(?:all|any)',
            r'non[\s-]refundable',
            r'termination\s*fee\s*(?:of|equal)',
        ],
        'severity': 'MEDIUM',
        'label': 'Penalty / Liquidated Damages',
        'advice': 'Penalties should be proportional to actual damages. Challenge excessive penalties.'
    },
    'jurisdiction_far': {
        'patterns': [
            r'exclusive\s*jurisdiction\s*(?:of|in)\s*(?:the\s*)?(?:courts?\s*(?:of|in|located\s*in)?)?\s*[A-Z][a-z]+(?:\s*,?\s*[A-Z][a-z]+)*',
            r'governed\s*by\s*(?:the\s*)?laws?\s*of\s*[A-Z]',
        ],
        'severity': 'LOW',
        'label': 'Jurisdiction Clause',
        'advice': 'Check if the specified jurisdiction is convenient for you. Negotiate for your home jurisdiction if not.'
    },
    'data_collection': {
        'patterns': [
            r'collect(?:s|ing)?\s*(?:and\s*)?(?:store|retain|process|use)\s*(?:your|personal|user)\s*data',
            r'share\w*\s*(?:your|personal)\s*(?:information|data)\s*with\s*(?:third[\s-]part)',
            r'license\s*(?:to|granted|to\s*use)\s*(?:your|user)\s*(?:content|data)',
        ],
        'severity': 'MEDIUM',
        'label': 'Broad Data Rights',
        'advice': 'Understand what data is collected and shared. Look for opt-out options and data deletion rights.'
    },
}

KEY_TERMS = {
    'effective_date': r'(?:effective|commence(?:ment)?|start)\s*date[:\s]*(\w+\s+\d{1,2},?\s+\d{4}|\d{1,2}/\d{1,2}/\d{4})',
    'term_duration': r'(?:initial\s*)?term\s*(?:of|shall\s*be|is)\s*(\d+)\s*(month|year|day)',
    'payment_amount': r'(?:total|payment|fee|price|compensation)\s*(?:of|is|shall\s*be)?[:\s]*\$?([\d,]+(?:\.\d{2})?)',
    'payment_schedule': r'(?:payable|paid|due)\s*(?:on|by|within|every)\s*(\d+)\s*(day|month|week)',
    'notice_period': r'(?:written\s*)?notice\s*(?:of|period\s*of\s*)?(\d+)\s*(day|month|week|hour)',
    'termination_fee': r'(?:early\s*)?termination\s*(?:fee|penalty|charge)\s*(?:of|equal\s*to)?[:\s]*\$?([\d,]+(?:\.\d{2})?|\d+%\s*(?:of\s*(?:the\s*)?(?:remaining|total)\s*(?:fee|amount)))',
    'liability_cap': r'(?:maximum|cap(?:ped)?|limit(?:ed)?|not\s*exceed)\s*(?:liability|damages)?\s*(?:of|at|to)?[:\s]*\$?([\d,]+(?:\.\d{2})?|\d+\s*(?:month|year)s?\s*(?:of\s*)?(?:fee|payment|compensation))',
    'non_compete_period': r'non[\s-]compet\w*\s*(?:period|duration|for)\s*(?:of\s*)?(\d+)\s*(month|year)',
    'confidentiality_period': r'confidential\w*\s*(?:for|period\s*of)\s*(?:a\s*)?(?:of\s*)?(\d+)\s*(month|year)',
    'governing_law': r'govern(?:ed|s)?\s*by\s*(?:the\s*)?laws?\s*of\s*(?:the\s*(?:State|Province|Country)\s*of\s*)?([A-Z][A-Za-z\s,]+?)(?:\.|,|\s+without)',
}


def extract_text(file_path):
    """Extract text from various file formats."""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext == '.pdf':
        try:
            import pdfplumber
            text = ''
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ''
            return text
        except ImportError:
            print("  ❌ Install pdfplumber: pip install pdfplumber")
            sys.exit(1)
    
    elif ext == '.docx':
        try:
            import docx
            doc = docx.Document(path)
            return '\n'.join(p.text for p in doc.paragraphs)
        except ImportError:
            print("  ❌ Install python-docx: pip install python-docx")
            sys.exit(1)
    
    elif ext in ('.png', '.jpg', '.jpeg', '.bmp', '.tiff'):
        try:
            import pytesseract
            from PIL import Image
            return pytesseract.image_to_string(Image.open(path))
        except ImportError:
            print("  ❌ Install pytesseract and pillow")
            sys.exit(1)
    
    else:  # txt or unknown
        return path.read_text()


def analyze_red_flags(text):
    """Scan text for red flags."""
    flags = []
    text_lower = text.lower()
    
    for flag_id, flag_info in RED_FLAGS.items():
        for pattern in flag_info['patterns']:
            if re.search(pattern, text_lower):
                flags.append({
                    'id': flag_id,
                    'label': flag_info['label'],
                    'severity': flag_info['severity'],
                    'advice': flag_info['advice'],
                    'pattern_matched': pattern[:50]
                })
                break  # one match per flag type
    
    return flags


def extract_terms(text):
    """Extract key terms from the contract."""
    terms = {}
    for term_id, pattern in KEY_TERMS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            terms[term_id] = match.group(0).strip()[:100]
    return terms


def extract_parties(text):
    """Try to extract party names."""
    parties = []
    
    # Common patterns: "between X ("Party A") and Y ("Party B")"
    patterns = [
        r'between\s+([A-Z][A-Za-z\s,.&]+?)(?:\s*\(|\s*,|\s+and)',
        r'("Company"|"Client"|"Licensor"|"Licensee"|"Employer"|"Employee"|"Landlord"|"Tenant")\s*(?:means|is|refers\s*to)[:\s]+([A-Z][A-Za-z\s,.&]+)',
        r'([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*(?:\s+(?:Inc|LLC|Ltd|Corp|Co)\.?))',
    ]
    
    for p in patterns:
        for m in re.finditer(p, text[:2000]):
            party = m.group(1).strip()
            if len(party) > 3 and party not in parties:
                parties.append(party)
    
    return parties[:4]  # max 4 parties


def calculate_risk_score(flags):
    """Calculate overall risk score."""
    severity_weights = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4}
    total = sum(severity_weights.get(f['severity'], 1) for f in flags)
    
    if total == 0:
        return 'LOW', '🟢'
    elif total <= 3:
        return 'MEDIUM', '🟡'
    elif total <= 6:
        return 'HIGH', '🟠'
    else:
        return 'CRITICAL', '🔴'


def generate_summary(text, terms, parties):
    """Generate a brief plain-English summary."""
    summary_parts = []
    
    if parties:
        summary_parts.append(f"This agreement is between {' and '.join(parties[:2])}.")
    
    if terms.get('term_duration'):
        summary_parts.append(f"The term is {terms['term_duration']}.")
    
    if terms.get('payment_amount'):
        summary_parts.append(f"Payment: {terms['payment_amount']}.")
    
    if terms.get('governing_law'):
        summary_parts.append(f"Governed by the laws of {terms['governing_law']}.")
    
    if not summary_parts:
        summary_parts.append("This document contains terms and conditions that should be reviewed carefully.")
    
    return ' '.join(summary_parts)


def format_report(file_path, text, flags, terms, parties):
    """Format the analysis report."""
    risk_level, risk_emoji = calculate_risk_score(flags)
    
    lines = [
        f"\n{'═'*60}",
        f"  📋 CONTRACT ANALYSIS REPORT",
        f"{'═'*60}",
        f"",
        f"  📄 File: {file_path}",
        f"  📏 Length: {len(text):,} characters ({len(text.split())} words)",
        f"",
        f"  ── Risk Assessment ──",
        f"  {risk_emoji} Overall Risk: {risk_level}",
        f"",
    ]
    
    # Summary
    summary = generate_summary(text, terms, parties)
    lines.extend([
        f"  ── Plain English Summary ──",
        f"  {summary}",
        f"",
    ])
    
    # Parties
    if parties:
        lines.extend([
            f"  ── Parties ──",
            *[f"  • {p}" for p in parties],
            f"",
        ])
    
    # Key Terms
    if terms:
        lines.extend([
            f"  ── Key Terms ──",
        ])
        term_labels = {
            'effective_date': '📅 Effective Date',
            'term_duration': '⏱️  Term Duration',
            'payment_amount': '💰 Payment Amount',
            'payment_schedule': '💳 Payment Schedule',
            'notice_period': '📬 Notice Period',
            'termination_fee': '⚠️  Termination Fee',
            'liability_cap': '🛡️  Liability Cap',
            'non_compete_period': '🚫 Non-Compete Period',
            'confidentiality_period': '🔒 Confidentiality Period',
            'governing_law': '⚖️  Governing Law',
        }
        for tid, value in terms.items():
            label = term_labels.get(tid, tid)
            lines.append(f"  {label}: {value}")
        lines.append(f"")
    
    # Red Flags
    if flags:
        lines.extend([
            f"  ── Red Flags ({len(flags)}) ──",
        ])
        severity_emoji = {'LOW': '🟡', 'MEDIUM': '🟠', 'HIGH': '🔴', 'CRITICAL': '🚨'}
        for i, flag in enumerate(flags, 1):
            emoji = severity_emoji.get(flag['severity'], '⚠️')
            lines.extend([
                f"  {emoji} #{i} — {flag['label']} [{flag['severity']}]",
                f"     💡 {flag['advice']}",
                f"",
            ])
        
        # Recommendations
        lines.extend([
            f"  ── Recommendations ──",
            f"  1. Address all HIGH/CRITICAL flags before signing",
            f"  2. Negotiate liability caps and termination terms",
            f"  3. Have a qualified attorney review before execution",
            f"  4. Keep a signed copy for your records",
        ])
    else:
        lines.extend([
            f"  ── Red Flags ──",
            f"  ✅ No obvious red flags detected.",
            f"  ⚠️  Always have a qualified attorney review important contracts.",
        ])
    
    lines.append(f"\n{'═'*60}")
    lines.append(f"  ⚖️  Disclaimer: This is an automated analysis, NOT legal advice.")
    lines.append(f"{'═'*60}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Contract Analyzer')
    sub = parser.add_subparsers(dest='command')
    
    p_analyze = sub.add_parser('analyze', help='Analyze a contract')
    p_analyze.add_argument('file', help='Contract file (PDF/DOCX/TXT/image)')
    p_analyze.add_argument('--json', action='store_true', help='Output as JSON')
    
    p_diff = sub.add_parser('diff', help='Compare two contract versions')
    p_diff.add_argument('file1', help='First version')
    p_diff.add_argument('file2', help='Second version')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'analyze':
        if not os.path.exists(args.file):
            print(f"  ❌ File not found: {args.file}")
            sys.exit(1)
        
        text = extract_text(args.file)
        if not text.strip():
            print("  ❌ No text could be extracted from the file.")
            sys.exit(1)
        
        flags = analyze_red_flags(text)
        terms = extract_terms(text)
        parties = extract_parties(text)
        
        if getattr(args, 'json'):
            result = {
                'file': args.file,
                'risk_level': calculate_risk_score(flags)[0],
                'red_flags': flags,
                'key_terms': terms,
                'parties': parties,
                'summary': generate_summary(text, terms, parties)
            }
            print(json.dumps(result, indent=2))
        else:
            print(format_report(args.file, text, flags, terms, parties))
    
    elif args.command == 'diff':
        text1 = extract_text(args.file1)
        text2 = extract_text(args.file2)
        
        flags1 = set(f['label'] for f in analyze_red_flags(text1))
        flags2 = set(f['label'] for f in analyze_red_flags(text2))
        
        terms1 = extract_terms(text1)
        terms2 = extract_terms(text2)
        
        print(f"\n{'═'*60}")
        print(f"  📋 CONTRACT COMPARISON")
        print(f"{'═'*60}")
        print(f"\n  V1: {args.file1}")
        print(f"  V2: {args.file2}")
        
        # New red flags in V2
        new_flags = flags2 - flags1
        removed_flags = flags1 - flags2
        
        if new_flags:
            print(f"\n  🆕 New Red Flags in V2:")
            for f in new_flags:
                print(f"     🔴 {f}")
        
        if removed_flags:
            print(f"\n  ✅ Removed Red Flags (V1 → V2):")
            for f in removed_flags:
                print(f"     🟢 {f}")
        
        # Changed terms
        all_terms = set(list(terms1.keys()) + list(terms2.keys()))
        changed = []
        for t in all_terms:
            v1 = terms1.get(t, '(not found)')
            v2 = terms2.get(t, '(not found)')
            if v1 != v2:
                changed.append((t, v1, v2))
        
        if changed:
            print(f"\n  📝 Changed Terms:")
            for term, v1, v2 in changed:
                print(f"     {term}:")
                print(f"       V1: {v1}")
                print(f"       V2: {v2}")
        
        if not new_flags and not removed_flags and not changed:
            print(f"\n  ✅ No significant differences detected.")
        
        print(f"\n{'═'*60}")


if __name__ == '__main__':
    main()
