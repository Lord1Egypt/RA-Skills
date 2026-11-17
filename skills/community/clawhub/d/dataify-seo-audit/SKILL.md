---
name: dataify-seo-audit
description: "Audit a public webpage or website for crawlability, indexing signals, metadata, canonical URLs, headings, structured data, and evidence-backed SEO fixes. Use for technical or on-page SEO diagnosis. Do not use for keyword-only SERP lookup, paid advertising, or guaranteed ranking claims."
metadata:
  author: Dataify
  version: "1.1.1"
  documentation: https://doc.dataify.com
  support: https://www.dataify.com/
---

# Dataify SEO Audit

Produce a bounded technical and on-page SEO audit using live page evidence. Do not claim measured Core Web Vitals without field or lab performance data.

## Workflow

1. Normalize the public HTTP(S) URL and choose a page limit.
2. Run `scripts/run_seo_audit.py`; start with dry-run when scope is uncertain.
3. Inspect robots, sitemap and a stratified sample rather than the first URLs only. Read [audit-framework.md](references/audit-framework.md); use [site-type-playbooks.md](references/site-type-playbooks.md) when the site shape is clear.
4. Always run one `site:<domain>` indexation proxy. Run keyword SERPs only for user-supplied target keywords via `--keywords`.
5. Separate measured findings from external-only checks such as field Core Web Vitals, Search Console coverage and backlink authority.
6. Produce `report.json`, raw evidence and Markdown. Every finding must include layer, priority, impact, evidence and fix; follow [output-contract.md](references/output-contract.md).

## Quick Start

```bash
python3 scripts/run_seo_audit.py --url "https://www.dataify.com/" --max-pages 3 --output-dir seo-audit
```

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
