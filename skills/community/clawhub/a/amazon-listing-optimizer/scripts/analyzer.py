#!/usr/bin/env python3
"""
Amazon Listing Optimizer — Analyze and optimize any Amazon product listing
Scrapes listing data, scores quality, suggests improvements.
Free alternative to Helium 10's Listing Analyzer ($97/mo).
"""

import json
import re
import sys
import urllib.request
import urllib.parse
from html.parser import HTMLParser


class ListingData:
    """Extracted Amazon listing data."""
    def __init__(self):
        self.title = ""
        self.bullets = []
        self.description = ""
        self.price = ""
        self.rating = ""
        self.review_count = ""
        self.images_count = 0
        self.asin = ""
        self.brand = ""
        self.category = ""


def fetch_listing(asin, marketplace="com"):
    """Fetch an Amazon listing page."""
    url = f"https://www.amazon.{marketplace}/dp/{asin}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"❌ Failed to fetch listing: {e}")
        return None


def parse_listing(html, asin):
    """Extract listing data from HTML."""
    data = ListingData()
    data.asin = asin

    # Title
    title_match = re.search(r'id="productTitle"[^>]*>(.*?)</span>', html, re.DOTALL)
    if title_match:
        data.title = title_match.group(1).strip()

    # Bullets
    bullet_section = re.search(r'id="feature-bullets"(.*?)</div>', html, re.DOTALL)
    if bullet_section:
        bullets = re.findall(r'<span class="a-list-item">\s*(.*?)\s*</span>', bullet_section.group(1), re.DOTALL)
        data.bullets = [b.strip() for b in bullets if b.strip() and len(b.strip()) > 5]

    # Price
    price_match = re.search(r'class="a-price-whole">(\d+)</span>.*?class="a-price-fraction">(\d+)', html, re.DOTALL)
    if price_match:
        data.price = f"${price_match.group(1)}.{price_match.group(2)}"

    # Rating
    rating_match = re.search(r'(\d+\.?\d*) out of 5 stars', html)
    if rating_match:
        data.rating = rating_match.group(1)

    # Review count
    review_match = re.search(r'id="acrCustomerReviewText"[^>]*>(\d[\d,]*)', html)
    if review_match:
        data.review_count = review_match.group(1)

    # Image count (approximate)
    img_count = len(re.findall(r'"hiRes":"https://m\.media-amazon\.com', html))
    data.images_count = max(img_count, 1)

    # Brand
    brand_match = re.search(r'id="bylineInfo"[^>]*>.*?>(.*?)</a>', html, re.DOTALL)
    if brand_match:
        data.brand = brand_match.group(1).strip().replace("Visit the ", "").replace(" Store", "")

    return data


def score_title(title):
    """Score the listing title (0-100)."""
    score = 0
    feedback = []

    if not title:
        return 0, ["❌ No title found"]

    length = len(title)

    # Length scoring
    if 80 <= length <= 200:
        score += 30
    elif 50 <= length < 80:
        score += 20
        feedback.append("⚠️ Title is short. Aim for 80-200 characters to maximize keywords.")
    elif length > 200:
        score += 15
        feedback.append("⚠️ Title is too long. Amazon may truncate it. Keep under 200 chars.")
    else:
        score += 5
        feedback.append("❌ Title is very short. You're leaving keyword real estate on the table.")

    # Word count
    words = title.split()
    if len(words) >= 8:
        score += 15
    else:
        feedback.append("⚠️ Title has few words. Include more relevant keywords.")

    # Capitalization
    if title == title.upper():
        feedback.append("❌ ALL CAPS title. Use Title Case — it looks more professional.")
    elif title[0].isupper():
        score += 10

    # Brand in title
    if any(c.isupper() for c in title[:20]):
        score += 10

    # Special characters (avoid excessive)
    special_count = len(re.findall(r'[!@#$%^&*(){}|]', title))
    if special_count == 0:
        score += 10
    elif special_count > 3:
        feedback.append("⚠️ Too many special characters in title. Keep it clean.")

    # Pipe/dash separators (good for readability)
    if '|' in title or ' - ' in title or ',' in title:
        score += 10
        feedback.append("✅ Good use of separators for readability.")

    # Numbers (specifics sell)
    if re.search(r'\d', title):
        score += 15
        feedback.append("✅ Numbers in title (size, count, etc.) help conversion.")
    else:
        feedback.append("💡 Consider adding specific numbers (size, quantity, count).")

    return min(score, 100), feedback


