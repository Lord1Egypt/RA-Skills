---
name: cm-linkedin-profile-optimizer
description: Audit and rewrite LinkedIn profiles for recruiter visibility, inbound leads, and category authority. Diagnoses headline, About, Experience, Skills, Featured, banner, and activity feed against keyword density, SSI signals, and recruiter Boolean searches. Produces a rewritten profile, a 30-day activity playbook, and a recommendation outreach plan. Use when asked to optimize a LinkedIn profile, rewrite a LinkedIn headline, fix LinkedIn About section, get more recruiter messages, attract inbound LinkedIn leads, improve SSI score, rank in LinkedIn search, or build personal brand on LinkedIn. Triggers on "linkedin profile", "linkedin headline", "linkedin about", "linkedin bio", "linkedin optimization", "linkedin SEO", "recruiter search", "SSI score", "social selling index", "personal brand linkedin", "linkedin keywords", "linkedin rewrite".
metadata:
  tags: ["linkedin", "personal-branding", "career", "job-search", "recruiting", "b2b-sales", "marketing", "founders", "social-selling", "copywriting"]
---

# LinkedIn Profile Optimizer

Audit and rewrite LinkedIn profiles for three outcomes: (1) showing up in recruiter and buyer searches, (2) converting profile views into inbound DMs, and (3) building category authority that compounds. Acts as a profile strategist who has reviewed thousands of profiles for engineers, PMs, designers, sales reps, founders, and marketers.

## Usage

Invoke this skill when a profile is underperforming or being prepared for a job search, fundraise, or B2B outbound campaign.

**Basic invocation:**
> Audit my LinkedIn profile: [paste headline + About + last 2 roles]
> Rewrite my LinkedIn headline — I'm a backend engineer targeting senior roles at Stripe-tier companies
> My profile gets views but no DMs, what's broken?

**With context:**
> I'm a founder raising a seed round, optimize my profile for VC searches
> I'm a SaaS AE, rewrite my About to attract inbound buyers not recruiters
> Help me rank for "Kubernetes platform engineer" — recruiters can't find me

The agent diagnoses against a fixed framework, rewrites every section, and produces a 30-day activity plan.

## How It Works

### Step 1: Run the Profile Audit Framework

The agent scores eight surfaces. A profile must hit all eight to compound — fixing only one creates a leaky funnel.

| Surface | What It Does | Pass Criteria |
|---------|-------------|---------------|
| **Banner** | First visual; signals seriousness | Not the default blue. Includes value prop or proof (logos, tagline, headshot at conference). |
| **Headline (220 chars)** | The single biggest ranking and click factor — appears in search, comments, DMs | Outcome + role + niche + 1-2 keywords recruiters Boolean-search. Not just job title. |
| **About (2,600 chars)** | Where the visitor decides to act | Hook in line 1, credibility in lines 2-3 (above the "see more" fold), proof, CTA. |
| **Featured** | Above-the-fold proof | 3-4 items: best post, case study, podcast, lead magnet. Refresh quarterly. |
| **Experience** | Where recruiters/ATS scan keywords; where buyers verify legitimacy | STAR bullets with metrics, not job descriptions. Top 3 roles get the most depth. |
| **Skills** | Drives "People also viewed" matching, recruiter filters | Top 3 pinned = the 3 keywords you want to rank for. 50+ endorsements on the top 3. |
| **Recommendations** | Social proof recruiters and buyers explicitly read | Minimum 5 recent (within 18 months). Mix of manager, peer, customer, report. |
| **Activity** | Drives all-LinkedIn distribution; SSI; profile views | Active in the last 7 days. Comments > posts > shares for first 30 days. |

The agent produces a per-surface score (0-2: missing / weak / strong) and ranks fixes by ROI.

### Step 2: Optimize SSI (Social Selling Index)

SSI is LinkedIn's internal ranking signal (sales-nav.linkedin.com/sales/ssi). It's scored 0-100 across four pillars of 25 each. A score above 70 is the working threshold for inbound. Above 80 unlocks meaningful reach.

