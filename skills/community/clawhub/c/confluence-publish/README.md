# Confluence Publish Skill

Create or update Confluence pages from Python using the Confluence REST API.

## Available Actions

| Action | Description |
|--------|-------------|
| `publish_page` | Upsert a page (update if title exists in space, otherwise create) |
| `test_connection` | Validate Confluence credentials and connectivity |

## Required Credentials

Provide credentials in one of these ways:

- `config.credentials` object with `EMAIL`, `DOMAIN`, `API_TOKEN`
- `config.env_file` path to a `.env`-style file in the current workspace
- process environment variables `EMAIL`, `DOMAIN`, `API_TOKEN`

`DOMAIN` can be:
- short domain (`exampletenant`)
- Atlassian domain (`exampletenant.atlassian.net`)
- full URL (`https://exampletenant.atlassian.net/wiki`)

Security constraints:
- `DOMAIN` and optional `base_url` must target Atlassian Cloud only (`https://<tenant>.atlassian.net/wiki`).
- `config.env_file` and `config.page_path` must resolve to files under the current workspace directory.

## Publish Input Format

`publish_page` accepts either:

- HTML input containing a metadata comment with JSON:

```html
<!--
{"space_key":"SPACE","page_title":"My Page","parent_page_id":"12345"}
-->
<h1>Body content</h1>
```

- or direct `config` keys: `space_key`, `page_title`, optional `parent_page_id`, and `body_html`

You can also pass `config.page_path` to load page input from a workspace file.

## Usage

```python
from main import handler

result = handler({
    "action": "publish_page",
    "input": '<!-- {"space_key":"SPACE","page_title":"Demo"} --><h1>Hello</h1>',
    "config": {
        "credentials": {
            "EMAIL": "user@example.com",
            "DOMAIN": "exampletenant",
            "API_TOKEN": "your-token"
        }
    }
})
```

## Local Testing

```bash
pytest tests/ -v
```
