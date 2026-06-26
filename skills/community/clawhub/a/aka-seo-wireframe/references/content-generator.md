# AKA Content Generator

## Purpose
Generates SEO-optimized content for Authority, Knowledge, and Answer pages with automatic variable injection and link placeholders following the AKA framework.

## Model
claude-opus-4

## When to Use
- After strategy is generated
- To create individual pages or batches
- For any page type (Authority, Knowledge, Answer)
- When content needs updating or refreshing

## Capabilities
- Authority page generation (4,000 words)
- Knowledge page generation (2,000 words)
- Answer page generation (1,000 words, featured snippet optimized)
- Automatic {{VARIABLE}} injection from config
- [LINK:...] placeholder injection for internal linking
- SEO optimization (titles, meta, headings, keywords)
- Brand voice consistency (VOMA framework)
- Schema markup suggestions

## Input Required

**Required Files**:
1. `.factory/config/aka-wireframe/business-config.json` - Business variables
2. `.factory/config/aka-wireframe/aka-strategy-output.json` - Complete strategy
3. Hub number and page type

**Parameters**:
- `--type` authority|knowledge|answer
- `--hub` 1-7 (which hub)
- `--page` N (specific page number within hub)
- `--batch` (generate all pages for hub)

## Output Generated

**Files Created**:
```
generated-content/
├── hub-1/
│   ├── authority/
│   │   └── ac-repair-services.md
│   ├── knowledge/
│   │   ├── ac-not-cooling-troubleshooting.md
│   │   ├── ac-refrigerant-leak-repair.md
│   │   └── ... (15 total)
│   └── answers/
│       ├── how-much-ac-repair-cost.md
│       ├── why-ac-not-cooling.md
│       └── ... (25 total)
└── hub-2/
    └── ...
```

**Content Format** (Markdown with frontmatter):
```markdown
---
title: "AC Repair Services in Atlanta | Cool Air HVAC"
metaDescription: "Expert AC repair in Atlanta. Same-day service, upfront pricing..."
slug: "ac-repair-services"
pageType: "authority"
hubId: 1
primaryKeyword: "AC repair Atlanta"
secondaryKeywords: ["Atlanta AC repair", "air conditioning repair", "AC service"]
wordCount: 4247
generatedAt: "2024-10-15T12:30:00Z"
---

# AC Repair Services in Atlanta, GA

[Content with {{VARIABLES}} replaced and [LINK:...] placeholders...]
```

## Variable Injection System

All content automatically replaces these placeholders:

**Business Variables**:
- `{{BUSINESS_NAME}}` → "Cool Air HVAC"
- `{{INDUSTRY}}` → "Home Services (HVAC)"
- `{{LOCATION}}` → "Atlanta, GA"
- `{{PRIMARY_SERVICE}}` → "AC Repair"
- `{{PHONE}}` → "404-555-1234"
- `{{EMAIL}}` → "info@coolairhvac.com"

**Audience Variables**:
- `{{TARGET_AUDIENCE}}` → "Homeowners with HVAC problems"
- `{{PAIN_POINTS}}` → "Broken AC, High bills, Emergency repairs"
- `{{UNIQUE_VALUE}}` → "Same-day service, upfront pricing"

**Trust Variables**:
- `{{YEARS_IN_BUSINESS}}` → "15"
- `{{CLIENTS_SERVED}}` → "10,000+"
- `{{KEY_RESULTS}}` → "$5M+ in satisfied customers"

**Brand Voice**:
- `{{BRAND_VOICE}}` → "Helpful, fast, available"

## Link Placeholder System

Content includes strategic link placeholders that will be converted by aka-internal-linker:

**Format**: `[LINK:page-slug|anchor text]`

**Example in Generated Content**:
```markdown
When your AC stops cooling, the problem could be a 
[LINK:knowledge-refrigerant-leaks|refrigerant leak], a 
[LINK:knowledge-compressor-failure|failed compressor], or 
[LINK:knowledge-thermostat-issues|thermostat problems].

Many homeowners wonder [LINK:answer-how-much-repair-cost|how much AC repair costs] 
and [LINK:answer-diy-vs-professional|whether to DIY or hire a pro].
```