| Pillar | What Moves It | Tactic |
|--------|--------------|--------|
| **Establish your professional brand** | Profile completeness, posts published, long-form articles | Hit "All-Star" status; publish 1 long-form per quarter; pin Featured. |
| **Find the right people** | Sales Navigator searches, saved leads, advanced filters used | Even without Sales Nav: do 5 saved-search-style queries per week, view 10 profiles in target niche per day. |
| **Engage with insights** | Posts, comments, reactions, shares, message replies | Comment thoughtfully on 5 posts/day from people 1-2 levels above you. |
| **Build relationships** | Connections at decision-maker level, acceptance rate, message reply rate | Connect with 10 targeted people/week with personalized notes. Maintain >50% acceptance. |

**Quick wins (raise SSI 10-15 points in two weeks):**
- Fill every profile field (raises Brand pillar instantly).
- Post once, comment 25 times, react 50 times in week 1.
- Send 10 personalized connection requests with a specific reason.
- Reply to every DM within 24h (Relationships pillar).

### Step 3: Build the Keyword Strategy

LinkedIn search is closer to ATS keyword matching than Google — recurring exact phrases win. Recruiters use Boolean: `"product manager" AND ("fintech" OR "payments") AND "B2B" NOT "junior"`.

**Keyword extraction process:**

1. Pull 10 target job postings (or 10 ICP company About pages for sales/founders).
2. Extract repeated nouns and noun phrases: tools (`Snowflake`, `dbt`, `Figma`), frameworks (`Jobs-to-be-done`, `OKRs`), domains (`B2B SaaS`, `marketplaces`, `series A`), and outcomes (`MRR growth`, `0-to-1`, `migration`).
3. Rank by frequency. Top 5-7 become your "spine keywords."
4. Place each spine keyword in: headline, About first 200 chars, current role title, current role first bullet, top-3 skills, and one Featured item.

**Density rules:**
- Each spine keyword should appear 3-5 times across the profile (not stuffed in one section).
- Use exact phrasing recruiters search for, not your internal title (e.g., "Engineering Manager" beats "EM3" or "Tech Lead Coach").
- Include both the abbreviation and the expansion ("PLG / product-led growth", "ABM / account-based marketing") because Boolean searches use both.

**Recruiter Boolean fluency — what they actually type:**
```
("software engineer" OR "backend engineer") AND ("Go" OR "Golang") AND "Kubernetes" AND ("staff" OR "principal")
("product manager" OR "product lead") AND "fintech" AND ("0-1" OR "0 to 1") NOT (intern OR junior OR associate)
("VP marketing" OR "head of marketing") AND ("B2B SaaS") AND ("series A" OR "seed")
```
Audit your profile by literally pasting these into LinkedIn search and checking whether you appear in the first 10 results for your target string.

### Step 4: Rewrite the Headline

The headline is 220 characters, weighted heaviest by search, and shown next to your name on every comment. The default — your job title — wastes the slot.

**Formula:** `Outcome | Role + Niche | Keywords | Proof or Hook`

Use `|`, `→`, or `•` as separators. Avoid emoji noise (one is fine; five is spam).

**Five before/after rewrites:**

```
WEAK:    Senior Software Engineer at Acme Corp
STRONG:  I help fintechs ship secure payment APIs | Senior Backend Engineer | Go, Kubernetes, PCI-DSS | ex-Stripe
WHY:     Adds outcome ("ship secure payment APIs"), niche ("fintechs"), three Boolean keywords,
         and a proof anchor. Same person, 8x more searchable.

WEAK:    Product Manager
STRONG:  0-to-1 PM for B2B SaaS | I take products from first 10 customers to first $1M ARR | ex-Notion, ex-Linear
WHY:     "0-to-1" and "$1M ARR" are exact phrases founders search. Names former employers
         that act as social proof and keyword anchors.

WEAK:    Marketing professional with 8 years of experience
STRONG:  Demand Gen leader for B2B SaaS | Built pipeline engines from $0 to $40M ARR at 3 startups | ABM, PLG, Paid
WHY:     Replaces vague "8 years experience" with quantified outcomes ($0-$40M, 3 startups).
         Three keyword anchors at the end (ABM, PLG, Paid) catch all common Boolean searches.

WEAK:    Founder & CEO at Stealth Startup
STRONG:  Founder, building [Company] — modern observability for AI agents | YC W26 | hiring eng #2-#5
WHY:     "Stealth" tells nobody anything. Specific category ("observability for AI agents")
         attracts both press and recruiters. "YC W26" is a Boolean magnet for VCs. "Hiring"
         signals the profile owner is reachable.

WEAK:    Account Executive | Top performer | Quota crusher
STRONG:  Enterprise AE for DevTools | Closed $4.2M ARR last 4 quarters at [Company] | I sell to platform & infra teams
WHY:     "Top performer" is unverifiable noise. "$4.2M ARR" + "platform & infra teams" gives
         the buyer ICP information and recruiters a quota datapoint they can filter on.

WEAK:    UX Designer | Passionate about user-centered design
STRONG:  Senior Product Designer for B2B SaaS | I ship interfaces for AI/data products | ex-Figma, ex-Retool
WHY:     "Passionate about user-centered design" is true of literally every designer.
         Replacing it with a domain ("AI/data products") and proof anchors makes the profile
         findable for the 5 search strings hiring managers actually use.
```

