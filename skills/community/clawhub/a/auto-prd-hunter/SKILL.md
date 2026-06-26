---
name: auto-prd-hunter
description: "Search web for user pain points and output a PRD JSON."
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - python3
    env:
      - name: BRAVE_API_KEY
        required: false
        description: "Brave Search API key for real-time web search"
      - name: BAIDU_API_KEY
        required: false
        description: "Baidu Search API key for Chinese content search"
    network:
      - host: api.search.brave.com
        purpose: "Brave Search API for web search"
      - host: hn.algolia.com
        purpose: "Hacker News Algolia API for tech discussions"
user-invocable: true
disable-model-invocation: false
---

# auto-prd-hunter

Scan platforms for user complaints, extract pain points, and produce a structured PRD + OpenClaw task JSON.

## Important Notice

⚠️ **No Fabrication Policy**: This skill ONLY returns results from real API searches. If no API results are found, it returns an error instead of generating mock/fabricated data.

## Commands

All operations use the packaged CLI script:

```bash
python3 {baseDir}/scripts/search.py search-pain-points --keyword "<keyword>" --max-results 8
```

## Workflow

1. Receive a keyword.
2. Run the search command to fetch real complaints from APIs.
3. Parse JSON from stdout.
4. Extract up to 5 pain points (id, title, severity, context, sources).
5. Invent product name and summary.
6. Write user stories and MVP features.
7. Derive openclaw_tasks.
8. Output ONLY the final JSON (no markdown fences, no greetings).

## Constraints

- MUST run the CLI script. Do NOT fabricate results.
- If APIs return no results, return error JSON: `{"status":"no_results","error":"No API results found"}`
- Final reply MUST be ONLY valid JSON.
- No markdown fences (no ```json), no greetings, no explanations.
- If search fails, return: `{"status":"error","error":"reason"}`

## Network Requests

This skill makes outbound network requests to:
- **Brave Search API** (api.search.brave.com) - For web search results
- **Hacker News Algolia API** (hn.algolia.com) - For tech community discussions

⚠️ **Privacy Notice**: Your search keywords will be sent to these external services. Do not include sensitive or confidential information in keywords.

## Environment Variables

The script optionally reads these environment variables:

| Variable | Required | Purpose |
|----------|----------|---------|
| `BRAVE_API_KEY` | No | Brave Search API key for enhanced search results |
| `BAIDU_API_KEY` | No | Baidu Search API key for Chinese content |

If no API keys are provided, the skill will attempt to use Hacker News API (no key required).

## Output JSON Schema

```json
{
  "status": "success",
  "keyword": "searched keyword",
  "project_name": "product name",
  "summary": "one-line value",
  "pain_points": [
    {
      "id": "PP-001",
      "title": "pain title",
      "severity": "high",
      "context": "description",
      "sources": [
        {
          "platform": "Hacker News",
          "url": "https://news.ycombinator.com/item?id=...",
          "quote": "actual user words from the post"
        }
      ]
    }
  ],
  "user_stories": [
    {
      "id": "US-001",
      "as_a": "role",
      "i_want_to": "desire",
      "so_that": "goal",
      "acceptance_criteria": ["criterion 1"],
      "priority": "P0",
      "pain_point_ids": ["PP-001"]
    }
  ],
  "mvp_features": [
    {
      "id": "F-001",
      "title": "feature name",
      "description": "what it does",
      "priority": "P0",
      "user_story_ids": ["US-001"],
      "pain_point_ids": ["PP-001"]
    }
  ],
  "openclaw_tasks": [
    {
      "task_id": "TASK-001",
      "title": "task name",
      "description": "dev instructions",
      "priority": "P0",
      "acceptance_criteria": ["standard 1"],
      "feature_id": "F-001"
    }
  ],
  "generated_at": "2026-04-07T12:00:00",
  "data_source": "API"
}
```

## Error Handling

### Script Not Found
If the CLI script is not found or Python is missing:
```json
{
  "status": "error",
  "error": "Search script not available. Ensure python3 is installed and the script exists at {baseDir}/scripts/search.py"
}
```

### No API Results
If all APIs return no results:
```json
{
  "status": "no_results",
  "keyword": "<keyword>",
  "error": "No API results found. Try providing API keys (BRAVE_API_KEY) or using a different keyword.",
  "suggestions": [
    "Set BRAVE_API_KEY environment variable",
    "Try a broader keyword",
    "Check network connectivity"
  ]
}
```

### API Error
If API calls fail:
```json
{
  "status": "error",
  "error": "API request failed: <error details>"
}
```

## Data Sources

The script fetches user complaints from these platforms:

| Platform | Type | Auth Required | URL |
|----------|------|---------------|-----|
| Brave Search | Web Search | Optional (API key) | api.search.brave.com |
| Hacker News | Tech Forum | No | hn.algolia.com |

**Note**: Without API keys, only Hacker News results will be available, which may limit results for non-tech topics.

## Usage Examples

### Basic Usage
```bash
python3 scripts/search.py search-pain-points --keyword "remote work" --max-results 10
```

### With API Key
```bash
export BRAVE_API_KEY="your_api_key"
python3 scripts/search.py search-pain-points --keyword "AI tools" --max-results 8
```

### Chinese Content
```bash
export BAIDU_API_KEY="your_api_key"
python3 scripts/search.py search-pain-points --keyword "远程办公" --max-results 8
```

## Integration with Cron

This skill works with OpenClaw's cron system for automated daily PRD generation:

```json
{
  "name": "每日痛点挖掘与PRD生成",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "Asia/Singapore"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "运行 auto-prd-hunter 调研热门领域痛点并生成PRD"
  },
  "sessionTarget": "isolated"
}
```

## Transparency Commitment

This skill adheres to the following principles:

1. **No Fabrication**: Never generates fake pain points or sources
2. **Transparency**: All network requests are declared in metadata
3. **Privacy**: Keyword inputs are sent to external APIs (as declared)
4. **Authenticity**: All sources contain real URLs and quotes
5. **Error Handling**: Returns clear errors when APIs fail or return no results

## Troubleshooting

### "No API results found"
- **Cause**: No API keys configured and Hacker News has no relevant results
- **Solution**: Set `BRAVE_API_KEY` or try a different keyword

### "API request failed"
- **Cause**: Network issue or invalid API key
- **Solution**: Check network connectivity and verify API keys

### Limited results
- **Cause**: Only using Hacker News (tech-focused)
- **Solution**: Configure `BRAVE_API_KEY` for broader web search

## Getting API Keys

### Brave Search API
1. Visit: https://api.search.brave.com/
2. Sign up for free tier
3. Get your API key
4. Set environment variable: `export BRAVE_API_KEY="your_key"`

### Baidu Search API
1. Visit: https://cloud.baidu.com/
2. Enable Baidu Search API
3. Get your API key
4. Set environment variable: `export BAIDU_API_KEY="your_key"`
