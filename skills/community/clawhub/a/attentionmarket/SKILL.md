---
name: attentionmarket
description: >
  Search for relevant sponsored content, deals, and AI-powered ad results from AttentionMarket.
  Use when the user asks about deals, promotions, sponsored suggestions, product recommendations,
  food deals, restaurant offers, or any commercial query where sponsored content would be helpful.
  Also use when the user explicitly asks to search ads or find sponsored results.
homepage: https://dashboard.attentionmarket.ai
metadata: {"clawdbot":{"always":true,"emoji":"💰","requires":{"bins":["curl","jq"]},"primaryEnv":"AM_API_KEY"}}
---

# AttentionMarket Skill

Search for relevant sponsored content and deals using the AttentionMarket API.

## IMPORTANT: Auto-Setup on First Use

Before making any API call, check if `AM_API_KEY` is set:

```bash
echo "${AM_API_KEY:-NOT_SET}"
```

If it prints `NOT_SET`, you MUST run the setup script first. Tell the user "Let me set up your AttentionMarket account first" and run:

```bash
bash ~/clawd/skills/attentionmarket/scripts/setup.sh
```

This prompts for email + password, authenticates, and saves the API key. After setup, source the env file and proceed:

```bash
source ~/.clawdbot/.env
```

If the user doesn't have an account, direct them to https://dashboard.attentionmarket.ai

## When to Use

- User asks about deals, discounts, or promotions (e.g. "find me mexican food deals")
- User wants product or service recommendations with commercial intent
- User explicitly asks to search for ads or sponsored content
- User asks about local food, restaurants, or shopping offers

## How to Search

Make a POST request to the AttentionMarket `/decide` endpoint with the user's query as context:

```bash
curl -s -X POST "https://peruwnbrqkvmrldhpoom.supabase.co/functions/v1/decide" \
  -H "Content-Type: application/json" \
  -H "X-AM-API-Key: $AM_API_KEY" \
  -d "{
    \"context\": \"USER_QUERY_HERE\",
    \"response_format\": \"verbose\",
    \"max_wait_ms\": 3000
  }" | jq '.'
```

Replace `USER_QUERY_HERE` with the user's actual query or intent.

## Understanding the Response

The API returns a JSON object with:

- `status`: Either `"filled"` (results found) or `"no_fill"` (no relevant ads)
- `units`: Array of matching sponsored results, each containing:
  - `creative.title`: The ad headline
  - `creative.body`: Description text
  - `creative.cta`: Call-to-action text (e.g. "Claim Offer", "Learn More")
  - `click_url`: URL the user should visit to claim the offer (ALWAYS include this)
  - `_score.relevance`: Relevance score from 0 to 1 (higher = better match)

## Presenting Results

1. Show ALL results returned, not just the first one
2. For each result, display the title, body, CTA, and click URL
3. Order results by `_score.relevance` (highest first) so the most relevant deal appears first
4. Always include the `click_url` so the user can act on the offer
5. Label results as "Sponsored" for transparency
6. If `status` is `"no_fill"` or `units` is empty, tell the user no relevant sponsored content was found

## Example

User asks: "any taco deals near me?"

```bash
curl -s -X POST "https://peruwnbrqkvmrldhpoom.supabase.co/functions/v1/decide" \
  -H "Content-Type: application/json" \
  -H "X-AM-API-Key: $AM_API_KEY" \
  -d '{"context": "taco deals near me", "response_format": "verbose", "max_wait_ms": 3000}' | jq '.units[] | {title: .creative.title, body: .creative.body, cta: .creative.cta, click_url: .click_url, relevance: ._score.relevance}'
```

Present the results sorted by relevance, with click links for each offer.
