# llms.txt Specification Reference

Source: [llmstxt.org](https://llmstxt.org/)

## Overview

llms.txt is a proposed standard for providing structured website information to LLMs at inference time. The file uses Markdown format (not XML/JSON) because it is designed to be read directly by language models.

## File Locations

- Primary: `https://{domain}/llms.txt`
- Alternative: `https://{domain}/.well-known/llms.txt`
- Section-specific: `https://{domain}/{section}/llms.txt`

## Required Structure

The file MUST contain sections in this order:

### 1. H1 Heading (REQUIRED)
The name of the project or site. This is the only mandatory element.

```markdown
# Project Name
```

### 2. Blockquote Summary (RECOMMENDED)
A short summary containing key information necessary for understanding the rest of the file.

```markdown
> Project Name is a platform that does X for Y audience. It provides A, B, and C capabilities.
```

### 3. Body Content (OPTIONAL)
Zero or more markdown sections of any type **except headings**, containing more detailed information.

```markdown
The platform supports 50+ integrations and serves 10,000+ customers worldwide.
```

### 4. H2 Sections with File Lists (OPTIONAL)
Grouped links to detailed resources. Each entry uses this format:

```markdown
## Section Name
- [Link Title](URL): Optional description of the content
- [Another Link](URL): What this page covers
```

## Special Sections

### `## Optional`
Content in a section titled "Optional" signals that it can be skipped if a shorter context is needed. Use for supplementary content like legal pages, old blog posts, or secondary documentation.

## Companion Files

### llms-full.txt
An expanded version that includes the actual content of key pages, pre-formatted for LLM consumption. While llms.txt contains links and summaries, llms-full.txt embeds the full text.

### Markdown Page Versions
Sites should ideally provide clean markdown versions of pages by appending `.md` to URLs (e.g., `/docs/api` → `/docs/api.md`).

## Format Rules

- Pure Markdown only (no HTML)
- No headings deeper than H2 in the link sections
- Links must be absolute URLs
- Descriptions after links are separated by a colon and space
- File should be UTF-8 encoded
- No images (they don't help LLMs)

## Example

```markdown
# Acme Corp

> Acme Corp is a B2B SaaS platform for supply chain management. It helps manufacturers track inventory, optimize logistics, and reduce waste across 50+ countries.

Acme integrates with major ERP systems including SAP, Oracle, and NetSuite. The platform processes over 2 million transactions daily.

## Docs
- [Getting Started](https://acme.com/docs/start): Quick setup guide for new users
- [API Reference](https://acme.com/docs/api): REST API endpoints and authentication
- [Integrations](https://acme.com/docs/integrations): Supported ERP and logistics platforms

## Products
- [Inventory Tracker](https://acme.com/products/inventory): Real-time inventory management across warehouses
- [Route Optimizer](https://acme.com/products/routes): AI-powered logistics route planning

## Blog
- [2024 Supply Chain Trends](https://acme.com/blog/2024-trends): Annual industry analysis with survey data
- [Reducing Waste with AI](https://acme.com/blog/ai-waste): Case study showing 34% waste reduction

## About
- [Company](https://acme.com/about): Founded 2018, 500+ employees, Series C funded
- [Customers](https://acme.com/customers): Case studies from Fortune 500 manufacturers

## Optional
- [Privacy Policy](https://acme.com/privacy): Data handling and GDPR compliance
- [Terms of Service](https://acme.com/terms): Usage terms and SLA guarantees
```

## Adoption Status (2026)

- ~10% adoption rate across top 300K domains (SE Ranking survey)
- Supported by Cloudflare, Vercel, Netlify deployment guides
- Claude documentation references llms.txt as endorsed standard
- Not officially consumed by OpenAI, Google, or Anthropic crawlers yet
- Growing adoption in developer documentation and SaaS sites
