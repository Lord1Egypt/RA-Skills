---
name: Content Calendar Planner with AI-powered Content Scheduling & Google Calendar Integration
description: "Generate optimized 30/60/90-day content calendars by analyzing brand voice, industry trends, and engagement data. Use when the user needs content strategy planning, editorial calendars, or campaign scheduling for solopreneurs and agencies."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","GOOGLE_ANALYTICS_KEY"],"bins":["python3"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📅"}}
---

## Overview

The **AI-Powered Content Calendar Planner** is a comprehensive content strategy automation skill that transforms scattered content ideas into strategically aligned, data-driven publishing calendars. This skill leverages OpenAI's GPT models, Google Analytics insights, and industry trend analysis to generate personalized content plans that maximize engagement and conversion.

**Why This Matters:**
- **Time Savings**: Reduces planning time from 8-12 hours to 15 minutes
- **Strategic Alignment**: Ensures every piece of content connects to business goals
- **Data-Driven**: Uses real analytics and trend data instead of guesswork
- **Scalability**: Perfect for solopreneurs managing 1-3 brands or agencies managing 10+ client accounts
- **Integrations**: Works with WordPress, HubSpot, Google Calendar, Slack, and Airtable

**Perfect For:**
- Content strategists planning multi-channel campaigns
- Small business owners juggling blog, email, and social media
- Digital agencies managing multiple client calendars
- SaaS companies aligning content with product roadmaps
- E-commerce brands synchronizing content with seasonal trends

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Basic 30-Day Calendar
```
Generate a 30-day content calendar for my SaaS productivity tool. 
My brand voice is casual but professional. Target audience: remote workers 
aged 25-45. Key topics: time management, focus techniques, and workflow automation. 
Include 3 blog posts, 10 social media posts, and 2 email campaigns.
```

### Example 2: Data-Driven 60-Day Plan
```
Create a 60-day content plan using my Google Analytics data. My blog averages 
1,200 monthly visitors, with highest engagement on Tuesdays and Thursdays. 
Top-performing content: productivity hacks (42% engagement), case studies (38%), 
how-tos (35%). Include recommended publishing times and content types optimized 
for each platform.
```

### Example 3: Trend-Aligned 90-Day Strategy
```
Build a 90-day content calendar for my e-commerce skincare brand aligned with 
Q2 trends. Include seasonal content hooks, upcoming holidays (Mother's Day, 
Father's Day), and trending topics in skincare. Mix educational content (40%), 
product features (35%), and user-generated content (25%).
```

### Example 4: Agency Multi-Client Setup
```
Generate content calendars for 3 of my agency clients simultaneously:
1. Tech startup (B2B, LinkedIn-focused, technical audience)
2. Fashion brand (B2C, Instagram-focused, Gen Z audience)
3. Fitness coaching (Community-driven, YouTube + email focus)

Provide separate 30-day plans optimized for each platform and audience.
```

---

## Capabilities

### 1. **Multi-Timeline Planning**
Generate calendars for 30, 60, or 90-day periods with flexible start dates:
- Automatic content distribution across timeframes
- Built-in buffer days for flexibility
- Holiday and seasonal event integration
- Promotional event spacing

### 2. **Brand Voice & Tone Matching**
Analyzes your brand voice and maintains consistency:
- Custom tone profiles (corporate, casual, humorous, educational, etc.)
- Audience-specific language optimization
- Maintains brand guidelines across all suggested content
- Persona-based content creation recommendations

### 3. **Analytics Integration**
Pulls real data from your existing platforms:
- **Google Analytics**: Traffic patterns, engagement metrics, top-performing content
- **Social Media APIs**: Historical engagement rates, optimal posting times, audience demographics
- **WordPress REST API**: Existing post performance, category trends
- Automatic identification of your best-performing content pillars

### 4. **Trend & Industry Intelligence**
Incorporates current trends and seasonal opportunities:
- Real-time industry trend detection
- Seasonal event calendar (holidays, awareness months, industry events)
- Competitor content analysis (optional)
- Emerging topics in your niche
- SEO keyword opportunity mapping

### 5. **Multi-Channel Content Optimization**
Generates platform-specific variations:
- **Blog Posts**: Full SEO-optimized outlines with keywords
- **Social Media**: Hashtag recommendations, optimal posting times
- **Email Campaigns**: Subject lines with A/B testing suggestions
- **LinkedIn**: Professional formatting with engagement tactics
- **YouTube/Video**: Script outlines and content hooks

### 6. **Content Repurposing Engine**
Maximizes ROI by suggesting content variations:
- 1 blog post → 8 social posts + email newsletter + video script
- Automatically cross-references related content pieces
- Identifies opportunities to update and repromote existing content

### 7. **Engagement & Conversion Optimization**
Strategically sequences content for maximum impact:
- Educational content → Product introduction → Promotional content → Case study
- Call-to-action (CTA) recommendations for each piece
- Content gap identification
- Customer journey mapping

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API access (for content generation and analysis)
export OPENAI_API_KEY="sk-..."

