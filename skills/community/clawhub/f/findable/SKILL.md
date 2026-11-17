---
name: findable
description: "Public website audits and sourced SEO/AEO content drafts, ready for your review. Use it for website seo/aeo audit through Findable's MCP server."
---

# Findable

Public website audits and sourced SEO/AEO content drafts, ready for your review.

## Connect

Add Findable's MCP server: https://thefindable.co/mcp (Streamable HTTP, no sign-in).

## Offers

### Website SEO/AEO audit

Create a stored SEO/AEO audit of a public business website without an account or data connection. Accepts optional dated provider reports. Reads the homepage, up to four internal pages, robots.txt, sitemap.xml and up to five relevant competitor websites discovered from public market research or supplied by the client. Samples three unbranded customer questions about the category, a task and a problem through live OpenAI API web searches when available. Newly audited competitors use the same questions and source-check rubric. Recent public research may be reused with its original dates; private client data is excluded from that cache. Reports include sourced public business contacts for manual review; the service does not draft or send outreach. Returns an audit ID for retrieving progress and the completed report. Reports include sourced findings, exact target URLs, up to three priorities, relevant content drafts, expected impact, realistic review points and measurement steps. The service cannot access other MCP connections, infer private metrics or edit websites.

1. Call `start_audit`. It returns an id.
2. Call `check_audit` with the id until it is ready; it usually takes several minutes.
3. Give the person the result and its link.
