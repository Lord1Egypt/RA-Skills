# geo-fix-schema

Analyze a website's structured data and generate ready-to-use JSON-LD schema markup for AI discoverability.

## What it does

1. **Audits** existing structured data (JSON-LD, Microdata, RDFa)
2. **Scores** current schema coverage against GEO audit rubric (0-100)
3. **Explains** why each missing schema matters for AI visibility
4. **Generates** copy-paste-ready JSON-LD with real data extracted from the site
5. **Estimates** score improvement after applying fixes

## Usage

```bash
# Analyze and generate missing schemas
"Fix the schema markup for https://example.com"

# Claude Code slash command
/geo-fix-schema https://example.com
```

## Output

| File | Purpose |
|------|---------|
| `schema-{domain}.json` | All generated JSON-LD blocks with installation comments |

The summary includes a before/after score comparison and explains each schema's impact on AI visibility.

## Supported Schema Types

| Category | Types |
|----------|-------|
| Core Identity | Organization, LocalBusiness, WebSite, SearchAction |
| Content | Article, BlogPosting, Person |
| AI-Boost | FAQPage, HowTo, BreadcrumbList, Product |

## Installation

```bash
npx skills add Cognitic-Labs/geoskills --skill geo-fix-schema
```
