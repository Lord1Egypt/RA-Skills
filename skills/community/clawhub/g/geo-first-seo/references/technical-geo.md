# Technical GEO

Copy-paste structured-data snippets, an `llms.txt` template, and a markup checklist for Phase 3 of
`SKILL.md`. Replace every placeholder with a real value; never fabricate authors, dates, or URLs —
leave a clearly labeled placeholder if you do not know one.

**Rule:** only mark up content that actually appears on the page. Mismatched structured data hurts
trust and can be flagged as spam.

## schema.org JSON-LD

Add as a `<script type="application/ld+json">` block in the page `<head>` or body.

### Article / BlogPosting

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "PAGE_TITLE",
  "description": "ONE_SENTENCE_SUMMARY",
  "author": {
    "@type": "Person",
    "name": "AUTHOR_NAME",
    "url": "AUTHOR_PROFILE_URL"
  },
  "publisher": {
    "@type": "Organization",
    "name": "ORG_NAME",
    "logo": { "@type": "ImageObject", "url": "ORG_LOGO_URL" }
  },
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "CANONICAL_URL" }
}
```

### FAQPage

Mirror the on-page FAQ block exactly — same questions, same answers.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "QUESTION_TEXT",
      "acceptedAnswer": { "@type": "Answer", "text": "ANSWER_TEXT" }
    }
  ]
}
```

### HowTo

For step-by-step content.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "TASK_NAME",
  "step": [
    { "@type": "HowToStep", "name": "STEP_NAME", "text": "STEP_INSTRUCTION" }
  ]
}
```

### Organization (site-wide)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "ORG_NAME",
  "url": "ORG_URL",
  "logo": "ORG_LOGO_URL",
  "sameAs": ["SOCIAL_PROFILE_URL_1", "SOCIAL_PROFILE_URL_2"]
}
```

Validate output with Google's Rich Results Test or the schema.org validator before shipping.

## llms.txt

A plain-text file at the site root (`/llms.txt`) that points AI crawlers to your key content. Use
Markdown. An optional `/llms-full.txt` inlines the full text of those pages.

```markdown
# ORG_NAME

> ONE_OR_TWO_SENTENCE_DESCRIPTION_OF_THE_SITE_AND_WHO_IT_SERVES.

## Core pages

- [PAGE_TITLE](FULL_URL): one-line description of what this page answers.
- [PAGE_TITLE](FULL_URL): one-line description.

## Docs

- [DOC_TITLE](FULL_URL): one-line description.

## Optional

- [SECONDARY_PAGE_TITLE](FULL_URL): one-line description.
```

Keep entries to the pages you actually want cited, each with a description that states the question
the page answers.

## Semantic structure & metadata checklist

- [ ] Exactly one `<h1>`, then a logical `<h2>`/`<h3>` hierarchy (no skipped levels).
- [ ] Headings phrased as the questions from the Phase 1 query cluster.
- [ ] Descriptive `<title>` (under ~60 chars) and meta description (under ~155 chars).
- [ ] Canonical URL set.
- [ ] On-page FAQ block whose questions/answers match the `FAQPage` JSON-LD exactly.
- [ ] Lists and comparison tables used for enumerable or comparative content.
- [ ] Visible author byline and "Last updated: YYYY-MM-DD".
- [ ] Primary sources linked inline next to the claims they support.
- [ ] Valid JSON-LD for the types that match on-page content, validated before shipping.
- [ ] `llms.txt` present at the site root and listing the pages you want cited.
