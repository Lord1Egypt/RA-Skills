# Mailfully API essentials

What a coding agent needs to send email through Mailfully: the base URL, keys, the send body, the
response, templates, batches, new-account pacing and the errors a migrating app will meet.

## Base URL and auth

- Base URL: `https://api.mailfully.com`. Every route is under `/v1`.
- Auth header: `Authorization: Bearer mf_test_…` (test key) or `Authorization: Bearer mf_live_…` (live key).
- The app reads the key from the `MAILFULLY_API_KEY` environment variable. The user pastes the key
  into the env file themselves. Never print the env file, never put a key on a command line, and never
  write a real key into any file.
- Bodies are JSON. Wire field names are snake_case (`reply_to`, `scheduled_at`). The one exception is
  the attachment field `contentType`, which is camelCase on the wire too.
- Every error comes back in one envelope: `{ "error": { "type": "...", "message": "...", "param": "..." } }`.
  `param` is present only when one field is at fault. Branch on `type`, show `message`.

The Node SDK (`mailfully` on npm, Node 24 or later) takes camelCase input and never throws: every
method returns `{ data, error }`, with `error.type`, `error.statusCode` and `error.param` on failure.

```ts mailfully-sdk
import { Mailfully } from "mailfully";

let client: Mailfully | undefined;

/** Gives up on a request with no answer after 10 seconds, like the `fetch` helper in rest-clients.md. */
const timedFetch: typeof fetch = (input, init) =>
  fetch(input, { ...init, signal: init?.signal ?? AbortSignal.timeout(10_000) });

/** Reads the key on first send, so importing this module never fails while the key is unset. */
export function getMailfully(): Mailfully {
  const apiKey = process.env.MAILFULLY_API_KEY;
  if (!apiKey) throw new Error("MAILFULLY_API_KEY is not set");
  return (client ??= new Mailfully({ apiKey, fetch: timedFetch }));
}
```

Build the client lazily, as above, never at module level: the module is imported by the code that
still sends through the old provider, so a module-level `new Mailfully(...)` or key check would crash
the app at startup (or fail `next build`) before `MAILFULLY_API_KEY` is set. The SDK refuses an
empty key, so `?? ""` is no fix. Without `timedFetch`, a request that never gets an answer waits as
long as the platform lets it; with it, the SDK returns an `error` whose `statusCode` is `null`, and
the outcome of that send is unknown (see `sendEach` in [migrate-sendgrid.md](migrate-sendgrid.md)).

## Replacing an existing send path

Whenever the Mailfully helper takes over mail the app already sends (a migration from any provider,
or a new integration that rewires an existing mailer), the old code stays and stays the default. Put
one `EMAIL_PROVIDER` check at the place mail leaves the app, and leave the old function exactly as it
was in the other branch:

```ts
import { sendWithOldProvider, type OutgoingEmail } from "./old-mailer"; // the existing code, unchanged
import { getMailfully } from "./mailfully"; // the client module above

// EMAIL_PROVIDER=mailfully selects Mailfully. Unset, or any other value, keeps the old provider.
export async function sendEmail(email: OutgoingEmail): Promise<void> {
  if (process.env.EMAIL_PROVIDER === "mailfully") {
    const { data, error } = await getMailfully().emails.send({
      from: email.from,
      to: email.to,
      subject: email.subject,
      html: email.html,
      text: email.text,
    });
    if (error) throw new Error(`Mailfully ${error.type ?? "error"} (${String(error.statusCode)}): ${error.message}`);
    if (data.status === "canceled") console.warn(`Mailfully sent nothing for ${data.id}: every recipient is suppressed`);
    return;
  }
  await sendWithOldProvider(email);
}
```

Each migration reference's `### Switch` example assumes a standalone function such as
`sendWelcome(to)`. When the send is written inline instead (a route handler that builds the message
and calls the old SDK in its body):

- Move the old code, unchanged, into a function of its own, returning what the handler used from it.
- Add the Mailfully function beside it, and switch between the two on `EMAIL_PROVIDER` as above.
- Keep the handler's response shape (status code and JSON body) the same on both branches.
- Where the old branch returned an error in the response (`Response.json({ error })`), catch the
  Mailfully error and return the same shape built from its fields, such as
  `{ error: { message: err.message } }`. An `Error` object serializes to `{}` in `Response.json` and
  `JSON.stringify`, so returning it as is loses the message.

