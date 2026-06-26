# Authentication & Registration

## Registering a new account

Registration requires a credit card payment to activate. The flow is:

### Step 1 — Create the account

```bash
faces auth:register \
  --email user@example.com \
  --password 'SecurePass123!' \
  --username alice \
  --json
```

`--name` is optional — if omitted, the username is used as the display name.

The response includes:

```json
{
  "status": "registered",
  "user_id": "...",
  "activation_required": true,
  "activation_checkout_url": "https://checkout.stripe.com/c/pay/..."
}
```

The JWT is saved automatically. The account exists but is not yet active.

### Step 2 — Activate via payment

The `activation_checkout_url` is a Stripe Checkout page. The human must open it in a browser and complete payment.

Tell the user:

> Paste this link into your browser and complete the payment. When you see the confirmation page, come back here and let me know it's done.
>
> `<activation_checkout_url>`

Do **not** attempt to open the URL or complete payment programmatically. Only a human can do this step.

### Step 3 — Confirm activation

Once the user says payment is done:

```bash
faces billing:balance --json
```

Check that `is_active` is `true`. If not, tell the user the payment may not have gone through and ask them to try the link again.

### Full example

```bash
# 1. Register
RESULT=$(faces auth:register --email user@example.com --password 'SecurePass123!' --username alice --json)
URL=$(echo "$RESULT" | jq -r '.activation_checkout_url')

# 2. Give URL to human, wait for them to confirm payment

# 3. Verify
faces billing:balance --json | jq '.is_active'
```

## Logging in

For existing accounts:

```bash
faces auth:login --email user@example.com --password 'SecurePass123!'
```

The JWT is saved to `~/.faces/config.json` automatically.

To verify:

```bash
faces auth:whoami
```

## API key authentication

For non-interactive use (scripts, deployed agents), API keys are preferred over JWT:

```bash
# Create a key (requires JWT)
faces keys:create --name "my-agent" --budget 10.00 --expires-days 30

# Use it
faces config:set api_key sk-proj-...
# Or set the environment variable:
export FACES_API_KEY=sk-proj-...
```

API keys support optional restrictions:
- `--face USERNAME` — restrict to specific faces (repeatable)
- `--model NAME` — restrict to specific LLM models (repeatable)
- `--budget F` — spending cap in USD
- `--expires-days N` — auto-expiry

## Plans

### Free (pay-per-token)

- **Activation:** $5 minimum initial spend (added as API credits)
- **Compilation:** Charged per token used during extraction. Compiling a 1,000-token document costs more than 1,000 tokens because the platform makes multiple LLM calls to extract cognitive primitives. The exact cost depends on the source material and cannot be estimated in advance.
- **Inference:** Charged per token at the underlying provider's rate.
- **Markup:** 5% on all token usage (compilation and inference).
- **No monthly fee.**

### Connect ($17/month)

- **Compilation:** 100,000 tokens/month included. Same extraction cost structure as free — the quota is measured in tokens consumed during compilation, not source tokens.
- **Inference:** Charged per token with 5% markup, same as free — **except** for OpenAI gpt-5.x models when the user has linked their ChatGPT Plus/Pro subscription via `faces auth:connect openai`. Those requests route through the user's own OpenAI Codex subscription at no additional cost (no markup, no per-token charge from Faces).
- **ChatGPT passthrough:** Connect-plan users with a linked ChatGPT account get free inference on gpt-5.x models via `chat:responses`. See [OAUTH.md](OAUTH.md) for setup.

### Checking the current plan

```bash
faces billing:subscription --json   # plan, status, period end
faces billing:balance --json        # credit balance, is_active
faces billing:quota --json          # compile token usage and limits
```

### Upgrading

```bash
faces billing:checkout --plan connect
```

Returns a Stripe Checkout URL. The human must open it in a browser to complete payment.

## JWT vs API key

| Command group | Requires |
|---|---|
| `faces auth:*`, `faces keys:*` | JWT only — run `faces auth:login` first |
| Everything else | JWT **or** API key |

## Credential storage

Credentials are stored in `~/.faces/config.json`. The CLI reads from there automatically, or from environment variables:

| Variable | Purpose |
|---|---|
| `FACES_TOKEN` | JWT authentication token |
| `FACES_API_KEY` | API key authentication |

## Refreshing a token

If a JWT expires:

```bash
faces auth:refresh    # refresh existing token
faces auth:login ...  # or re-login
```
