# SKILL: frontend-builder

## Purpose
Build frontend applications (React / Next.js / Vite) with predictable structure, accessibility, and safe API integration.

## When to Use
- A new UI app/page/component system is required.
- The task includes routing, state management, or API consumption.
- You need a repeatable scaffold with quality gates (lint/tests/build).

## Inputs
- `stack` (required, enum: `react-vite|nextjs|react-spa`).
- `ui_requirements` (required, string|object): pages, components, UX constraints.
- `api_contract` (optional, object): endpoints/events and schemas.
- `constraints` (optional, string[]): theming, perf, accessibility, browser support.

## Steps
1. Confirm scope:
   - routes/pages
   - global layout/navigation
   - state boundaries (server vs client)
2. Scaffold project in the target directory with minimal dependencies.
3. Implement component structure:
   - `components/`, `pages/`/`routes/`, `lib/`, `styles/`
4. Implement API client layer with:
   - base URL via env
   - timeouts
   - error normalization
5. Add accessibility and UX guardrails:
   - semantic HTML
   - keyboard navigation
   - loading/error states
6. Add tests (where the repo conventions support them).
7. Validate build/lint/test.

## Validation
- App builds cleanly.
- No secrets in client bundles.
- API calls handle errors and cancellations.
- Key user flows are covered by at least smoke tests.

## Output
- Files created/changed
- Run commands (`dev`, `build`, `test`)
- Notes about env vars and configuration

## Safety Rules
- Never embed API keys in frontend code; use server-side proxy if needed.
- Avoid untrusted HTML injection; sanitize where necessary.
- Prefer stable, well-maintained libraries.

## Example
Input:
- `stack`: `react-vite`
- `ui_requirements`: “Dashboard page + settings form; calls `/api/me`.”
Output: Vite project with `src/pages/Dashboard.tsx`, `src/lib/api.ts`, and build validation commands.

