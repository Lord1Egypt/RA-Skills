---
name: ad-library-scraper
description: Search public ad libraries through ToolRouter's MCP server - Meta (Facebook and Instagram) Ad Library, Google Ads Transparency Center, LinkedIn, TikTok and Reddit ads. Use when the user wants to see a competitor's running ads, ad copy and creative, how long ads have run, which platforms they run on, or video ad transcripts.
metadata: {"homepage":"https://toolrouter.com/tools/ad-library-search","openclaw":{"emoji":"📣","requires":{"bins":[],"env":[]}}}
---

# Ad Library Scraper

Read the public ad libraries that Meta, Google, LinkedIn, TikTok and Reddit publish, from one MCP connection. Returns ad copy, creative URLs, start dates, platforms and, where the library publishes it, reach and spend.

## Installation

Install with `pnpm dlx skills add Humanleap/agent-skills --skill ad-library-scraper`. Connect the client's remote MCP server to `https://api.toolrouter.com/mcp` (Claude: Customize → Connectors → Add custom connector; Claude Code: `claude mcp add toolrouter -- npx -y toolrouter-mcp`). Setup: https://toolrouter.com/docs/markdown/quickstart.

## Hard Rules

1. **Resolve the advertiser first.** Keyword search matches any ad that contains the word. To see one company's ads, look up its page or advertiser ID, then fetch that company's ads.
2. **Use the exact operation.** Pick the `tool` and `skill` below, or call `discover`. Never invent an input field.
3. **State the window.** Say which country, status and date range the results cover.
4. **No guessing at spend.** Only report spend or reach when the library returns it.

## Authentication and Cost

The server provisions an anonymous account on first use. Paid calls need credits: if `use_tool` returns a claim link, give it to the user so they can sign in and add credits. Most ad library calls cost $0.005; `discover` shows the live price. `get_google_company_ads` with `get_ad_details: true` costs more per ad, so leave it off until the user needs full detail.

## Core Workflow

1. **Find the advertiser.** Meta: `search_facebook_ad_companies` → `page_id`. Google: `search_google_advertisers` → `advertiser_id`, or pass the `domain`.
2. **Pull their ads.** `get_facebook_company_ads` with `page_id`, `country`, `status:"ACTIVE"` and `trim:true`. `get_google_company_ads` with `domain` or `advertiser_id`.
3. **Open the winners.** `get_facebook_ad` with `get_transcript:true` for a video ad's script; `get_google_ad` for one Google creative.
4. **Summarise.** Table of start date, days running, platforms, format, hook (first line) and call to action. Long-running ads are the ones the advertiser keeps paying for.

## Essential Operations

All `tool: "ad-library-search"`.

| Job | `skill` | Input |
|---|---|---|
| Find a brand's Meta page ID | `search_facebook_ad_companies` | `{"query":"Notion"}` |
| A brand's active Meta ads in one country | `get_facebook_company_ads` | `{"page_id":"825120160874613","country":"GB","status":"ACTIVE","trim":true}` |
| Meta ads mentioning a keyword | `search_facebook_ads` | `{"query":"protein bar","country":"US","search_type":"keyword_exact_phrase","trim":true}` |
| One Meta ad, with video transcript | `get_facebook_ad` | `{"url":"https://www.facebook.com/ads/library/?id=123","get_transcript":true}` |
| Find a Google advertiser | `search_google_advertisers` | `{"query":"Shopify"}` |
| A domain's Google ads | `get_google_company_ads` | `{"domain":"shopify.com","region":"US"}` |
| One Google ad (text via OCR) | `get_google_ad` | `{"url":"https://adstransparency.google.com/advertiser/AR.../creative/CR..."}` |
| LinkedIn ads by company | `search_linkedin_ads` | `{"company":"Salesforce"}` |
| TikTok ads by advertiser | `search_tiktok_ads` | `{"advertiser_name":"Duolingo"}` |
| One TikTok ad (hook, landing page, video) | `get_tiktok_ad` | `{"ad_id":"<id or library.tiktok.com URL>"}` |
| Reddit promoted posts | `search_reddit_ads` | `{"query":"project management"}` |

Call these through `use_tool` with `tool`, `skill` and `input`.

## Common Patterns

- **Competitor ad teardown:** resolve 3 competitors' Meta page IDs, pull active ads in the user's market, sort by start date, and compare hooks, offers and formats.
- **Creative brief:** take the 5 longest-running ads, pull transcripts for the video ones, and list the hooks, proof points and calls to action that repeat.
- **Channel mix check:** run the same brand through Meta, Google, LinkedIn and TikTok to see where it actually advertises.
- **Landing page follow-through:** pass an ad's landing URL to `web-scraper/scrape_page` to read the offer behind the ad.
- **Organic vs paid:** pair with the `social-media-scraper` skill to compare what a brand promotes with what it posts.

## Gotchas

- `search_facebook_ads` is a keyword search across all advertisers: "notion" also matches unrelated ads that use the word. Resolve the page ID for brand research.
- Several pages can share a brand name. Pick the one with the matching Instagram handle, follower count or page alias.
- Meta results default to active ads; set `status:"ALL"` for history. Use `trim:true` to keep responses small, and `cursor` to page.
- An empty Google result for a domain can mean the advertiser is registered under another name. Try `search_google_advertisers`.
- Pass `query` or `advertiser_name` to `search_tiktok_ads`, not both.

## Quick Reference

**Connect → resolve page/advertiser ID → company ads (country, active, trim) → open top ads → table of hooks, dates and platforms.**

More: https://toolrouter.com/tools/ad-library-search