# Google Analytics 4 access (for engagement data)
export GOOGLE_ANALYTICS_KEY="your-ga4-property-id"

# Optional: For social media insights
export FACEBOOK_ACCESS_TOKEN="your-token"
export TWITTER_API_KEY="your-key"
export INSTAGRAM_BUSINESS_ACCOUNT_ID="your-id"

# Optional: For WordPress integration
export WORDPRESS_SITE_URL="https://yourblog.com"
export WORDPRESS_API_KEY="your-app-password"

# Optional: For HubSpot email data
export HUBSPOT_API_KEY="your-hubspot-key"
```

### Setup Instructions

**1. Enable Google Analytics Data:**
```
Set up your Google Analytics 4 property and create a service account with 
read access. Download the credentials JSON file and provide the property ID.
```

**2. Configure Brand Profile:**
Create a `brand_profile.json` in your working directory:
```json
{
  "brand_name": "Your Company",
  "industry": "SaaS",
  "target_audience": "Small business owners, age 30-50",
  "tone": "Professional yet approachable",
  "content_pillars": [
    "productivity tips",
    "customer success stories",
    "product updates",
    "industry trends"
  ],
  "publishing_goals": {
    "blog_posts_monthly": 4,
    "social_posts_weekly": 10,
    "email_campaigns_monthly": 2
  },
  "platform_focus": ["blog", "linkedin", "email", "twitter"]
}
```

**3. Connect Analytics Platforms:**
```
Link your Google Analytics, WordPress, and social media accounts for 
real data integration. The skill will automatically pull historical 
engagement data to inform recommendations.
```

---

## Example Outputs

### Output 1: 30-Day Content Calendar (JSON Format)

```json
{
  "calendar_period": "30 days",
  "start_date": "2024-02-15",
  "brand_name": "TechFlow Productivity",
  "content_summary": {
    "total_pieces": 15,
    "blog_posts": 3,
    "social_posts": 10,
    "email_campaigns": 2
  },
  "days": [
    {
      "date": "2024-02-15",
      "day_name": "Thursday",
      "content": [
        {
          "type": "blog_post",
          "title": "5 Focus Techniques Remote Workers Swear By",
          "focus_keyword": "remote work productivity",
          "word_count": 1800,
          "estimated_read_time": "7 min",
          "cta": "Download our free focus guide",
          "seo_score": 87,
          "content_pillar": "productivity tips"
        }
      ]
    },
    {
      "date": "2024-02-16",
      "day_name": "Friday",
      "content": [
        {
          "type": "social_post",
          "platform": "LinkedIn",
          "copy": "80% of remote workers struggle with distractions. Here's a simple 5-minute technique that changed our team's productivity...",
          "hashtags": ["#RemoteWork", "#Productivity", "#FocusTips"],
          "optimal_posting_time": "09:00 AM",
          "estimated_reach": "2,400",
          "engagement_prediction": "120-150 likes"
        },
        {
          "type": "social_post",
          "platform": "Twitter",
          "copy": "Quick win: The Pomodoro Technique works even better when combined with our 'notification silence' feature. 25 min of deep work = 3x output.",
          "hashtags": ["#ProductivityHack", "#RemoteWork"],
          "optimal_posting_time": "02:00 PM",
          "estimated_reach": "1,200"
        }
      ]
    }
  ],
  "analytics_insights": {
    "best_posting_days": ["Tuesday", "Thursday"],
    "best_posting_times": ["09:00 AM", "02:00 PM"],
    "recommended_content_mix": "45% educational, 35% promotional, 20% community",
    "historical_top_performer": "How-to articles (avg. 1,200 views)"
  }
}
```

### Output 2: Email Campaign Suggestions

```
CAMPAIGN: "Deep Work Series" (3-part email sequence)

Email 1 (Day 3): "The Focus Crisis: Why Remote Workers Can't Concentrate"
- Subject line A: "Why your focus is broken (and how to fix it)"
- Subject line B: "The #1 distraction killing your productivity"
- Preview text: "Hint: It's probably what you think it is..."
- CTA: "Get my 5-technique framework (free download)"
- Best send time: Tuesday, 9:00 AM
- Estimated open rate: 28-32%

Email 2 (Day 8): "The Proof: Real Results from 2,000+ Users"
- Subject line: "These 3 techniques increased our output by 40%"
- CTA: "See how [Customer Name] tripled their output"
- Best send time: Thursday, 2:00 PM
- Estimated conversion: 4-6%

Email 3 (Day 15): "Ready to Transform Your Workday?"
- Subject line: "Only 3 seats left in this month's cohort"
- CTA: "Join the Deep Work Challenge"
- Best send time: Wednesday, 10:00 AM
- Estimated sales: $2,400-3,200
```

### Output 3: Visual Calendar Markdown

```
## February 2024 Content Calendar - TechFlow Productivity

