# Enrichment Field Definitions

## Company Fields

| Field | Description | Source |
|-------|-------------|--------|
| company_name | Official registered name | Website, LinkedIn |
| industry | Primary industry classification | LinkedIn, website |
| sub_industry | Niche within industry | Website, product descriptions |
| employee_count | Estimated headcount range | LinkedIn, job postings |
| revenue_range | Estimated annual revenue bracket | Public filings, industry benchmarks |
| founded_year | Year company was established | LinkedIn, Crunchbase |
| funding_total | Total capital raised | Crunchbase, press releases |
| funding_last_round | Most recent funding round details | Crunchbase, news |
| location_hq | Headquarters city and country | Website, LinkedIn |
| website | Primary domain | Direct |
| linkedin_url | Company LinkedIn page | LinkedIn search |
| tech_stack | Detected technologies | BuiltWith, Wappalyzer, page source |
| recent_news | Noteworthy events last 90 days | News aggregators |
| growth_signals | Hiring, expansion, launches | Job boards, press |

## Contact Fields

| Field | Description | Source |
|-------|-------------|--------|
| full_name | First and last name | LinkedIn, website team page |
| title | Current job title | LinkedIn |
| seniority | C-level / VP / Director / Manager / IC | Inferred from title |
| linkedin_url | Personal LinkedIn profile | LinkedIn search |
| email_pattern | Company email format (if detectable) | Website, public records |
| recent_activity | Posts, articles, job changes | LinkedIn, X/Twitter |

## Scoring Fields

| Field | Description | Range |
|-------|-------------|-------|
| lead_score | Composite fit score | 1-100 |
| fit_tag | Categorical classification | hot / warm / cold |
| priority_rank | Position in outreach queue | 1-N |
| confidence | How reliable the enrichment data is | high / medium / low |
