# Available Domain Search Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `available-domain-search`

x402 availability: not enabled for this product.

## `domains_check_availability`

Action slug: `domains-check-availability`

Price: `3` credits

Check if domain names are available for registration. Works with single domains or lists of multiple domains. Returns formatted results with availability status and registration options ready for display. IMPORTANT: Always display the registration links from the response to the user - each domain has a direct GoDaddy registration URL that must be shown.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domains` | `string` | yes | Domain name(s) to check for availability. Single domain: 'example.com' OR Multiple domains (comma-separated): 'example.com, test.org, mybrand.io'. Each domain must include TLD extension (.com, .net, .org, etc.). Automatically routes to exact search (1 domain) or bulk search (2+ domains). Maximum 1000 domains per request. |

Sample parameters:

```json
{
  "domains": "example domains"
}
```

Generated JSON parameter schema:

```json
{
  "domains": {
    "description": "Domain name(s) to check for availability. Single domain: 'example.com' OR Multiple domains (comma-separated): 'example.com, test.org, mybrand.io'. Each domain must include TLD extension (.com, .net, .org, etc.). Automatically routes to exact search (1 domain) or bulk search (2+ domains). Maximum 1000 domains per request.",
    "examples": [
      "example.com",
      "example.com, test.org, mybrand.io"
    ],
    "title": "Domains",
    "type": "string"
  }
}
```

## `domains_suggest`

Action slug: `domains-suggest`

Price: `3` credits

Generate domain name suggestions based on keywords, seed domains, or business descriptions. Returns an interactive widget with clickable domain links for clients that support HTML rendering (browsers, web-based AI assistants), with automatic fallback to formatted text for other clients. IMPORTANT: Always display the registration links from the response to the user - each domain has a direct GoDaddy registration URL that must be shown.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Maximum number of domain suggestions to return. Valid range: 1-100. Default: 40. |
| `query` | `string` | yes | Search query for domain suggestions. Can be: 1) Keywords (e.g., 'tech startup', 'coffee shop') 2) Seed domain name (e.g., 'example') 3) Business description (e.g., 'AI-powered customer service chatbot'). Maximum 300 characters. Longer queries will be optimized using AI. |

Sample parameters:

```json
{
  "limit": 40,
  "query": "example search query"
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "default": 40,
    "description": "Maximum number of domain suggestions to return. Valid range: 1-100. Default: 40.",
    "maximum": 100,
    "minimum": 1,
    "title": "Limit",
    "type": "integer"
  },
  "query": {
    "description": "Search query for domain suggestions. Can be: 1) Keywords (e.g., 'tech startup', 'coffee shop') 2) Seed domain name (e.g., 'example') 3) Business description (e.g., 'AI-powered customer service chatbot'). Maximum 300 characters. Longer queries will be optimized using AI.",
    "maxLength": 300,
    "minLength": 1,
    "title": "Query",
    "type": "string"
  }
}
```

## `get_instructions`

Action slug: `get-instructions`

Price: `3` credits

Get tool instructions and available actions.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```
