# Podcast Growth Engine

A complete 12-phase system for launching, producing, and growing a podcast from zero to monetization. Covers strategy, production, guest management, audience growth, monetization, and repurposing — platform-agnostic, zero dependencies.

---

## Quick Health Check

Run `/podcast-check` on any show to score readiness:

| Signal | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Episodes published | 10+ | 3-9 | <3 |
| Release cadence | Weekly consistent | Biweekly | Irregular |
| Average episode length | Matches format | Varies >50% | No standard |
| Show notes quality | SEO-optimized | Basic description | Title only |
| Distribution platforms | 5+ directories | 2-4 | 1 only |
| Social clips per episode | 3-5 | 1-2 | 0 |
| Guest pipeline | 10+ confirmed | 3-9 | Empty |
| Download trend | Growing | Flat | Declining |

Score: /16. Below 8 = follow this skill end-to-end.

---

## Phase 1: Podcast Strategy & Positioning

### Show Brief

```yaml
show_brief:
  name: ""
  tagline: ""  # 10 words max — elevator pitch
  format: ""   # solo | interview | co-hosted | panel | narrative | hybrid
  niche: ""
  target_listener:
    who: ""          # Specific persona
    pain_points: []  # 3-5 problems you solve
    aspiration: ""   # What they want to become
    listens_when: "" # Commute, gym, cooking, work
  positioning:
    category: ""     # Apple Podcasts category
    subcategory: ""
    competitors: []  # 3-5 shows in your space
    differentiation: "" # Why listen to YOU vs them
  goals:
    primary: ""      # Brand, leads, revenue, community, thought leadership
    metric: ""       # Downloads, leads generated, revenue
    timeline: ""     # 6-month target
```

### Format Decision Matrix

| Format | Best For | Episode Length | Prep Time | Scalability |
|--------|----------|---------------|-----------|-------------|
| Solo | Thought leadership, tutorials | 15-30 min | 2-4 hrs | High (no scheduling) |
| Interview | Network building, diverse content | 30-60 min | 1-2 hrs + scheduling | Medium |
| Co-hosted | Chemistry, entertainment | 30-60 min | 1 hr | Medium (coordination) |
| Panel | Industry roundtables | 45-75 min | 3-5 hrs | Low (scheduling nightmare) |
| Narrative | Storytelling, documentary | 20-45 min | 10-20 hrs | Low (production heavy) |
| Hybrid | Variety, audience retention | Varies | Varies | Medium |

### Format Selection Rules
1. Starting out? Interview format — built-in content + guest promotes episode
2. Deep expertise? Solo — fastest to produce, highest authority
3. Great co-host chemistry? Co-hosted — most fun, best retention
4. Never start with narrative — production cost kills beginners

### Niche Scoring

Score your niche (each 0-3):

| Factor | Score | Notes |
|--------|-------|-------|
| Personal expertise | /3 | Can you talk about this for 200 episodes? |
| Audience size | /3 | Enough listeners but not oversaturated |
| Monetization potential | /3 | Can you sell to this audience? |
| Guest availability | /3 | Enough interesting guests? |
| Content longevity | /3 | Evergreen vs trending? |
| Passion/energy | /3 | Will you still care in year 2? |

Score: /18. Below 12 = reconsider niche.

---

## Phase 2: Pre-Launch Setup

### Technical Stack Decision

| Component | Budget ($0) | Mid ($50-200/mo) | Premium ($500+/mo) |
|-----------|-------------|-------------------|---------------------|
| Microphone | Phone + quiet room | Audio-Technica ATR2100x ($79) | Shure SM7dB ($399) |
| Recording | Riverside.fm free | Riverside.fm ($15/mo) | Squadcast + pro mic |
| Editing | Descript free tier | Descript Pro ($24/mo) | Adobe Audition + editor |
| Hosting | Spotify for Podcasters | Buzzsprout ($12/mo) | Transistor ($19/mo) |
| Remote guests | Riverside.fm | Riverside.fm | Riverside.fm |
| Music | YouTube Audio Library | Epidemic Sound ($15/mo) | Custom composition |

### Hosting Platform Comparison

