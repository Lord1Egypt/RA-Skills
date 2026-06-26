---
name: canmarket-blog
description: "Write and publish SEO-optimized blog posts to canmarket.ai. Researches topic, writes article with original data, creates Nuxt page, commits, pushes, auto-deploys. Optionally cross-posts to DEV.to. Triggers on 'write blog', 'new blog post', 'publish article', '写博客', '发文章', '/canmarket-blog'."
homepage: https://canlah.ai
---

# CanMarket Blog Writer

Write, publish, and deploy SEO-optimized blog posts to canmarket.ai in one command.

## When to Use

- "Write a blog post about X"
- "New article for canmarket.ai"
- "/canmarket-blog [topic]"
- "写一篇关于 X 的博客"

## Blog Strategy Rules

### Frequency
- **Max 3 posts/week** for new domain (avoid spam signals)
- **Gradual ramp**: Week 1-2: 2 posts/week → Week 3-4: 3 posts/week
- Never publish multiple posts in one day

### Content Rules (Google E-E-A-T safe)
- AI writes draft → MUST add original data from CanMarket's real simulations
- Include specific numbers: "$499", "9.2/10", "105 actions", "6 minutes"
- Every post needs at least ONE thing Google can't find elsewhere
- No generic filler — every paragraph must add value
- Include author byline: "Haoyang Pang, Founder & CEO at CanMarket"

### SEO Requirements
- Title: < 60 chars, include primary keyword
- Meta description: 150-160 chars
- H1 = title (exactly one)
- H2s for major sections, H3s for sub-sections
- Internal links back to homepage (/), pricing (#pricing), case study (#case-studies)
- Target 1,200-2,000 words (long-form ranks better for B2B)

### Topic Pillars (rotate between these)
1. **Case Studies** — Real simulation results, brand analysis
2. **Industry Education** — Brand safety, XHS marketing, campaign planning
3. **Product Comparison** — CPT™ vs focus groups, vs Aaru, vs manual testing
4. **How-To Guides** — How to test campaigns, how to optimize for XHS
5. **Market Intelligence** — Fashion marketing trends, AI in marketing, SEA insights

## Execution Flow

### Step 1: Research Topic
```
Use WebSearch to find:
- What's currently ranking for the target keyword
- What angle is NOT covered (content gap)
- 2-3 data points to reference
```

### Step 2: Write Article
```
Structure:
- Hook (1-2 sentences, problem or surprising stat)
- Context (why this matters to fashion/DTC brands)
- Main content (3-5 sections with H2s)
- Original data section (CanMarket simulation results)
- Actionable takeaways (numbered list)
- CTA ("Try Campaign Pressure Test™ free — canmarket.ai")
```

### Step 3: Create Nuxt Blog Page

Blog posts go in: `/tmp/canmarket-landing/app/pages/blog/`

**First time setup** (if /blog/ doesn't exist):
```bash
mkdir -p /tmp/canmarket-landing/app/pages/blog
```

Create blog index page if it doesn't exist: `app/pages/blog/index.vue`
Create individual post: `app/pages/blog/[slug].vue` (dynamic route)
Store content as markdown in: `content/blog/YYYY-MM-DD-slug.md`

Or simpler: create static Vue pages per post:
`app/pages/blog/campaign-pressure-test-vs-focus-groups.vue`

### Step 4: SEO Meta
```typescript
useSeoMeta({
  title: 'Article Title | CanMarket Blog',
  description: '150-char meta description with keyword',
  ogTitle: 'Article Title',
  ogDescription: 'Same as description',
  ogImage: 'https://canmarket.ai/blog/og-[slug].png',
  ogType: 'article',
})

// Article JSON-LD
useHead({
  script: [{
    type: 'application/ld+json',
    innerHTML: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: 'Title',
      author: { '@type': 'Person', name: 'Haoyang Pang' },
      publisher: { '@type': 'Organization', name: 'CanMarket AI' },
      datePublished: '2026-03-21',
      image: 'https://canmarket.ai/blog/og-[slug].png',
    })
  }]
})
```

### Step 5: Build + Deploy
```bash
cd /tmp/canmarket-landing
npm run build  # verify no errors
git add -A
git commit -m "blog: [title] — [primary keyword]"
git push origin main  # Vercel auto-deploys
```

### Step 6: Cross-post to DEV.to (optional)
```bash
# Use devto-post skill with canonical URL pointing back to canmarket.ai
# Add at top of DEV.to article:
# canonical_url: https://canmarket.ai/blog/[slug]
```

### Step 7: Submit to GSC
Remind user to use URL Inspection tool in Google Search Console to request indexing of the new blog URL.

## Content Templates

### Case Study Template
```markdown
# We Ran [Product] Through an AI Audience Simulation. Here's What Happened.

## The Setup
[Brand context, target audience, platform, competitors]

## What the Simulation Found
[Key metrics: Brand Safety Score, actions, engagement]

### Finding 1: [Insight]
[Data + quote from simulation]

### Finding 2: [Insight]
[Data + competitive risk]

### Finding 3: [Insight]
[Unexpected discovery]

## What We Changed (and Why)
[How insights improved the campaign]

## Try It Yourself
Campaign Pressure Test™ simulates your audience in 6 minutes.
First test free — [canmarket.ai](https://canmarket.ai)
```

### Comparison Template
```markdown
# [Our Product] vs [Alternative]: [Key Differentiator]

## TL;DR
[One-sentence verdict]

## Side-by-Side Comparison
| Feature | CPT™ | [Alternative] |
|---------|------|---------------|
| Cost | $499/sim | $X |
| Time | 6 min | X weeks |
| ... | ... | ... |

## When to Use [Alternative]
[Be fair — builds trust]

## When to Use Campaign Pressure Test™
[Our sweet spot]

## The Bottom Line
[Recommendation based on use case]
```

## Important Notes

- **Canonical URL**: If cross-posting to DEV.to, always set `canonical_url` to canmarket.ai
- **No keyword stuffing**: Natural language, 1-2% keyword density max
- **Images**: Generate OG image for each post (1200x630, dark theme matching site)
- **Internal linking**: Every post links to at least 2 other pages on canmarket.ai
- **Build verify**: ALWAYS `npm run build` before pushing — broken builds kill SEO

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
