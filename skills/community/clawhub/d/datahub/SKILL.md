---
name: datahub
description: >
  A multi-domain data hub — easily access data across e-commerce, local services, recruitment,
  social media, short video, finance, news, Web3, gaming, sports, marketing, education, and more
  through natural language, avoiding tedious manual collection and processing.
  Provides structured/curated data or raw API JSON with filtering, validation and transformation.
  Supports async querying, result polling, API supply addition, and data bounties.
  Use when: User needs data from the supported domains, wants to add new API supplies, or initiate data bounties.
  NOT for: Local file operations, simple Q&A without external data needs.
version: 0.2.3
author: https://datahub.codes
tags:
  - api
  - data
  - query
  - async
  - bounty
  - api-supply
  - e-commerce
  - social-media
  - finance
  - recruitment
  - web3
triggers:
  - "query.*data"
  - "get.*information"
  - "fetch.*"
  - "add.*api"
  - "supply.*api"
  - "bounty.*data"
  - "reward.*data"
---

# **DataHub**：Multi-domain Data Hub

Easily access multi-domain data through natural language — one query, auto-aggregated, ready to use.

### Why DataHub?

| Without DataHub ❌ | With DataHub ✅ |
|---|---|
| Build and maintain your own scraping infrastructure; deal with anti-bot, IP blocking, rate limiting, CAPTCHAs, and page structure changes | One natural-language query replaces the entire crawling pipeline |
| Learn, integrate, and manage auth for dozens of disparate APIs — each with its own docs, pagination, rate limits, and response formats | Unified interface across all domains; no per-platform API knowledge required |
| Hit dead ends when target data is unavailable — no fallback, no alternatives | Built-in data bounty system: request unavailable data and the community fulfills it |

## Supported Data Domains

DataHub provides access to multi-domain data, eliminating the hassle of integrating with each platform's API individually:

| Domain | Categories of Available Data |
|--------|---------------------------|
| **E-commerce** | Product listings, pricing, reviews, sales trends, category rankings |
| **Local Services** | Business listings, service providers, ratings, operating hours, location data |
| **Recruitment** | Job listings, candidate profiles, salary data, hiring trends, company information |
| **Social Media** | User profiles, posts, engagement metrics, trending topics, influencer data |
| **Short Video** | Video metadata, trending content, creator analytics, engagement statistics |
| **Finance** | Stock data, company financials, market indicators, economic reports, crypto prices |
| **News** | Headlines, articles, sentiment analysis, topic clustering, source aggregation |
| **Web3** | On-chain data, token metrics, NFT collections, DeFi protocols, wallet activity |
| **Gaming** | Game statistics, player data, esports results, in-game economies, release schedules |
| **Sports** | Match results, player statistics, league standings, betting odds, schedules |
| **Marketing** | Campaign analytics, ad performance, market research, competitor intelligence |
| **Education** | Course listings, institution data, academic research, learning resources, certifications |


| Domain | Examples of Available Data |
|--------|---------------------------|
| **E-commerce** | Amazon, eBay, Alibaba, Bestbuy, Shopee, Shopify, Taobao, Pinduoduo, ... (product listings, prices, reviews, sales trends, etc.) |
| **Local Services** | Google Maps, Yelp, Airbnb, Opentable, Baike (business listings, service providers, ratings, business hours, etc.) |
| **Recruitment** | LinkedIn, Indeed, Upwork, Freelancer (job listings, candidate profiles, salary data, etc.) |
| **Social Media** | Twitter, Facebook, Telegram, Snapchat, Wechat, Weibo (user profiles, posts, engagement metrics, trending topics, etc.) |
| **Short Video** | TikTok, Douyin, Rednote, Xiaohongshu, Bilibili (video metadata, trending content, creator analytics, etc.) |
| **Finance** | Yahoo Finance, Bloomberg, CoinGecko (stock data, corporate financials, market indicators, cryptocurrency prices, etc.) |
| **News** | Reuters, BBC, Google News, Sina News (news headlines, articles, sentiment analysis, topic clustering, etc.) |
| **Web3** | Etherscan, Dune Analytics, OpenSea (on-chain data, token metrics, NFT collections, DeFi protocols, etc.) |
| **Gaming** | Steam, Twitch, Esports Platforms (game stats, player data, esports results, etc.) |
| **Sports** | ESPN, Sofascore, Flashscore (match results, player statistics, league rankings, betting odds, etc.) |
| **Marketing** | Google Analytics, SEMrush, SimilarWeb (campaign analytics, ad performance, market research, etc.) |
| **Education** | Coursera, Udemy, university websites (course listings, institutional information, academic research, learning resources, etc.) |
| **Travel** | TripAdvisor, Expedia, Booking.com (hotel listings, flight data, user reviews, destination insights, pricing trends, etc.) |

