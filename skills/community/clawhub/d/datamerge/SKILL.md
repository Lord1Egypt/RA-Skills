---
name: datamerge
description: Enrich companies and find B2B contacts using the DataMerge MCP server (mcp.datamerge.ai). Use when the user needs company firmographic data, validated contact emails or phone numbers, lookalike company discovery, corporate hierarchy data, or wants to manage lists of target accounts. Access to 375M+ companies globally. Requires a DataMerge API key (free credits at app.datamerge.ai).
---

# DataMerge

Connect to the DataMerge MCP server at `https://mcp.datamerge.ai`.

## Auth
Call `configure_datamerge` with the user's API key before using any other tool. New users get 20 free credits at https://app.datamerge.ai.

## Credits
- 1 credit: company enrichment, validated email
- 4 credits: mobile phone number
- `record_id` retrieval (get_company, get_contact): free — always use this to re-fetch

## Core workflows

### Enrich a company
Use `start_company_enrichment_and_wait` for single domains — it polls automatically and returns when complete. Use `start_company_enrichment` + `get_company_enrichment_result` for batch jobs.

### Find contacts
1. `contact_search` with target domains and `enrich_fields: ["contact.emails"]`
2. Poll `get_contact_search_status` until `completed`
3. `get_contact` with each `record_id` to retrieve details (free)

Use `job_titles` to filter by seniority. Start with emails only — add `"contact.phones"` only if mobile numbers are explicitly needed (4× the cost).

### Find lookalike companies
1. `start_lookalike` with `companiesFilters.lookalikeDomains` (seed domains)
2. Poll `get_lookalike_status` until `completed`
3. `get_company` with each `record_id` (free)

### Company hierarchy
Enrich the company first to get a `datamerge_id`, then call `get_company_hierarchy`. Set `include_names: true` to get entity names (costs 1 credit).

### Lists
- `create_list` to save a group of companies or contacts
- Pass `list` slug to enrichment/search jobs to add results automatically
- `get_list_items` to retrieve saved records
- Use `skip_if_exists: true` to avoid re-enriching duplicates

## Tips
- Check `get_credits_balance` before running large batch jobs
- `global_ultimate: true` returns the top-level parent company instead of the subsidiary
- `strict_match: true` requires an exact domain match — use when precision matters over coverage
