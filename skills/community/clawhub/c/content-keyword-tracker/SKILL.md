---
name: content-keyword-tracker
description: An OpenClaw skill for tracking keyword trends and generating structured reports. Uses Tavily API for search and supports webhook notifications for daily report delivery.
version: 1.5.0
author: yesong-Hue
homepage: https://clawhub.ai/yesong-Hue/content-keyword-tracker
tags: [keyword, tracker, monitoring, reports, automation, tavily]
readme: |
  # Content Keyword Tracker

  A comprehensive OpenClaw skill designed for tracking keyword trends across multiple platforms and generating detailed markdown reports with webhook support.

  ## Overview

  This skill helps you stay informed about keyword trends by automatically gathering search results and compiling them into organized daily reports.

  ## Features

  ### Multi-Keyword Parallel Tracking
  Track multiple keywords simultaneously with independent result collection for each keyword. Each keyword can be configured with different weight priorities and platform preferences.

  ### Comprehensive Search Coverage
  Automatically searches across major platforms including social media sites, forums, blogs, and news outlets. Results include title, URL, platform source, and engagement metrics.

  ### Structured Markdown Reports
  Generates clean markdown format reports with sortable tables containing: Rank, Title, Platform, Trend Score, Publish Date, and Source URL. Easy to read and share with teams.

  ### Webhook Integration
  Supports webhook notifications for automated report delivery. Configure your webhook URL in environment variables to send daily reports directly to your team's communication channels.

  ### Local Data Persistence
  All reports are saved locally in the reports directory with timestamp-based file naming. Supports historical queries and trend analysis over time.

  ## Installation

  Install via OpenClaw skills command:

  ```
  openclaw skills install content-keyword-tracker
  ```

  ## Configuration

  Create or edit the keywords configuration file with one keyword per line:

  ```
  technology trends
  product updates
  industry news
  ```

  Required environment variables:

  - TAVILY_API_KEY: Your Tavily API key for search functionality

  Optional environment variables:

  - WEBHOOK_URL: Your webhook endpoint for report delivery
  - MAX_RESULTS: Maximum results per keyword (default: 10)
  - REPORT_DIR: Local directory for storing reports

  ## Usage

  Run the skill with:

  ```
  node index.js
  ```

  The skill will read your keyword configuration, perform searches using Tavily API, generate a comprehensive markdown report, and optionally send it to your configured webhook.

  ## Report Format

  The generated report includes:

  - Timestamp header
  - Section per keyword with results table
  - Summary statistics
  - Trend indicators

  ## Use Cases

  - Content Strategy: Identify trending topics for content planning
  - Competitive Intelligence: Monitor competitor mentions and industry trends
  - Market Research: Track product demand and consumer interest patterns
  - Academic Research: Monitor keyword trends for research papers

  ## Privacy Note

  - All data processing happens locally on your machine
  - No external servers store your keyword data
  - Webhook endpoints are only used for report delivery

  ## Requirements

  - Node.js version 18 or higher
  - Valid Tavily API key (available at https://tavily.com)
  - Internet connection for search functionality

  ## Resources

  - Tavily API: https://tavily.com
  - ShadowAI API (alternative): https://referer.shadowai.xyz/r/1056448
  - More OpenClaw Skills: http://ai.qnitgroup.com

  ## License

  MIT License

  ## Author

  yesong-Hue | AI Skills at http://ai.qnitgroup.com
---

# Content Keyword Tracker

> Track keyword trends and generate structured reports with this OpenClaw skill

## Features

- Multi-keyword parallel tracking with independent results per keyword
- Comprehensive search across multiple platforms using Tavily API
- Structured markdown report generation with sortable data tables
- Webhook notification support for automated report delivery
- Local data storage with timestamp-based file management

## Installation

```
openclaw skills install content-keyword-tracker
```

## Configuration

Configure your keywords in the keywords.txt file, one per line:

```
technology trends
product updates
industry news
```

Set your Tavily API key in environment variables:

```
TAVILY_API_KEY=your_api_key_here
```

Optional: Set webhook URL for report delivery:

```
WEBHOOK_URL=https://your-webhook-endpoint.com
```

## Usage

Run with:

```
node index.js
```

Reports are generated in markdown format and saved locally.

## Requirements

- Node.js 18+
- Tavily API key

## Resources

- More skills: http://ai.qnitgroup.com
- ShadowAI API: https://referer.shadowai.xyz/r/1056448