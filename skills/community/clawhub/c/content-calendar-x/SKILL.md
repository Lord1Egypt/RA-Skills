---
name: content-calendar
description: Content strategy, planning, and calendar creation for any business or creator. Use when asked to build a content calendar, plan social media posts, create a content strategy, generate post ideas, schedule content across platforms, repurpose existing content, build a 30/60/90 day content plan, or create platform-specific content frameworks. Triggers on phrases like "content calendar", "content strategy", "social media plan", "post ideas", "content schedule", "30 day content plan", "what should I post", "content for LinkedIn", "repurpose content", "editorial calendar", "content pillars".
---

# Content Calendar Skill

Build a full content strategy and actionable calendar. Output should be ready to execute — not a vague plan.

## Workflow

### 1. Understand the Context
Gather (ask if not provided):
- **Business/brand:** What do they do? Who's the audience?
- **Goal:** Awareness? Leads? Community? Sales?
- **Platforms:** LinkedIn, Twitter/X, Instagram, TikTok, YouTube, Blog — which ones?
- **Cadence:** How many posts per week per platform?
- **Timeframe:** 2 weeks, 30 days, 90 days?
- **Existing content:** Any blog posts, videos, or content to repurpose?
- **Voice/tone:** Professional, casual, educational, entertaining?

### 2. Define Content Pillars
Create 3–5 content pillars (recurring themes) based on:
- Audience pain points and interests
- Business expertise areas
- SEO/discovery opportunities
- Competitor content gaps

Each pillar gets a name, description, and % of content mix.

### 3. Generate Post Ideas
For each pillar, generate post ideas using formats in `references/post-formats.md`:
- **Educational:** How-to, tips, explainers, myths debunked
- **Social proof:** Case studies, testimonials, results screenshots
- **Behind the scenes:** Process, team, day-in-the-life
- **Engagement:** Questions, polls, controversial takes, hot takes
- **Promotional:** Offers, product features, announcements (keep to 20% max)

Aim for 3–5x more ideas than needed — let them pick the best.

### 4. Build the Calendar
Use `scripts/build_calendar.py` to generate a structured calendar.

Output structure per post:
- Date + platform
- Pillar
- Format (text, image, video, carousel, thread)
- Hook (first line / opening 3 seconds)
- Body content / talking points
- CTA
- Hashtags (platform-appropriate)
- Repurposing notes (can this become something else?)

### 5. Repurposing Map
If existing content provided, create a repurposing matrix:
- Blog post → LinkedIn carousel + Twitter thread + 3x short tips
- Video → 5x short clips + transcript blog post + quote graphics
- Podcast episode → audiogram + key quotes + newsletter section

See `references/post-formats.md` for platform-specific formatting rules.
See `assets/calendar-template.md` for the full calendar output template.