def score_bullets(bullets):
    """Score bullet points (0-100)."""
    score = 0
    feedback = []

    if not bullets:
        return 0, ["❌ No bullet points found. This is critical — add 5 bullets."]

    count = len(bullets)

    # Count scoring
    if count >= 5:
        score += 25
        feedback.append(f"✅ {count} bullet points — good coverage.")
    elif count >= 3:
        score += 15
        feedback.append(f"⚠️ Only {count} bullets. Amazon allows 5 — use them all.")
    else:
        score += 5
        feedback.append(f"❌ Only {count} bullet(s). You need at least 5.")

    # Length scoring
    avg_length = sum(len(b) for b in bullets) / max(count, 1)
    if avg_length >= 150:
        score += 25
        feedback.append("✅ Detailed bullets with good keyword density.")
    elif avg_length >= 80:
        score += 15
        feedback.append("⚠️ Bullets could be longer. Aim for 150-200 chars each for SEO.")
    else:
        score += 5
        feedback.append("❌ Bullets are too short. You're wasting keyword space.")

    # Keyword density (uppercase words often = features)
    all_text = " ".join(bullets)
    caps_words = re.findall(r'\b[A-Z]{2,}\b', all_text)
    if len(caps_words) >= 3:
        score += 15
        feedback.append("✅ Good use of CAPS for feature emphasis.")

    # Benefit-focused language
    benefit_words = ['you', 'your', 'enjoy', 'perfect', 'ideal', 'best', 'premium',
                     'quality', 'guaranteed', 'satisfaction', 'easy', 'comfortable']
    benefit_count = sum(1 for w in benefit_words if w.lower() in all_text.lower())
    if benefit_count >= 3:
        score += 20
        feedback.append("✅ Benefits-focused language — tells customers WHY they need this.")
    elif benefit_count >= 1:
        score += 10
        feedback.append("💡 Add more benefit-focused language (you, your, enjoy, perfect).")
    else:
        feedback.append("❌ Bullets are feature-focused. Sell the BENEFIT, not just the feature.")

    # Emoji usage (mixed opinions but can help stand out)
    if any(ord(c) > 127 for c in all_text):
        score += 15
        feedback.append("✅ Using special characters/symbols for visual appeal.")

    return min(score, 100), feedback


def score_images(count):
    """Score image count (0-100)."""
    feedback = []
    if count >= 7:
        score = 100
        feedback.append(f"✅ {count} images — maximum coverage.")
    elif count >= 5:
        score = 75
        feedback.append(f"⚠️ {count} images. Add {7-count} more — Amazon allows 7+.")
    elif count >= 3:
        score = 50
        feedback.append(f"⚠️ Only {count} images. Add lifestyle shots, infographics, size charts.")
    else:
        score = 20
        feedback.append(f"❌ Only {count} image(s). This kills conversion. Add at least 5 more.")

    return score, feedback


def score_reviews(rating, count):
    """Score reviews (0-100)."""
    feedback = []
    score = 0

    if rating:
        r = float(rating)
        if r >= 4.5:
            score += 50
            feedback.append(f"✅ {rating}⭐ — excellent rating.")
        elif r >= 4.0:
            score += 35
            feedback.append(f"⚠️ {rating}⭐ — good but room for improvement.")
        elif r >= 3.5:
            score += 20
            feedback.append(f"⚠️ {rating}⭐ — below average. Address negative feedback.")
        else:
            score += 5
            feedback.append(f"❌ {rating}⭐ — critical. Fix product issues ASAP.")
    else:
        feedback.append("⚠️ No rating data found.")

    if count:
        c = int(count.replace(",", ""))
        if c >= 100:
            score += 50
            feedback.append(f"✅ {count} reviews — strong social proof.")
        elif c >= 30:
            score += 35
            feedback.append(f"⚠️ {count} reviews. Keep building — 100+ is the sweet spot.")
        elif c >= 10:
            score += 20
            feedback.append(f"⚠️ Only {count} reviews. Use Amazon Vine or insert cards.")
        else:
            score += 5
            feedback.append(f"❌ Only {count} reviews. This is a conversion killer.")
    else:
        feedback.append("⚠️ No review count found.")

    return min(score, 100), feedback


