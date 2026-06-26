---
name: dataforseo-reporting
description: Run SEO, SERP, keyword, and search intelligence workflows with DataForSEO — powered by ClawLink.
---

# DataForSEO

![DataForSEO](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/dataforseo.svg)

Work with DataForSEO from chat — run SEO, SERP, keyword, and search intelligence workflows.

Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=dataforseo-reporting), an integration hub for OpenClaw that handles hosted connection flows and credentials so you don't need to configure DataForSEO API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect DataForSEO |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect DataForSEO |

## Connection flow

```
User → ClawLink → DataForSEO account
         ↓
    OpenClaw tools
    (via ClawLink)
```

**Step 1** — Install the ClawLink plugin:
```
openclaw plugins install clawhub:clawlink-plugin
```
Start a fresh chat after installing.

**Step 2** — Pair ClawLink:
1. Call `clawlink_begin_pairing`
2. Open the returned URL in your browser
3. Sign in to ClawLink and approve the device

**Step 3** — Connect DataForSEO:
Open [claw-link.dev/dashboard?add=dataforseo](https://claw-link.dev/dashboard?add=dataforseo), complete the connection flow, then confirm.

*App-specific connection GIF coming soon*

**Step 4** — Verify and discover:
```javascript
// 1. Verify DataForSEO is connected
clawlink_list_integrations()

// 2. List available tools
clawlink_list_tools({ integration: "dataforseo" })

// 3. Search tools if needed
clawlink_search_tools({ query: "keyword", integration: "dataforseo" })
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw (you)                       │
├─────────────────────────────────────────────────────────┤
│  ClawLink Plugin  →  clawlink_* tools                   │
├─────────────────────────────────────────────────────────┤
│                    ClawLink Cloud                       │
│         (credentials, connection state, routing)        │
├─────────────────────────────────────────────────────────┤
│           DataForSEO API (user's account)               │
└─────────────────────────────────────────────────────────┘
```

## Tool reference

DataForSEO uses an async task model — most `create_*` tools return a task ID, and `get_*` tools retrieve results by task ID.

### Tasks (create → get retrieval model)

| Tool | Description | Risk |
|------|-------------|------|
| `dataforseo_create_app_data_apple_app_reviews_task` | Create Apple App Store reviews retrieval task | confirm |
| `dataforseo_create_app_data_apple_app_searches_task` | Create Apple App Store search task (up to 100 per request) | confirm |
| `dataforseo_create_app_data_google_app_list_task` | Create Google Play top charts app list task | confirm |
| `dataforseo_create_app_data_google_app_reviews_task` | Create Google Play app reviews retrieval task | confirm |
| `dataforseo_create_business_data_trustpilot_search_task` | Create Trustpilot business profile search task | confirm |
| `dataforseo_create_keywords_data_google_trends_explore_task` | Create Google Trends Explore task | confirm |
| `dataforseo_create_kw_bing_audience_est_task` | Create Bing audience estimation task for ad planning | confirm |
| `dataforseo_create_kw_google_kw_for_kw_task` | Create keyword research task with search volume/CPC | confirm |
| `dataforseo_create_merchant_amazon_sellers_task` | Get Amazon sellers for a product | confirm |
| `dataforseo_create_on_page_lighthouse_task_post` | Create Lighthouse audit task for page quality | confirm |
| `dataforseo_create_on_page_task_post` | Create on-page SEO crawl task (60+ parameters) | confirm |
| `dataforseo_create_serp_google_autocomplete_task` | Create Google Autocomplete SERP task | confirm |
| `dataforseo_create_serp_google_events_task` | Create Google Events SERP task (English only) | confirm |
| `dataforseo_create_serp_google_finance_explore_task` | Create Google Finance Explore task | confirm |
| `dataforseo_create_serp_google_local_finder_task` | Create Google Local Finder SERP task | confirm |
| `dataforseo_create_serp_google_maps_task` | Create Google Maps SERP task | confirm |
| `dataforseo_create_serp_google_organic_task_post` | Create Google organic SERP task with featured snippets | confirm |
| `dataforseo_create_serp_seznam_organic_task` | Create Seznam (Czech) organic SERP task | confirm |
| `dataforseo_create_serp_youtube_video_comments_task` | Create YouTube video comments retrieval task | confirm |
| `dataforseo_create_serp_youtube_video_subtitles_task` | Create YouTube video subtitles extraction task | confirm |
| `dataforseo_force_on_page_crawl` | Force-stop ongoing website crawl | high_impact |

### Results retrieval

| Tool | Description | Risk |
|------|-------------|------|
| `dataforseo_get_ai_keyword_data_available_filters` | Discover filterable fields for AI keyword queries | safe |
| `dataforseo_get_ai_keyword_data_locations_and_languages` | Get supported locations/languages for AI keyword API | safe |
| `dataforseo_get_ai_opt_chat_gpt_llm_scraper_html_by_id` | Get ChatGPT LLM scraper results in HTML (task ID valid 7 days) | safe |
| `dataforseo_get_ai_opt_chat_gpt_llm_scraper_task_adv_by_id` | Get advanced ChatGPT LLM scraper results with markdown/sources | safe |
| `dataforseo_get_ai_opt_gemini_llm_scraper_task_adv` | Get Gemini LLM scraper results (results valid 30 days) | safe |
| `dataforseo_get_ai_optimization_chat_gpt_llm_responses_live` | Get live ChatGPT responses with optional web search | safe |
| `dataforseo_get_ai_optimization_gemini_llm_scraper_html_by_id` | Get Gemini scraper HTML results (valid 7 days) | safe |
| `dataforseo_get_ai_optimization_llm_mentions_top_domains_live` | Get top domains mentioned by LLMs for keywords | safe |
| `dataforseo_get_app_data_apple_app_list_task_advanced` | Get Apple App Store app list results by task ID | safe |
| `dataforseo_get_app_data_apple_app_searches_task_advanced` | Get Apple App Search results by task ID | safe |
| `dataforseo_get_app_data_google_app_info_task_html_by_id` | Get Google Play app HTML (valid 7 days) | safe |
| `dataforseo_get_app_data_google_app_list_task_advanced_by_id` | Get Google Play app list results by task ID | safe |
| `dataforseo_get_app_data_google_app_reviews_task_html` | Get Google Play reviews HTML (valid 7 days) | safe |
| `dataforseo_get_app_data_google_app_searches_task_html_by_id` | Get Google Play search HTML by task ID | safe |
| `dataforseo_get_app_google_app_reviews_task_get_adv_by_id` | Get Google Play review details by task ID | safe |
| `dataforseo_get_app_google_app_searches_task_adv_by_id` | Get Google Play search results by task ID | safe |
| `dataforseo_get_apple_app_info_task_advanced` | Get advanced Apple App Info results by task ID | safe |
| `dataforseo_get_backlinks_bulk_pages_summary_live` | Get backlinks summary for up to 1000 targets at once | safe |
| `dataforseo_get_backlinks_bulk_spam_score_live` | Get spam scores for multiple domains | safe |
| `dataforseo_get_backlinks_summary_live` | Get comprehensive backlinks overview for a domain | safe |
| `dataforseo_get_bing_kw_performance_locations_and_languages` | Get supported Bing keyword locations/languages | safe |
| `dataforseo_get_biz_business_listings_available_filters` | Discover filterable fields for business listings | safe |
| `dataforseo_get_biz_google_hotel_info_task_get_adv_by_id` | Get Google Hotel Info by task ID | safe |
| `dataforseo_get_biz_google_hotel_searches_task_by_id` | Get Google Hotel search results (valid 30 days) | safe |
| `dataforseo_get_biz_google_my_business_updates_task_by_id` | Get Google My Business updates (valid 30 days) | safe |
| `dataforseo_get_biz_google_questions_and_answers_task` | Get Google Business Q&A by task ID | safe |
| `dataforseo_get_business_data_google_extended_reviews_task` | Get extended Google Business reviews by task ID | safe |
| `dataforseo_get_business_data_google_my_business_info_task` | Get Google My Business info by task ID | safe |
| `dataforseo_get_business_data_google_reviews_task` | Get Google Business reviews by task ID | safe |
| `dataforseo_get_business_data_tripadvisor_reviews_task_by_id` | Get TripAdvisor reviews by task ID | safe |
| `dataforseo_get_business_data_tripadvisor_search_task_by_id` | Get TripAdvisor business search results by task ID | safe |
| `dataforseo_get_business_data_trustpilot_search_task_by_id` | Get Trustpilot search results by task ID | safe |
| `dataforseo_get_chat_gpt_llm_scraper_locations_by_country` | Get valid locations for ChatGPT LLM scraper tasks | safe |
| `dataforseo_get_dataforseo_labs_available_filters` | Discover filterable fields for Labs API | safe |
| `dataforseo_get_dataforseo_labs_bing_related_keywords_live` | Get Bing related keywords (up to 4680 ideas) | safe |
| `dataforseo_get_dataforseo_labs_google_available_history` | Get available historical dates for Labs domain metrics | safe |
| `dataforseo_get_dataforseo_labs_google_top_searches_live` | Get top Google search keywords with trends | safe |
| `dataforseo_get_dataforseo_labs_status` | Get last update dates for Labs data sources | safe |
| `dataforseo_get_dataforseo_trends_locations_by_country` | Get valid locations for DataForSEO Trends tasks | safe |
| `dataforseo_get_domain_analytics_tech_technology_stats_live` | Get historical technology adoption statistics | safe |
| `dataforseo_get_gemini_llm_responses_task_by_id` | Get Gemini LLM responses by task ID (valid 30 days) | safe |
| `dataforseo_get_google_hist_bulk_traffic_est_live` | Get historical monthly traffic for up to 1000 domains | safe |
| `dataforseo_get_keywords_data_bing_keywords_for_site_task` | Get Bing keywords for a site by task ID | safe |
| `dataforseo_get_keywords_data_bing_search_volume_task_by_id` | Get Bing search volume by task ID (valid 30 days) | safe |
| `dataforseo_get_keywords_data_google_ads_status` | Check Google Ads keyword data update status | safe |
| `dataforseo_get_keywords_data_google_search_volume_task_by_id` | Get Google search volume by task ID | safe |
| `dataforseo_get_kw_bing_audience_est_industries` | Get 147 Bing audience estimation industry IDs | safe |
| `dataforseo_get_kw_bing_kw_for_kw_task_by_id` | Get Bing keyword suggestions by task ID (up to 3000) | safe |
| `dataforseo_get_kw_bing_kw_suggestions_for_url_live` | Get Bing keyword suggestions for a URL (live) | safe |
| `dataforseo_get_kw_bing_kw_suggestions_for_url_task` | Get Bing keyword suggestions for URL (task-based, 30 days) | safe |
| `dataforseo_get_kw_google_ads_ad_traffic_by_kw_task_by_id` | Get Google Ads ad traffic forecasts by task ID | safe |
| `dataforseo_get_kw_google_ads_kw_for_kw_live` | Get Google Ads keyword suggestions (live) | safe |
| `dataforseo_get_kw_google_ads_kw_for_kw_task_by_id` | Get Google Ads keywords by task ID | safe |
| `dataforseo_get_kw_google_ads_kw_for_site_task` | Get Google Ads keywords for a site by task ID | safe |
| `dataforseo_get_kw_google_ads_search_vol_task_by_id` | Get Google Ads search volume by task ID | safe |
| `dataforseo_get_kw_google_kw_for_category_live` | Get Google keywords for a product category (up to 700) | safe |
| `dataforseo_get_kw_google_kw_for_kw_task_by_id` | Get Google keyword suggestions by task ID | safe |
| `dataforseo_get_kw_google_trends_explore_task_by_id` | Get Google Trends explore results by task ID | safe |
| `dataforseo_get_kw_google_trends_locations_by_country` | Get valid Google Trends locations | safe |
| `dataforseo_get_llm_mentions_available_filters` | Discover filterable fields for LLM mentions API | safe |

### Appendix (always-on utilities)

| Tool | Description | Risk |
|------|-------------|------|
| `dataforseo_get_appendix_errors` | Get complete API error codes and HTTP status codes | safe |
| `dataforseo_get_appendix_status` | Get current operational status of all APIs | safe |
| `dataforseo_get_appendix_user_data` | Get account balance, rate limits, spending, pricing | safe |

## Code examples

### Example 1: Run keyword research

```javascript
// Create a Google keyword research task
const task = await clawlink_call_tool({
  tool: "dataforseo_create_kw_google_kw_for_kw_task",
  parameters: {
    keywords: ["content marketing", "SEO strategy"],
    location_name: "United States",
    language_name: "English"
  }
});

// Retrieve results (after async processing)
const results = await clawlink_call_tool({
  tool: "dataforseo_get_kw_google_kw_for_kw_task_by_id",
  parameters: { task_id: task.id }
});
```

### Example 2: Run a SERP task

```javascript
// Create a Google organic SERP task
const serpTask = await clawlink_call_tool({
  tool: "dataforseo_create_serp_google_organic_task_post",
  parameters: {
    keyword: "best CRM software 2024",
    location_name: "United States",
    language_name: "English"
  }
});

// Get results
const serpResults = await clawlink_call_tool({
  tool: "dataforseo_get_keywords_data_google_search_volume_task_by_id",
  parameters: { task_id: serpTask.id }
});
```

### Example 3: Analyze backlinks

```javascript
// Get backlinks summary for a domain
const backlinks = await clawlink_call_tool({
  tool: "dataforseo_get_backlinks_summary_live",
  parameters: {
    target: "example.com"
  }
});

// Get spam scores
const spamScores = await clawlink_call_tool({
  tool: "dataforseo_get_backlinks_bulk_spam_score_live",
  parameters: {
    targets: ["example.com", "competitor.com"]
  }
});
```

### Example 4: AI Optimization queries

```javascript
// Get top domains mentioned by LLMs for a keyword
const llmMentions = await clawlink_call_tool({
  tool: "dataforseo_get_ai_optimization_llm_mentions_top_domains_live",
  parameters: {
    keyword: "project management software"
  }
});

// Get live ChatGPT response with web search
const chatGptResponse = await clawlink_call_tool({
  tool: "dataforseo_get_ai_optimization_chat_gpt_llm_responses_live",
  parameters: {
    prompt: "What are the top 10 project management tools?",
    temperature: 0.7
  }
});
```

## Error handling

| Error pattern | Likely cause | Resolution |
|---------------|--------------|------------|
| `Task not ready` | Async task still processing | Wait and retry with same task ID |
| `Task expired` | Task older than 30 days | Create a new task |
| `Invalid location` | Unsupported country/location | Use `dataforseo_get_dataforseo_trends_locations_by_country` to find valid codes |
| `Rate limit exceeded` | Too many requests | Check `dataforseo_get_appendix_user_data` for rate limits; slow down requests |
| `Insufficient balance` | Out of DataForSEO credits | User needs to add funds to their DataForSEO account |

## Security & Permissions

- ClawLink stores only the API credentials, never raw keys in plaintext
- Device credentials are stored locally in OpenClaw plugin config
- Some tasks (e.g., large crawls) can consume significant credits — always confirm before running large jobs

## Troubleshooting

**Task results not available:**
- Tasks are async — results may take minutes to be ready
- Check task status by calling the appropriate `get_*` tool with the task ID
- Task results expire after 30 days for most task types

**Empty results from keyword tools:**
- Verify the keyword and location are valid
- Some very niche keywords may have no data
- Check `dataforseo_get_appendix_status` to verify the API is operational

**Credit consumption higher than expected:**
- Use `dataforseo_get_appendix_user_data` to check current balance
- On-page crawls and bulk backlink queries consume credits
- Use narrow filters and specific targets to minimize credit usage

---

Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=dataforseo-reporting) — your OpenClaw integration hub for DataForSEO.