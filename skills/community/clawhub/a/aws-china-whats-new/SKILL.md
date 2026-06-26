# AWS China What's New

Query AWS China Region (Beijing / Ningxia) service launch announcements from 2016 to present.

## When to use

Activate this skill when the user asks about:
- What AWS services are available in China regions (cn-north-1 Beijing, cn-northwest-1 Ningxia)
- Recent AWS China service launches or announcements
- Whether a specific service (e.g., Lambda, EKS, Bedrock) is available in AWS China
- Comparing AWS China region availability between Beijing and Ningxia
- Timeline of when a service launched in AWS China

## Data management

### Update data (fetch latest announcements)

```bash
# Incremental update (current year only, fast)
python3 scripts/fetch_data.py --incremental

# Full refresh (all years 2016-2026)
python3 scripts/fetch_data.py

# Specific year(s)
python3 scripts/fetch_data.py --year 2025 2026
```

Run incremental update before answering queries if data might be stale.

## Querying

```bash
# Search by service name
python3 scripts/query.py --service "Lambda"
python3 scripts/query.py --service "Elastic Kubernetes"

# Filter by region
python3 scripts/query.py --service "S3" --region beijing
python3 scripts/query.py --region ningxia --year 2025

# Filter by date
python3 scripts/query.py --after 2025-01-01 --before 2025-12-31
python3 scripts/query.py --service "EKS" --after 2024-06-01

# Latest announcements
python3 scripts/query.py --latest
python3 scripts/query.py --limit 10

# Combine filters
python3 scripts/query.py --service "SageMaker" --region beijing --year 2025
```

All commands output JSON to stdout:
```json
{
  "count": 2,
  "items": [
    {
      "title": "Amazon Lambda adds support for ...",
      "date": "2026-01-09",
      "link": "/en/new/2026/amazon-lambda-adds-support-for-.../",
      "regions": ["beijing", "ningxia"],
      "year": 2026,
      "body_preview": "Short text preview..."
    }
  ]
}
```

## How to respond

1. Run the query and parse the JSON output
2. Summarize the results clearly:
   - List matching services with dates and regions
   - If no results, say the service may not be available in AWS China yet
   - Mention the data source date range (2016-present)
3. For availability questions, note that absence from the list does not guarantee unavailability -- it may just mean no announcement was indexed
4. Include the announcement link when relevant: prepend `https://www.amazonaws.cn` to the relative link path
