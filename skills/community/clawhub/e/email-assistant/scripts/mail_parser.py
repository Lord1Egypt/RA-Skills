#!/usr/bin/env python3
"""
Mail Parser - Email parsing and important email analysis
Parses plain text/HTML emails and identifies important emails
"""

import json
import re
import argparse
import sys
from datetime import datetime
from typing import List, Dict, Optional
from html import unescape


# Important email keywords (case-insensitive)
IMPORTANT_KEYWORDS = {
    "urgent": ["urgent", "紧急", "紧迫", "asap", "immediately"],
    "deadline": ["deadline", "截止", "截止日期", "due", "最后期限", "截止时间"],
    "meeting": ["meeting", "会议", "conference", "call", "zoom", "teams"],
    "invoice": ["invoice", "发票", "账单", "payment", "付款", "invoice"],
    "contract": ["contract", "合同", "agreement", "协议", "legal"],
    "action": ["action required", "需要处理", "请回复", "please respond", "需确认"],
    "important": ["important", "重要", "priority", "高优先级", "urgent"],
    "money": ["payment", "付款", "invoice", "账单", "转账", "金额", "payment"],
    "security": ["security", "安全", "password", "密码", "account", "账户", "登录"]
}

# Priority patterns (more specific = higher priority)
PRIORITY_PATTERNS = [
    (r"(?i)(urgent|immediate|asap|紧急|紧迫|立刻)", 10),
    (r"(?i)(deadline|due|截止|最后期限)", 9),
    (r"(?i)(meeting|会议|call|zoom|teams|conference)", 8),
    (r"(?i)(invoice|payment|付款|发票|账单)", 7),
    (r"(?i)(contract|合同|agreement|协议)", 7),
    (r"(?i)(action required|需要处理|请回复|please respond)", 6),
    (r"(?i)(important|重要|priority|高优先级)", 5),
]


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    # Unescape HTML entities
    text = unescape(text)
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text.strip()


def strip_html(html: str) -> str:
    """Strip HTML tags and return plain text."""
    if not html:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', html)
    # Decode HTML entities
    text = unescape(text)
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def detect_important_keywords(text: str) -> List[Dict[str, any]]:
    """Detect important keywords in email text."""
    text_lower = text.lower()
    found = []
    
    for category, keywords in IMPORTANT_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                # Find position
                pos = text_lower.find(keyword.lower())
                found.append({
                    "category": category,
                    "keyword": keyword,
                    "position": pos,
                    "context": text[max(0, pos-20):min(len(text), pos+len(keyword)+20)]
                })
    
    return found


def calculate_priority(text: str) -> int:
    """Calculate email priority (0-10)."""
    text_lower = text.lower()
    priority = 0
    
    for pattern, score in PRIORITY_PATTERNS:
        if re.search(pattern, text_lower):
            priority = max(priority, score)
    
    return priority


def analyze_email(email_data: Dict) -> Dict:
    """Analyze a single email for importance."""
    subject = email_data.get("subject", "")
    preview = email_data.get("preview", "")
    body_text = email_data.get("body_text", "")
    body_html = email_data.get("body_html", "")
    
    # Combine text for analysis
    full_text = f"{subject} {preview} {body_text}"
    if not full_text.strip():
        full_text = strip_html(body_html)
    
    # Clean text
    full_text = clean_text(full_text)
    
    # Calculate priority
    priority = calculate_priority(full_text)
    
    # Detect keywords
    keywords = detect_important_keywords(full_text)
    
    # Determine categories
    categories = list(set(k["category"] for k in keywords))
    
    # Generate summary
    summary = {
        "id": email_data.get("id"),
        "subject": subject,
        "from": email_data.get("from"),
        "date": email_data.get("date"),
        "priority": priority,
        "is_important": priority >= 6,
        "categories": categories,
        "keywords": [k["keyword"] for k in keywords],
        "preview": preview[:200] if preview else (full_text[:200] if full_text else "")
    }
    
    return summary


def load_emails_from_file(filepath: str) -> List[Dict]:
    """Load emails from JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "emails" in data:
                return data["emails"]
            else:
                return [data]
    except Exception as e:
        print(f"✗ Failed to load emails: {e}")
        sys.exit(1)


def analyze_emails(emails: List[Dict]) -> Dict:
    """Analyze a list of emails."""
    results = []
    important_emails = []
    
    for email_data in emails:
        analysis = analyze_email(email_data)
        results.append(analysis)
        
        if analysis["is_important"]:
            important_emails.append(analysis)
    
    return {
        "total": len(emails),
        "important_count": len(important_emails),
        "results": results,
        "important": important_emails
    }


def print_summary(results: Dict):
    """Print analysis summary."""
    print(f"\n{'='*60}")
    print(f"Email Analysis Summary")
    print(f"{'='*60}")
    print(f"Total emails analyzed: {results['total']}")
    print(f"Important emails found: {results['important_count']}")
    print(f"\n{'='*60}")
    
    if results["important"]:
        print("\n📌 IMPORTANT EMAILS:")
        print("-" * 60)
        for email in results["important"]:
            print(f"\nPriority: {'🔥' * (email['priority'] // 3)} ({email['priority']}/10)")
            print(f"Subject: {email['subject']}")
            print(f"From: {email['from']}")
            print(f"Categories: {', '.join(email['categories'])}")
            print(f"Keywords: {', '.join(email['keywords'][:5])}")
            print(f"Preview: {email['preview'][:100]}...")
    
    print(f"\n{'='*60}")
    print("\nAll Emails (sorted by priority):")
    print("-" * 60)
    
    sorted_results = sorted(results["results"], key=lambda x: x["priority"], reverse=True)
    for i, email in enumerate(sorted_results, 1):
        icon = "🔥" if email["is_important"] else "  "
        print(f"{icon} [{email['priority']:>2}] {email['subject'][:50]}")


def main():
    parser = argparse.ArgumentParser(description="Email Parser and Analyzer")
    parser.add_argument("--emails", help="Path to JSON file containing emails")
    parser.add_argument("--analyze", action="store_true", help="Analyze loaded emails")
    parser.add_argument("--input", help="Input JSON file")
    parser.add_argument("--output", help="Output JSON file for results")
    parser.add_argument("--important-only", action="store_true", help="Show only important emails")
    parser.add_argument("--min-priority", type=int, default=0, help="Minimum priority to show (0-10)")
    
    args = parser.parse_args()
    
    emails = []
    
    # Load emails from file
    if args.emails or args.input:
        filepath = args.emails or args.input
        print(f"Loading emails from {filepath}...")
        emails = load_emails_from_file(filepath)
        print(f"Loaded {len(emails)} emails")
    
    if args.analyze or args.emails:
        if not emails:
            print("✗ No emails to analyze")
            sys.exit(1)
        
        print("\nAnalyzing emails...")
        results = analyze_emails(emails)
        
        # Filter by priority
        if args.important_only:
            results["results"] = [r for r in results["results"] if r["priority"] >= args.min_priority]
        
        # Print summary
        print_summary(results)
        
        # Save to file if requested
        if args.output:
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "total": results["total"],
                "important_count": results["important_count"],
                "results": results["results"],
                "important": results["important"]
            }
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"\n✓ Results saved to {args.output}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
