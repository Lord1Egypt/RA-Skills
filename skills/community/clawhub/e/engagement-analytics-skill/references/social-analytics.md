# Social Media Engagement Tracker

## Owned Social — What to Collect

### Per Post
```
post_id              platform              post_type (image/video/reel/story/carousel)
published_at         caption_length        hashtags_used []
reach                impressions           engagement_count
likes                comments              shares / reposts
saves                click_throughs        profile_visits_from_post
video_views          watch_time_avg        completion_rate
story_replies        story_exits           poll_responses
```

### Per Profile / Account (Weekly Snapshot)
```
follower_count       follower_growth        follower_growth_rate (%)
following_count      avg_engagement_rate    reach_rate (reach / followers)
total_posts          posting_frequency      best_performing_content_type
profile_visits       bio_link_clicks        branded_hashtag_mentions
audience_quality_score   (engaged vs ghost/bot estimate)
```

### Engagement Rate Formula
```
Engagement Rate = (Likes + Comments + Shares + Saves) / Reach × 100

Industry benchmarks (2025):
  Instagram:  1–3% (good), >3% (excellent)
  Facebook:   0.5–1% (good), >1% (excellent)  
  LinkedIn:   1–5% (varies by content type)
  TikTok:     3–8% (good), >8% (excellent)
  Twitter/X:  0.5–1% (good)
```

---

## Platform APIs for Owned Social

### Meta Graph API (Instagram + Facebook)

```python
import requests

TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"
ACCOUNT_ID = "YOUR_IG_BUSINESS_ACCOUNT_ID"

# Get recent posts with engagement metrics
resp = requests.get(
    f"https://graph.facebook.com/v21.0/{ACCOUNT_ID}/media",
    params={
        "fields": "id,caption,media_type,timestamp,like_count,comments_count,reach,impressions,saved,video_views",
        "access_token": TOKEN,
    }
)
posts = resp.json().get("data", [])

# Get post-level insights (for a specific post)
post_id = posts[0]["id"]
resp = requests.get(
    f"https://graph.facebook.com/v21.0/{post_id}/insights",
    params={
        "metric": "reach,impressions,saved,video_views,profile_visits",
        "access_token": TOKEN,
    }
)

# Get profile-level follower metrics
resp = requests.get(
    f"https://graph.facebook.com/v21.0/{ACCOUNT_ID}/insights",
    params={
        "metric": "follower_count,profile_views,reach,impressions",
        "period": "week",
        "access_token": TOKEN,
    }
)
```

**Token requirements:**
- Need Instagram Business or Creator account linked to a Facebook Page
- Tokens expire — use long-lived tokens (60-day) + refresh before expiry
- Rate limit: 200 requests/hour per token

### LinkedIn API (Company Pages)

```python
# LinkedIn Marketing API — requires Company Admin access
resp = requests.get(
    "https://api.linkedin.com/v2/organizationalEntityShareStatistics",
    headers={"Authorization": f"Bearer {OAUTH_TOKEN}"},
    params={
        "q": "organizationalEntity",
        "organizationalEntity": "urn:li:organization:YOUR_ORG_ID",
        "timeIntervals.timeGranularityType": "WEEK",
    }
)
```

---

## Competitor Social Tracking

### What to Monitor (Competitor)
```
post_frequency (posts/week)       content_mix (video%, image%, text%)
avg_engagement_rate               follower_growth_rate
top_performing_post_types         dominant_themes / messaging
offer_types_in_ads                branded_hashtag_strategy
influencer_partnerships           response_time_to_comments
```

### Data Sources for Competitor Tracking

**Free:**
- Manual observation + Google Sheets logging
- Social Blade (follower growth history): https://socialblade.com
- Meta Ads Library (for paid social competitor ads)
- LinkedIn Company Page (follower count visible publicly)

**Paid tools:**
- **Sprout Social** — competitor benchmarking, sentiment analysis
- **Brandwatch / Mention** — brand monitoring, sentiment, share of voice
- **Phlanx** — engagement rate calculators
- **Iconosquare** — Instagram/TikTok competitor analytics

**Apify Actors (for scraping):**
```python
# Instagram profile scraper
actor_input = {
    "usernames": ["competitor_handle"],
    "resultsLimit": 30,
}
# Actor: apify/instagram-scraper
# Returns: follower count, post data, engagement metrics

# TikTok profile scraper
actor_input = {
    "profiles": ["@competitor_handle"],
    "resultsPerPage": 30,
}
# Actor: clockworks/free-tiktok-scraper
```

---

## Sentiment Analysis

### For Owned Comments
```python
from anthropic import Anthropic

client = Anthropic()

def analyze_comment_sentiment(comments: list[str]) -> dict:
    prompt = f"""Analyze these social media comments and classify each as:
    - positive, neutral, or negative
    - category: product_feedback, shipping, price, comparison, question, praise, complaint
    - urgency: high (requires response), medium, low
    
    Comments: {comments}
    
    Return JSON: [{{"comment": "...", "sentiment": "...", "category": "...", "urgency": "..."}}]"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

### Competitor Sentiment Signals
Monitor competitor comments for:
- Recurring complaints (product, price, support issues) → your opportunity
- Praise themes → what customers value that you should match or beat
- Questions never answered → gaps you can position against

---

## Owned Social — Performance Dashboard Schema

```python
# Weekly snapshot to store per account per platform
weekly_snapshot = {
    "week": "2025-W15",
    "platform": "instagram",
    "account_id": "YOUR_ID",
    
    # Growth
    "followers_end": 45230,
    "followers_start": 44800,
    "follower_growth": 430,
    "follower_growth_pct": 0.96,
    
    # Reach & Impressions
    "total_reach": 128000,
    "total_impressions": 210000,
    "reach_rate": 2.83,               # reach / followers * 100
    
    # Engagement
    "total_engagements": 4100,
    "avg_engagement_rate": 3.20,      # %
    "total_comments": 380,
    "total_likes": 3200,
    "total_shares": 290,
    "total_saves": 230,
    
    # Content
    "posts_published": 7,
    "reels_published": 3,
    "stories_published": 21,
    "best_performing_post_id": "ABC123",
    "best_performing_format": "reel",
    
    # Profile
    "profile_visits": 2100,
    "bio_link_clicks": 340,
}
```

---

## User-Generated Content (UGC) Tracking

Track content your audience creates about your brand:
```
branded_hashtag_mentions_count
tagged_posts_count
mention_sentiment (positive / neutral / negative)
ugc_reach_total              (sum of creators' reach)
top_ugc_creators []          (accounts with most engagement on your brand content)
ugc_response_rate            (how often you're engaging back)
```

**Collection:** Use Meta Graph API hashtag search (`/ig_hashtag_search`) or
Apify Instagram Hashtag Scraper for owned hashtags.
