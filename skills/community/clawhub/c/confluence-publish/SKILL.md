---
name: confluence-publish
description: Publish, create, and update Confluence pages from HTML content.
required_env_vars:
  - EMAIL
  - DOMAIN
  - API_TOKEN
primary_credential: API_TOKEN
required_credentials:
  - EMAIL
  - DOMAIN
  - API_TOKEN
permissions:
  filesystem:
    read:
      - workspace
  network:
    allow:
      - https://*.atlassian.net
---

# Confluence Publish

Publish, create, and update Confluence pages from HTML content.

## What this skill does

This skill upserts Confluence pages through the Confluence REST API:

- If a page with the same title exists in the target space, it updates the page.
- If no page exists, it creates a new page.

It supports credentials from config, env file, or process environment variables.

## Actions

### `publish_page`

Create or update a Confluence page.

Expected input:
- `input`: HTML content, optionally with metadata JSON in the first HTML comment.
- `config`: runtime options and credentials.

Metadata comment format:

```html
<!--
{"space_key":"SPACE","page_title":"My Page","parent_page_id":"12345"}
-->
<h1>Body content</h1>
```

Alternative config keys:
- `space_key`
- `page_title`
- `parent_page_id` (optional)
- `body_html`
- `page_path` (path to a file in the current workspace containing metadata comment + body)

Credential options:
- `config.credentials.EMAIL`, `config.credentials.DOMAIN`, `config.credentials.API_TOKEN`
- `config.env_file` pointing to a `.env` style file in the current workspace
- Environment vars: `EMAIL`, `DOMAIN`, `API_TOKEN`

Security constraints:
- `config.env_file` and `config.page_path` must resolve to files under the current workspace directory.
- `DOMAIN` and optional `base_url` must target Atlassian Cloud (`https://<tenant>.atlassian.net/wiki`).

Success output includes:
- `status: "success"`
- `operation: "created" | "updated"`
- `page_id`
- `title`
- `url`
- `space_key`

### `test_connection`

Checks Confluence authentication and returns user identity info.

## Example call payload

```json
{
  "action": "publish_page",
  "input": "<!-- {\"space_key\":\"SPACE\",\"page_title\":\"Demo\"} --><h1>Hello</h1>",
  "config": {
    "credentials": {
      "EMAIL": "user@example.com",
      "DOMAIN": "exampletenant",
      "API_TOKEN": "your-token"
    }
  }
}
```