def analyze_listing(asin, marketplace="com"):
    """Full listing analysis."""
    print(f"\n🔍 Analyzing ASIN: {asin}")
    print("=" * 60)

    html = fetch_listing(asin, marketplace)
    if not html:
        return None

    data = parse_listing(html, asin)

    # Score each component
    title_score, title_fb = score_title(data.title)
    bullet_score, bullet_fb = score_bullets(data.bullets)
    image_score, image_fb = score_images(data.images_count)
    review_score, review_fb = score_reviews(data.rating, data.review_count)

    # Overall score (weighted)
    overall = int(
        title_score * 0.30 +
        bullet_score * 0.25 +
        image_score * 0.25 +
        review_score * 0.20
    )

    # Grade
    if overall >= 90:
        grade = "A+"
    elif overall >= 80:
        grade = "A"
    elif overall >= 70:
        grade = "B"
    elif overall >= 60:
        grade = "C"
    elif overall >= 50:
        grade = "D"
    else:
        grade = "F"

    # Print report
    print(f"\n📦 {data.brand} | {data.price}")
    print(f"📝 Title: {data.title[:80]}{'...' if len(data.title) > 80 else ''}")
    print(f"⭐ {data.rating} ({data.review_count} reviews)")

    print(f"\n{'=' * 60}")
    print(f"📊 LISTING SCORE: {overall}/100 (Grade: {grade})")
    print(f"{'=' * 60}")

    print(f"\n📝 TITLE ({title_score}/100)")
    for fb in title_fb:
        print(f"   {fb}")

    print(f"\n📋 BULLETS ({bullet_score}/100)")
    for fb in bullet_fb:
        print(f"   {fb}")

    print(f"\n📸 IMAGES ({image_score}/100)")
    for fb in image_fb:
        print(f"   {fb}")

    print(f"\n⭐ REVIEWS ({review_score}/100)")
    for fb in review_fb:
        print(f"   {fb}")

    # Save report
    report = {
        "asin": asin,
        "brand": data.brand,
        "title": data.title,
        "price": data.price,
        "rating": data.rating,
        "review_count": data.review_count,
        "bullet_count": len(data.bullets),
        "image_count": data.images_count,
        "scores": {
            "overall": overall,
            "grade": grade,
            "title": title_score,
            "bullets": bullet_score,
            "images": image_score,
            "reviews": review_score,
        },
        "title_feedback": title_fb,
        "bullet_feedback": bullet_fb,
        "image_feedback": image_fb,
        "review_feedback": review_fb,
    }

    return report


def generate_optimized_title(current_title, keywords=None):
    """Generate an optimized title suggestion."""
    # Basic optimization rules
    suggestions = []

    if len(current_title) < 80:
        suggestions.append("Expand title to 80-200 characters with relevant keywords")

    if current_title == current_title.upper():
        suggestions.append("Convert from ALL CAPS to Title Case")

    if not re.search(r'\d', current_title):
        suggestions.append("Add specific numbers (size, quantity, weight)")

    if '|' not in current_title and ' - ' not in current_title:
        suggestions.append("Add separators (|, -, ,) for readability")

    return suggestions


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyzer.py <ASIN> [marketplace]")
        print("Example: python3 analyzer.py B0XXXXXXXXX")
        print("Example: python3 analyzer.py B0XXXXXXXXX co.uk")
        sys.exit(1)

    asin = sys.argv[1]
    marketplace = sys.argv[2] if len(sys.argv) > 2 else "com"

    report = analyze_listing(asin, marketplace)

    if report:
        # Save report to file
        import os
        report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
        os.makedirs(report_dir, exist_ok=True)
        report_file = os.path.join(report_dir, f"{asin}-report.json")
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 Report saved: {report_file}")