A provider with no reference of its own here (Mailgun, Brevo, Mailjet, SparkPost, MailerSend, Loops,
django-anymail, a Rails `delivery_method` other than SMTP) maps onto the field table in Send below:
match each of its fields to a Mailfully one, split any per-recipient send into one send per
recipient (`sendEach` in [migrate-sendgrid.md](migrate-sendgrid.md)), and list in the report every
field that has no match. Several providers in one app get one such check at each send point.

## Test keys and live keys

- A test key (`mf_test_…`) runs the real send path but delivers to no real inbox. Use it until the
  user has verified a sending domain and decided to go live.
- In test mode the recipient's local part picks the simulated outcome:
  `bounce@…` simulates a hard bounce, `complaint@…` a spam complaint, `ooto@…` an out-of-office
  reply and `suppressionlist@…` an address already on a suppression list. Any other address simulates
  a delivery. The match is on the local part only and is case-insensitive, so `bounce@example.com`
  works.
- Test mode does not need a verified domain for `from` (unless the key was restricted to one domain).
- A live key (`mf_live_…`) sends real mail. Live sending needs a verified domain, and the `from`
  address must be on it.

## Send: `POST /v1/emails`

A message carries up to 50 recipients across `to`, `cc` and `bcc` combined, and at least one. It needs
at least one of `html`, `text` or `template`.

| Wire field | SDK field | Notes |
| --- | --- | --- |
| `from` | `from` | `"Acme <hello@example.com>"` or a bare address. Live mode: the domain must be verified. |
| `to` | `to` | A string or an array of strings. |
| `cc`, `bcc` | `cc`, `bcc` | A string or an array. Counted toward the recipient ceiling. |
| `reply_to` | `replyTo` | A string or an array. |
| `subject` | `subject` | Templates carry no subject, so send it here. |
| `html`, `text` | `html`, `text` | Send both when you have both. |
| `template` | `template` | `{ id, variables }`. See Templates below. |
| `attachments` | `attachments` | See Attachments below. |
| `tags` | `tags` | An array of `{ name, value }`. Both match `[A-Za-z0-9_-]+`. |
| `headers` | `headers` | Extra headers as an object. `From`, `Sender`, `Return-Path`, `X-Mailfully-Mid` and `X-SES-*` are reserved and refused (any letter case), and so is a name with a space or a colon. |
| `scheduled_at` | `scheduledAt` | ISO 8601 date-time such as `2026-10-07T09:00:00Z`, up to 90 days ahead. |
| `type` | `type` | `transactional` (the default) or `marketing`. See Marketing below. |

The request on the wire:

```http mailfully-rest
POST https://api.mailfully.com/v1/emails
Authorization: Bearer mf_test_…
Content-Type: application/json

{
  "from": "Acme <hello@example.com>",
  "to": ["user@example.com"],
  "reply_to": "support@example.com",
  "subject": "Your receipt",
  "html": "<p>Thanks for your order.</p>",
  "text": "Thanks for your order.",
  "tags": [{ "name": "kind", "value": "receipt" }],
  "attachments": [
    { "filename": "receipt.pdf", "content": "JVBERi0xLjcK", "contentType": "application/pdf" }
  ]
}
```

The same send with the SDK:

```ts mailfully-sdk
import { Mailfully } from "mailfully";

export async function sendReceipt(mailfully: Mailfully, to: string, pdfBase64: string): Promise<string> {
  const { data, error } = await mailfully.emails.send({
    from: "Acme <hello@example.com>",
    to,
    replyTo: "support@example.com",
    subject: "Your receipt",
    html: "<p>Thanks for your order.</p>",
    text: "Thanks for your order.",
    tags: [{ name: "kind", value: "receipt" }],
    attachments: [{ filename: "receipt.pdf", content: pdfBase64, contentType: "application/pdf" }],
  });
  if (error) throw new Error(`Mailfully ${error.type ?? "error"} (${String(error.statusCode)}): ${error.message}`);
  if (data.status === "canceled") {
    console.warn(`Mailfully accepted ${data.id} but sent nothing: every recipient is suppressed`);
  }
  return data.id;
}
```

