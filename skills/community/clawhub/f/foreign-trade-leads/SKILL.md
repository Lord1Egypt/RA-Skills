---
name: foreign-trade-leads
description: 从 Google Maps 抓取 B2B 外贸潜在客户名单。用于找海外分销商、批发商、采购商、本地商家线索；触发词包括“获客”“找客户”“Google Maps客户”“外贸客户名单”。
---

# Foreign Trade Leads

Use this skill when the user asks to collect overseas B2B leads from Google Maps.

## Do

- Confirm the product keyword, target country/region, and target count.
- Prefer Google Maps first for local distributors, wholesalers, retailers, and importers.
- Run the bundled script instead of rewriting the scraper.
- Save output as CSV in the current workspace.

## Inputs to confirm

- Product keyword in English, e.g. `shower head distributor`
- Region, e.g. `USA`, `California`, `Germany`
- Count, e.g. `30`, `50`, `100`

## Command

Run:

```bash
python3 scripts/get_google_maps_leads.py "<keyword>" "<region>" <count>
```

Example:

```bash
python3 scripts/get_google_maps_leads.py "shower head distributor" "USA" 50
```

## Output

The script writes a CSV with these columns:

- name
- phone
- address
- website
- email

## Notes

- Google Maps may rate-limit or block scraping.
- Use moderate target sizes and avoid aggressive repeated runs.
- If Chrome/driver is unavailable, stop and report the environment issue.
