# Zero G Talent API Reference

All endpoints are public — no authentication required.

## Search Jobs

```
GET https://zerogtalent.com/api/jobs/search
```

### Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `q` | string | — | Full-text + fuzzy keyword search |
| `company` | string | — | Company slug filter (see `references/companies.md`) |
| `location` | string | — | Location slug (e.g., `california`, `remote`, `texas`, `new-york`) |
| `employmentType` | string | — | `full-time`, `internship`, `part-time`, `contract` |
| `remote` | string | — | `true` for remote-only jobs |
| `limit` | number | 10 | Results per page (max 50) |
| `offset` | number | 0 | Pagination offset |

### JSON Response

```json
{
  "jobs": [
    {
      "title": "Research Scientist, Alignment",
      "slug": "research-scientist-alignment",
      "externalId": "abc-123-def",
      "location": "San Francisco, CA",
      "remote": false,
      "employmentType": "Full-time",
      "category": "Research",
      "isActive": true,
      "salaryMin": 200000,
      "salaryMax": 350000,
      "salaryCurrency": "USD",
      "salaryInterval": "YEAR",
      "company": {
        "name": "Anthropic",
        "slug": "anthropic",
        "logoUrl": "https://zerogtalent.com/logos/anthropic.png"
      }
    }
  ],
  "total": 42,
  "hasMore": true,
  "pagination": { "offset": 0, "limit": 10, "total": 42 }
}
```

Salary fields (`salaryMin`, `salaryMax`, `salaryCurrency`, `salaryInterval`) are null when not available. For salary research, search multiple roles at a company to compare ranges.

## Get Job Description

```
GET https://zerogtalent.com/api/job?company={company-slug}&jobId={externalId}
```

Returns a `job` object with title, company, location, salary, and an HTML `description` field.

**Important:** Use `externalId` from search results, never `slug`. The `slug` is for URL display only.
