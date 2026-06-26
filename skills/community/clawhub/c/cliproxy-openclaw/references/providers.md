# Providers and account onboarding

Use this file when the user needs help adding OAuth-backed providers or accounts inside CLIProxy.

## Typical provider classes

Users often want to add one or more of:
- Claude Code
- Gemini
- Codex or OpenAI-backed login
- Qwen
- iFlow

## Goal

The goal is not just successful sign-in. The real goal is:
- accounts are connected
- expected models appear
- requests can route through them

## Workflow

1. Have the user open the dashboard or management UI.
2. Add one provider or account at a time.
3. Confirm the provider finishes auth cleanly.
4. Check that models become visible or selectable.
5. If multi-account routing is needed, confirm the dashboard reflects that state.

## What to capture for downstream use

After onboarding, record:
- available model names
- whether routing or fallback is enabled
- any account grouping or aliasing the user expects

## Common failure patterns

- auth succeeded but no models appear
- model alias exists but upstream model is unavailable
- the provider is connected but rate-limited or quota-limited
- stale session or expired login causes silent failures

When that happens, move to `references/troubleshooting.md`.