> 💡 **More domains available upon request.** If you need data from a domain not listed above, ask or create a data bounty.

## Data Output Formats

### Format 1: Structured & Curated Data
Pre-processed, cleaned, and organized data ready for analysis:
```json
{
  "summary": "Key insights extracted from raw data",
  "structured_data": {
    "field1": "value1",
    "field2": "value2"
  },
  "trends": [...],
  "recommendations": [...]
}

```

### Format 2: Raw API JSON
Original, unmodified JSON response from the underlying API:
```json
{
  "source": "original-api-name",
  "timestamp": "2024-01-15T10:30:00Z",
  "raw_response": { ... }
}
```

### Format 3: Markdown Report
Human-readable report format for consumption and sharing:
```text
# Data Report: Topic X

## Summary
Key findings and insights...

## Detailed Data
Structured presentation of results...

## Sources
List of data sources used...
```
## Data Processing Capabilities
All queries benefit from the following built-in capabilities:
| Capability | Description |
|------------|-------------|
| *Filtering* | Filter data by date range, category, location, value thresholds, and custom criteria |
| *Validation* | Automatic data quality checks, duplicate removal, format verification |
| *Deduplication* | Remove duplicate entries across multiple data sources |
| *Transformation* | Convert between formats, normalize values, currency/unit conversion |
| *Enrichment* | Cross-reference with other datasets to add context |
| *Aggregation* | Summarize, group, and calculate statistics across datasets |

## Natural Language Filtering Examples
Users can specify filters directly in their query:
- *"Show me e-commerce products with rating above 4.5 and price under $50"*
- "Get job listings in San Francisco posted in the last 7 days"
- "Find trending social media posts with over 10k likes from this week"
- "Show Web3 projects with at least $1M TVL and active in the last 30 days"
- "Get sports results for Premier League matches from January 2024 onwards"
- *"Filter for only verified local service providers with 4+ star ratings"*

## Core Capabilities
| Capability | Description |
|------------|-------------|
| Natural Language Queries | Convert user's natural language into API calls with automatic parameter extraction |
| Async Result Polling | Automatically poll until data is ready |
| API Supply Addition | Add new API supplies using natural language + documentation link |
| Data Bounties | Initiate data bounties when requested data is unavailable |
| Multi-Format Output | Return structured data, raw JSON, or Markdown reports |
| Data Processing | Built-in filtering, validation, deduplication, and transformation |

## When to Use
- User needs data from any supported domain (e-commerce, finance, recruitment, etc.) — skip building scraping infrastructure, handling anti-bot measures, or writing crawler maintenance code
- User wants structured/pre-processed data instead of learning each platform's API, dealing with inconsistent formats, and cleaning raw responses
- User needs data filtering, validation, or cross-source enrichment
- User wants to add a new API supply to the system
- User cannot find desired data and wants to offer a bounty — instead of hitting a dead end with no alternatives

## When NOT to Use
- Local file read/write operations
- Pure computation tasks (no external data needed)
- Scenarios requiring sub-second real-time responses
- General knowledge questions not related to the supported data domains

## Prerequisites: Getting an API Key
Before using this Skill, you need a DataHub API Key. Two ways to get one:

### Option 1: Apply via Website
- Visit DataHub official website: https://datahub.codes
- Register or log in to your account
- Navigate to "API Management" or "Developer" page
- Create a new API Key and copy it

### Option 2: Get it Directly in Chat
- Visit https://datahub.codes
- Simply type in the website's chat dialog:

```text
Please give me an API Key
```
or
```text
I want to apply for an API key
```
- The system will automatically generate and return an API Key

>💡 Tip: New users typically receive free credits sufficient for first-time use.

## Configuring the API Key
After obtaining your API Key, configure it using one of these methods:

### Method A: Environment Variable (Recommended)

```bash
export DATAHUB_API_KEY="your-api-key-here"
```

### Method B: User Config File
Create ~/.datahub/config.json:

```json
{
  "apiKey": "your-api-key-here"
}
```

### Method C: Project Config File
Create datahub.config.json in your project root:

```json
{
  "apiKey": "your-api-key-here"
}
```

Configuration priority: Environment Variable > User Config > Project Config

## Workflows
### Workflow 1: Standard Data Query
Use this when the user wants to fetch data from any supported domain — no scraping setup, no per-API integration work, just natural language.

#### Step 1: Submit Query
Execute scripts/query.js to submit the user's natural language query:

```bash
node scripts/query.js "<user's natural language query>" [sessionId]
```

Parameters:
- First argument: User's natural language query (required)
- Second argument: Session ID for context retention (optional)