| Platform | Free Tier | Paid From | Analytics | Monetization | Best For |
|----------|-----------|-----------|-----------|-------------|----------|
| Spotify for Podcasters | Unlimited | Free | Basic | Spotify ads | Beginners |
| Buzzsprout | 2 hrs/mo | $12/mo | Good | Affiliate | Small shows |
| Transistor | No | $19/mo | Excellent | Multiple shows | Professionals |
| Podbean | 5 hrs | $9/mo | Good | Built-in | Monetization |
| Captivate | No | $19/mo | Advanced | Growth tools | Growth-focused |
| RSS.com | Limited | $6/mo | Basic | Simple | Budget |

### Selection Rules
1. Just starting? Spotify for Podcasters (free, easy, adequate)
2. Serious about growth? Transistor or Captivate (analytics matter)
3. Multiple shows? Transistor (unlimited shows on all plans)
4. Monetization focus? Podbean or Captivate (built-in tools)

### Pre-Launch Checklist

```yaml
pre_launch:
  branding:
    - [ ] Show name finalized (check trademark + domain availability)
    - [ ] Cover art designed (3000×3000px, readable at 55px)
    - [ ] Color palette defined (consistent across all platforms)
    - [ ] Show description written (SEO keywords + listener benefit)
  technical:
    - [ ] Hosting platform selected and configured
    - [ ] RSS feed validated (use Cast Feed Validator)
    - [ ] Recording setup tested (audio quality check)
    - [ ] Intro/outro produced (15-30 seconds max each)
    - [ ] Music licensed (royalty-free or custom)
  content:
    - [ ] First 3 episodes recorded (launch with batch)
    - [ ] Episode format template created
    - [ ] Show notes template ready
    - [ ] Content calendar for first 8 weeks
  distribution:
    - [ ] Apple Podcasts submitted (allow 1-5 days for review)
    - [ ] Spotify connected
    - [ ] Google Podcasts / YouTube Podcasts connected
    - [ ] Amazon Music / Audible submitted
    - [ ] Podcast Index submitted
    - [ ] iHeartRadio, Stitcher, TuneIn submitted
  launch:
    - [ ] Launch date set (Tuesday or Wednesday optimal)
    - [ ] Launch promo plan (email list, social, ask for reviews)
    - [ ] First 3 episodes scheduled
    - [ ] Trailer episode published (1-2 min teaser)
```

### Cover Art Rules
1. Readable at 55×55px (how it appears in apps)
2. Bold, high-contrast colors
3. Show name prominent — subtitle optional
4. NO small text, NO busy backgrounds, NO stock photos
5. Professional design > DIY (invest $50-200 on Fiverr/99designs)
6. Test: screenshot at phone size — can you read the title?

---

## Phase 3: Episode Production

### Episode Planning Template

```yaml
episode:
  number: 0
  title: ""           # SEO-friendly, curiosity-driven
  type: ""             # solo | interview | special
  topic: ""
  target_listener_problem: ""
  key_takeaways: []    # 3-5 bullet points listener walks away with
  hook: ""             # First 60 seconds — why should they keep listening?
  outline:
    - segment: "Hook"
      duration: "0:00-1:00"
      notes: ""
    - segment: "Context"
      duration: "1:00-5:00"
      notes: ""
    - segment: "Core Content"
      duration: "5:00-25:00"
      notes: ""
    - segment: "Actionable Takeaway"
      duration: "25:00-28:00"
      notes: ""
    - segment: "CTA + Close"
      duration: "28:00-30:00"
      notes: ""
  cta: ""              # What do you want listener to DO?
  show_notes_keywords: []
  resources_mentioned: []
```

### Title Formulas That Work

| Formula | Example | Best For |
|---------|---------|----------|
| Number + Outcome | "7 Ways to Double Your Revenue" | Solo, how-to |
| How [Person] Did [Thing] | "How Sara Blakely Built Spanx from $5K" | Interview |
| The [Counterintuitive] Truth About [Topic] | "The Uncomfortable Truth About Passive Income" | Thought leadership |
| [Topic] 101: Everything You Need to Know | "SEO 101: Everything You Need to Know in 2026" | Educational |
| Why [Common Belief] Is Wrong | "Why Hustle Culture Is Killing Your Business" | Contrarian |
| [Guest Name]: [Their Unique Insight] | "Naval Ravikant: How to Get Rich Without Getting Lucky" | Big guest |

