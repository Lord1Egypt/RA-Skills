---
name: cloudsway-smartsearch

description: 
  Smartsearch web search skill for searching the internet, retrieving online information, news, and research data.
  Supports:
  - AI search
  - web search
  - online search
  - internet search
  - information retrieval

  Similar to search engines like  Brave Search, and Tavily.

  Use this skill when users need:
  - web search
  - online information lookup
  - latest news
  - internet research
  - real-time information
  - AI agent research
  - fact checking
  - browsing websites

homepage: https://cloudsway.ai

metadata:
  {
    "openclaw":
      {
        "emoji":"🔎",
        "requires":{"env":["CLOUDSWAYS_AK"]},
        "bins":["curl","jq"]
      }
  }
---

# AI Search Skill (Web Search for AI Agents)

This skill enables **AI agents and LLM systems** to perform web search and retrieve real-time information from the internet.

It works similarly to modern search engines such as:

- Google
- Bing
- Perplexity
- Brave Search
- Tavily

The skill allows AI systems to access **up-to-date information**, including:

- news
- websites
- research articles
- documentation
- trending topics

---

# When Should This Skill Be Used

Use this skill when the user asks about:

• searching the internet  
• latest news or current events  
• information from websites  
• online research topics  
• finding articles or documentation  
• verifying facts  
• gathering information from multiple sources  

Example queries:

- "latest AI news"
- "search the web for vector database benchmarks"
- "find information about GPT models"
- "what happened in AI this week"
- "latest updates from OpenAI"
- "research agentic AI architecture"

---

# Example Use Cases

## Web Search

Search the internet for general information.

Example:

```

search the web for latest AI developments

```

---

## News Search

Retrieve recent news or trending events.

Example:

```

latest AI news this week

```

---

## Research Tasks

AI agents gathering information from multiple sources.

Example:

```

research agentic AI architecture

```

---

## Fact Checking

Verify claims using multiple web sources.

Example:

```

check if GPT-5 has been released

````

---

# Quick Setup

1. **Get your API Key**

Sign up at:

https://cloudsway.ai

2. **Set environment variable**

```bash
export CLOUDSWAYS_AK="your-api-key"
````

That's it. The skill is ready to use.

---

# Quick Start

## Method 1: Using the Script

```bash
cd ~/scripts/search
./scripts/search.sh '{"q": "your search query"}'
```

### Examples

```bash
# Basic search
./scripts/search.sh '{"q": "latest AI developments"}'

# Search with time filter
./scripts/search.sh '{"q": "OpenAI news", "freshness": "Week", "count": 20}'

# Deep research
./scripts/search.sh '{"q": "Agentic AI architecture", "enableContent": true, "mainText": true}'
```

---

## Method 2: Direct API Call

```bash
curl -s -G \
  --url "https://aisearchapi.cloudsway.net/api/search/smart" \
  --header "Authorization: ${CLOUDSWAYS_AK}" \
  --data-urlencode "q=your search query" \
  --data-urlencode "count=20" \
  --data-urlencode "freshness=Week"
```

### Real-world Example

```bash
curl -s -G \
  --url "https://aisearchapi.cloudsway.net/api/search/smart" \
  --header "Authorization: ${CLOUDSWAYS_AK}" \
  --data-urlencode "q=latest AI news February 2026" \
  --data-urlencode "count=20" \
  --data-urlencode "freshness=Week" \
  --data-urlencode "enableContent=true" \
  --data-urlencode "mainText=true"
```

---

# API Reference

## Endpoint

```
GET https://aisearchapi.cloudsway.net/api/search/smart
```

---

## Headers

| Header        | Type   | Value       | Description           |
| ------------- | ------ | ----------- | --------------------- |
| Authorization | String | `{YOUR_AK}` | Your assigned API Key |

---

## Request Parameters

| Parameter      | Required | Type    | Default | Description                    |
| -------------- | -------- | ------- | ------- | ------------------------------ |
| q              | Yes      | String  | -       | Search query                   |
| count          | No       | Integer | 10      | Must be 10 / 20 / 30 / 40 / 50 |
| freshness      | No       | String  | null    | Day / Week / Month             |
| offset         | No       | Integer | 0       | Pagination offset              |
| enableContent  | No       | Boolean | false   | Extract full text              |
| contentType    | No       | String  | TEXT    | HTML / MARKDOWN / TEXT         |
| contentTimeout | No       | Float   | 3.0     | Extraction timeout             |
| mainText       | No       | Boolean | false   | Smart summary fragments        |

---

# Response Format

```json
{
  "queryContext": {
    "originalQuery": "your search query"
  },
  "webPages": {
    "value": [
      {
        "name": "Article Title",
        "url": "https://example.com/article",
        "datePublished": "2026-02-27T15:46:11.0000000",
        "snippet": "Short summary...",
        "mainText": "Relevant excerpts...",
        "content": "Full webpage text...",
        "score": 0.85
      }
    ]
  }
}
```

---

# Content Strategy

Choose the right field based on your needs:

| Field    | Latency | Token Cost | Use Case         |
| -------- | ------- | ---------- | ---------------- |
| snippet  | Fast    | Low        | Quick browsing   |
| mainText | Medium  | Medium     | Focused research |
| content  | Slower  | High       | Deep analysis    |

---

# Recommended Settings

### Quick Research

```json
{"q": "topic", "count": 10}
```

---

### Focused Research

```json
{"q": "topic", "count": 20, "freshness": "Week", "enableContent": true, "mainText": true}
```

---

### Deep Research

```json
{"q": "topic", "count": 20, "enableContent": true, "contentType": "MARKDOWN"}
```

---

# Troubleshooting

### Invalid JSON

Use curl directly if the script fails.

### Count Parameter Error

Valid values:

```
10 / 20 / 30 / 40 / 50
```

### Environment Variable Missing

Check configuration:

```bash
echo $CLOUDSWAYS_AK
```

---

# Keywords

web search
AI search
internet search
online search
search engine
Google search
Bing search
Perplexity search
Brave search
Tavily search
AI research tool
LLM web search
AI agent search
internet information retrieval

---

Last Updated: 2026-03-09

```

---
