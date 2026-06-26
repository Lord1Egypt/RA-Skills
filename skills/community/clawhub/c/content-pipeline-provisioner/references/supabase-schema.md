# Supabase Schema — pipeline_clients

Table: `pipeline_clients`
Database: Xero AI Supabase project

## Columns

| Column | Type | Default | Description |
|---|---|---|---|
| id | uuid | gen_random_uuid() | Primary key |
| created_at | timestamptz | now() | When the row was created |
| stripe_session_id | text | — | Stripe checkout session ID from payment |
| name | text | — | Client's full name |
| email | text | — | Client's email address (for confirmation) |
| business_name | text | — | Their product or business name |
| product_description | text | — | What their product/service does (2-4 sentences) |
| target_audience | text | — | Who their audience is |
| brand_voice | text | — | 3 words describing their tone (e.g. "bold, educational, casual") |
| off_limits | text | nullable | Topics to never post about |
| twitter_username | text | — | Their Twitter/X handle (e.g. @yourbrand) |
| tiktok_username | text | — | Their TikTok handle (e.g. @yourbrand) |
| newsletter_platform | text | — | MailerLite / Beehiiv / ConvertKit / Other / none |
| newsletter_api_key | text | nullable | API key for their newsletter platform |
| telegram_username | text | nullable | Their Telegram username for briefings |
| notes | text | nullable | Any extra info they provided |
| status | text | 'pending' | Lifecycle state (see below) |
| cron_ids | jsonb | null | Array of registered cron job IDs |
| went_live_at | timestamptz | null | When status flipped to 'live' |

## Status Lifecycle

```
pending → building → live → cancelled
                   ↘ error
```

- `pending` — form submitted, not yet provisioned
- `building` — Evo is setting up the system, waiting for operator Postiz connection
- `live` — fully running, all crons active
- `cancelled` — subscription cancelled, crons disabled
- `error` — provisioning failed, needs manual review

## RLS Policies

- INSERT: anon (form submissions from the website)
- SELECT/UPDATE/DELETE: service role only (Evo reads/updates via service key)

## Supabase Connection

Use the service role key from `~/.openclaw/.env` or the Supabase secrets.
Project URL: read from environment / existing Supabase client config in the Larry scripts.