### Title Rules
1. Front-load keywords (Apple Podcasts search)
2. 60 characters max (truncation on mobile)
3. NO episode number in title (wastes characters, not SEO-friendly)
4. Include the BENEFIT to the listener
5. Write 5 titles, pick the most clickable

### Audio Quality Standards

| Metric | Target | Acceptable | Fix |
|--------|--------|------------|-----|
| Noise floor | <-60 dB | <-50 dB | Noise gate + reduction |
| Loudness (LUFS) | -16 LUFS | -14 to -19 | Limiter + compressor |
| Sample rate | 44.1 kHz | 44.1 kHz | Recording settings |
| Bit depth | 16-bit | 16-bit | Export settings |
| Format | MP3 128kbps mono | MP3 96-192kbps | Export settings |
| Room echo | None audible | Minimal | Blankets, closet, foam |
| Mouth clicks | None | Rare | Hydration + gate |

### Recording Rules
1. Record in the quietest room available — closets work
2. Speak 4-6 inches from the mic
3. Record a 10-second silence sample for noise profile
4. Use headphones — always (prevents feedback)
5. Record locally, not through the platform (higher quality)
6. Keep raw files for 30 days minimum

### Editing Workflow

```
1. Import raw audio
2. Noise reduction (profile from silence sample)
3. Remove long pauses (>3 seconds → trim to 1 second)
4. Cut filler words (um, uh, like, you know) — but keep some for naturalness
5. Remove tangents that don't serve the listener
6. Level audio (compressor → limiter → target -16 LUFS)
7. Add intro/outro music
8. Add chapter markers (if platform supports)
9. Export: MP3, 128kbps mono, 44.1kHz
10. Listen to final version at 1.5x speed (catches errors faster)
```

### Editing Decision Guide

| Issue | Remove? | Notes |
|-------|---------|-------|
| Long "umm" (>1s) | Yes | Cut to natural pause |
| Quick "uh" | Sometimes | Keep some — sounds human |
| Tangent (>30s off-topic) | Yes | Unless entertaining |
| Awkward silence (>3s) | Trim to 1s | Keep brief pauses for impact |
| Coughing/sneezing | Yes | Replace with room tone |
| Repeated sentence | Yes | Keep the better take |
| Cross-talk | Depends | Keep if energetic; cut if confusing |
| Guest rambling | Trim | Cut the weakest 20% |

---

## Phase 4: Guest Management

### Guest Pipeline

```yaml
guest_pipeline:
  wishlist:      # Dream guests (reach in 6-12 months)
    - name: ""
      topic: ""
      contact: ""
      mutual_connections: []
  targets:       # Realistic guests (reach now)
    - name: ""
      topic: ""
      contact: ""
      status: "research | outreach | confirmed | scheduled | recorded | published"
      outreach_date: ""
      follow_up_dates: []
  booked:        # Confirmed upcoming
    - name: ""
      record_date: ""
      topic: ""
      prep_status: ""
```

### Guest Outreach Template

```
Subject: Would you be a great fit for [Show Name]?

Hi [Name],

I host [Show Name], a podcast about [topic] for [audience].
[1 sentence about why THEIR audience would benefit from the exposure].

I'd love to have you on to discuss [specific topic related to their expertise].

Recent guests include [2-3 names they'd recognize].

The recording takes about [time] and we handle all editing and promotion.

Would you be open to a [time] conversation in the next few weeks?

[Your name]
[Show link]
```

### Guest Outreach Rules
1. Personalize EVERY email — reference their specific work
2. Make it about THEM, not you (their exposure, their audience reach)
3. Include social proof (download numbers OR notable past guests)
4. Make scheduling frictionless (send Calendly link)
5. Follow up once at 5 days, once at 14 days, then stop
6. Don't pitch cold on social — warm up first (engage with their content for 2 weeks)

### Guest Prep Kit (send 3-5 days before recording)

