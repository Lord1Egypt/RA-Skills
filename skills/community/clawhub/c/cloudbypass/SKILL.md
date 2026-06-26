---
name: cloudbypass
description: Use Cloudbypass API (穿云API/穿云) to fetch pages protected by Cloudflare/Turnstile/JS challenge. Use when normal requests fail with challenge/403 and compliant protected-page retrieval is required. Requires CLOUDBYPASS_APIKEY; V2/V2S also require CLOUDBYPASS_PROXY.
---

Use the bundled script to call Cloudbypass API.

- Script: `{baseDir}/scripts/cloudbypass_request.js`

Required env:
- `CLOUDBYPASS_APIKEY` (required)
- `CLOUDBYPASS_PROXY` (required for V2/V2S)
- `CLOUDBYPASS_PART` (optional, default: `0`)
- `CLOUDBYPASS_SITEKEY` (optional)

Security / usage notes:
- API key is sent to `api.cloudbypass.com` to perform requests and may incur billing.
- Review legal/ethical permissions before bypassing site protections.
- For autonomous usage, scope targets and monitor/rotate keys.

## Quick usage

```javascript
const skill = await openclaw.getSkill('cloudbypass');

// V1 (simple)
const r1 = await skill.get('https://example.com');

// V2 (challenge-heavy; proxy required)
const r2 = await skill.requestV2({
url: 'https://example.com',
proxy: process.env.CLOUDBYPASS_PROXY
});