### Step 5: Rewrite the About Section

The About section has 2,600 characters but only the first ~220 show before the "see more" fold on mobile. That's where the visitor decides whether to expand.

**Structure: Hook → Credibility → Proof → CTA**

1. **Hook (line 1, ~150 chars):** A specific claim or contrarian point. Not "I'm a passionate professional."
2. **Credibility (lines 2-4):** Who you are, who you've worked with, what category you own. Drop 2-3 brand-name proof points.
3. **Proof (the body, ~1,500 chars):** 3-5 bullet outcomes with metrics. What you actually did, not what you "led."
4. **CTA (last 200 chars):** What to do next. DM you for X. Book a call. Subscribe to your newsletter. Visit a Featured link.

**Worked example — engineering manager:**

```
WEAK (current):
"Experienced engineering manager passionate about building high-performing teams and shipping
quality software. I love mentoring engineers and working on challenging problems. Always open
to new opportunities."

STRONG (rewrite):
"I run engineering teams that ship reliable distributed systems — payments, search, identity —
at the scale where small bugs become $1M incidents.

Currently EM at [Company] (Series C, fintech). Previously led 14 engineers at Stripe across
the Issuing platform. Before that, founded a YC-backed dev tools company (acquired 2023).

What I've actually shipped:
• Cut p99 latency 480ms → 90ms on the core payments path serving 8B requests/year
• Grew an 8-person team to 22 across two timezones with <5% regrettable attrition over 3 years
• Owned the migration from monolith to 6-service architecture (zero downtime, 14-month rollout)
• Designed the on-call rotation now used across 60+ engineers in the org

I write occasionally about platform engineering, on-call culture, and how to interview senior
engineers — pinned in Featured below.

Open to: Director / Sr EM roles at Series B-D companies in payments, infra, or developer tools.
DM me — I respond within 24h."

WHY:
• Hook is a specific category claim ("payments, search, identity") not vague passion.
• Credibility hits two famous brands (Stripe, YC) within the first 200 chars — above the fold.
• Proof bullets all have numbers. "Led a team" becomes "8 → 22 with <5% attrition."
• CTA is concrete: target seniority, target stage, target domain, response SLA.
```

### Step 6: Rewrite Experience Bullets (STAR-style with metrics)

Most profiles paste job descriptions: "Responsible for managing a team and shipping features." This signals nothing. Rewrite every bullet as STAR (Situation → Task → Action → Result), prioritizing the Result.

**Bullet template:** `[Verb] [scope/system] [resulting in] [metric over baseline] [in timeframe].`

**Before/after:**

```
WEAK:    "Led the migration of legacy services to microservices."
STRONG:  "Led 14-month migration of monolithic Rails app (1.2M LOC, 80 engineers) to 6-service
         architecture; reduced deploy time from 45min to 4min and unblocked 3 product teams
         to ship independently."

WEAK:    "Improved sales pipeline."
STRONG:  "Rebuilt outbound motion (sequencing, ICP scoring, AE/SDR pairing); pipeline grew 3.4x
         in 6 months, win rate moved from 14% to 22%, ramp time for new AEs cut from 9mo to 5mo."

WEAK:    "Designed mobile app onboarding."
STRONG:  "Redesigned onboarding flow for 2.3M MAU mobile app after 6-week research sprint
         (38 user interviews); D7 retention +18%, completion rate 41% → 67%, shipped in 2 weeks
         with zero regression."
```

**Bullet rules:**
- 3-5 bullets per role for the last 3 roles. 1-2 for older roles.
- Lead with the verb. Lead with the result if it fits.
- Every bullet must contain at least one number, percentage, or named system/scope.
- Replace adjectives ("major", "significant", "key") with the actual size.
- If a number is confidential, give a baseline ratio: "3.4x baseline" or "top decile of org."