```yaml
guest_prep:
  logistics:
    recording_date: ""
    duration: "45 minutes recording → 30 min published"
    platform: "Riverside.fm (link: [URL])"
    tech_requirements: "Chrome browser, headphones, quiet room"
  content:
    topic_focus: ""
    discussion_questions:  # 5-7 questions, NOT a rigid script
      - ""
    audience_context: "Our listeners are [who] who want to [what]"
    tone: "Conversational, practical, story-driven"
  promotion:
    headshot_needed: true
    bio_needed: true      # 2-3 sentences
    social_handles: true
    links_to_promote: true  # Their book, course, website
```

### Interview Question Design
1. Start easy — warm-up question about their background (2 min)
2. "What's the biggest mistake you see in [topic]?" — always gets good answers
3. Ask "why" and "how" — not "what" (deeper answers)
4. Prepare 10 questions, expect to use 5-7 (let conversation flow)
5. Always end with: "What's one thing our listeners can do TODAY?"
6. Never read questions verbatim — use as guide, listen and follow up

---

## Phase 5: Show Notes & SEO

### Show Notes Template

```markdown
# [Episode Title]

[2-3 sentence summary optimized for search — include primary keyword]

## Key Takeaways
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

## Timestamps
- 00:00 — Introduction
- 02:30 — [Topic 1]
- 12:15 — [Topic 2]
- 22:00 — [Key insight]
- 28:00 — Actionable takeaway

## Resources Mentioned
- [Resource 1](URL)
- [Resource 2](URL)

## About [Guest Name]
[2-3 sentences + links to their work]

## Connect
- [Your website/newsletter signup]
- [Social links]
- Leave a review on [Apple Podcasts link]
```

### Podcast SEO Checklist

| Element | Optimization | Priority |
|---------|-------------|----------|
| Episode title | Primary keyword + benefit | P0 |
| Show description | Category keywords + listener persona | P0 |
| Episode description | 150+ words, keyword-rich summary | P0 |
| Show notes | Timestamped, linked, keyword-rich | P1 |
| Transcript | Full text (Apple indexes transcripts) | P1 |
| Chapter markers | Descriptive titles with keywords | P1 |
| Cover art alt text | Show name + keywords | P2 |
| Website/blog post | Full episode page with transcript | P2 |
| YouTube upload | Title, description, tags, chapters | P1 |

### SEO Rules
1. Apple Podcasts search is the #1 discovery engine — optimize for it
2. Include your primary keyword in the FIRST 10 words of the title
3. Write episode descriptions as if they're blog posts (150+ words)
4. Transcripts are FREE SEO — Apple, Google, and Spotify index them
5. YouTube is the #2 podcast platform — always upload video version
6. Create a blog post for every episode (website SEO)

---

## Phase 6: Distribution & Growth

### Platform Priority

| Platform | Priority | % of Listeners | Notes |
|----------|----------|----------------|-------|
| Apple Podcasts | P0 | ~35% | Reviews matter, search discovery |
| Spotify | P0 | ~30% | Growing fastest, video support |
| YouTube | P0 | ~20% | Video + shorts = massive reach |
| Google Podcasts | P1 | ~5% | Auto from RSS |
| Amazon/Audible | P1 | ~5% | Growing, easy submission |
| Others (iHeart, Stitcher, etc.) | P2 | ~5% | Submit and forget |

### Growth Strategies by Stage

#### 0-100 Downloads/Episode
1. Tell everyone you know — personal network is launch fuel
2. Appear on OTHER podcasts as a guest (podcast swaps)
3. Ask for reviews on Apple Podcasts (5-star reviews boost ranking)
4. Share clips on social media (Reels, TikTok, LinkedIn, X)
5. Email list promotion (if you have one)

#### 100-1,000 Downloads/Episode
1. Podcast guest swaps (appear on 2-3 shows/month)
2. YouTube clips strategy (3-5 clips per episode)
3. SEO-optimized show notes on your website
4. Cross-promotion with complementary podcasts
5. Submit to podcast newsletters and curators
6. Consistent release schedule (same day, same time)