**Link Placement Rules** (AKA Framework):

**Authority Pages** include links to:
- All 12-15 Knowledge pages in hub (distributed naturally)
- Top 5-10 Answer pages in hub
- 1-2 other Authority hubs (cross-hub linking)

**Knowledge Pages** include links to:
- Parent Authority page (2-3 times)
- 2-3 sibling Knowledge pages (related topics)
- 3-5 relevant Answer pages

**Answer Pages** include links to:
- Parent Authority page (once, prominently)
- 1-2 relevant Knowledge pages (for deep-dive)
- 2-3 related Answer pages (similar questions)

## Content Generation by Page Type

### Authority Page (4,000 words)

**Structure**:
```markdown
# {{PRIMARY_SERVICE}} in {{LOCATION}} | {{BUSINESS_NAME}}

[Trust Bar: ⭐⭐⭐⭐⭐ Reviews | 💰 Results | 📞 Free Consultation]

## Quick Navigation
[Table of contents]

## 🚨 Emergency Banner (if applicable)
**Need {{PRIMARY_SERVICE}} now?** Call {{PHONE}} - Available 24/7

## Introduction: You're Not Alone (300 words)
[Empathy for {{TARGET_AUDIENCE}}]
[Address {{PAIN_POINTS}}]
[{{BUSINESS_NAME}} value proposition]
[Trust signals: {{YEARS_IN_BUSINESS}}, {{CLIENTS_SERVED}}]

## Section 1: Understanding {{PRIMARY_SERVICE}} (900 words)
[Comprehensive explanation]
[{{LOCATION}} specific details]
[Statistics and data]
[Links to 3-4 Knowledge pages: [LINK:knowledge-page-slug|anchor]]

## Section 2: Types of {{PRIMARY_SERVICE}} (800 words)
[8-10 specific types]
[Each type links to Knowledge page: [LINK:...]]

## Section 3: The Process (800 words)
[Step-by-step walkthrough]
[What {{TARGET_AUDIENCE}} can expect]
[Timeline and pricing transparency]

## Section 4: Why Choose {{BUSINESS_NAME}} (600 words)
[{{UNIQUE_VALUE}}]
[{{KEY_RESULTS}}]
[Testimonials and proof]

## FAQ Section (400 words)
[5-7 questions linking to Answer pages: [LINK:answer-slug|question]]

## Conclusion with CTA (200 words)
[Summary, next steps, contact info: {{PHONE}}, {{EMAIL}}]
```

**SEO Optimization**:
- Primary keyword density: 0.8-1.2%
- H1: One per page with primary keyword
- H2-H3: Hierarchical with secondary keywords
- Meta title: 60 characters max
- Meta description: 155 characters max
- Internal links: 25-30 via placeholders
- Schema: Article + Service + LocalBusiness

### Knowledge Page (2,000 words)

**Structure**:
```markdown
# {{SPECIFIC_TOPIC}} | {{BUSINESS_NAME}}

## Introduction (200 words)
[What this topic is]
[Why it matters to {{TARGET_AUDIENCE}}]
[Link to parent: [LINK:hub-slug|{{PRIMARY_SERVICE}}]]

## Understanding {{SPECIFIC_TOPIC}} (500 words)
[Comprehensive explanation]
[{{LOCATION}} specific factors]
[Technical details made simple]

## Signs/Symptoms (400 words)
[How to identify the issue]
[When it's urgent vs routine]
[What {{TARGET_AUDIENCE}} often misses]

## Solutions and Process (600 words)
[How {{BUSINESS_NAME}} addresses this]
[Step-by-step breakdown]
[Timeline and cost factors]
[Links to related Knowledge: [LINK:sibling-knowledge|topic]]

## FAQ (200 words)
[3-5 questions linking to Answers: [LINK:answer-slug|question]]

## Next Steps (100 words)
[Clear call-to-action]
[{{PHONE}} or consultation link]
```

**SEO Optimization**:
- Primary keyword density: 1.0-1.5%
- Word count: 2,000-2,500
- Internal links: 8-12 via placeholders
- H2-H3 structure
- Schema: Article + HowTo (if process-based)

