#!/usr/bin/env python3
"""
Free Novel License Checker

Check if a website/novel platform offers truly free and legal content.
"""

import argparse
import re
import sys


# Known legitimate free novel platforms
LEGITIMATE_PLATFORMS = {
    "gutenberg.org": {"license": "public_domain", "type": "public_domain"},
    "openlibrary.org": {"license": "mixed", "type": "digital_library"},
    "manybooks.net": {"license": "public_domain", "type": "e_book"},
    "feedbooks.com": {"license": "mixed", "type": "e_book"},
    "wattpad.com": {"license": "ad_supported", "type": "user_generated"},
    "royalroad.com": {"license": "ad_supported", "type": "web_fiction"},
    "ao3.org": {"license": "cc_by_nc_sa", "type": "fan_fiction"},
    "archive.org": {"license": "mixed", "type": "digital_archive"},
    "librivox.org": {"license": "public_domain", "type": "audiobooks"},
    "en.wikisource.org": {"license": "public_domain", "type": "digital_library"},
    "www.aozora.gr.jp": {"license": "public_domain", "type": "digital_library"},
    "syosetu.com": {"license": "free", "type": "web_novels"},
    "kakuyomu.jp": {"license": "free", "type": "web_novels"},
}

# Red flags for potentially illegal sites
RED_FLAGS = [
    r"best.*novel.*free",
    r"download.*premium.*free",
    r".*novels?.*without.*registration",
    r"read.*latest.*bestseller.*free",
]

# Green flags
GREEN_FLAGS = [
    (r"public.?domain", 2),
    (r"copyright.*policy", 1),
    (r"dmca", 1),
    (r"creative.?commons", 2),
    (r"author.*verification", 1),
    (r"official.*partner", 2),
    (r"publisher.*agreement", 1),
]


def check_platform legitimacy(url):
    """Check if a platform is likely legitimate."""
    url_lower = url.lower()
    url_clean = re.sub(r'^https?://(www\.)?', '', url_lower)

    # Check known legitimate platforms
    for domain, info in LEGITIMATE_PLATFORMS.items():
        if domain in url_clean:
            return {
                "status": "known_legitimate",
                "domain": domain,
                "license": info["license"],
                "type": info["type"],
                "confidence": "high"
            }

    # Check red flags
    red_score = 0
    for pattern in RED_FLAGS:
        if re.search(pattern, url_lower):
            red_score += 1

    if red_score > 0:
        return {
            "status": "potential_concern",
            "red_flag_count": red_score,
            "warning": "This URL may contain questionable content",
            "confidence": "medium"
        }

    # Check green flags
    green_score = 0
    for pattern, weight in GREEN_FLAGS:
        if re.search(pattern, url_lower):
            green_score += weight

    if green_score >= 2:
        return {
            "status": "likely_legitimate",
            "green_score": green_score,
            "confidence": "medium"
        }

    return {
        "status": "unknown",
        "message": "Platform not in known databases, verify manually",
        "confidence": "low"
    }


def check_dmca_compliance(website_content):
    """Check if website mentions DMCA compliance."""
    dmca_indicators = [
        r"dmca.?compliant",
        r"dmca.?policy",
        r"copyright.?notification",
        r"takedown.?request",
        r"intellectual.?property",
    ]

    found_indicators = []
    for indicator in dmca_indicators:
        if re.search(indicator, website_content, re.IGNORECASE):
            found_indicators.append(indicator)

    return {
        "has_dmca": len(found_indicators) > 0,
        "indicators": found_indicators
    }


def check_license_type(license_text):
    """Analyze license text to determine type."""
    license_lower = license_text.lower()

    if "public domain" in license_lower and "cc0" in license_lower:
        return "CC0"
    elif "public domain" in license_lower:
        return "Public Domain"
    elif "cc-by-sa" in license_lower:
        return "CC-BY-SA"
    elif "cc-by-nc-sa" in license_lower:
        return "CC-BY-NC-SA"
    elif "cc-by-nc" in license_lower:
        return "CC-BY-NC"
    elif "cc-by" in license_lower:
        return "CC-BY"
    elif "all rights reserved" in license_lower:
        return "All Rights Reserved"
    else:
        return "Unknown - verify on site"


def main():
    parser = argparse.ArgumentParser(
        description="Check if a novel platform/URL is legitimate and free",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--url", "-u",
        required=True,
        help="URL to check"
    )

    parser.add_argument(
        "--verify-license",
        action="store_true",
        help="Show license determination (for manual verification)"
    )

    args = parser.parse_args()

    print(f"Checking: {args.url}")
    print("="*50)

    result = check_platform_legitimacy(args.url)

    print(f"\nStatus: {result.get('status', 'unknown')}")
    print(f"Confidence: {result.get('confidence', 'unknown')}")

    if result.get('license'):
        print(f"License Type: {result.get('license')}")

    if result.get('type'):
        print(f"Platform Type: {result.get('type')}")

    if result.get('warning'):
        print(f"\nWarning: {result.get('warning')}")

    if result.get('message'):
        print(f"\nNote: {result.get('message')}")

    print("\n" + "="*50)
    print("Recommendations:")
    print("1. Always verify copyright status on the actual website")
    print("2. Prefer platforms with clear DMCA policies")
    print("3. Support authors by using official/authorized platforms")
    if result.get('status') == 'potential_concern':
        print("\nCaution: This site may offer unauthorized content")

    return 0


if __name__ == "__main__":
    main()