#### 1,000-10,000 Downloads/Episode
1. Paid social ads on best-performing clips
2. Newsletter cross-promotions
3. Speaking at industry events
4. Community building (Discord, Slack, Facebook group)
5. Seasonal limited series (7-10 episode deep dives)
6. Collaborate with bigger shows

#### 10,000+ Downloads/Episode
1. Brand deals and sponsorships
2. Live events and tours
3. Premium content (paid feed)
4. Book or course launch leveraging audience
5. Media appearances and press
6. Network building (join or create a podcast network)

### Social Clips Strategy

| Platform | Length | Aspect Ratio | Format | Volume |
|----------|--------|-------------|--------|--------|
| YouTube Shorts | 30-60s | 9:16 | Vertical, captions | 3-5/episode |
| Instagram Reels | 30-60s | 9:16 | Vertical, captions | 2-3/episode |
| TikTok | 30-90s | 9:16 | Vertical, captions | 2-3/episode |
| X (Twitter) | 60-120s | 16:9 or 1:1 | Horizontal, captions | 1-2/episode |
| LinkedIn | 60-180s | 16:9 or 1:1 | Horizontal, captions | 1-2/episode |

### Clip Selection Rules
1. Pick the most SURPRISING or COUNTERINTUITIVE moment
2. The clip must stand alone — no context needed
3. First 3 seconds must hook ("Most people don't realize...")
4. Always add captions — 85% of social video is watched muted
5. Include show name + episode number as text overlay
6. CTA at end: "Full episode in bio" or "Link in comments"

---

## Phase 7: Audience Engagement

### Community Building

```yaml
community:
  platform: ""  # Discord | Slack | Facebook Group | Circle
  access: ""    # Free | Paid | Patreon tier
  channels:
    - general       # Episode discussion
    - introductions  # New member welcome
    - resources      # Links and tools
    - feedback       # Episode requests
  engagement_rituals:
    - "Weekly discussion thread on latest episode"
    - "Monthly AMA with host"
    - "Guest nomination thread"
    - "Listener spotlight"
```

### Engagement Tactics

| Tactic | Effort | Impact | Frequency |
|--------|--------|--------|-----------|
| Respond to every review | Low | High | Ongoing |
| Read listener questions on air | Low | High | Every episode |
| Listener shoutouts | Low | Medium | Weekly |
| Q&A episodes | Medium | High | Monthly |
| Live recording sessions | Medium | High | Quarterly |
| Listener surveys | Medium | High | Quarterly |
| Community challenges | High | High | Quarterly |

### Review Generation Strategy
1. Ask at the END of your best episodes (not every episode)
2. Make it specific: "Leave a review telling me which episode changed something for you"
3. Read reviews on air — incentivizes more
4. Direct link to Apple Podcasts review page in show notes
5. Target: 50 reviews in first 3 months (helps Apple ranking)

---

## Phase 8: Monetization

### Revenue Streams by Audience Size

| Stream | Min Audience | Revenue Range | Effort |
|--------|-------------|---------------|--------|
| Affiliate links | 100+ downloads | $50-500/mo | Low |
| Listener support (Patreon/Buy Me a Coffee) | 500+ downloads | $100-2,000/mo | Low |
| Sponsorships (host-read) | 1,000+ downloads | $15-50 CPM | Medium |
| Premium content (paid feed) | 1,000+ downloads | $500-5,000/mo | Medium |
| Courses/digital products | 2,000+ downloads | $1,000-20,000/mo | High |
| Consulting/services | Any | $2,000-50,000/mo | Medium |
| Live events | 5,000+ downloads | $5,000-50,000/event | High |
| Book deal | 10,000+ downloads | $10,000-100,000+ | Very High |

### Sponsorship Rate Card

```yaml
sponsorship:
  cpm_range:  # Cost per thousand downloads
    pre_roll: "$18-25"   # 15-30 seconds, before content
    mid_roll: "$25-50"   # 60 seconds, during content
    post_roll: "$10-15"  # 15-30 seconds, after content
  package_options:
    single_episode: "1x mid-roll"
    starter: "4 episodes (1 month)"
    standard: "12 episodes (3 months) — 10% discount"
    premium: "52 episodes (1 year) — 20% discount"
  value_adds:
    - "Show notes link + logo"
    - "Social media mention (clips)"
    - "Newsletter mention"
    - "Dedicated sponsor segment"
  metrics_to_share:
    - "Average downloads per episode (30-day)"
    - "Audience demographics"
    - "Listener geography"
    - "Engagement rate (completion %)"
```

