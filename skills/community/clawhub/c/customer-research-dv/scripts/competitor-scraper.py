#!/usr/bin/env python3
"""
Competitor Review Scraper
Scrapes product reviews from public platforms to identify gaps and sentiment.
"""

import argparse
import json
import sys
import time
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlparse, urljoin

try:
    from bs4 import BeautifulSoup
    import requests
    from textblob import TextBlob
except ImportError:
    print("Error: Missing dependencies. Install with:", file=sys.stderr)
    print("  pip install beautifulsoup4 requests textblob", file=sys.stderr)
    sys.exit(1)

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        return "positive", polarity
    elif polarity < -0.1:
        return "negative", polarity
    else:
        return "neutral", polarity

def extract_features_mentioned(review_text):
    """Extract potential feature mentions from review text."""
    # Common feature keywords
    feature_keywords = [
        "interface", "ui", "ux", "design", "dashboard",
        "speed", "performance", "fast", "slow",
        "integration", "api", "export", "import",
        "support", "customer service", "help",
        "price", "pricing", "cost", "expensive", "cheap",
        "mobile", "app", "desktop",
        "reporting", "analytics", "data",
        "security", "privacy", "encryption",
        "automation", "manual", "automatic"
    ]
    
    text_lower = review_text.lower()
    found = [kw for kw in feature_keywords if kw in text_lower]
    return found