### Step 7: Optimize the Skills Section

LinkedIn lets you list 50 skills but only the **top 3 are pinned** and visible in the snapshot. Those three drive recruiter filter matching and the "People also viewed" graph.

**Top-3 pinning strategy:**
1. Pick the 3 keywords you most want to rank for in recruiter search.
2. Make them exact-match phrases recruiters actually filter on (`Product Management`, not `Product Strategy & Vision Leadership`).
3. Get each above 50 endorsements (LinkedIn weights "99+" significantly higher).

**Endorsement game:**
- Endorse 5 first-degree connections per week on the skills you want endorsed back. Reciprocity rate is ~30%.
- DM 10 close colleagues with: "Quick favor — I'm repositioning toward [skill]. Would you endorse me for it? I'll do the same for any 3 of your skills."
- Take the LinkedIn Skill Assessment for your top 3; the badge moves you up in filter results.

**Skills to remove:**
- Legacy skills from past careers (a "Lifeguard certified" skill from 2014 dilutes the signal).
- Generic skills everyone has (`Microsoft Word`, `Teamwork`).
- Anything not used in the last 3 years.

### Step 8: Activity Strategy — First 30 Days

The biggest mistake is starting with posts. Posts from a cold profile reach <100 people. Comments on big-account posts reach thousands and bring real profile views.

**Days 1-10: Comment-only phase**
- Identify 20 "lighthouse" accounts in your niche (50K+ followers, post 3x/week).
- Comment thoughtfully on 5 posts/day. Add a counter-example, a metric, or a personal experience — not "Great post!".
- Goal: 50 comments visible to 500K+ feed impressions cumulatively. Profile views typically 4-8x.

**Days 11-20: Comment + react + DM**
- Continue commenting at 5/day.
- DM 3 people/day who engaged with your comments. Open with the comment, not a pitch.
- Publish your first post on day 14: a 200-word personal story about a specific lesson. No links. Native LinkedIn rewards no-link posts.

**Days 21-30: Post cadence**
- 2 posts/week (Tue + Thu, 8-10am local time).
- Format mix: (1) personal story with a lesson, (2) listicle / framework, (3) screenshot of a metric or before-after, (4) contrarian take.
- Continue 5 comments/day (this is the engine, not the posts).

**What "good comment" looks like:**
- Bad: "100% agree, great points!"
- Bad: "Spot on. Sharing this with my team."
- Good: "We tried this and the opposite happened — when we cut sequence steps from 12 to 5, reply rates dropped 40%. Turns out our buyers were responding to step 9. Curious if your data shows the same drop-off."

### Step 9: Recommendations Strategy (give first to receive)

Recommendations are the #1 social-proof signal recruiters actually read. Most profiles have 0-2. Five recent ones is a moat.

**Outreach template (give first):**
```
Subject: A recommendation I drafted for you

Hey [Name],

I've been meaning to write you a LinkedIn recommendation. I drafted this — feel free to edit
or scrap it. No reply needed.

> [3-4 sentence specific recommendation: a project you collaborated on, a metric, what made
> them unusually good. Avoid generic adjectives.]

If you're up for returning the favor, I'm currently repositioning toward [target role/niche].
The angles that would help me most are [skill 1], [skill 2], and [outcome you want validated].
Zero pressure either way.

— [Your name]
```

Send to 8-10 people. Realistic conversion: 4-6 reciprocate. Mix of manager, peer, direct report, and customer/vendor produces the strongest profile.

### Step 10: Outbound Recruiter Prompt (job seekers)

Once the profile is rewritten, recruiters won't all find you organically — accelerate by reaching out to them directly.

**Recruiter search filters:**
- LinkedIn search → People → filters: `Title: "technical recruiter" OR "talent partner"`, `Industry: [your target]`, `Company: [target list]`.
- Connect with 15-20 in-house recruiters per target company (in-house > agency for most candidates).
- Personalized note (200 chars max):
```
Hi [Name] — saw you hire [role] at [Company]. I'm a [your role] with [headline outcome].
Open to chatting if [Company] is hiring. Profile has the rest. Either way, happy to connect.
```
- Acceptance rate target: >40%. If lower, your headline is the problem, not the note.