### Sponsorship Rules
1. Don't sell ads below 500 downloads/episode — build audience first
2. Only promote products you'd actually use (trust > revenue)
3. Host-read ads outperform produced ads 3-5x — always host-read
4. Start with affiliate deals — prove value, then pitch sponsorship
5. Package deals > single episode buys (recurring revenue)
6. Never do more than 2 ad spots per episode (listener tolerance)

### Alternative Monetization: Premium Content

| Model | Platform | Price Point | Content Type |
|-------|----------|-------------|-------------|
| Bonus episodes | Apple Subscriptions | $2.99-4.99/mo | Extended interviews, Q&A |
| Ad-free feed | Supercast | $4.99-9.99/mo | Same content, no ads |
| Community access | Patreon/Circle | $5-25/mo | Discord, live events, early access |
| Back catalog | Glow.fm | $4.99/mo | Archive access |
| Course | Teachable | $47-497 one-time | Deep-dive curriculum |

---

## Phase 9: Content Repurposing (1→12 Method)

### One Episode → 12+ Content Pieces

```
1 Podcast Episode (30-60 min)
├── 1 YouTube full video
├── 3-5 YouTube Shorts / Reels / TikToks
├── 1 Blog post (show notes + transcript)
├── 1 Newsletter issue
├── 3-5 Social media posts (quotes, insights)
├── 1 LinkedIn article or thread
├── 1 Twitter/X thread (key takeaways)
├── 1 Audiogram (quote card with waveform)
├── 1 Carousel (Instagram/LinkedIn)
└── 1 Email to list
```

### Repurposing Workflow

```yaml
repurposing:
  day_of_publish:
    - Upload full episode to YouTube with chapters
    - Publish blog post with transcript + show notes
    - Send newsletter with episode summary + key takeaways
    - Post announcement on all social platforms
  day_1_after:
    - Create and post 2 short clips (best moments)
    - Create audiogram with key quote
  day_2_after:
    - Post LinkedIn article or thread
    - Create Instagram/LinkedIn carousel
  day_3_after:
    - Post 2 more short clips (different moments)
    - Twitter/X thread with takeaways
  day_4_after:
    - Community discussion post
    - Share behind-the-scenes content
  ongoing:
    - Repost evergreen clips monthly
    - Compile "best of" episodes quarterly
```

### Repurposing Rules
1. Every episode gets at MINIMUM: 3 clips + 1 blog post + 1 newsletter
2. Batch repurposing: do all clips for the week in one session
3. Evergreen episodes get reshared every 3-6 months
4. Best clips get boosted with paid ads
5. Track which clips drive the most new listeners → make more like those

---

## Phase 10: Analytics & Optimization

### Key Metrics Dashboard

```yaml
metrics:
  growth:
    downloads_per_episode_30day: 0    # Primary metric
    total_downloads_monthly: 0
    subscriber_count: 0               # Platform-specific
    new_subscribers_monthly: 0
    download_trend: ""                # Growing | Flat | Declining
  engagement:
    completion_rate: ""               # % who listen to end
    average_listen_duration: ""
    reviews_count: 0
    reviews_rating: 0.0
    social_engagement: 0              # Clip views + shares
  monetization:
    monthly_revenue: 0
    revenue_per_episode: 0
    cpm_achieved: 0
    affiliate_clicks: 0
  content:
    episodes_published: 0
    consistency_streak: 0             # Consecutive on-time releases
    guest_acceptance_rate: ""
```

### Benchmarks by Category

| Metric | Top 50% | Top 25% | Top 10% | Top 1% |
|--------|---------|---------|---------|--------|
| Downloads/episode (30d) | 28+ | 75+ | 250+ | 5,000+ |
| Completion rate | >50% | >65% | >75% | >85% |
| Monthly growth | >5% | >10% | >20% | >50% |
| Reviews (Apple) | 10+ | 50+ | 200+ | 1,000+ |