### Answer Page (1,000 words)

**Structure** (Featured Snippet Optimized):
```markdown
# {{EXACT_QUESTION}}

## Quick Answer (50-100 words)
**[Direct answer in bold, optimized for featured snippet]**

[Can be formatted as:]
- Numbered list (for steps)
- Bullet points (for multiple answers)
- Table (for comparisons)
- Paragraph (for explanations)

## Detailed Explanation (400 words)
[Expand on quick answer]
[{{LOCATION}} specific context]
[Address related concerns]
[Link to parent: [LINK:hub-slug|{{PRIMARY_SERVICE}}]]

## Important Considerations (200 words)
[Things people often miss]
[Common mistakes]
[{{BUSINESS_NAME}} recommendations]

## What to Do Next (150 words)
[Clear action steps]
[When to contact {{BUSINESS_NAME}}]
[{{PHONE}} or consultation CTA]

## Related Questions (100 words)
[3-5 related questions: [LINK:answer-slug|question]]
[Link to deeper content: [LINK:knowledge-slug|topic]]
```

**SEO Optimization**:
- Question as H1 exactly as searched
- Quick answer in first paragraph
- Featured snippet formatting
- Schema: FAQPage
- Internal links: 5-8 via placeholders

## Brand Voice Integration (VOMA)

Content tone matches `{{BRAND_VOICE}}`:

**"Helpful, fast, available"** (HVAC example):
- Short paragraphs (2-3 sentences)
- Active voice, action-oriented
- Emergency emphasis where relevant
- Transparent about pricing/timeline
- Reassuring, not pushy

**"Professional, empathetic, assertive"** (Law example):
- Formal but approachable
- Acknowledge customer stress
- Strong value proposition
- Clear about process and rights
- Confident without overpromising

## Batch Generation

When `--batch` flag used:

**Process**:
1. Load strategy for specified hub
2. Generate Authority page first
3. Generate all 12-15 Knowledge pages
4. Generate all 20-30 Answer pages
5. Save all files to hub directory
6. Report summary and next steps

**Output**:
```
✅ Hub 1 Content Generation Complete!

Generated:
- 1 Authority page (4,247 words)
- 15 Knowledge pages (31,450 words)  
- 25 Answer pages (23,180 words)

Total: 41 pages, 58,877 words
Time: ~8 minutes
Link placeholders: 247

Files saved to: generated-content/hub-1/

Next: Run 'aka-wireframe-wp link --hub 1' to process links
```

## Quality Control

Each generated page includes:
- ✅ Proper word count for page type
- ✅ All {{VARIABLES}} replaced
- ✅ Link placeholders follow format
- ✅ SEO metadata complete
- ✅ Proper heading hierarchy
- ✅ Brand voice consistent
- ✅ Grammar and spelling correct
- ✅ No duplicate content

## Example Generated Content

**Authority Page Excerpt**:
```markdown
# AC Repair Services in Atlanta, GA | Cool Air HVAC

⭐⭐⭐⭐⭐ 500+ Five-Star Reviews | 💰 15 Years Serving Atlanta | 📞 404-555-1234

## Your AC Stopped Working? We're Here to Help 24/7

When summer temperatures soar in Atlanta, a broken air conditioner isn't 
just inconvenient—it's an emergency. At Cool Air HVAC, we understand the 
stress of dealing with AC problems. Our team has been serving homeowners 
across Atlanta for 15 years, completing over 10,000 successful repairs.

Whether you're dealing with [LINK:knowledge-ac-not-cooling|an AC that won't cool], 
[LINK:knowledge-refrigerant-leaks|a refrigerant leak], or 
[LINK:knowledge-compressor-failure|a failed compressor], we provide same-day 
service with upfront pricing.

Many customers wonder [LINK:answer-how-much-cost|how much AC repair costs] 
before calling. We believe in transparency...
```

## Notes

- Generated content is Markdown (easy to edit, version control)
- Variables inject automatically based on business-config.json
- Link placeholders converted later by aka-internal-linker
- Content follows AKA framework strictly
- SEO optimization is automatic, not manual
- Brand voice pulled from VOMA config
- All content is unique and customized per business
