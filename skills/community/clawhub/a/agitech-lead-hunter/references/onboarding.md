# Lead Hunter - Onboarding Interview

When `config.json` has `"configured": false`, run this interview to set up the skill.

## Interview Flow

Ask these questions one at a time. Use natural conversation, not a rigid form.

### 1. About Your Company
- "What does your company do? Give me the one-liner."
- "What's your main offering? (services, SaaS product, consulting, recruiting, etc.)"
- "What's your value proposition - why would a prospect pick you over alternatives?"

→ Saves to `config.company`

### 2. Ideal Customer Profile
- "What size companies are you targeting? (pre-revenue, seed-stage, Series A, enterprise, etc.)"
- "What team size is your sweet spot? (1-10, 10-50, 50-200, 200+)"
- "Any specific industries or verticals? (fintech, healthtech, SaaS, e-commerce, etc.)"
- "What geographies? (US, UK, EU, APAC, global, specific countries)"
- "What signals tell you someone needs what you offer?" (Examples: just raised funding, no CTO, hiring engineers, launching new product)

→ Saves to `config.ideal_customer`

### 3. Lead Sources
Based on the industry, suggest sources from `references/sources.md`. Then ask:
- "Here are the best sources for [industry] leads: [list]. Want to use all of these or pick specific ones?"
- "Any other sources you already follow for leads? (newsletters, sites, Twitter accounts)"

→ Saves to `config.sources`

### 4. Output Destination
- "Where should I put the leads? Options:"
  - **Asana** - creates subtasks under a parent task (needs workspace ID + parent task ID)
  - **Markdown** - writes to `leads/YYYY-MM-DD.md` files
  - **CSV** - appends to `leads/leads.csv`
  - **All of the above**
- If Asana: "What's your Asana workspace ID and parent task ID for leads?"

→ Saves to `config.output`

### 5. Outreach Style
- "How do you usually reach out? (LinkedIn DM, email, Twitter DM, cold call)"
- "What tone works for your industry? (casual, professional, technical, founder-to-founder)"
- "Any specific things to always mention or never mention?"

→ Saves to `config.outreach`

### 6. Filters
- "Any industries to always skip? (e.g., crypto, biotech, hardware)"
- "Minimum funding amount to care about?"
- "Maximum funding amount? (too big = probably not your customer)"

→ Saves to `config.filters`

### 7. Schedule
- "How often should I hunt? (daily, weekdays only, twice a week)"
- "What time? (e.g., 6:30 AM your timezone)"

→ If the user wants a cron, offer to set one up automatically.

## After Onboarding

1. Write the complete `config.json` with all answers
2. Set `"configured": true`
3. Initialize `scripts/seen.json` as empty array `[]`
4. Create `leads/` directory if output type needs it
5. Run the first hunt immediately to validate everything works
6. If cron requested, create the cron job

## Config Schema

```json
{
  "configured": true,
  "company": {
    "name": "string",
    "offering": "string (services|saas|consulting|recruiting|other)",
    "one_liner": "string",
    "value_prop": "string"
  },
  "ideal_customer": {
    "stages": ["pre-seed", "seed"],
    "team_size": { "min": 1, "max": 50 },
    "industries": ["fintech", "saas", "ai"],
    "geographies": ["US", "UK", "Singapore"],
    "signals": ["no CTO", "hiring engineers", "early product"]
  },
  "sources": [
    {
      "name": "finsmes",
      "url": "https://finsmes.com",
      "type": "funding_news",
      "search_fallback": "site:finsmes.com"
    }
  ],
  "output": {
    "type": "asana|markdown|csv|all",
    "asana_workspace": "string (optional)",
    "asana_parent_task": "string (optional)",
    "leads_dir": "leads/"
  },
  "outreach": {
    "channel": "linkedin_dm|email|twitter_dm",
    "tone": "casual|professional|technical|founder",
    "template": "Hi {first_name}, congrats on the {round} raise! ...",
    "always_mention": [],
    "never_mention": []
  },
  "filters": {
    "skip_industries": ["biotech", "hardware"],
    "min_funding": 500000,
    "max_funding": 15000000,
    "max_leads_per_run": 5
  },
  "schedule": {
    "frequency": "daily|weekdays|twice_weekly",
    "time": "06:30",
    "timezone": "Asia/Kuala_Lumpur"
  }
}
```
