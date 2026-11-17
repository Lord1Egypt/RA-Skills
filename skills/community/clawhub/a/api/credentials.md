# Credential Naming Convention

When working with multiple accounts for the same service, use this naming pattern:

## Format

```
{SERVICE}_{ACCOUNT}_{TYPE}
```

## Examples

| Variable Name | Purpose |
|---------------|---------|
| `STRIPE_PROD_API_KEY` | Production Stripe |
| `STRIPE_TEST_API_KEY` | Test/sandbox Stripe |
| `OPENAI_PERSONAL_API_KEY` | Personal OpenAI account |
| `OPENAI_COMPANY_API_KEY` | Company OpenAI account |
| `GITHUB_WORK_TOKEN` | Work GitHub PAT |
| `GITHUB_PERSONAL_TOKEN` | Personal GitHub PAT |

## Credential Types

| Type | Suffix |
|------|--------|
| API Key | `_API_KEY` |
| Access Token | `_TOKEN` |
| Secret Key | `_SECRET` |
| Client ID | `_CLIENT_ID` |
| Client Secret | `_CLIENT_SECRET` |

## Selection Rules

1. **Discover names, never values.** List candidate variables without printing secrets: `env | cut -d= -f1 | grep -i stripe`. Echoing a value puts it in shell history and transcripts.
2. **Exactly one match → use it. Multiple matches → ask which account.** Never pick prod by default; if the user hasn't specified, default to the test/sandbox variable when one exists.
3. **Live vs test is often visible in the key itself** — Stripe prefixes `sk_live_`/`sk_test_`. If the variable name says TEST but the value's prefix says live, stop and tell the user: mislabeled credentials cause real charges from "test" scripts.
4. **Rotation needs a grace window.** Issue the new key, deploy it everywhere, then revoke the old one — revoke-first means downtime for every consumer still holding the old key.

## Usage in curl

When the API reference shows `$API_KEY`, substitute your actual environment variable:

```bash
# Example from Stripe docs shows:
curl https://api.stripe.com/v1/charges -H "Authorization: Bearer $API_KEY"

# You would use your specific variable:
curl https://api.stripe.com/v1/charges -H "Authorization: Bearer $STRIPE_PROD_API_KEY"
```
