---
name: courtlistener-research
description: Researches public US legal opinions, courts, and judicial people through CourtListener via the Crawlora API, returning clean JSON. Use when the user wants to search opinions, browse courts, or look up public judge/person records without scraping CourtListener pages.
---

# CourtListener research

Search CourtListener's public opinion index and browse its court and judicial
person directories as normalized JSON.

## When to use this skill

- Search public opinions by text.
- Discover courts and retrieve one court record.
- Browse or look up public judicial-person records.
- Build an initial legal-research shortlist before opening primary documents.

## Setup

- Get a Crawlora API key at [crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`.

## How it works

Use `/courtlistener/search` for opinion text search, `/courtlistener/courts`
for court discovery/detail, and `/courtlistener/people` for public judicial
person records. Treat results as research leads and verify legal conclusions
against the underlying opinion and applicable jurisdiction.

Full endpoint list: [`reference/endpoints.md`](reference/endpoints.md).