An app that already retries failed sends can pass an `Idempotency-Key` header (SDK:
`mailfully.emails.send(input, { idempotencyKey })`) so a retried request is not sent twice.

### Attachments

- Each attachment is `{ "filename", "content", "contentType" }`, plus an optional `cid` for an inline
  image referenced as `cid:` in the HTML.
- `content` is bare base64. Never add a `data:` URI prefix; the API refuses it with a 422.
- `contentType` stays camelCase on the wire. It is the only camelCase wire field.
- The total base64 across all attachments may not exceed 40 MiB.

### Marketing

`type: "marketing"` allows exactly one recipient across `to`, `cc` and `bcc`, and needs a postal
address on file for the account. This skill does not migrate marketing or bulk mail in v1: an old
provider's unsubscribe lists cannot be imported, so such sends would lose their opt-outs. Recognise
those sends (newsletters, campaigns, list sends), leave them on the old provider, and tell the user.

## Response

A send returns HTTP 202 with the accepted message:

```json
{
  "object": "email",
  "id": "01K6T0V1Q5H8C3D7E9F2G4J6KM",
  "status": "queued",
  "type": "transactional",
  "to": ["user@example.com"],
  "cc": [],
  "bcc": [],
  "from": "Acme <hello@example.com>",
  "subject": "Your receipt",
  "scheduled_at": null,
  "created_at": "2026-10-03T12:00:00.000Z"
}
```

- `status` is `queued` (it will be sent, or sent at `scheduled_at`) or `canceled`.
- `canceled` means suppression removed every `to` recipient (or every recipient), because those
  addresses hard-bounced, complained or were blocked earlier. It is not an error and the call
  succeeded, but nothing will be sent. Report it to the user; never describe a canceled send as sent.

## Status vocabulary

- `GET /v1/emails/{id}` returns `last_event` in STATUS words. Examples: `queued`, `sending`, `sent`,
  `delivered`, `bounced`, `complained`, `failed`, `rejected`, `held`, `canceled`, `suppressed`,
  `unsubscribed`, `paused`. The list is not complete, so never match on it exhaustively.
- Only `delivered` means delivered. Six words mean the message is still on its way: `queued`,
  `sending`, `sent`, `held`, `paused_hold` and `released`. Keep polling on those up to a deadline,
  then report the last value instead of claiming success. Every other word, including one not listed
  here, is final and not delivered: `bounced` and `complained` are delivery failures, and `failed`,
  `rejected`, `canceled`, `suppressed` and the rest mean the message will not be sent. Stop and
  report it.
- `GET /v1/emails/{id}/events` lists the message's events under different names: `send`, `delivery`,
  `bounce`, `complaint`, `open`, `click`.
- Poll `last_event` for `delivered`, never for `delivery`: a loop waiting for `last_event == "delivery"`
  never ends.

## Templates

- Send a stored template with `template: { id, variables }`. Template ids start with `tmpl_`.
- Placeholders are `{{ name }}`, with optional spaces inside the braces. Keys are flat: `{{ user.name }}`
  looks up the literal key `"user.name"`, never `variables.user.name`.
- Values are HTML-escaped in the HTML body and inserted as is in the text body. A missing variable
  renders as an empty string, unless the template's variables schema marks it required: then the send
  is refused with 422 `validation_error` and `param` `variables.<key>`.
- There are no loops, conditionals or partials. If the app's email needs them, render it with the
  app's own template engine and send `html` and `text` instead.

## Batch: `POST /v1/emails/batch`

- The body is a JSON array of send objects (the same shape as `POST /v1/emails`), up to 100 messages
  per request. Each message still holds up to 50 recipients.
- The response is `{ "data": [ ...one accepted message per input... ] }` in input order. SDK:
  `mailfully.emails.batch([...])`.
- The batch is all or nothing: one invalid message refuses the whole request, and a 422 names the
  index in `param` (for example `[3].to`).
