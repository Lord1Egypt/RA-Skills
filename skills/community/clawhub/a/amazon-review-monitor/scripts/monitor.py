#!/usr/bin/env python3
"""
Amazon Review Monitor — Track reviews, analyze sentiment, draft responses
Alerts on new negative reviews. Analyzes review trends over time.
"""

import json
import re
import sys
import urllib.request
import os
from collections import Counter
from datetime import datetime


def fetch_reviews(asin, marketplace="com", page=1):
    """Fetch reviews for an ASIN."""
    url = f"https://www.amazon.{marketplace}/product-reviews/{asin}?pageNumber={page}&sortBy=recent"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"❌ Failed to fetch reviews: {e}")
        return None


def parse_reviews(html):
    """Extract reviews from HTML."""
    reviews = []

    # Find review blocks
    review_blocks = re.findall(
        r'data-hook="review".*?data-hook="review-date"[^>]*>(.*?)</span>.*?'
        r'class="a-icon-alt">(.*?)</span>.*?'
        r'data-hook="review-title"[^>]*>.*?>(.*?)</span>.*?'
        r'data-hook="review-body"[^>]*>(.*?)</div>',
        html, re.DOTALL
    )

    for date_text, rating_text, title, body in review_blocks:
        # Clean up
        rating_match = re.search(r'(\d+\.?\d*) out of 5', rating_text)
        rating = float(rating_match.group(1)) if rating_match else 0

        # Clean HTML
        title = re.sub(r'<[^>]+>', '', title).strip()
        body = re.sub(r'<[^>]+>', '', body).strip()
        date_text = re.sub(r'<[^>]+>', '', date_text).strip()

        reviews.append({
            "date": date_text,
            "rating": rating,
            "title": title,
            "body": body[:500],
        })

    return reviews


def analyze_sentiment(reviews):
    """Simple sentiment analysis on reviews."""
    positive_words = [
        'love', 'great', 'excellent', 'amazing', 'perfect', 'best',
        'delicious', 'fantastic', 'wonderful', 'quality', 'fresh',
        'recommend', 'favorite', 'good', 'tasty', 'happy', 'pleased'
    ]
    negative_words = [
        'bad', 'terrible', 'awful', 'worst', 'disappointed', 'poor',
        'waste', 'horrible', 'disgusting', 'stale', 'expired',
        'broken', 'damaged', 'wrong', 'fake', 'scam', 'refund',
        'return', 'complaint', 'never', 'hate'
    ]

    pos_count = 0
    neg_count = 0
    themes_pos = Counter()
    themes_neg = Counter()

    for review in reviews:
        text = (review.get("title", "") + " " + review.get("body", "")).lower()

        for word in positive_words:
            if word in text:
                pos_count += 1
                themes_pos[word] += 1

        for word in negative_words:
            if word in text:
                neg_count += 1
                themes_neg[word] += 1

    return {
        "positive_mentions": pos_count,
        "negative_mentions": neg_count,
        "sentiment_ratio": round(pos_count / max(pos_count + neg_count, 1) * 100, 1),
        "top_positive_themes": themes_pos.most_common(5),
        "top_negative_themes": themes_neg.most_common(5),
    }


def draft_response(review):
    """Draft a seller response to a negative review."""
    rating = review.get("rating", 0)
    title = review.get("title", "")
    body = review.get("body", "")

    if rating >= 4:
        return None  # Don't respond to positive reviews

    response = f"""Thank you for your feedback. We're sorry to hear about your experience. """

    # Customize based on content
    text = (title + " " + body).lower()

    if any(w in text for w in ["expired", "stale", "old", "bad taste"]):
        response += "Product freshness is our top priority, and we take this seriously. "
        response += "Please contact us directly so we can send a replacement or issue a full refund."
    elif any(w in text for w in ["damaged", "broken", "crushed", "leak"]):
        response += "We apologize for the shipping damage. "
        response += "Please contact us and we'll send a replacement immediately at no charge."
    elif any(w in text for w in ["wrong", "not what", "different", "expected"]):
        response += "We want to make sure you get exactly what you ordered. "
        response += "Please reach out to us and we'll resolve this right away."
    else:
        response += "Your satisfaction matters to us. "
        response += "Please contact us so we can make this right."

    response += " We stand behind our products 100%."

    return response


def monitor_asin(asin, marketplace="com", pages=3):
    """Full review monitoring for an ASIN."""
    print(f"\n📊 Review Monitor: {asin}")
    print("=" * 60)

    all_reviews = []

    for page in range(1, pages + 1):
        html = fetch_reviews(asin, marketplace, page)
        if html:
            reviews = parse_reviews(html)
            all_reviews.extend(reviews)
            print(f"   Page {page}: {len(reviews)} reviews found")

    if not all_reviews:
        print("❌ No reviews found. The ASIN may be wrong or have no reviews.")
        return None

    print(f"\n📝 Total reviews analyzed: {len(all_reviews)}")

    # Rating distribution
    ratings = Counter()
    for r in all_reviews:
        ratings[int(r["rating"])] = ratings.get(int(r["rating"]), 0) + 1

    print(f"\n⭐ Rating Distribution:")
    for star in [5, 4, 3, 2, 1]:
        count = ratings.get(star, 0)
        pct = count / len(all_reviews) * 100 if all_reviews else 0
        bar = "█" * int(pct / 2)
        print(f"   {star}⭐ {bar} {count} ({pct:.0f}%)")

    # Average rating
    avg = sum(r["rating"] for r in all_reviews) / len(all_reviews) if all_reviews else 0
    print(f"\n   Average: {avg:.1f}⭐")

    # Sentiment
    sentiment = analyze_sentiment(all_reviews)
    print(f"\n😊 Sentiment: {sentiment['sentiment_ratio']}% positive")

    if sentiment["top_positive_themes"]:
        print(f"   ✅ Positive themes: {', '.join(w for w, _ in sentiment['top_positive_themes'])}")
    if sentiment["top_negative_themes"]:
        print(f"   ❌ Negative themes: {', '.join(w for w, _ in sentiment['top_negative_themes'])}")

    # Negative reviews that need attention
    negatives = [r for r in all_reviews if r["rating"] <= 2]
    if negatives:
        print(f"\n🚨 Negative Reviews Needing Response ({len(negatives)}):")
        for i, review in enumerate(negatives[:5]):
            print(f"\n   {i+1}. {'⭐' * int(review['rating'])} — {review['title']}")
            print(f"      {review['body'][:150]}...")
            response = draft_response(review)
            if response:
                print(f"      💬 Draft response: {response[:120]}...")

    return {
        "asin": asin,
        "total_reviews": len(all_reviews),
        "average_rating": round(avg, 1),
        "rating_distribution": dict(ratings),
        "sentiment": sentiment,
        "negative_count": len(negatives),
        "reviews": all_reviews,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 monitor.py <ASIN> [marketplace] [pages]")
        print("Example: python3 monitor.py B0XXXXXXXXX")
        print("Example: python3 monitor.py B0XXXXXXXXX com 5")
        sys.exit(1)

    asin = sys.argv[1]
    marketplace = sys.argv[2] if len(sys.argv) > 2 else "com"
    pages = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    result = monitor_asin(asin, marketplace, pages)

    if result:
        report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
        os.makedirs(report_dir, exist_ok=True)
        report_file = os.path.join(report_dir, f"reviews-{asin}.json")
        with open(report_file, "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n💾 Report saved: {report_file}")
