# SEO Strategy Framework

Compiled from Dennis Yu, Search Logistics, Kyle Roof, and Matt Diggity.

## Tier 1: Foundational (Always Execute)

### On-Page Keyword Placement (Kyle Roof)
- Target keyword in URL, title tag, H1, meta description, paragraph tags
- This alone is 60% of SEO
- The #1 ranking factor is the ABSENCE of a factor — missing from one of Google's checkboxes is worse than being weak on any single one
- For every page: verify keyword presence in URL, title, H1, meta description, first paragraph. Flag any missing.

### Schema Markup (Search Logistics + Diggity)
- 90% of sites are missing critical schema
- Every page type needs its own: LocalBusiness, FAQ, Service, Product, Article, BreadcrumbList, Organization
- Both Google and LLMs use structured data to understand and surface content
- Once added, benefits are permanent

### Trust Signals / E-E-A-T (Search Logistics + Kyle Roof)
- Business info in footer, about page, contact page
- Real team photos, staff bios, testimonials, "featured in" sections
- Review presence on GBP, Trustpilot, Facebook
- Citations in directories for Google to confirm identity
- "If you're real, you don't have E-E-A-T problems" (Roof)

### Mobile Core Web Vitals (Search Logistics)
- Google uses mobile-first indexing exclusively
- Poor mobile speeds hurt your ENTIRE site's rankings (desktop too)
- Fix stack: Cloudflare CDN + caching plugin + image compression

### Kill Mobile Pop-ups (Search Logistics)
- Penalized since 2016, still found constantly
- Replace with small sliding banners or bottom bars

## Tier 2: High-ROI Amplifiers (Do After Tier 1)

### Internal Linking (Dennis Yu)
**Must follow this sequence:**

1. **GCT (Goals, Content, Targeting)** — understand the business before touching links
2. **Fix Categories & Tags** — correct page assignments reflecting entity structure
3. **Build Links Based on Relevance** — contextually relevant, specific anchors, surrounding context matters
4. **QA Against Google Guidelines** — audit own work
5. **MAA Loop (Metrics, Analysis, Action)** — connect to GA/GSC, weekly/monthly review, iterate

**What NOT to do:** Don't spray hundreds of random links. Don't link everything to the money page. Don't use generic anchors. Don't stuff footer links.

### FAQ Freshness Hack (Search Logistics)
- Add FAQ sections with FAQ schema to every page
- Update ONE question every 6 months
- Google and ChatGPT favor aged content that's continuously updated
- Cheapest way to signal freshness

### Content Quality Audit (Search Logistics)
- One excellent page beats 100 mediocre ones
- 100 junk pages can sink your entire site (Helpful Content Update)
- Per page: Improve, Noindex, or Delete & redirect

## Tier 3: Context-Dependent

### Outreach Link Building (Diggity)
- Best for: businesses needing external backlinks
- Prospect in shoulder niches (not competitors)
- Filter for quality (DR, traffic), find decision-maker emails
- Warm up sending accounts, personalized multi-step sequences
- Only after on-page and internal linking are solid

### E-commerce Micromoments (Diggity)
- Only for product/e-commerce businesses
- Map content to know/go/do/buy stages
- Faceted navigation for long-tail combinations
- Pre-build seasonal pages 3 months ahead

### Programmatic SEO (Diggity)
- Only for scalable datasets (directories, comparisons, location-based)
- Head term + modifier patterns
- Free datasets, content templates, auto-generate pages
- NOT for small local businesses with 10-20 pages

### Exact Match & Aged Domains (Kyle Roof)
- Experiencing a resurgence in 2025-2026
- Check Wayback Machine, rebuild pages that actually existed
- Only for new projects or complementary domain acquisition

## What NOT to Worry About

| Myth | Reality | Source |
|---|---|---|
| Grammar as ranking factor | Tested — NOT a ranking factor | Kyle Roof |
| Reading level as ranking factor | Tested — NOT a ranking factor | Kyle Roof |
| Domain Authority obsession | Useful benchmark, NOT a direct ranking factor | Kyle Roof |
| "Semantic triples" / NLP tricks | "I think it's just writing a sentence" — overly complicated | Kyle Roof |
| AI content detection by Google | Google detects poorly optimized content, not AI writing per se | Kyle Roof |
| One-click SEO tools | Any tool that doesn't understand business context creates vandalism | Dennis Yu |
| Broad topical authority blogging | Quality > quantity; 20% of content drives 80% of leads | Diggity |

## Recommended Execution Order

```
PHASE 1: DISCOVERY & FOUNDATION
├── 1.1 Business intake (GCT: Goals, Content, Targeting)
├── 1.2 Crawl entire site — inventory all pages
├── 1.3 Check keyword placement on every page
├── 1.4 Audit Core Web Vitals (mobile)
├── 1.5 Check for mobile pop-ups
└── 1.6 Audit trust signals

PHASE 2: STRUCTURAL FIXES
├── 2.1 Fix/add schema markup on every page
├── 2.2 Fix categories & tags based on GCT
├── 2.3 Thin content audit — improve/noindex/delete
├── 2.4 Add FAQ sections with schema to key pages
└── 2.5 Fix any missing keyword placements

PHASE 3: INTERNAL LINKING
├── 3.1 Map entity relationships (people, services, locations, topics)
├── 3.2 Build contextually relevant internal links
├── 3.3 QA all links against Google Guidelines
└── 3.4 Human review checkpoint

PHASE 4: EXTERNAL GROWTH
├── 4.1 Citation/directory campaign
├── 4.2 Content placement articles
├── 4.3 Competitor backlink gap analysis
└── 4.4 Outreach link building (if budget allows)

PHASE 5: RECURSIVE OPTIMIZATION
├── 5.1 Connect to GA/GSC
├── 5.2 Weekly/monthly MAA loop
├── 5.3 Update FAQ questions every 6 months
└── 5.4 Continuous internal link refinement
```
