---
name: form2api
description: A web form reverse-engineering tool. Submit any login-required form once manually, and it automatically intercepts the real API requests, analyzes the structure, and generates reusable API documentation and call code — so you never have to fill out that form again. Triggers: reverse a form, find the API behind a form, intercept form requests, capture network requests, form to API, form2api, automate form submission, bulk submit form, generate API docs from form, what API does this form call, scrape form API, reverse engineer web form, form automation, no API docs, internal system API, batch form operations.
---

# Form2API

> **All you need to do: send me the form URL, then submit the form once manually. I'll handle the rest.**

**What it does:**
- Injects a network interceptor into the page to capture real API requests on form submission
- Analyzes the request structure, annotating which fields are user input vs fixed values vs auto-generated
- Generates complete API documentation with curl and Python examples
- Enables batch/automated operations without manual form filling

**Typical use cases:**
- Internal system forms are tedious — you want to create data in bulk via script
- You need to automate a workflow but there's no official API documentation
- You want to understand what APIs a form is actually calling under the hood

**How to trigger:**
Send me the form page URL and say something like "reverse this form" / "find the API for this form" / "I want to automate this form".

---

## Workflow (Agent execution steps)

### Step 1: Inject interceptor

After opening the target page, inject the interceptor script via the `browser` tool's `evaluate` action:

```
Read script content from:
<skill_dir>/scripts/inject_interceptor.js

Then execute it via browser(action=act) evaluate to inject into the page.
```

On success returns `{ status: 'injected' }`. Returns `already_active` if already injected.

### Step 2: Prompt user to submit the form

Tell the user:
> "Interceptor is ready. Please fill out and submit the form normally in the browser, then let me know when done."

### Step 3: Read captured results

After user submits, run evaluate to read captured requests:

```javascript
JSON.stringify(window.__capturedRequests)
```

Save the result to `/tmp/form_api_raw.json`.

### Step 4: Analyze requests

```bash
python3 <skill_dir>/scripts/analyze_requests.py /tmp/form_api_raw.json
```

Outputs a ranked list of candidate API requests. Structured result saved to `/tmp/form_api_analysis.json`.

### Step 5: Extract cookies

```bash
COOKIE=$(python3 <skill_dir>/scripts/extract_cookies.py <target_url>)
echo $COOKIE
```

Cookies are auto-cached in `/tmp/form_api_cookies/` for 1 hour. Repeated calls reuse the cache.

### Step 6: Generate API documentation

Based on the analysis, using `references/output_template.md` as reference, generate complete API docs including:
- Endpoint info (URL, method, content-type)
- Request parameter table (user input / fixed value / system-generated)
- Cookie extraction command
- curl and Python call examples

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/inject_interceptor.js` | Injected into page to hook fetch/XHR |
| `scripts/extract_cookies.py` | Standardized cookie extraction with caching |
| `scripts/analyze_requests.py` | Filter and annotate captured requests |

## Notes

- **Browser requirement**: The target page must already be open and logged in within the current browser session
- **Interceptor lifecycle**: Interceptor is cleared on page refresh — re-inject if needed
- **Multiple submissions**: `window.__capturedRequests` accumulates across submissions; analysis picks the most relevant batch
- **Cookie expiry**: If API returns 401/403, re-extract with `--force` flag
- **Output format reference**: `references/output_template.md`