Response Format:
```json
{
  "success": true,
  "processId": "xxx-xxx-xxx",
  "message": "Query submitted"
}
```
#### Step 2: Poll for Results
Execute scripts/poll.js to poll for the processed result:

```bash
node scripts/poll.js <processId> [--max-attempts 60] [--interval 1000]
```
Parameters:
- processId: Process ID returned from Step 1 (required)
- --max-attempts: Maximum polling attempts, default 60
- --interval: Polling interval in milliseconds, default 1000

Response Format:
```json
{
  "success": true,
  "data": { ... },
  "attempts": 5,
  "elapsed": 5234
}
```
#### Step 3: Parse and Present Results
- If structured JSON returned: Present key insights clearly with appropriate formatting
- If raw JSON returned: Present the data with source attribution; offer to further process if needed
- If Markdown returned: Maintain the formatted report as-is for readability
- If query fails: Explain possible reasons and suggest alternatives (including data bounties)

### Workflow 2: Adding an API Supply
Use this when the user wants to add a new API supply to the system — no need to write custom integration code or manage auth/pagination on their own.

#### Step 1: Submit API Supply Addition
Execute scripts/query.js with a specially formatted query that includes the API documentation link:

```bash
node scripts/query.js "Add API supply: <description>. Documentation: <DocLink>" [sessionId]
```

#### Examples:
```bash
# E-commerce API
node scripts/query.js "Add API supply: Amazon product search and reviews API. Documentation: https://api.example.com/docs"

# Social Media API
node scripts/query.js "Add API supply: LinkedIn company page data API. Docs: https://linkedin-api.example.com"

# Web3 API
node scripts/query.js "Supply a DEX trading volume API for Uniswap and PancakeSwap: https://defi-api.example.com/docs"
```

Alternative Natural Language Formats:
- "I want to add a new API for job board data. Docs: https://jobs-api.example.com"
- "Register new data source for esports match results: https://esports-api.example.com"
- "Add supply: Short video trending data from TikTok. DocLink: https://tiktok-api.example.com"

#### Step 2: Poll for Confirmation
Execute scripts/poll.js with the returned processId:

```bash
node scripts/poll.js <processId>
```
Expected Response:

```json
{
  "success": true,
  "data": {
    "apiId": "new-api-xxx",
    "domain": "e-commerce",
    "status": "registered",
    "message": "API supply successfully added and pending approval"
  }
}
```
#### Step 3: Confirm to User
Inform the user that:
- The API supply has been submitted and categorized under the appropriate domain
- It will be reviewed and activated shortly
- They can start using it once approved

### Workflow 3: Creating a Data Bounty
Use this when the user requests data that is not currently available — instead of hitting a dead end, create a bounty and let the community supply the data.

#### Step 1: Submit Data Bounty
Execute scripts/query.js with a query describing the desired data and bounty details:

```bash
node scripts/query.js "Create data bounty: <data description>. Reward: <bounty details>" [sessionId]
```

#### Examples:

```bash
# E-commerce data bounty
node scripts/query.js "Create data bounty: I need Amazon Best Seller rankings updated daily for the electronics category. Reward: $100"

# Recruitment data bounty
node scripts/query.js "Bounty: Looking for LinkedIn job posting data with salary info across tech companies. Will pay $200"

# Gaming data bounty
node scripts/query.js "I need real-time player statistics for Valorant competitive matches. Offering $150 bounty"
```

Alternative Natural Language Formats:
- "I need data on short video trends by region but can't find it. Can I create a bounty?"
- "Offer reward for marketing campaign performance data across platforms"
- "Start a bounty for Web3 developer activity metrics. Reward: $500"
- "The education dataset I want isn't available. How can I request it with a bounty?"

#### Step 2: Poll for Bounty Creation Confirmation
Execute scripts/poll.js with the returned processId:
```bash
node scripts/poll.js <processId>
```
Expected Response:
```json
{
  "success": true,
  "data": {
    "bountyId": "bounty-xxx-xxx",
    "status": "active",
    "domain": "gaming",
    "description": "Real-time player statistics for Valorant competitive matches",
    "reward": "$150",
    "createdAt": "2024-01-15T10:30:00Z",
    "message": "Bounty created successfully"
  }
}
```
#### Step 3: Inform User
Provide the user with:
- Bounty ID for tracking
- Confirmation that the bounty is now active
- The domain it was categorized under
- Estimated timeframe (if available)
- How they can check bounty status later

