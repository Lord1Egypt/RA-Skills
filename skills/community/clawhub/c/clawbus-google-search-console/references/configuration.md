# Configuration

Read this file when authentication, connection setup, or property formatting is
unclear.

## Authentication

The bundled script accepts a MyBrandMetrics API key in either form:

- `--api-key "YOUR_API_KEY"`
- `MYBRANDMETRICS_API_KEY="YOUR_API_KEY"`

Prefer environment variables for routine use. Do not store real keys in this
repository.

## Connection ID

The script requires a Google Search Console connection ID configured in
MyBrandMetrics. Common examples:

- Domain property: `sc-domain:example.com`
- URL-prefix style connection: `https://www.example.com/`

Use the exact identifier configured in MyBrandMetrics. If a query returns no
rows, first verify that the connection ID matches the connected Search Console
property.

## Python Dependencies

The script needs Python 3 and `requests`:

```bash
python3 -m pip install requests
```

Install dependencies only when the user asks to run the query in the current
environment.

## Common Failures

- Missing API key: set `MYBRANDMETRICS_API_KEY` or pass `--api-key`.
- HTTP 401 or 403: the API key is missing, invalid, or not authorized for the
  connected Search Console account.
- Empty rows: the connection ID, filters, sitemap data, or MyBrandMetrics
  connection may not match the requested site.
- Rate limiting: retry later or reduce request volume.

## Security Rules

- Never commit API keys, access tokens, service account files, private keys, or
  OAuth credentials.
- Avoid printing keys in terminal logs.
- Redact credentials before sharing command output or screenshots.
