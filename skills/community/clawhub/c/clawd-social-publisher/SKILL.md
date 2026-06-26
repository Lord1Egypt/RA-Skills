---
name: social-publisher
description: "Automate social media publishing, engagement, and analytics. Schedule posts across 10+ platforms (Twitter/X, LinkedIn, Instagram, Facebook, TikTok, YouTube, Pinterest, Mastodon, Bluesky). Auto-generate content from RSS, blogs, or AI. Smart timing and cross-platform formatting. Save 15+ hours per week on social media management."
homepage: https://clawhub.com/skills/social-publisher
metadata:
  openclaw:
    emoji: "📱"
    requires:
      bins: ["openclaw", "curl"]
    tags: ["social-media", "marketing", "content", "automation", "smm"]
---

# Social Publisher Skill

**Automate your entire social media presence. One schedule, publish everywhere.**

## When to Use

✅ **USE this skill when:**

- "Schedule posts across all my social accounts"
- "Auto-post my blog content to Twitter/LinkedIn/Instagram"
- "Generate daily content from RSS feeds"
- "Create social posts from YouTube videos"
- "Repurpose long-form content into social posts"
- "Auto-engage with mentions and comments"
- "Track performance across platforms"

## When NOT to Use

❌ **DON'T use this skill when:**

- Manual creative work (painting, complex video editing)
- Personalized customer service (needs human empathy)
- Crisis communications (requires human judgment)
- One-time spontaneous posts

## 💸 The Business Case

**Time Savings**:
- Manual posting: 1-2 hours/day = 30-60 hours/month
- Content creation: 20 hours/month
- Analytics/reporting: 5 hours/month
- **Total: 55-85 hours/month = $3,300-5,100 value (at $60/hr)**

**Pricing**: $15-50/month
**Payback**: < 1 day of saved time

## Supported Platforms

| Platform | Features | Status |
|----------|----------|--------|
| Twitter / X | Posts, threads, polls, media | ✅ Full |
| LinkedIn | Posts, articles, company pages | ✅ Full |
| Instagram | Posts, Stories, Reels | ✅ Full |
| Facebook | Pages, groups | ✅ Full |
| TikTok | Video posts | ✅ Full |
| YouTube | Video uploads, Shorts | ✅ Full |
| Pinterest | Pins, boards | ✅ Full |
| Mastodon | Posts, CW, media | ✅ Full |
| Bluesky | Posts, media | ✅ Full |
| Threads | Posts, media | ✅ Full |
| Custom APIs | Any platform with API | ✅ Full |

## Quick Start: Cross-Platform Posting

### 1. Connect Your Accounts

Create `social-config.yaml`:

```yaml
accounts:
  twitter:
    api_key: "..."
    api_secret: "..."
    access_token: "..."
    access_secret: "..."

  linkedin:
    client_id: "..."
    client_secret: "..."
    access_token: "..."

  instagram:
    access_token: "..."
    user_id: "..."

# Add as many as needed
```

### 2. Create a Post Template

```yaml
campaign:
  name: "Blog Promotion"
  content_template: |
    🚀 New blog post!

    {{title}}

    Key insights:
    • {{insight_1}}
    • {{insight_2}}

    Read more: {{url}}

    #{{platform_hashtags}} #automation #productivity

  platforms:
    - twitter:
        max_length: 280
        hashtags: ["productivity", "automation"]
        # Auto-threads for long content

    - linkedin:
        max_length: 3000
        format: "article_summary"
        hashtags: ["productivity", "business"]

    - instagram:
        media: "image"  # or "video", "carousel"
        caption_template: |
          {{title}}
          .
          Swipe up for full article 🔗
          .
          .

  schedule:
    - platform: "twitter"
      time: "09:00 EST"
      days: ["mon", "wed", "fri"]

    - platform: "linkedin"
      time: "11:00 EST"
      days: ["tue", "thu"]

    - platform: "instagram"
      time: "13:00 EST"
      days: ["mon", "wed", "fri"]
```

### 3. Run the Workflow

```bash
# Preview what will be posted
clawhub workflow preview blog-promotion

# Start publishing
clawhub workflow start blog-promotion

# Check calendar
clawhub workflow calendar
```

---

## Core Features

### 1. Multi-Platform Scheduling

**One content, many destinations**:
- Write once, auto-format for each platform
- Platform-specific constraints (length, media)
- Optimal timing per platform
- Queue management with drag-and-drop calendar

### 2. AI Content Generation

**Turn any source into social posts**:

```yaml
content_generator:
  source: "rss"
  feeds:
    - https://blog.yoursite.com/feed
    - https://news.yoursite.com/rss

  ai_enhancement:
    rewrite_for: ["twitter", "linkedin", "instagram"]
    tone: "friendly_professional"
    add_hashtags: true
    generate_images: true  # DALL-E / Midjourney integration

  output:
    - draft: "Create draft in platform"
    - schedule: "Add to calendar"
```

**Supported sources**:
- RSS/Atom feeds
- YouTube videos (auto-generate posts from transcripts)
- Blog posts / articles
- Podcast episodes (audio → transcript → posts)
- Newsletters (Substack, Beehiiv)
- Product updates (Shopify, WooCommerce)
- Custom APIs

### 3. Auto-Engagement

**Never miss a mention**:

```yaml
engagement:
  triggers:
    - "@yourbrand mentioned"
    - "keyword: your_product"
    - "#yourhashtag"

  actions:
    - like: true
    - retweet: true
    - reply: "Thanks for sharing! Check out our latest: {{latest_post_url}}"
    - follow_back: true
    - add_to_list: "brand_mentions"

  filters:
    exclude_retweets: true
    min_engagement: 10
    sentiment: "positive"
```