### Episode Performance Analysis

When an episode significantly over/underperforms:

**Overperformed (2x+ average):**
- What was the title? (Test similar formulas)
- Who was the guest? (Book similar guests)
- What was the topic? (Create related episodes)
- Which clips went viral? (Format more clips this way)

**Underperformed (<50% average):**
- Was the title boring or unclear?
- Wrong topic for audience?
- Released at unusual time?
- Poor audio quality?
- Too long or too short?

### Monthly Review Template

```yaml
monthly_review:
  period: "YYYY-MM"
  episodes_published: 0
  avg_downloads_30day: 0
  best_performing:
    title: ""
    downloads: 0
    why: ""
  worst_performing:
    title: ""
    downloads: 0
    why: ""
  revenue: 0
  new_reviews: 0
  guest_pipeline_health: ""
  social_clip_performance:
    total_views: 0
    best_clip: ""
  learnings: []
  next_month_priorities: []
```

---

## Phase 11: Podcast Operations

### Weekly Production Schedule

| Day | Task | Time |
|-----|------|------|
| Monday | Plan next episode, guest prep | 1-2 hrs |
| Tuesday | Record | 1-2 hrs |
| Wednesday | Edit + produce | 2-3 hrs |
| Thursday | Write show notes, create clips | 1-2 hrs |
| Friday | Schedule + upload | 30 min |
| Weekend | Promote + engage | 30 min |

### Batch Production (Recommended After Episode 10)

Record 3-4 episodes in one session:
1. **Prep day**: Plan all episodes, confirm guests
2. **Record day**: Back-to-back recordings (15 min breaks between)
3. **Edit week**: Edit all episodes in batch
4. **Schedule**: Queue 3-4 weeks of content

Benefits: Consistent quality, buffer for emergencies, more efficient use of creative energy.

### Burnout Prevention
1. Build a 4-episode buffer before you need it
2. Repurpose your best episodes as "encore" episodes when needed
3. Do seasonal series (10 episodes → break → 10 episodes)
4. Co-host episodes when your energy is low
5. If you hate editing, outsource it (Fiverr: $20-50/episode)
6. Quality > quantity — biweekly is better than forced weekly

### SOPs to Create

| SOP | Purpose | When |
|-----|---------|------|
| Guest booking | Standard outreach + prep | Before launch |
| Recording checklist | Equipment + settings | Before launch |
| Editing workflow | Step-by-step production | After episode 3 |
| Publishing checklist | Upload + distribution | After episode 3 |
| Clip creation | Social media assets | After episode 5 |
| Sponsor management | Invoicing + tracking | When monetized |

---

## Phase 12: Advanced Strategies

### Podcast Network Effects
1. **Guest referral chain**: Every guest introduces you to 2 more potential guests
2. **Podcast swap network**: Build a group of 5-10 shows for cross-promotion
3. **Listener-generated content**: Top listeners become guests → bring their network
4. **Affiliate partnerships**: Guests promote products → you earn affiliate → guests return

### Video Podcast Strategy (YouTube)

| Element | Specification |
|---------|--------------|
| Camera | 1080p minimum, 4K preferred |
| Framing | Chest up, rule of thirds |
| Lighting | Ring light or 2-point setup, no backlighting |
| Background | Clean, branded, or virtual (consistent) |
| Thumbnails | Face + emotion + 3-5 words (different from audio cover) |
| Chapters | YouTube chapters in description (00:00 format) |
| Cards/End screens | Drive to other episodes + subscribe |

### YouTube Podcast Rules
1. Audio-only shows lose to video on YouTube — add video
2. Thumbnail is 50% of YouTube success — invest time
3. First 30 seconds must hook the VIEWER (different from audio listener)
4. Upload full episode AND clips (separate uploads, not just trimmed)
5. YouTube titles can differ from podcast titles (optimize for YouTube search)

### International Expansion
1. If your topic has global appeal, consider subtitling clips
2. Translate show notes for SEO in other languages
3. Partner with hosts in other markets for cross-language episodes
4. Consider separate feeds for different languages (when audience justifies)