- New-account pacing counts every recipient in the batch together, so a new account should send
  per-recipient mail one request at a time instead of batching it (see below).

## New-account pacing

A new account's live mail is paced per minute. Build the integration so pacing never loses mail:

- Send per-recipient mail (receipts, password resets, notifications) as one request per recipient,
  one request at a time, in sequence. Never collapse a per-recipient loop into one `to` array: every
  recipient would see every other recipient's address.
- On 429 `send_rate_limited`, wait the number of seconds in the `retry-after` header, then send the
  same request again. The SDK's `{ data, error }` result carries no response headers. The
  ready-made loop for any integration, SendGrid or not, is `sendEach` in `migrate-sendgrid.md`
  ([migrate-sendgrid.md](migrate-sendgrid.md)), in SDK, Node `fetch` and Python versions; it reads
  `retry-after` through a wrapped `fetch`, and the TypeScript and Python helpers in
  [rest-clients.md](rest-clients.md) put it on their errors.
- On 422 `young_sender_batch_too_large`, the single request names more recipients than a new account
  may send in a minute, so waiting never helps. Split it into smaller requests and send them in
  sequence.
- Test mode is not paced.

## Errors

| Type | Status | Fix |
| --- | --- | --- |
| `missing_api_key` | 401 | No `Authorization` header. Check that the app loads `MAILFULLY_API_KEY`. |
| `invalid_api_key` | 401 or 403 | The key is wrong or revoked. Ask the user to create a new key in the dashboard and paste it into the env file. |
| `insufficient_scope` | 403 | The key lacks the scope for this route. Webhook endpoints are managed in the dashboard, not with an API key. |
| `validation_error` | 422 | The body failed validation; `param` names the field. A live send whose `from` domain is not verified is this error with `param` `from`. |
| `unverified_domain_required` | 403 | Live key with no verified sending domain. The error carries `next_action` (`add_domain`, `finish_domain_dns` or `fix_domain_dns`) and `action_url`, a dashboard link to that step; tell the user to open it. A test key keeps working meanwhile. |
| `domain_not_verified` | 409 | Receiving was turned on for a domain that has not verified yet. Wait for verification, then try again. |
| `marketing_single_recipient` | 422 | A marketing send named more than one recipient. Leave marketing mail on the old provider (see Marketing). |
| `marketing_missing_postal_address` | 422 | A marketing send with no postal address on file. Leave marketing mail on the old provider. |
| `recipient_unsubscribed` | 422 | The recipient opted out of this account's marketing mail. Transactional mail to them still sends. |
| `rate_limit_exceeded` | 429 | Too many API requests too quickly. Wait for `retry-after`, then retry. |
| `send_rate_limited` | 429 | New-account pacing. Wait `retry-after` seconds, then resend the same request. |
| `young_sender_batch_too_large` | 422 | One request names more recipients than a new account may send in a minute. Split it into smaller requests. |
| `account_under_review` | 429 | New accounts are reviewed before full-volume sending. Wait for the review to finish; tell the user. |
| `daily_quota_exceeded` | 429 | A daily limit is used up. Wait for `retry-after`. On a live Free plan (100 a day), upgrading raises it; test mode has its own daily cap, which upgrading does not change. |
| `monthly_quota_exceeded` | 429 | The plan's monthly allowance is used up. Upgrade the plan to keep sending this month. |
| `spend_cap_exceeded` | 429 | The account's monthly spend cap is reached. Tell the user; sending resumes next month, or sooner if the cap is raised (contact@mailfully.com). |
| `volume_limit_reached` | 429 | The account reached its daily sending volume limit. Tell the user to contact contact@mailfully.com to raise it. Test keys keep working. |
| `payment_past_due` | 402 | Live sending is paused because a payment is past due. The user updates the payment method on the dashboard's Billing page; sending resumes once it goes through. |
| `account_suspended` | 403 | Live sending is suspended because setup was never completed. Verifying a sending domain resumes it. |
| `account_rejected` | 403 | The account was not approved for live sending. Only Mailfully can reverse this; tell the user to contact contact@mailfully.com. |