| Date | Type | Topic | Platform | CTA | Priority |
|------|------|-------|----------|-----|----------|
| Feb 15 | Blog | 5 Focus Techniques | Blog | Download guide | High |
| Feb 16 | Social | Pomodoro + Silence | LinkedIn | Read blog | Medium |
| Feb 16 | Social | Focus hack | Twitter | Link | Low |
| Feb 20 | Email | Deep Work Crisis | Email | Download PDF | High |
| Feb 22 | Blog | Case Study: 40% boost | Blog | Email signup | High |
| Feb 23 | Social | Case study teaser | Instagram | Link to blog | Medium |
| Feb 28 | Email | Social proof | Email | Enroll | High |

**Content Gaps Identified:**
- No video content scheduled (recommendation: add 1 YouTube video per month)
- Underutilized TikTok (recommendation: repurpose 2-3 social posts monthly)
```

---

## Tips & Best Practices

### 1. **Maximize Data Integration**
- Connect Google Analytics for at least 3 months of historical data before planning
- Include 2-3 months of social media insights for accurate posting time recommendations
- Update your brand profile quarterly to reflect strategy shifts

### 2. **Content Pillar Strategy**
- Define 3-5 core content pillars that ladder up to business goals
- Ensure 60% of content supports one of your top 2 pillars
- Reserve 10-15% for trending/experimental content
- The other 25-30% should directly support conversions or retention

### 3. **Batch & Repurpose Ruthlessly**
- Generate all social posts from one blog post (reduces creation time by 70%)
- Create video scripts from written content
- Refresh top-performing posts every 6 months with updated data
- Build email sequences around your highest-performing content

### 4. **Optimal Posting Rhythm**
- Blog: 2-4 posts per month (depending on audience size and resources)
- Social: 3-5 posts per week on primary platform
- Email: 1-2 campaigns per week (not daily; quality > quantity)
- Video: 2-4 per month (if applicable to your niche)

### 5. **Analytics Loop (Critical for Iteration)**
- Check performance weekly; adjust posting times if data shows different peaks
- Update content pillars quarterly based on performance data
- Track engagement-to-conversion, not just vanity metrics
- A/B test email subject lines (the skill suggests these automatically)

### 6. **Seasonal & Event Planning**
- Input holidays and industry events 90 days in advance
- Plan 2-3 pieces around major industry conferences
- Create evergreen + seasonal content mix (70/30 split recommended)
- Align product launches with content campaigns for maximum impact

### 7. **Agency-Specific Tips**
- Create a master brand profile template for faster client onboarding
- Use the multi-client feature to generate 5+ calendars in one session
- Version your calendars (v1.0, v1.1) to track client feedback and iterations
- Automate sharing with Slack integrations for team approval workflows

---

## Safety & Guardrails

### What This Skill DOES:
✅ Generate content ideas and calendar structures  
✅ Analyze your analytics and suggest optimization  
✅ Create outlines, headlines, and social copy  
✅ Identify trends and seasonal opportunities  
✅ Provide strategic recommendations  

### What This Skill DOES NOT DO:
❌ Publish content directly (no automated posting to WordPress, social media, or email platforms)  
❌ Make legal claims about product results or guarantees  
❌ Generate medical, financial, or legal advice  
❌ Create content that violates platform guidelines (spam, misinformation, hate speech)  
❌ Guarantee traffic, engagement, or conversion rates  
❌ Access private analytics without explicit credentials  

### Limitations & Boundaries:

**1. Data Privacy:**
- Never stores your analytics credentials or brand data after session ends
- Google Analytics data is pulled in read-only mode
- Recommend IP whitelisting for sensitive brand accounts
- GDPR compliant: does not store PII or customer data

**2. Content Quality:**
- Generated outlines are starting points, not finished content
- Always review for factual accuracy and brand alignment
- AI-generated headlines should be tested with A/B testing
- Recommended: Human editing of all AI-generated copy before publishing

**3. Timeline Realism:**
- Cannot guarantee traffic predictions (too many variables)
- Seasonal trends have ±15% variance based on external factors
- Engagement estimates are based on historical averages ± 20%
- Market changes can affect recommendations (oil prices, geopolitics, etc.)

**4. Platform Restrictions:**
- Social media algorithms change frequently; recommendations updated quarterly
- Some platforms (TikTok, Instagram) have strict content guidelines
- Video content recommendations assume adequate production resources
- International campaigns may face platform-specific restrictions

**5. Compliance Notes:**
- FTC disclosure requirements vary by platform (include #ad/#sponsored where required)
- GDPR email marketing requires proper consent documentation
- No content should make health/medical claims without proper disclaimers
- Always verify SEO recommendations comply with search engine guidelines

---

## Troubleshooting & FAQ

### ❓ Q: "The skill is recommending posting times that don't match my audience's peak activity."
**A:** 
- Check if your Google