### Podcast-to-Product Pipeline

```
Free Podcast → Email List → Lead Magnet → 
    ├── Low-ticket ($47-97): Templates, guides, courses
    ├── Mid-ticket ($297-997): Workshops, cohorts
    └── High-ticket ($2,000+): Consulting, coaching, services
```

Rules:
1. Podcast builds trust → converts to email → email converts to sale
2. Mention your product naturally, not as an ad read
3. Create episodes that solve 80% of the problem; your product solves 100%
4. Guest episodes → joint ventures (guest promotes your product to their audience)

---

## Quality Scoring (0-100)

| Dimension | Weight | Score Range |
|-----------|--------|-------------|
| Audio quality | 15% | 0-15 |
| Content value (listener takeaway) | 25% | 0-25 |
| Production consistency | 15% | 0-15 |
| SEO & discoverability | 10% | 0-10 |
| Audience engagement | 15% | 0-15 |
| Growth trajectory | 10% | 0-10 |
| Monetization readiness | 10% | 0-10 |

- **90-100**: Top-tier show, ready for major sponsors and network deals
- **70-89**: Strong show, focus on growth and monetization
- **50-69**: Solid foundation, optimize production and SEO
- **30-49**: Needs work — focus on audio quality and consistency
- **Below 30**: Relaunch recommended

---

## 10 Podcast Killers

| Mistake | Why It Kills | Fix |
|---------|-------------|-----|
| Inconsistent release schedule | Algorithms punish gaps, listeners forget | Batch record, build buffer |
| Poor audio quality | Listeners leave in first 30 seconds | Invest $79 in a proper mic |
| No hook in first 60 seconds | 30% of listeners drop in minute 1 | Script your opening hook |
| Episodes too long | Completion rate tanks above 60 min | Match length to format |
| No social promotion | Podcast apps have terrible discovery | 3-5 clips per episode minimum |
| Ignoring SEO | 25% of podcast discovery is search | Optimize titles + descriptions |
| No CTA | Listeners don't know what to do next | One clear CTA per episode |
| Guest-dependent content | Guest cancels = no episode | Mix solo and interview |
| Not reading analytics | Can't improve what you don't measure | Monthly review ritual |
| Quitting before episode 20 | Most shows die before they find their voice | Commit to 25 episodes minimum |

---

## Edge Cases

### Solo Show Burnout
- Batch record when energy is high (3-4 episodes)
- Repurpose best-of compilations
- Invite occasional guests for variety
- Try "answering listener questions" format (low prep)

### Guest No-Shows
- Always have a solo episode ready as backup
- Confirm 48 hours AND 2 hours before recording
- Build relationships first — no-shows are rare with warm guests
- Keep a "hot standby" guest who can record with 24h notice

### Going Viral
- Be ready for server load (hosting platform capacity)
- Have a clear funnel (podcast → email list → product)
- Record a "welcome new listeners" intro for next 2-3 episodes
- Capitalize: reach out to press, book more high-profile guests

### Negative Reviews
- Respond graciously if the platform allows
- Don't argue — thank them for feedback
- Legitimate criticism = improve; trolling = ignore
- 1-star reviews barely affect rankings if you have volume

### Podfade Prevention (The #1 Podcast Killer)
- 80% of podcasts die before episode 10
- Season format reduces pressure (commit to 10, then decide)
- Public accountability (announce schedule to audience)
- Track your "why" — return to it when motivation drops
- Find a podcast buddy or mastermind for accountability

---

## Natural Language Commands

```
/podcast-check       → Run quick health check
/podcast-plan        → Create episode plan from topic
/podcast-title       → Generate 5 title options for a topic
/podcast-guest       → Create guest outreach email
/podcast-notes       → Generate show notes template
/podcast-clips       → Identify clip-worthy moments from transcript
/podcast-seo         → Audit episode for search optimization
/podcast-review      → Monthly performance review
/podcast-monetize    → Assess monetization readiness
/podcast-repurpose   → Generate repurposing checklist for an episode
/podcast-launch      → Full pre-launch checklist
/podcast-grow        → Stage-appropriate growth recommendations
```
