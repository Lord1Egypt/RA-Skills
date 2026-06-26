#!/usr/bin/env python3
"""
Email Deliverability Checker
Usage: python3 deliverability_check.py --file email.txt
       echo "email body text" | python3 deliverability_check.py
Checks for spam triggers, formatting issues, and deliverability risks.
"""

import sys
import re
import argparse

SPAM_TRIGGER_WORDS = [
    "free", "guarantee", "no risk", "limited time", "act now", "earn money",
    "make money", "winner", "congratulations", "click here", "buy now", "order now",
    "cash bonus", "prize", "earn extra", "lose weight", "miracle", "no obligation",
    "save up to", "special promotion", "this is not spam", "100% free", "100% satisfied",
    "additional income", "be your own boss", "billion", "cable converter",
    "casino", "cheap", "compare rates", "consolidate debt", "dear friend",
    "double your income", "extra cash", "fast cash", "financial freedom",
    "free access", "free consultation", "free gift", "free hosting", "free info",
    "free investment", "free leads", "free membership", "free money", "free offer",
    "free preview", "free quote", "free sample", "free trial", "free website",
    "full refund", "get paid", "giveaway", "incredible deal", "information you requested",
    "internet marketing", "investment decision", "join millions", "lower rates",
    "luxury", "marketing solutions", "mass email", "meet singles", "money back",
    "money making", "mortgage rates", "multi-level marketing", "no catch",
    "no cost", "no credit check", "no fees", "no gimmick", "no hidden costs",
    "no hidden fees", "no interest", "now only", "offer expires", "once in a lifetime",
    "only", "open", "opportunity", "opt in", "order today", "outstanding values",
    "potential earnings", "promise you", "pure profit", "remove before printing",
    "risk free", "satisfaction guaranteed", "search engine", "see for yourself",
    "serious cash", "shop now", "sign up free", "subject to credit", "subscribe",
    "this is not junk", "this is not spam", "thousands", "trial", "undisclosed",
    "unsecured credit", "unsolicited", "urgent", "us dollars", "vacation", "web traffic",
    "while supplies last", "why pay more", "will not believe your eyes",
    "winner", "winning", "work at home", "work from home", "you have been selected",
    "you're a winner", "your income",
]

def check_spam_words(text):
    text_lower = text.lower()
    found = []
    for word in SPAM_TRIGGER_WORDS:
        if word in text_lower:
            found.append(word)
    return found

def check_subject_length(subject):
    length = len(subject)
    if length < 20:
        return "warning", f"Subject too short ({length} chars) — may look spammy"
    elif length > 60:
        return "warning", f"Subject too long ({length} chars) — gets clipped on mobile"
    return "ok", f"Subject length OK ({length} chars)"

def check_link_ratio(text):
    links = re.findall(r'https?://\S+', text)
    words = len(text.split())
    if words == 0:
        return "ok", "No content to check"
    ratio = len(links) / words
    if ratio > 0.05:
        return "warning", f"High link-to-word ratio ({len(links)} links, {words} words) — use max 1–2 links"
    return "ok", f"Link ratio OK ({len(links)} links in {words} words)"

def check_caps_ratio(text):
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return "ok", "No text to check"
    caps = [c for c in letters if c.isupper()]
    ratio = len(caps) / len(letters)
    if ratio > 0.3:
        return "warning", f"Too many CAPS ({ratio:.0%}) — triggers spam filters"
    return "ok", f"Caps ratio OK ({ratio:.0%})"

def check_exclamation(text):
    count = text.count("!")
    if count > 3:
        return "warning", f"Too many exclamation marks ({count}) — reduce to 0–2"
    return "ok", f"Exclamation marks OK ({count})"

def check_html_tags(text):
    html_tags = re.findall(r'<[^>]+>', text)
    if html_tags:
        return "warning", f"HTML tags detected ({len(html_tags)}) — plain text emails have better deliverability"
    return "ok", "Plain text (good for deliverability)"

def check_word_count(text):
    words = len(text.split())
    if words < 30:
        return "warning", f"Very short email ({words} words) — may look like phishing"
    elif words > 300:
        return "warning", f"Long email ({words} words) — cold emails should be 75–150 words"
    return "ok", f"Word count OK ({words} words)"

def run_checks(text, subject=""):
    results = []
    score = 100

    # Spam words
    spam_found = check_spam_words(text + " " + subject)
    if spam_found:
        penalty = min(40, len(spam_found) * 5)
        score -= penalty
        results.append({
            "check": "Spam trigger words",
            "status": "fail",
            "detail": f"Found {len(spam_found)} triggers: {', '.join(spam_found[:10])}",
            "penalty": penalty
        })
    else:
        results.append({"check": "Spam trigger words", "status": "pass", "detail": "None found", "penalty": 0})

    # Subject length
    if subject:
        status, detail = check_subject_length(subject)
        penalty = 5 if status == "warning" else 0
        score -= penalty
        results.append({"check": "Subject line length", "status": status, "detail": detail, "penalty": penalty})

    # Link ratio
    status, detail = check_link_ratio(text)
    penalty = 10 if status == "warning" else 0
    score -= penalty
    results.append({"check": "Link-to-text ratio", "status": status, "detail": detail, "penalty": penalty})

    # Caps
    status, detail = check_caps_ratio(text)
    penalty = 10 if status == "warning" else 0
    score -= penalty
    results.append({"check": "Excessive caps", "status": status, "detail": detail, "penalty": penalty})

    # Exclamation
    status, detail = check_exclamation(text)
    penalty = 5 if status == "warning" else 0
    score -= penalty
    results.append({"check": "Exclamation marks", "status": status, "detail": detail, "penalty": penalty})

    # HTML
    status, detail = check_html_tags(text)
    penalty = 5 if status == "warning" else 0
    score -= penalty
    results.append({"check": "HTML content", "status": status, "detail": detail, "penalty": penalty})

    # Word count
    status, detail = check_word_count(text)
    penalty = 5 if status == "warning" else 0
    score -= penalty
    results.append({"check": "Word count", "status": status, "detail": detail, "penalty": penalty})

    return max(0, score), results


def main():
    parser = argparse.ArgumentParser(description="Email Deliverability Checker")
    parser.add_argument("--file", help="Path to email text file")
    parser.add_argument("--subject", default="", help="Email subject line")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("Provide email text via --file or stdin")
        sys.exit(1)

    score, results = run_checks(text, subject=args.subject)

    print(f"\n📧 Deliverability Score: {score}/100\n")

    for r in results:
        icon = "✅" if r["status"] in ("pass", "ok") else "⚠️"
        print(f"{icon} {r['check']}: {r['detail']}")

    print()
    if score >= 80:
        print("✅ Good deliverability. Safe to send.")
    elif score >= 60:
        print("⚠️  Moderate risk. Review warnings before sending.")
    else:
        print("❌ High spam risk. Fix issues before sending.")


if __name__ == "__main__":
    main()
