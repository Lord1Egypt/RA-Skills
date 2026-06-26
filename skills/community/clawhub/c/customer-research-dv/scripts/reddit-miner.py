#!/usr/bin/env python3
"""
Reddit/Forum Mining Script
Extracts customer insights from Reddit discussions.
"""

import argparse
import json
import sys
from datetime import datetime
from collections import defaultdict
import praw
from textblob import TextBlob

def analyze_sentiment(text):
    """Analyze sentiment of text using TextBlob."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        return "positive", polarity
    elif polarity < -0.1:
        return "negative", polarity
    else:
        return "neutral", polarity

def extract_pain_points(text):
    """Extract potential pain points from text."""
    pain_keywords = [
        "hate", "frustrated", "annoying", "difficult", "confusing", 
        "expensive", "slow", "complicated", "wish", "should", 
        "needs", "missing", "lack", "problem", "issue", "bug"
    ]
    
    text_lower = text.lower()
    found_keywords = [kw for kw in pain_keywords if kw in text_lower]
    
    return found_keywords

def extract_feature_requests(text):
    """Extract potential feature requests."""
    request_patterns = [
        "would be nice if", "wish it had", "needs to", "should have",
        "would love", "looking for", "want", "need", "require"
    ]
    
    text_lower = text.lower()
    found_patterns = [p for p in request_patterns if p in text_lower]
    
    return found_patterns

def mine_reddit(category, subreddits, limit=100, time_filter="month"):
    """
    Mine Reddit for customer insights.
    
    Args:
        category: Product category to search for
        subreddits: List of subreddit names
        limit: Number of posts to fetch per subreddit
        time_filter: Time filter (hour, day, week, month, year, all)
    
    Returns:
        dict: Structured insights
    """
    # Initialize Reddit API (read-only mode, no credentials needed)
    reddit = praw.Reddit(
        client_id="reddit_public",
        client_secret=None,
        user_agent="customer-research/1.0"
    )
    
    insights = {
        "category": category,
        "subreddits_searched": subreddits,
        "timestamp": datetime.now().isoformat(),
        "total_posts_analyzed": 0,
        "total_comments_analyzed": 0,
        "themes": defaultdict(int),
        "pain_points": [],
        "feature_requests": [],
        "sentiment_distribution": {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        },
        "top_mentions": [],
        "competitor_mentions": defaultdict(lambda: {"count": 0, "sentiment": []})
    }
    
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            
            # Search for category mentions
            for post in subreddit.search(category, time_filter=time_filter, limit=limit):
                insights["total_posts_analyzed"] += 1
                
                # Analyze post title and body
                text = f"{post.title} {post.selftext}"
                sentiment, polarity = analyze_sentiment(text)
                insights["sentiment_distribution"][sentiment] += 1
                
                # Extract pain points
                pain_keywords = extract_pain_points(text)
                if pain_keywords:
                    insights["pain_points"].append({
                        "text": post.title,
                        "keywords": pain_keywords,
                        "url": f"https://reddit.com{post.permalink}",
                        "score": post.score,
                        "sentiment": sentiment
                    })
                
                # Extract feature requests
                feature_patterns = extract_feature_requests(text)
                if feature_patterns:
                    insights["feature_requests"].append({
                        "text": post.title,
                        "patterns": feature_patterns,
                        "url": f"https://reddit.com{post.permalink}",
                        "score": post.score
                    })
                
                # Analyze top comments
                post.comments.replace_more(limit=0)
                for comment in post.comments.list()[:10]:
                    insights["total_comments_analyzed"] += 1
                    
                    comment_sentiment, _ = analyze_sentiment(comment.body)
                    insights["sentiment_distribution"][comment_sentiment] += 1
                    
                    # Extract pain points from comments
                    pain_keywords = extract_pain_points(comment.body)
                    if pain_keywords and comment.score > 5:
                        insights["pain_points"].append({
                            "text": comment.body[:200],
                            "keywords": pain_keywords,
                            "url": f"https://reddit.com{post.permalink}",
                            "score": comment.score,
                            "sentiment": comment_sentiment
                        })
        
        except Exception as e:
            print(f"Error processing subreddit {subreddit_name}: {e}", file=sys.stderr)
            continue
    
    # Sort by score
    insights["pain_points"].sort(key=lambda x: x["score"], reverse=True)
    insights["feature_requests"].sort(key=lambda x: x["score"], reverse=True)
    
    # Limit to top results
    insights["pain_points"] = insights["pain_points"][:50]
    insights["feature_requests"] = insights["feature_requests"][:50]
    
    return insights

def main():
    parser = argparse.ArgumentParser(
        description="Mine Reddit for customer insights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Mine tax software discussions
  python reddit-miner.py --category "tax software" --subreddits personalfinance,tax --output insights.json
  
  # Search multiple subreddits with custom limit
  python reddit-miner.py --category "budgeting app" --subreddits personalfinance,Fire,leanfire --limit 200 --time-filter year
        """
    )
    
    parser.add_argument("--category", required=True, help="Product category to search")
    parser.add_argument("--subreddits", required=True, help="Comma-separated list of subreddits")
    parser.add_argument("--limit", type=int, default=100, help="Posts per subreddit (default: 100)")
    parser.add_argument("--time-filter", default="month", choices=["hour", "day", "week", "month", "year", "all"], help="Time filter (default: month)")
    parser.add_argument("--output", required=True, help="Output JSON file")
    
    args = parser.parse_args()
    
    subreddits = [s.strip() for s in args.subreddits.split(",")]
    
    print(f"Mining Reddit for '{args.category}' in {len(subreddits)} subreddit(s)...", file=sys.stderr)
    
    insights = mine_reddit(args.category, subreddits, args.limit, args.time_filter)
    
    with open(args.output, "w") as f:
        json.dump(insights, f, indent=2)
    
    print(f"\nResults saved to {args.output}", file=sys.stderr)
    print(f"Posts analyzed: {insights['total_posts_analyzed']}", file=sys.stderr)
    print(f"Comments analyzed: {insights['total_comments_analyzed']}", file=sys.stderr)
    print(f"Pain points identified: {len(insights['pain_points'])}", file=sys.stderr)
    print(f"Feature requests identified: {len(insights['feature_requests'])}", file=sys.stderr)

if __name__ == "__main__":
    main()