## Usage Examples
### Example 1: E-commerce Data with Filtering
User Input:
```text
"Show me the top 10 best-selling electronics on Amazon with rating above 4 stars and price under $100"
```
Execution:
```bash
RESULT=$(node scripts/query.js "Show me the top 10 best-selling electronics on Amazon with rating above 4 stars and price under $100")
PROCESS_ID=$(echo $RESULT | jq -r '.processId')
node scripts/poll.js $PROCESS_ID
```
### Example 2: Recruitment Data
User Input:
```text
"Get software engineer job listings in New York posted this week with salary range above $120k"
```
Execution:
```bash
RESULT=$(node scripts/query.js "Get software engineer job listings in New York posted this week with salary range above \$120k")
PROCESS_ID=$(echo $RESULT | jq -r '.processId')
node scripts/poll.js $PROCESS_ID
```
### Example 3: Social Media Analytics
User Input:
```text
"Fetch trending Twitter posts about AI from the past 24 hours with at least 1000 likes, filter out retweets"
```
Execution:
```bash
RESULT=$(node scripts/query.js "Fetch trending Twitter posts about AI from the past 24 hours with at least 1000 likes, filter out retweets")
PROCESS_ID=$(echo $RESULT | jq -r '.processId')
node scripts/poll.js $PROCESS_ID
```
### Example 4: Web3/DeFi Data
User Input:
```text
"Get the top 10 DeFi protocols by TVL on Ethereum, with 7-day change percentage"
```
Execution:
```bash
RESULT=$(node scripts/query.js "Get the top 10 DeFi protocols by TVL on Ethereum, with 7-day change percentage")
PROCESS_ID=$(echo $RESULT | jq -r '.processId')
node scripts/poll.js $PROCESS_ID
```
### Example 5: Creating a Data Bounty for Sports Data
User Input: 
```text
"I need NBA player performance data with advanced metrics but can't find it. I'll offer $200 for anyone who can supply this."
```
Execution:
```bash
RESULT=$(node scripts/query.js "Create data bounty: NBA player advanced performance metrics API with historical data. Reward: $200")
PROCESS_ID=$(echo $RESULT | jq -r '.processId')
node scripts/poll.js $PROCESS_ID
```

## Error Handling
| Error Type | Handling Approach |
|------------|-------------------|
| API Key not configured | Guide user to visit https://datahub.codes to obtain an API Key |
| Invalid/Expired API Key | Prompt user to refresh their API Key or verify it's correct |
| Query timeout | Retry up to 3 times with incremental backoff |
| Polling timeout | Inform user the task is taking longer; suggest checking back later |
| Invalid response format | Attempt to extract useful information; otherwise report format issue |
| Network error | Prompt user to check network connection |
| Insufficient credits | Direct user to website to check balance and upgrade options |
| API supply already exists | Inform user the API is already available and can be used immediately |
| Bounty creation failed | Explain reason and suggest adjusting reward or description |
| Data not found (bounty eligible) | Proactively suggest creating a data bounty |
| Domain not supported | Suggest creating a bounty or API supply to add the domain |
| Filter too restrictive | Suggest broadening filter criteria and retry |

## Proactive Suggestions
The Skill should proactively suggest:
1. Data processing options: "Would you like this data filtered, validated, or returned as raw JSON?"
2. When data is unavailable: "This data isn't currently available. Would you like to create a bounty for it?"
3. When user mentions an API: "Would you like to add this as an API supply? Just provide the documentation link."
4. Domain expansion: "I notice you're requesting data from [domain]. If we don't have it yet, I can help you create a bounty or API supply."
5. Format preference: "I can return this as structured data, raw JSON, or a Markdown report. Which do you prefer?"
6. After successful API supply addition: "Your API supply has been submitted and categorized. You can check its status later with the API ID."
7. When bounty is created: "Your bounty is now active. You'll be notified when someone fulfills it."

## Configuration Reference
| Variable | Description | Default |
|----------|-------------|---------|
| **DATAHUB_API_KEY** | Required, obtain from https://datahub.codes | None |
| **DATAHUB_BASE_URL** | DataHub API base URL | https://datahub.codes |
| **DATAHUB_TIMEOUT** | Request timeout in milliseconds | 60000 |

### Important Notes
- Each query generates a unique `processId` for result retrieval; results typically return in 3–30 seconds (complex queries may take longer)
- Use `sessionId` to maintain context across multi-turn conversations
- Scripts use only Node.js built-in modules — no additional dependencies required
- **API Key**: Register and log in at https://datahub.codes → obtain your key → recharge on the Profile page to ensure sufficient balance
- API supply additions require a valid documentation link (`DocLink`)
- Data bounties remain active until fulfilled or cancelled
- All three operations (query, supply, bounty) share the same API endpoint structure
- Data is returned as structured/curated data or raw API JSON — specify your preference
- All queries automatically benefit from filtering, validation, and deduplication

## Getting Help
- 🌐 Website: https://datahub.codes
- 💬 Live Support: Ask questions directly in the website's chat dialog
- 📧 Contact: Get technical support through the official website
- 📖 API Documentation: Available after login at https://datahub.codes/docs
