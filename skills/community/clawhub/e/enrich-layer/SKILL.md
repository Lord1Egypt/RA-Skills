---
name: enrich-layer
description: Enrich company, person, and contact data with 25 tools via the Enrich Layer API. Look up companies, find decision-makers, get work emails, search employees, verify contacts, and more.
version: 0.2.0
metadata:
  openclaw:
    requires:
      env:
        - ENRICH_LAYER_API_KEY
      bins:
        - node
    primaryEnv: ENRICH_LAYER_API_KEY
    emoji: "\U0001F50D"
    homepage: https://enrichlayer.com
---

# Enrich Layer

This skill connects to the Enrich Layer API via MCP, giving you 25 tools for enriching company, person, contact, school, and job data from professional networks.

## Setup

Add the Enrich Layer MCP server to your OpenClaw MCP configuration:

```json
{
  "mcpServers": {
    "enrich-layer": {
      "command": "npx",
      "args": ["-y", "@verticalint-michael/enrich-layer-mcp"],
      "env": {
        "ENRICH_LAYER_API_KEY": "${ENRICH_LAYER_API_KEY}"
      }
    }
  }
}
```

Get your API key at [enrichlayer.com/dashboard](https://enrichlayer.com/dashboard).

---

## Available Tools (25)

### Company (7 tools)

- **enrich_company_profile** — Get structured company data from a professional network URL. Returns name, industry, size, description, specialties, funding, and more. Cost: 1 credit. Optional add-ons (1 credit each): `categories`, `funding_data`, `exit_data`, `acquisitions`, `extra`.
- **enrich_company_lookup** — Look up a company by name or domain to find its professional network URL. Provide at least one of `company_name` or `company_domain`. Optionally pass `company_location` as an ISO 3166-1 alpha-2 country code to disambiguate. Cost: 2 credits.
- **enrich_company_id_lookup** — Look up a company by its internal numeric ID to get its professional network URL. Cost: 0 credits.
- **enrich_company_picture** — Get the profile picture URL of a company. Cost: 0 credits.
- **enrich_employee_list** — List employees of a company. Supports filtering by role (boolean search), country, employment status, and sorting. Cost: 3 credits per employee returned.
- **enrich_employee_count** — Get the number of employees at a company. Supports historical counts via `at_date`. Cost: 1 credit.
- **enrich_employee_search** — Search employees by keyword at a specific company. Uses boolean search syntax for job titles. Cost: 10 credits per request.

### Person (4 tools)

- **enrich_person_profile** — Get structured person data from a profile URL (professional network, Twitter/X, or Facebook). Returns experience, education, skills, and more. Cost: 1 credit. Optional add-ons: `extra` (1 credit), `personal_contact_number` (1 credit/number), `personal_email` (1 credit/email), `skills` (free).
- **enrich_person_lookup** — Look up a person by first name and company domain to find their professional network profile. Provide `first_name` and `company_domain`; optionally add `last_name`, `title`, `location` for precision. Cost: 2 credits.
- **enrich_person_picture** — Get the profile picture URL of a person. Cost: 0 credits.
- **enrich_role_lookup** — Find who holds a specific role at a company. Provide `company_name` and `role` (e.g., "ceo"). Cost: 3 credits.

### Contact (6 tools)

- **enrich_reverse_email** — Find a person's professional network profile by their email address. Cost: 3 credits.
- **enrich_reverse_phone** — Find a person's professional network profile by their phone number (E.164 format). Cost: 3 credits.
- **enrich_work_email** — Get the work email address of a person from their profile URL. Cost: 3 credits.
- **enrich_personal_contact** — Get personal phone numbers of a person from their profile URL. Cost: 1 credit per contact number.
- **enrich_personal_email** — Get personal email addresses of a person from their profile URL. Cost: 1 credit per email.
- **enrich_disposable_email** — Check if an email address is from a disposable email provider. Cost: 0 credits.

### School (2 tools)

- **enrich_school_profile** — Get structured school data from its professional network URL. Cost: 1 credit.
- **enrich_student_list** — List students of a school. Supports filtering by major (boolean search), country, and student status. Cost: 3 credits per student returned.

### Job (3 tools)

- **enrich_job_profile** — Get structured data of a job posting from its professional network URL. Cost: 2 credits.
- **enrich_job_search** — Search job postings. Filter by company, job type, experience level, location, flexibility, and keyword. Cost: 2 credits.
- **enrich_job_count** — Count job postings matching your criteria. Same filters as job search. Cost: 2 credits.

### Search (2 tools)

- **enrich_company_search** — Search companies by location, industry, size, funding, founding year, and more. Uses boolean search syntax for many fields. Cost: 3 credits per URL returned.
- **enrich_person_search** — Search people by name, location, education, role, company, skills, and more. Requires `country` (ISO 3166). Uses boolean search syntax. Cost: 3 credits per URL returned.

### Meta (1 tool)

- **enrich_credit_balance** — Check your current Enrich Layer credit balance. Cost: 0 credits.

---

## Usage Guidelines

When the user asks to enrich, look up, or find information about companies or people, follow these rules:

### 1. Check credits first for large operations

Before running bulk enrichment (employee lists, person searches, company searches), call `enrich_credit_balance` to check the user's remaining credits. Warn them about the estimated cost before proceeding with expensive operations.

### 2. Choose the cheapest tool that answers the question

- If you already have a professional network URL, use a `_profile` tool (1 credit) instead of a `_lookup` tool (2 credits).
- Use `enrich_company_id_lookup` (0 credits) when you have a numeric company ID.
- Use `enrich_company_picture` or `enrich_person_picture` (0 credits) when only the avatar is needed.
- Use `enrich_disposable_email` (0 credits) to validate emails before spending credits on enrichment.

### 3. Chain tools efficiently

Many tasks require chaining two or more tools. Follow these common patterns:

- **Find a person's work email by role**: `enrich_role_lookup` (get profile URL) then `enrich_work_email` (get email). Total: 6 credits.
- **Find a person's work email by name**: `enrich_person_lookup` (get profile URL) then `enrich_work_email` (get email). Total: 5 credits.
- **Enrich a company from just a name**: `enrich_company_lookup` (get URL) then `enrich_company_profile` (get full data). Total: 3 credits. Or pass `enrich_profile: "enrich"` to get both in one call for 3 credits.
- **Find decision-makers at a company**: `enrich_company_lookup` (get URL) then `enrich_employee_list` with `boolean_role_search` set to the target roles.
- **Verify a contact**: `enrich_disposable_email` (free check) then `enrich_reverse_email` (find the profile).

### 4. Use the `enrich_profile` / `enrich_profiles` shortcut

Several lookup and list tools accept an `enrich_profile` or `enrich_profiles` parameter set to `"enrich"`. This returns full profile data inline, saving a separate profile call. Use it when you need full details and not just the URL.

### 5. Use boolean search syntax correctly

Employee search, company search, and person search support boolean operators in many fields:

- `OR` / `||` — match either term: `"founder OR co-founder"`
- `AND` — match both terms: `"engineer AND manager"`
- `NOT` — exclude: `"director NOT assistant"`
- Quotes for exact phrases: `"'Vice President'"`
- Max 255 characters for boolean expressions.

### 6. Control cache behavior

All profile tools accept `use_cache`:
- `"if-present"` — use cached data regardless of age (fastest, cheapest).
- `"if-recent"` — only use cache if the profile is less than 29 days old.

Default to `"if-present"` unless the user explicitly needs fresh data.

### 7. Handle pagination for list endpoints

`enrich_employee_list`, `enrich_student_list`, and search tools accept `page_size`. When enriching profiles inline (`enrich_profiles: "enrich"`), the max page size drops to 10. Plan accordingly for large lists.

### 8. Country codes

Several tools accept country/location filters. Always use ISO 3166-1 alpha-2 codes (e.g., `us`, `gb`, `de`, `sg`). For person search, the `country` parameter is required.

---

## Example Workflows

### Enrich a list of leads

User: "I have a list of company names. Enrich them all."

1. Call `enrich_credit_balance` to check available credits.
2. For each company name, call `enrich_company_lookup` with `enrich_profile: "enrich"` to get the URL and full profile in one call (3 credits each).
3. Present results in a table with name, industry, size, location, and URL.

### Find decision-makers at a company

User: "Find the CTO and VP Engineering at Stripe."

1. Call `enrich_role_lookup` with `company_name: "Stripe", role: "cto"` (3 credits).
2. Call `enrich_role_lookup` with `company_name: "Stripe", role: "vp engineering"` (3 credits).
3. For each result, call `enrich_work_email` to get their email (3 credits each).
4. Total: 12 credits for two contacts with emails.

### Verify and enrich a contact from an email

User: "What can you tell me about john@acme.com?"

1. Call `enrich_disposable_email` with the email (0 credits) to verify it is not throwaway.
2. Call `enrich_reverse_email` with `email: "john@acme.com"` (3 credits) to get their profile URL.
3. Call `enrich_person_profile` with the returned URL (1 credit) to get full details.
4. Total: 4 credits.

### Search for companies in a market segment

User: "Find SaaS startups in the US with 50-200 employees founded after 2018."

1. Call `enrich_company_search` with `country: "US"`, `industry: "software"`, `employee_count_min: "50"`, `employee_count_max: "200"`, `founded_after_year: "2018"`, `type: "PRIVATELY_HELD"` (3 credits per result).
2. Present results in a structured format.

### Find alumni from a school

User: "List recent computer science graduates from MIT."

1. Call `enrich_student_list` with the MIT professional network URL, `boolean_search_keyword: "computer science"`, `student_status: "past"`, `sort_by: "recently-graduated"` (3 credits per student).
2. Present results with names, majors, and profile URLs.