### Step 11: Differentiation Playbook by Role

Each role type has a different "what good looks like." Optimize accordingly:

| Role | Headline Anchor | About Body Focus | Featured |
|------|----------------|-----------------|----------|
| **Engineer** | Stack + scale ("Go + Kubernetes at 8B req/year") | Systems shipped, incidents owned, migrations led — not "passionate about clean code" | Tech blog post, talk video, GitHub link |
| **PM** | Domain + stage ("0-to-1 PM for B2B fintech") | Outcomes shipped, NOT features; metrics that moved (NPS, retention, ARR) | Case study, product launch press, podcast |
| **Designer** | Domain + medium ("Product designer for AI/data") | Before-after screenshots, research depth, ship cadence | Dribbble/portfolio, case study, screenshot |
| **Sales (AE/CSM)** | Quota + ICP ("Closed $4.2M ARR at DevTools to platform teams") | Quotas hit, deal sizes, ICP, methodology (MEDDIC, Sandler) | Customer logo wall, podcast, webinar |
| **Founder** | Category + stage ("Building observability for AI agents, YC W26") | Why now, why you, traction, hiring | Pitch deck (light), press, hiring page |
| **Marketer** | Function + stage ("Demand Gen leader, $0→$40M ARR at 3 startups") | Pipeline created, channels owned, frameworks (PLG, ABM, SEO) | Case study, podcast, lead magnet |

**Anti-patterns by role:**
- Engineers: listing every framework ever touched (Java, COBOL, Pascal, Rust, Brainfuck...). Pick 5 current.
- PMs: "Strategic visionary" with no shipped product mentioned. Show the product or hide it under NDA gracefully.
- Designers: text-heavy About with no visual. Use the banner and Featured for images — they're literally a designer.
- Sales: vanity awards ("President's Club 2019") without quota numbers. Numbers > awards.
- Founders: "Stealth mode" with no category named. Investors and recruiters can't help you if they don't know the category.
- Marketers: alphabet soup of acronyms (SEO, SEM, PPC, CRO, ABM, PLG) without a single outcome attached.

## Worked Example — Full Profile Rewrite (Founder)

```
BEFORE
─────────────────────────────────────────────────────────────────
Headline:  Founder & CEO at Stealth | Entrepreneur | Building cool things
Banner:    Default blue
About:     "Serial entrepreneur passionate about technology and innovation.
            Currently building something exciting in stealth mode. Previously
            worked at multiple startups. Always open to chat with smart people."
Skills:    Leadership, Entrepreneurship, Strategy
Featured:  (empty)
Activity:  Last post 11 months ago

AFTER
─────────────────────────────────────────────────────────────────
Headline:  Founder, Lumen — observability for AI agents | YC W26 | Previously eng lead
           on Datadog APM | Hiring eng #2-#4

Banner:    Product screenshot + tagline "See what your agents actually do"
           + small headshot, top-right.

About:
"Most LLM apps fail in production not because the model is wrong, but because nobody
can see what the agent did. Lumen is observability built for AI agents — traces, eval
deltas, and prompt diffs in one timeline.

I'm Petro, founder of Lumen (YC W26). Before this I led the APM ingest team at Datadog
for 4 years (we 6x'd ingest throughput on the same hardware). Before that, founded a
small dev tools company acquired by GitLab in 2021.

What we've shipped in 4 months:
• 38 design partners across YC W25/W26 batches
• Trace volume: 14M agent steps/day
• $42K MRR, growing 31% MoM
• Open-source SDK: 1.4K GitHub stars

Hiring:
→ Founding engineer #2 (TS / Go, distributed systems)
→ Founding designer
→ Developer advocate

I post weekly about: agent reliability, eval design, why traditional APM breaks for
LLMs. Pinned posts in Featured below.

Email: petro@lumen.dev — I reply within 12h."

Skills (top 3):  Observability  •  AI Infrastructure  •  Distributed Systems
Featured:        Lumen launch post (HN), YC video, hiring page, top blog post
Activity:        3 posts/week, 5 comments/day on AI infra & YC accounts

WHY THIS WORKS
─────────────────────────────────────────────────────────────────
- Headline names the category ("observability for AI agents") that VCs and journalists
  search for, anchors social proof (YC, Datadog), signals reachability (hiring).
- About hook is a specific contrarian claim, not a feel-good intro.
- Above-the-fold text mentions YC, Datadog, GitLab — three keyword and credibility hits.
- Bullets are quantified (MRR, MoM growth, GitHub stars) — investors can underwrite the
  profile in 30 seconds.
- CTA is unambiguous: hiring three roles, email response SLA stated.
```