def scrape_gumroad_reviews(product_url):
    """
    Scrape Gumroad product page for reviews/comments.
    Note: Gumroad doesn't have a formal review system, this is a placeholder.
    """
    reviews = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(product_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Gumroad structure varies - this is a basic example
        # In practice, you'd need to inspect the actual HTML structure
        reviews.append({
            "platform": "gumroad",
            "source_url": product_url,
            "note": "Gumroad doesn't have built-in reviews. Check social proof on the page.",
            "scraped_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error scraping Gumroad: {e}", file=sys.stderr)
    
    return reviews

def scrape_producthunt_reviews(product_slug):
    """
    Scrape Product Hunt for reviews/comments.
    Note: Product Hunt has anti-scraping measures. This is a basic example.
    """
    reviews = []
    
    try:
        url = f"https://www.producthunt.com/posts/{product_slug}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Product Hunt structure changes frequently
        # This is a placeholder - real implementation would need regular updates
        reviews.append({
            "platform": "producthunt",
            "source_url": url,
            "note": "Product Hunt scraping requires API or manual review collection",
            "scraped_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error scraping Product Hunt: {e}", file=sys.stderr)
    
    return reviews

def scrape_generic_reviews(url):
    """
    Generic web scraper for review pages.
    Looks for common review HTML patterns.
    """
    reviews = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Common review selectors (generic patterns)
        review_selectors = [
            {'class': 'review'},
            {'class': 'review-content'},
            {'class': 'user-review'},
            {'itemprop': 'review'},
        ]
        
        for selector in review_selectors:
            review_elements = soup.find_all('div', selector)
            
            for elem in review_elements[:50]:  # Limit to 50
                text = elem.get_text(strip=True)
                
                if len(text) > 20:  # Minimum review length
                    sentiment, polarity = analyze_sentiment(text)
                    features = extract_features_mentioned(text)
                    
                    reviews.append({
                        "text": text[:500],  # Truncate long reviews
                        "sentiment": sentiment,
                        "polarity": polarity,
                        "features_mentioned": features,
                        "source_url": url
                    })
        
        if not reviews:
            reviews.append({
                "platform": "generic",
                "source_url": url,
                "note": "No reviews found with standard selectors. Manual inspection required.",
                "scraped_at": datetime.now().isoformat()
            })
        
    except Exception as e:
        print(f"Error scraping {url}: {e}", file=sys.stderr)
    
    return reviews

def analyze_reviews(reviews):
    """Analyze scraped reviews for insights."""
    analysis = {
        "total_reviews": len(reviews),
        "sentiment_distribution": defaultdict(int),
        "feature_mentions": defaultdict(int),
        "common_complaints": [],
        "common_praises": [],
        "pricing_mentions": 0,
        "support_mentions": 0
    }
    
    positive_reviews = []
    negative_reviews = []
    
    for review in reviews:
        if "sentiment" in review:
            analysis["sentiment_distribution"][review["sentiment"]] += 1
            
            if review["sentiment"] == "positive":
                positive_reviews.append(review)
            elif review["sentiment"] == "negative":
                negative_reviews.append(review)
        
        # Count feature mentions
        for feature in review.get("features_mentioned", []):
            analysis["feature_mentions"][feature] += 1
        
        # Check for pricing/support mentions
        text_lower = review.get("text", "").lower()
        if any(word in text_lower for word in ["price", "cost", "expensive", "cheap"]):
            analysis["pricing_mentions"] += 1
        if any(word in text_lower for word in ["support", "help", "service", "response"]):
            analysis["support_mentions"] += 1
    
    # Extract common complaints (top negative reviews)
    analysis["common_complaints"] = [
        {
            "text": r["text"][:200],
            "polarity": r["polarity"],
            "features": r.get("features_mentioned", [])
        }
        for r in sorted(negative_reviews, key=lambda x: x.get("polarity", 0))[:10]
    ]
    
    # Extract common praises (top positive reviews)
    analysis["common_praises"] = [
        {
            "text": r["text"][:200],
            "polarity": r["polarity"],
            "features": r.get("features_mentioned", [])
        }
        for r in sorted(positive_reviews, key=lambda x: x.get("polarity", 0), reverse=True)[:10]
    ]
    
    # Convert feature mentions to sorted list
    analysis["feature_mentions"] = sorted(
        [{"feature": k, "count": v} for k, v in analysis["feature_mentions"].items()],
        key=lambda x: x["count"],
        reverse=True
    )[:20]
    
    return analysis

def scrape_competitor(platform, identifier):
    """
    Scrape competitor reviews from specified platform.
    
    Args:
        platform: Platform name (gumroad, producthunt, url)
        identifier: Product identifier (URL or slug)
    
    Returns:
        list: Reviews
    """
    if platform == "gumroad":
        return scrape_gumroad_reviews(identifier)
    elif platform == "producthunt":
        return scrape_producthunt_reviews(identifier)
    elif platform == "url":
        return scrape_generic_reviews(identifier)
    else:
        print(f"Unknown platform: {platform}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(
        description="Scrape competitor reviews from public platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape Gumroad product
  python competitor-scraper.py --platform gumroad --url "https://gumroad.com/l/example" --output reviews.json
  
  # Scrape Product Hunt
  python competitor-scraper.py --platform producthunt --identifier "product-slug" --output reviews.json
  
  # Scrape generic review page
  python competitor-scraper.py --platform url --url "https://example.com/reviews" --output reviews.json
  
Note: Many platforms have anti-scraping measures. For production use:
  - Respect robots.txt
  - Add rate limiting
  - Consider using official APIs where available
  - Manual review collection may be more reliable
        """
    )
    
    parser.add_argument("--platform", required=True, choices=["gumroad", "producthunt", "url"], help="Platform to scrape")
    parser.add_argument("--identifier", help="Product identifier (slug or ID)")
    parser.add_argument("--url", help="Direct URL to scrape")
    parser.add_argument("--output", required=True, help="Output JSON file")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between requests (seconds)")
    
    args = parser.parse_args()
    
    identifier = args.url or args.identifier
    if not identifier:
        print("Error: Must provide --url or --identifier", file=sys.stderr)
        sys.exit(1)
    
    print(f"Scraping {args.platform}: {identifier}", file=sys.stderr)
    
    reviews = scrape_competitor(args.platform, identifier)
    
    # Add delay to be respectful
    time.sleep(args.delay)
    
    # Analyze reviews
    analysis = analyze_reviews(reviews)
    
    result = {
        "platform": args.platform,
        "identifier": identifier,
        "scraped_at": datetime.now().isoformat(),
        "reviews": reviews,
        "analysis": analysis
    }
    
    # Save results
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nScraping complete!", file=sys.stderr)
    print(f"Reviews collected: {len(reviews)}", file=sys.stderr)
    print(f"Results saved to {args.output}", file=sys.stderr)
    
    if analysis["total_reviews"] > 0:
        print(f"\nSentiment distribution:", file=sys.stderr)
        for sentiment, count in analysis["sentiment_distribution"].items():
            print(f"  {sentiment}: {count}", file=sys.stderr)

if __name__ == "__main__":
    main()
