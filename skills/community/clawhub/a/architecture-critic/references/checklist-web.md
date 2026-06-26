# Web / API Architecture Critic Checklist

Address each item explicitly in your review. "N/A" is a valid answer — state it.

## Payment & Charge Flow
- Does this touch any Stripe charge, intent, or webhook logic?
- Does this touch subscription or billing lifecycle (create, cancel, upgrade)?
- Does this touch payout or disbursement logic?
- Is any existing auto-charge or scheduled payment flow at risk of breaking?
- Are Stripe webhook secret and idempotency keys handled correctly?

## Auth & Data
- Are new database tables covered by row-level security (RLS) policies?
- Does any new endpoint expose a service key or bypass existing auth middleware?
- Are JWT/session tokens validated before any data mutation?
- Does this change user or account profile data in ways that affect existing records?
- Are API routes protected against unauthenticated access?

## Sacred / Protected Files
- Does the plan touch any file marked as protected (.sacred or equivalent)?
- Does the plan touch deployment config (vercel.json, next.config.js, etc.)?
- Does the plan touch environment variable handling or secrets loading?
- Are any critical cache headers or CDN rules at risk?

## Deployment & Environment
- Are all required environment variables confirmed to exist in the deployment target?
- Will this break staging/UAT before it can be tested?
- Does this require a database migration? Is the migration reversible?
- Does this require a Vercel project setting or domain change?
- Are there any cold-start or edge runtime constraints to consider?

## Architecture Drift
- Does this duplicate logic that already exists elsewhere in the codebase?
- Does this introduce a new pattern that conflicts with existing patterns?
- Does this add a dependency that's already available via an existing package?
- Does this create a new abstraction that should be merged with an existing one?

## Token / Cost (AI features only)
- Is any AI/LLM call on a hot path (per-request) instead of batch/async?
- Are there deterministic alternatives to any proposed AI calls?
- Is the chosen model the right size for the task (don't use GPT-4 to parse a date)?
- Are responses streamed or cached where appropriate?

## Integration Risk
- What external services does this touch? Are their rate limits and error modes handled?
- Does this add a synchronous dependency on a third-party API in a critical path?
- Are webhooks from external services validated (signature check)?
- Does this change any shared state that other services depend on?
