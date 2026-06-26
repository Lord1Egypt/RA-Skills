# Crawleo OpenClaw Skill Examples

These examples show how to use the Crawleo wrapper API safely.

## Offline fake-fetch example

```bash
node examples/offline-fake-fetch.js
```

This example injects a fake `fetch` implementation and calls every wrapper method without network access, `CRAWLEO_API_KEY`, or Crawleo credit usage.

Covered methods:

- `client.search`
- `client.googleSearch`
- `client.googleMaps`
- `client.crawl`
- `client.headfulBrowser`

## Live usage template

```bash
CRAWLEO_API_KEY=... CRAWLEO_ENABLE_LIVE_EXAMPLE=1 node examples/live-usage-template.js
```

The live template exits successfully without making a request unless both `CRAWLEO_API_KEY` and `CRAWLEO_ENABLE_LIVE_EXAMPLE=1` are present. Never print or commit API key values.

Default verification should use the offline example only or rely on the template's safe skip behavior.

Optional live tests use the same two-part gate:

```bash
CRAWLEO_API_KEY=... CRAWLEO_ENABLE_LIVE_TESTS=1 npm run test:live
```

Without both variables, the live test file skips safely and exits 0.