## The smoke script

Phase 4 of the main skill writes a temporary script that sends one test email through the new
helper. Before it sends, it loads the env file the way the app does, because the helper reads
`MAILFULLY_API_KEY` from the environment on first send:

- Node: run it with `node --env-file=<envfile>` or `tsx --env-file=<envfile>` (Node 20.6 or later;
  on older Node use `dotenv`), or call `@next/env`'s `loadEnvConfig` first in a Next.js app.
  `import "dotenv/config"` works only when the env file is `.env`; for another file, pass its path
  to `dotenv`.
- Python: `python-dotenv` when the project already has it; Django settings for a Django app. A
  Python app with no `python-dotenv`: ask the user before adding it. Without that yes, the script
  reads the env file itself, in code, keeps only the `MAILFULLY_API_KEY=` line and sets it in
  `os.environ`, and never prints it (the snippet below, at the top of the script, with `ENV_FILE`
  set to the env file from phase 0). The agent still never opens the env file in a shell.
- Rails: `bin/rails runner`, which loads the app's environment.
- TypeScript or JavaScript: put the body in an `async function main()` called at the end, never
  top-level `await`. `tsx` refuses top-level `await` in a project without `"type": "module"` (the
  error says it is not supported with the cjs output format).
- If the helper imports `server-only`, add `--conditions=react-server` to the Node command; never
  remove the import.

```python
import os

ENV_FILE = ".env"  # the env file the app loads


def load_mailfully_key(path=ENV_FILE):
    """Set MAILFULLY_API_KEY from the env file, keeping only that line. Never prints the value."""
    if os.environ.get("MAILFULLY_API_KEY"):
        return
    with open(path, encoding="utf-8") as env_file:
        for raw in env_file:
            line = raw.strip()  # surrounding whitespace, and the \r of a Windows line ending
            if line.startswith("export "):
                line = line[len("export "):].lstrip()
            name, sep, value = line.partition("=")
            if not sep or name.strip() != "MAILFULLY_API_KEY":
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            os.environ["MAILFULLY_API_KEY"] = value
            return


load_mailfully_key()
```

## Checking a send

With the CLI (Node 24 or later on the machine running it, after the user has run
`npx -y mailfully@1.4.0 login` and pasted the key into its hidden prompt):

```bash
npx -y mailfully@1.4.0 emails get <id> --json
npx -y mailfully@1.4.0 emails events <id> --json
```

### Logging the CLI in

The user runs `npx -y mailfully@1.4.0 login` in their own terminal window, where it reads the key
through a hidden prompt. On macOS they can instead copy the key and then type this at the agent
session's prompt, where `!` runs it in the session's shell. The CLI reads one line from the pipe,
and `echo` adds the line ending a copied key lacks (without it the CLI reads nothing):

```bash
# The user types this right after copying the key. Never run it yourself.
! { pbpaste; echo; } | npx -y mailfully@1.4.0 login
```

With the user present on Node 24 or later, the browser form needs no key to be copied at all:

```bash
npx -y mailfully@1.4.0 login --web --no-wait --write-env <envfile> --json
npx -y mailfully@1.4.0 login --web --wait --timeout 90
```

The first prints a link and a code for the user to open and approve; the second waits and exits 3
while the request is still pending, so run it again. If a live key is already stored, both need
`--force`. The key it creates is a test key. The agent never opens the link or approves for the user.

Either way, `login` confirms with the key's prefix and last four characters, the same hint the
dashboard shows. That is expected; the agent never repeats it or prints any part of the key itself.

### Without the CLI

The CLI needs Node 24 or later on the MACHINE that runs it. That is separate from the Node version
the project targets. When the machine's Node is older:

- The phase-4 smoke script does the status poll, because it reads the key the way the app does.
- Domain steps happen in the dashboard: Domains, then Add domain. The dashboard shows the DNS records
  and offers one-click DNS setup for supported DNS providers.
- There is no `curl` path that reads the key in a shell. Never print the env file or copy the key into
  a command.

## Pricing

Free for 3,000 emails a month. Paid plans start at $5 a month for 10,000. See
https://mailfully.com/pricing.