**Supported platforms**: Twitter, LinkedIn, Instagram, Mastodon, Bluesky

### 4. Analytics & Reporting

**Unified dashboard**:
```yaml
reporting:
  schedule: "0 8 * * mon"  # Mondays 8 AM

  metrics:
    - platform: "all"
      metrics: ["impressions", "engagement_rate", "follower_growth", "clicks"]

  insights:
    - "Best performing platform this week"
    - "Optimal posting time"
    - "Top content types"
    - "Hashtag performance"

  distribution:
    - email: "marketing@company.com"
    - slack: "#social-analytics"
    - pdf: "reports/weekly-{{date}}.pdf"
```

### 5. Content Calendar

**Visual planning**:
```bash
# View calendar (opens browser)
clawhub social calendar

# Drag to reschedule
# Click to edit content
# See platform-specific previews
```

---

## Advanced Workflows

### Workflow: Content Repurposing

**Blog → Twitter thread → LinkedIn article → Instagram carousel**:

```yaml
workflow:
  name: "Content Repurposing"
  trigger: "new_blog_post"

steps:
  - extract: "Get blog content"
    agent: "blog-parser"

  - twitter:
      agent: "twitter-formatter"
      task: "Create 5-tweet thread from blog"
      output: "twitter_draft"

  - linkedin:
      agent: "linkedin-formatter"
      task: "Create LinkedIn article summary"
      input: "{{extract.output}}"

  - instagram:
      agent: "visual-designer"
      task: "Generate 3 carousel images"
      prompt: "Create visuals for: {{title}}"

  - schedule_all:
      agent: "scheduler"
      platforms: ["twitter", "linkedin", "instagram"]
      depends_on: [twitter, linkedin, instagram]
```

### Workflow: User-Generated Content Campaign

```yaml
ugc_campaign:
  hashtag: "#MyProductStory"

  monitor:
    - scan: "Instagram, Twitter, TikTok"
    - filter: "mentions + photos"
    - engagement: "like + thank reply"

  curate:
    - select: "top 5 per week"
    - permission: "DM for repost"
    - add_to: "weekly roundup"

  repost:
    - platform: "instagram_stories"
      format: "customer_spotlight"
    - platform: "facebook"
      format: "testimonial"
```

---

## Platform-Specific Tips

### Instagram
- Best times: 11 AM-1 PM, 7-9 PM local time
- Carousels get 2x engagement
- Use up to 30 hashtags (10-15 optimal)
- First comment can be additional caption

### Twitter/X
- Threads get 3x engagement vs single tweets
- Optimal: 1-3 tweets per thread
- Best times: 8-10 AM, 12-2 PM, 5-7 PM
- Use polls for engagement

### LinkedIn
- Long-form content (1300+ chars) performs best
- Post Tue/Wed/Thu 9-11 AM
- Tag companies/people strategically
- Documents (PDFs) get high reach

### TikTok
- Vertical video only (9:16)
- First 3 seconds critical
- Trending sounds increase reach
- Post 7-9 PM local time

---

## Pricing Tiers

### Free (Limited)
- 1 connected account per platform
- 10 scheduled posts
- Basic analytics
- Community support

### Pro ($15/month)
- Unlimited accounts
- 500 scheduled posts
- AI content generation (100 posts/month)
- Advanced analytics
- Email support
- **Most popular**

### Business ($50/month)
- Everything in Pro
- White-label reports
- Team collaboration (5 users)
- API access
- Priority support
- Custom integrations

### Enterprise (Custom)
- Unlimited everything
- Custom platform integrations
- SLA guarantees
- Dedicated account manager
- On-premise deployment option
- **From $500/month**

---

## Money-Making Features to Enable

### 1. White-Label Reports
```yaml
client_report:
  branding:
    logo: "client-logo.png"
    colors: ["#FF0000", "#00FF00"]
    footer: "Generated by YourAgencyName"

  sections:
    - executive_summary
    - platform_breakdown
    - top_content
    - recommendations
```
→ Charge $100-500/month for branded reports

### 2. Content Packages
```yaml
content_packages:
  basic: "5 posts/week across 2 platforms" → $299/mo
  growth: "15 posts/week across 4 platforms" → $799/mo
  enterprise: "Unlimited + analytics" → custom
```
→ High-margin recurring revenue

### 3. Agency Reseller Program
- Agency buys bulk credits at discount
- Resells to clients at markup
- 20-40% margin for partners

---

## Competitive Advantages

| Feature | Competitors | Us |
|---------|-------------|----|
| AI content generation | Limited | ✅ Built-in |
| Unlimited platforms | $$ expensive | ✅ All-in-one |
| Custom integrations | No | ✅ Yes (OpenClaw) |
| Reposting/UGC | Manual | ✅ Automated |
| Pricing | $99-299/mo | $15-50/mo |
| Enterprise features | Add-ons | ✅ Included |

**Better, cheaper, more flexible** → Easy sell!

---

## Launch Checklist

- [x] Create skill with complete documentation
- [ ] Set up Stripe/PayPal for payments
- [ ] Create landing page (showcase ROI)
- [ ] Build 3 example workflows (free)
- [ ] Record 5-minute demo video
- [ ] Offer 14-day free trial
- [ ] Collect testimonials from beta users
- [ ] Publish to ClawHub
- [ ] Post on ProductHunt, Reddit, indiehackers
- [ ] Partner with OpenClaw for cross-promotion

---

_Automate social media. Focus on strategy, not scheduling._ 📱✨