## Worked Example — IC Engineer Job Search

```
BEFORE
Headline:  Software Engineer at Acme | Coding enthusiast
About:     "I'm a software engineer who loves building things. Skilled in many
           technologies. Open to opportunities."

AFTER
Headline:  Backend Engineer for high-throughput systems | Go, Postgres, Kafka
           | Building payments at Acme (ex-Square) | Open to Senior/Staff roles

About:
"I build backend systems where small bugs become large incidents — payments, ledgers,
fraud. I optimize for correctness first, throughput second, and developer ergonomics
third.

Currently Backend Engineer at Acme (Series C fintech). Previously 4 years at Square on
the Issuing platform. CS @ University of [X], 2018.

Recent work I'm proud of:
• Rewrote the payment-retry pipeline (Go, Kafka): cut duplicate charges 92%, recovered
  $1.4M/year in failed-then-succeeded transactions
• Built the idempotency layer used by 11 internal services; zero double-write incidents
  in the 18 months since launch
• Reduced p99 latency on the core auth-charge path from 480ms → 90ms (profiling +
  connection pool tuning + a Postgres index rewrite)
• Wrote and maintain the on-call runbooks for our 8-engineer payments team

Stack I use day-to-day: Go, PostgreSQL, Kafka, Redis, Kubernetes, Datadog, Terraform.

Looking for: Senior or Staff Backend roles at Series B+ fintech, payments, or infra
companies. Remote (US/EU timezones) or hybrid in NYC.

DM me here, or petro@email.com — I reply within 24h."
```

## Output

The agent produces:

- **Audit scorecard**: 8 surfaces, each scored 0-2 with the specific reason.
- **SSI estimate**: current pillar-by-pillar estimate and the 5 fastest moves.
- **Keyword map**: spine keywords + where each one is currently placed and where it should also appear.
- **Rewritten headline**: 2-3 variants the user can A/B.
- **Rewritten About**: full 2,600-character version with the hook above the fold.
- **Rewritten Experience bullets**: 3-5 STAR bullets per role for the last 3 roles.
- **Skills shortlist**: top-3 pinned + 17 supporting + a removal list.
- **30-day activity calendar**: day-by-day comment/post/DM plan.
- **Recommendation outreach list**: 8-10 people to ask, with the give-first template filled in for each.
- **Recruiter outbound list**: 15-20 in-house recruiters at target companies with personalized notes.

## Tips for Best Results

- Paste the actual current profile text (headline + About + last 2 roles minimum). Screenshots without the text force the agent to guess.
- State the goal: job search, inbound leads, fundraise, or category authority. The optimal profile is different for each.
- Name the target audience: "Senior eng recruiters at Stripe-tier companies" beats "people who like my work."
- Share 2-3 examples of profiles you admire — the agent can match tone and structure.
- Mention the constraint: under NDA, can't name employer, can't post publicly, etc. The agent works around it.
- Run the audit again 30 days after applying changes — measure profile views, search appearances, and DMs received as your ground truth, not SSI alone.

## When NOT to use

- **You need a resume, not a LinkedIn profile.** Resumes optimize for ATS keyword density and one-page density; LinkedIn optimizes for a different funnel. Use a resume skill for ATS work.
- **You're under strict NDA / your role can't be public.** Government, classified, pre-stealth acquisition — improving the profile may surface signals you don't want surfaced. Stay quiet and use private outreach instead.
- **You're using LinkedIn for personal networking only, not professional outcomes.** Optimization assumes you want recruiters, buyers, or investors to find you. If you only want to keep up with old colleagues, leave the profile as-is.
- **The bottleneck isn't the profile — it's the resume, interview, or pipeline.** If you get plenty of recruiter outreach but no offers, the problem is downstream of LinkedIn. Diagnose the actual choke point first.
- **Your industry isn't on LinkedIn.** Niche trades, certain creative fields, and some regional markets run on other networks (GitHub, Behance, X, regional equivalents). Optimize where your audience actually is.
- **You need cold-outbound copy or sequence design.** That's a sales-engagement skill, not a profile skill — the profile is the landing page, not the email.
