# AgentConcierge API Reference

## POST /api/recommend

**Endpoint:** `https://agentconcierge.io/api/recommend`  
**Rate limit:** 10 requests / 60 seconds per IP  
**Auth:** None required

### Request Body

```json
{
  "role":      "string (required) — user's job title or role",
  "painPoint": "string (required) — their primary time drain or challenge",
  "tools":     "string (optional) — current tools in their stack",
  "budget":    "string (optional) — monthly budget e.g. '$50', '$200', '$500+'",
  "teamSize":  "string (optional) — 'solo', 'small team', 'mid-size team', 'large organization'"
}
```

### Response

```json
{
  "recommendations": [
    {
      "id":           "uuid",
      "name":         "Agent Name",
      "tagline":      "Short description",
      "category":     "automation|content|marketing|engineering|operations|...",
      "marketplace":  "independent|n8n|hugging_face|zapier|openai_gpt_store|...",
      "pricingModel": "free|freemium|subscription|usage_based|enterprise",
      "pricePerMonth": 0,
      "tags":         ["tag1", "tag2"],
      "url":          "https://...",
      "matchScore":   92,
      "matchReasons": ["reason 1", "reason 2"]
    }
  ]
}
```

### Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Missing `role` or `painPoint` |
| 429 | Rate limit exceeded — retry after 60s |
| 500 | Internal error — try again |
| 503 | AI engine temporarily unavailable |

### Role Values (examples)

`Sales / Business Development`, `Marketing / Content`, `Engineering / Developer`,
`Operations / Management`, `Product / Design`, `Executive / Founder`,
`HR / Recruiter`, `Finance / Analyst`, `Customer Support`, `Freelancer / Consultant`,
`Researcher / Educator`, `Student`

### Budget Values (examples)

`$0` (free only), `$50`, `$200`, `$500`, `$500+`
