---
name: bing-webmaster-helper
description: "Bing Webmaster Tools API helper to submit URLs and fetch search traffic, keyword rankings, indexing status, and crawl issues without uploading verification files. Use when the user needs to: (1) Submit single or batch URLs to Bing for instant indexing (via GSC verified site, using Bing Webmaster API key), (2) Fetch website search performance, query keywords, impressions, clicks, and rankings, (3) Retrieve crawl health and page indexing statuses, (4) Automate SEO audits or diagnostics for zymetalforming.com or any other B2B client sites."
metadata:
  requires:
    bins: ["python3"]
    env: ["BING_WEBMASTER_API_KEY"]
  emoji: "🕷️"
---

# Bing Webmaster Helper

This skill connects to the Microsoft Bing Webmaster Tools API using your API key. It enables zero-dependency, file-free URL submissions for instant search engine indexing, and pulls rich, crawl-level SEO reporting.

## Setup

This skill requires a Bing Webmaster Tools API Key.

1. Sign in to [Bing Webmaster Tools](https://www.bing.com/webmasters/).
2. Click **Settings** (gear icon) in the top-right corner.
3. Under **API Access**, select **API Key** and generate one.
4. Configure the API key in your Agent workspace using:
   `env_config(action="set", key="BING_WEBMASTER_API_KEY", value="your_api_key_here")`
5. The skill will automatically activate once the environment variable is set.

---

## 🛠️ Core Capabilities & Workflows

All scripts are in the skill's base directory `<base_dir>/scripts/`.

### 1. Instant URL Submission (No Verification File Needed)

Submit new or updated page URLs to Bing for fast crawling and indexing. This bypasses the need to upload any `.txt` or `.html` verification files since the domain is already validated in your Bing/GSC account.

#### Submit a single URL:
```bash
python3 <base_dir>/scripts/submit_urls.py --site-url "https://zymetalforming.com" --urls "https://zymetalforming.com/new-product-page.html"
```

#### Submit a batch of URLs:
```bash
python3 <base_dir>/scripts/submit_urls.py --site-url "https://zymetalforming.com" --urls "https://zymetalforming.com/page1.html,https://zymetalforming.com/page2.html"
```

#### Submit URLs from a text file:
Create a text file with one URL per line and run:
```bash
python3 <base_dir>/scripts/submit_urls.py --site-url "https://zymetalforming.com" --file "path/to/urls.txt"
```

---

### 2. Fetch SEO Traffic & Search Statistics

Retrieve various search engine statistics directly from Bing.

#### Method 1: Get Rank & Traffic Stats
Find out how impressions and clicks are trending over the last few weeks:
```bash
python3 <base_dir>/scripts/fetch_data.py --site-url "https://zymetalforming.com" --method rank_traffic
```

#### Method 2: Get Keyword Rankings (Queries)
Analyze the exact query search terms driving clicks and impressions, along with CTR and search positions:
```bash
python3 <base_dir>/scripts/fetch_data.py --site-url "https://zymetalforming.com" --method query_stats
```

#### Method 3: Get Crawl Health Statistics
Monitor crawler activity, successfully crawled pages, and crawling errors:
```bash
python3 <base_dir>/scripts/fetch_data.py --site-url "https://zymetalforming.com" --method crawl_stats
```

#### Method 4: Get Remaining Submission Quota
Check how many more URLs you can submit today and this month:
```bash
python3 <base_dir>/scripts/fetch_data.py --site-url "https://zymetalforming.com" --method quota
```

---

### 3. Generate a Complete Markdown SEO Report

You can query all statistics at once and compile them into a unified Markdown report, suitable for automated emails, Slack/DingTalk push messages, or client deliverables.

```bash
python3 <base_dir>/scripts/fetch_data.py --site-url "https://zymetalforming.com" --method all
```

**Output Structure of `all` Method:**
- URL Submission Quota Status
- Recent Rank & Traffic (Last 10 Records table)
- Top Search Keywords (Driving Traffic table containing Query, Clicks, Impressions, CTR, Position)
- Crawl Health (Date, Pages Crawled, Crawl Errors table)

---

## 🎯 Best Practices & Automation

### Automated Bi-weekly Audit Integration
You can schedule automated audits using the workspace `scheduler` tool. For example, to run an audit every 1st and 16th of the month and save the report or push it via webhook:

1. Create a scheduled AI task:
   ```json
   {
     "action": "create",
     "name": "Bi-weekly Bing SEO Audit",
     "schedule_type": "cron",
     "schedule_value": "0 10 1,16 * *",
     "ai_task": "Run the bing-webmaster-helper 'all' report for https://zymetalforming.com and push the summary to the DingTalk Webhook."
   }
   ```
