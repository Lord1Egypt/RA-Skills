---
name: facebook
description: OpenClaw skill for Facebook Graph API workflows focused on Pages posting, comments, and Page management using direct HTTPS requests.
---

# Facebook Graph API Skill (Advanced)

## Purpose
Provide a production-oriented guide for building Facebook Graph API workflows for Pages: publishing posts, managing comments, and operating Page content safely using direct HTTPS calls.

## Best fit
- You need Page posting and comment workflows.
- You want a professional command design and safe operational guidance.
- You prefer direct HTTP requests rather than SDKs.

## Not a fit
- You need advanced ads or marketing APIs.
- You must use complex browser-based OAuth flows.

## Quick orientation
- Read `references/graph-api-overview.md` for base URLs, versions, and request patterns.
- Read `references/page-posting.md` for Page publishing workflows and fields.
- Read `references/comments-moderation.md` for comment actions and moderation flows.
- Read `references/permissions-and-tokens.md` for access types and scope guidance.
- Read `references/webhooks.md` for subscriptions and verification steps.
- Read `references/http-request-templates.md` for concrete HTTP request payloads.

## Required inputs
- Facebook App ID and App Secret.
- Target Page ID(s).
- Token strategy: user token → Page access token.
- Required permissions and review status.

## Expected output
- A clear Page workflow plan, permissions checklist, and operational guardrails.

## Operational notes
- Use least-privilege permissions.
- Handle rate limits and retries.
- Log minimal identifiers only.

## Security notes
- Never log tokens or app secrets.
- Validate webhook signatures.

## Credentials & Secret Management
This skill requires the following environment variables to be set:
- `FB_APP_ID` – Your Facebook App ID.
- `FB_APP_SECRET` – Your Facebook App Secret (highly sensitive).
- `FB_PAGE_ID` – The target Facebook Page ID.
- `FB_ACCESS_TOKEN` – A Page access token with sufficient permissions.

**Best practices:**
- Store secrets in a secure vault or environment manager; do not hardcode.
- Use different tokens for development and production.
- Rotate tokens periodically and after any suspected compromise.
- Restrict App Secret access to minimal personnel.

## Incident Response
If a token or secret is suspected to be leaked:
1. Immediately revoke the token in the Facebook Developer Dashboard.
2. Generate a new Page access token.
3. Rotate the App Secret if necessary.
4. Review logs for unauthorized usage.

## Authentication
All Graph API calls must include a valid access token either as a query parameter `access_token` or in the `Authorization: Bearer <token>` header. See `references/http-request-templates.md` for examples.

## Additional References
- `references/security-and-secrets.md` – Detailed security guidelines.
- `references/permissions-and-tokens.md` now includes environment variable requirements.
- `references/http-request-templates.md` includes authentication patterns.
