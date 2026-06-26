# GEO Content Publisher – Reference Templates

This file provides reusable templates and examples that the `geo-content-publisher` skill can draw
on without having to rewrite them from scratch every time.

Keep this file short, skimmable, and easy to adapt. The goal is to speed up reasoning and output
generation, not to be a full textbook.

---

## 1. Default longform page structure

Use this structure for **landing pages, pillar articles, and longform docs** that you want AI models
to cite. Adapt headings as needed, but try to preserve the overall logic.

```markdown
# [Clear, entity-focused H1]

## Summary
- 2–4 bullet points summarizing what this page is about.
- Focus on concrete facts, definitions, and stable product claims.

## What is [Topic or Product]?
Explain in clear, factual language:
- A short definition in 1–2 sentences.
- A slightly longer explanation (1–2 paragraphs) with simple examples.

## Why [Topic] matters
- Describe the main problems, risks, or opportunities.
- Use concrete, real-world scenarios.

## How [Brand/Product] helps
- Tie the topic back to the brand or product.
- Highlight 3–5 key capabilities or benefits.
- Optionally include a comparison table vs. alternatives.

## Key use cases
- Use case 1: [Name]
  - Who it is for
  - What changes for them
- Use case 2: [Name]
- Use case 3: [Name]

## Implementation or getting started
- Step 1: ...
- Step 2: ...
- Step 3: ...

## FAQ
Q1: [Common question]
A1: [Short, self-contained answer.]

Q2: [Common question]
A2: [Short, self-contained answer.]

Q3: [Common question]
A3: [Short, self-contained answer.]
```

---

## 2. Channel plan table template

Standard table for mapping the **core asset** to multiple channels.

```markdown
| Channel      | Role / Objective              | Format / Asset Type         | Primary Message / Angle                  | Primary CTA                    | Canonical Target |
|-------------|-------------------------------|-----------------------------|------------------------------------------|--------------------------------|------------------|
| Website LP  | GEO anchor & main converter   | Longform landing page       | Core value prop + social proof           | Start trial / Request demo     | Pricing LP       |
| Blog        | Educational context & support | Article + FAQ               | Zoom into one angle or problem scenario  | Read full guide / See pricing  | Pricing LP       |
| Docs / KB   | Implementation detail         | How-to / concept docs       | “How it works” and technical specifics   | Implement feature / Configure  | Docs home        |
| LinkedIn    | Thought leadership            | Post + optional carousel    | Strategic angle + 1–2 data points        | Visit LP / Comment             | Pricing LP       |
| X / Twitter | Awareness + curiosity         | Short threads / single post | Punchy hook + 1 key benefit or example   | Click through to LP or blog    | LP or blog       |
| Newsletter  | Deep-dive for subscribers     | Email feature or digest     | Why this matters now for this audience   | Read more / Book a call        | LP / blog        |
```

When generating a real plan, fill each cell with **concrete, user-specific content**, not placeholders.

---

## 3. Social post patterns

### 3.1 LinkedIn post pattern (B2B)

```markdown
Hook line introducing the core problem or opportunity in 1–2 sentences.

Short paragraph explaining:
- What has changed in the market / environment.
- Why this matters now for [target audience].

Bulleted list (3–5 bullets) covering:
- Key insight or data point #1
- Key insight or data point #2
- Key insight or data point #3

Transition: “We’ve put together a detailed guide on [topic] covering:”
- Section 1 summary
- Section 2 summary
- Section 3 summary

CTA: “Read the full guide here → [link to canonical LP or article]”

Optional: Ask a question to invite comments.
```

### 3.2 X / Twitter thread pattern

```markdown
1/ Strong hook about the core problem or surprising insight.

2/ Short explanation of why this matters for [audience].

3–5/ Each tweet covers:
- One clear idea
- One example or data point
- Plain language (no jargon if avoidable)

Final tweet:
“We put everything into a deep-dive on [topic], including [A], [B], [C]. Read it here → [link]”
```

---

## 4. Email / newsletter snippet template

```markdown
Subject: [Outcome-focused subject about topic or benefit]

Hi [First name / there],

In the last [time period], we’ve seen [problem or trend] become a top priority for [audience].

To help, we created a new resource on [topic], covering:
- [Key takeaway 1]
- [Key takeaway 2]
- [Key takeaway 3]

If you’re working on [situation 1] or [situation 2], this will help you:
- [Result / benefit 1]
- [Result / benefit 2]

👉 Read the full guide: [canonical link]

Best,
[Brand / Team]
```

---

## 5. Minimal JSON-LD examples

These are **skeletal** examples to keep in mind when generating schema. Always adapt fields to the
user’s actual site, URLs, and organization data.

### 5.1 Article / BlogPosting skeleton

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "TITLE HERE",
  "description": "1–2 sentence summary of the article.",
  "url": "https://example.com/path",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Brand Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2025-01-01",
  "mainEntityOfPage": "https://example.com/path"
}
```

### 5.2 FAQPage skeleton

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question 1?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Short, self-contained answer to question 1."
      }
    },
    {
      "@type": "Question",
      "name": "Question 2?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Short, self-contained answer to question 2."
      }
    }
  ]
}
```

---

## 6. Alt text and filename patterns

- Prefer: `alt="Dashboard showing monthly MRR by cohort for SaaS product"`  
  Over: `alt="screenshot"` or `alt="image"`.

- Prefer filenames like:
  - `zero-trust-data-governance-architecture.png`
  - `pricing-tier-comparison-startup-vs-enterprise.png`

Avoid:
- `image1.png`, `screenshot-final.png`, `diagram-new-new-2.png`

