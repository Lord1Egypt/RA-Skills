# Migrating from SendGrid

SendGrid's v3 send packs several messages into one request (`personalizations`, `isMultiple`).
Mailfully sends one message per request, so the main job is to keep every recipient's message
separate. Templates, schedules and categories map with small changes.

Read [api-essentials.md](api-essentials.md) first for the send body, test keys and errors. The Node SDK
needs Node 24 or later. On an older Node, use the `fetch` helper in [rest-clients.md](rest-clients.md)
(its errors carry `retryAfterSec`); in Python, use the Python helper there (its errors carry
`retry_after`). The mapping below holds for both, with snake_case wire keys.

## Detect

- npm: `@sendgrid/mail` (`sgMail.setApiKey(...)`, `sgMail.send(...)`, `sgMail.sendMultiple(...)`),
  `@sendgrid/client`, `@sendgrid/helpers`, `@sendgrid/eventwebhook`.
- Python: `sendgrid` on PyPI (`from sendgrid import SendGridAPIClient`,
  `from sendgrid.helpers.mail import Mail`, `Mail(from_email, to_emails, subject, html_content)`),
  and `from sendgrid.helpers.eventwebhook import EventWebhook` for webhooks.
- Raw API calls to `https://api.sendgrid.com/v3/mail/send`.
- Environment: `SENDGRID_API_KEY`, and the Event Webhook verification key (any name; it holds a
  public key, not a shared secret).

## Field map

| SendGrid Node (`@sendgrid/mail`) | SendGrid Python (`Mail`) | Mailfully SDK | Wire |
| --- | --- | --- | --- |
| `from` | `from_email` | `from` | `from` |
| `to` | `to_emails` | `to` | `to` |
| `cc`, `bcc` | `message.cc`, `message.bcc` | `cc`, `bcc` | `cc`, `bcc` |
| `replyTo` | `message.reply_to` | `replyTo` | `reply_to` |
| `subject` | `subject` | `subject` | `subject` |
| `text`, `html` | `plain_text_content`, `html_content` | `text`, `html` | `text`, `html` |
| `isMultiple: true`, `sendMultiple()` | `is_multiple=True` | one `emails.send` per recipient | one request per recipient |
| `personalizations` (more than one) | `add_personalization()` | one `emails.send` per personalization | one request each |
| `templateId` + `dynamicTemplateData` | `template_id` + `dynamic_template_data` | `template: { id, variables }`, flat templates only | `template` |
| `sendAt` (Unix seconds) | `send_at` | `scheduledAt` (UTC ISO string) | `scheduled_at` |
| `categories` | `category` | `tags`: `{ name: "category", value }` | `tags` |
| `customArgs` | `custom_arg` | `tags`, or drop | `tags` |
| `headers` | `header` | `headers` | `headers` |
| `attachments[].content` (base64) | `Attachment(FileContent(...))` | `content` | `content` |
| `attachments[].type` | `FileType` | `contentType` | `contentType` |
| `attachments[].content_id` + `disposition: "inline"` | `ContentId`, `Disposition` | `cid` | `cid` |
| `mailSettings.sandboxMode` | `mail_settings.sandbox_mode` | a test key (`mf_test_…`) | |
| `asm`, unsubscribe groups | `asm` | not supported (see below) | |
| `trackingSettings` | `tracking_settings` | per sending domain, in the dashboard | |
| `x-message-id` response header | `response.headers["X-Message-Id"]` | `data.id` (a ULID such as `01K6T0V1Q5H8C3D7E9F2G4J6KM`), plus `data.status` | `id`, `status` |

A Mailfully send can return `status: "canceled"`: every recipient was suppressed and nothing will be
sent. SendGrid reported that later as a `dropped` event. Log it or report it; never count it as sent.

## Before and after

### A single send

Before:

```js
const sgMail = require("@sendgrid/mail");

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

async function sendWelcome(to) {
  await sgMail.send({
    to,
    from: "Acme <hello@example.com>",
    replyTo: "support@example.com",
    subject: "Welcome to Acme",
    text: "Welcome aboard.",
    html: "<p>Welcome aboard.</p>",
    categories: ["Welcome Email"],
  });
}
```

After:

```ts mailfully-sdk
import { Mailfully } from "mailfully";

let client: Mailfully | undefined;

// A request with no answer gives up after 10 seconds (see api-essentials.md).
const timedFetch: typeof fetch = (input, init) =>
  fetch(input, { ...init, signal: init?.signal ?? AbortSignal.timeout(10_000) });

// Lazy: importing this module never fails while MAILFULLY_API_KEY is unset (see api-essentials.md).
function getMailfully(): Mailfully {
  const apiKey = process.env.MAILFULLY_API_KEY;
  if (!apiKey) throw new Error("MAILFULLY_API_KEY is not set");
  return (client ??= new Mailfully({ apiKey, fetch: timedFetch }));
}

export async function sendWelcome(to: string): Promise<string> {
  const { data, error } = await getMailfully().emails.send({
    from: "Acme <hello@example.com>",
    to,
    replyTo: "support@example.com",
    subject: "Welcome to Acme",
    text: "Welcome aboard.",
    html: "<p>Welcome aboard.</p>",
    tags: [{ name: "category", value: "welcome-email" }],
  });
  // The SDK never throws. statusCode is null when the request never reached the API.
  if (error) throw new Error(`${error.type ?? "error"} (${String(error.statusCode)}): ${error.message}`);
  if (data.status === "canceled") console.warn(`Mailfully sent nothing for ${data.id}: every recipient is suppressed`);
  return data.id;
}
```

SendGrid rejects with an error carrying `code` and `response.body.errors`; Mailfully returns
`error.statusCode`, `error.type` and `error.message`. Branch on `error.type`, using the Errors table
in [api-essentials.md](api-essentials.md).

### Python

Before:

```python
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_welcome(to_email):
    message = Mail(
        from_email="hello@example.com",
        to_emails=to_email,
        subject="Welcome to Acme",
        html_content="<p>Welcome aboard.</p>",
    )
    response = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY")).send(message)
    return response.status_code
```

After (with `send_email` from the Python helper in [rest-clients.md](rest-clients.md)):

```python mailfully-rest
# send_email (mailfully_client.py, from rest-clients.md) POSTs to https://api.mailfully.com/v1/emails.
import logging

from mailfully_client import send_email

logger = logging.getLogger(__name__)


def send_welcome(to_email):
    email_id, status = send_email({
        "from": "Acme <hello@example.com>",
        "to": to_email,
        "subject": "Welcome to Acme",
        "html": "<p>Welcome aboard.</p>",
        "text": "Welcome aboard.",
    })
    if status == "canceled":
        logger.warning("Mailfully sent nothing for %s: every recipient is suppressed", email_id)
    return email_id
```

`python_http_client.exceptions.HTTPError` becomes the helper's `MailfullyError`, with `.type`,
`.status`, `.param` and `.retry_after`.

### Several recipients who must not see each other

`isMultiple: true` (Python `is_multiple=True`), `sgMail.sendMultiple()`, `sgMail.send(msg, true)` and a
`personalizations` array with more than one entry all mean the same thing: each recipient gets their
own copy. Never put several recipients who should not see each other in one `to` array. Every
recipient would see every other recipient's address.

The Mailfully equivalent is one `emails.send` per recipient, sent one at a time, in order. Two kinds
of failure need care:

- **Pacing.** On a new account, live mail is paced per minute. A 429 `send_rate_limited` (or
  `rate_limit_exceeded`) names the wait in its `retry-after` header; send the same request again
  after that wait. The SDK result does not expose response headers, so the helper below reads
  `retry-after` through a wrapped `fetch`.
- **No answer, a timeout, or a 5xx.** The request may have been accepted before the connection
  dropped, so its outcome is unknown. Each message carries an `Idempotency-Key` built from the key
  kind, a run id the caller chooses and the message's index (`<test|live>:<runId>:<index>`). Sending
  the same key with the same body again within 24 hours returns the original accepted message
  instead of sending a second one. So the helper retries these a few times with the same key, and
  running the whole list again with the same run id, the same order and the same bodies within 24
  hours is safe. Test and live keys share one key space per account, which is why the key kind is
  part of every key. A key may be up to 256 characters (a longer one is 400 `invalid_idempotency_key`),
  so keep run ids short. After a request with that key was accepted, reusing it with a different
  body is 409 `invalid_idempotent_request`; while the first request is still in flight, the key gets
  409 `concurrent_idempotent_requests`, which the helper also waits out. Once any attempt for a
  message ended unknown, the message stays unknown even if a later attempt is refused, because a
  refusal from the rate limiter or auth does not say whether the earlier attempt went through.

The run id comes from an id the app already has for the event that sends the mail: the new user's
id for a welcome email (a signup route has just created it), the order id for a receipt, the project
id here. Never use a random id: a retried request then gets a new run id, so it is not deduplicated
and can send every message again.

Before:

```js
await sgMail.send({
  to: project.memberEmails,
  from: "Acme <hello@example.com>",
  subject: `${project.name} was archived`,
  text: `${project.name} was archived. You can restore it for 30 days.`,
  isMultiple: true,
});
```

After (save as `lib/mailfully-send-each.ts`):

```ts mailfully-sdk
import { setTimeout as sleep } from "node:timers/promises";
import { Mailfully, type SendEmailInput } from "mailfully";

/** Attempts per message, every cause together. */
const MAX_ATTEMPTS = 10;
/** Retries per message after no answer, a 5xx or a key still in flight. */
const MAX_UNKNOWN_RETRIES = 3;
/** A request with no answer by then is abandoned and counted as unknown. */
const REQUEST_TIMEOUT_MS = 15_000;

/**
 * A client that remembers the last `retry-after` header it saw. The SDK result has no headers,
 * so a wrapped fetch reads it. Safe only for one request at a time, which is how sendEach uses it.
 */
function createPacedMailfully(apiKey: string): { mailfully: Mailfully; retryAfterSec: () => number } {
  let retryAfterSec = 0;
  const pacedFetch: typeof fetch = async (input, init) => {
    const res = await fetch(input, { ...init, signal: init?.signal ?? AbortSignal.timeout(REQUEST_TIMEOUT_MS) });
    retryAfterSec = Number(res.headers.get("retry-after")) || 0;
    return res;
  };
  return { mailfully: new Mailfully({ apiKey, fetch: pacedFetch }), retryAfterSec: () => retryAfterSec };
}

export interface SendEachResult {
  /** Accepted messages, including ones a re-run got back from an earlier run. */
  sent: { index: number; id: string; status: "queued" | "canceled" }[];
  /**
   * Set when sending stopped. Messages after `index` were not sent. The message AT `index` was
   * refused when `outcome` is "refused" (every attempt got a 4xx). When it is "unknown" (some attempt
   * got no answer, timed out or got a 5xx) it may have been accepted: run sendEach again with the
   * same key kind, runId, order and messages within 24 hours, and the API returns the earlier result
   * for anything it already accepted.
   */
  stoppedAt: {
    index: number;
    outcome: "refused" | "unknown";
    statusCode: number | null;
    type: string | null;
    message: string;
  } | null;
}

/**
 * Sends each message in its own request, one at a time, in order. `runId` names this job with an
 * id the app already has for the event (the new user's id, the order id) and must be the same on a
 * re-run of the same job, with the same order. A random runId means a retried request is not
 * deduplicated: it can send every message again.
 */
export async function sendEach(apiKey: string, runId: string, messages: SendEmailInput[]): Promise<SendEachResult> {
  const { mailfully, retryAfterSec } = createPacedMailfully(apiKey);
  // Test and live keys share one key space per account, so the key kind is part of every key.
  const kind = apiKey.startsWith("mf_live_") ? "live" : "test";
  const result: SendEachResult = { sent: [], stoppedAt: null };
  for (const [index, message] of messages.entries()) {
    const idempotencyKey = `${kind}:${runId}:${index}`;
    let unknownRetries = 0;
    let everUnknown = false;
    for (let attempt = 1; ; attempt++) {
      const { data, error } = await mailfully.emails.send(message, { idempotencyKey });
      if (!error && data) {
        result.sent.push({ index, id: data.id, status: data.status });
        break;
      }
      // No error and no data: a 2xx whose body could not be read, so the outcome is unknown.
      const code = error ? error.statusCode : null;
      const paced = error?.type === "send_rate_limited" || error?.type === "rate_limit_exceeded";
      const unknown = code === null || code >= 500 || error?.type === "concurrent_idempotent_requests";
      everUnknown ||= unknown;
      if (paced && attempt < MAX_ATTEMPTS) {
        await sleep(Math.max(retryAfterSec(), 1) * 1000);
        continue;
      }
      if (unknown && attempt < MAX_ATTEMPTS && unknownRetries < MAX_UNKNOWN_RETRIES) {
        unknownRetries++;
        await sleep(2 ** unknownRetries * 1000);
        continue;
      }
      result.stoppedAt = {
        index,
        outcome: everUnknown ? "unknown" : "refused",
        statusCode: code,
        type: error?.type ?? null,
        message: error?.message ?? "the API answered 2xx with a body that could not be read",
      };
      return result;
    }
  }
  return result;
}

/** The isMultiple send above: one message per member, each addressed to that member alone. */
export function notifyArchived(
  apiKey: string,
  projectId: string,
  memberEmails: string[],
  projectName: string,
): Promise<SendEachResult> {
  return sendEach(
    apiKey,
    `project-archived:${projectId}`,
    memberEmails.map((to) => ({
      from: "Acme <hello@example.com>",
      to,
      subject: `${projectName} was archived`,
      text: `${projectName} was archived. You can restore it for 30 days.`,
    })),
  );
}
```

Report `stoppedAt` to the user when it is set, with its `outcome`, and any `canceled` entry in
`sent`. Never describe an `unknown` message as not sent. The key only protects a re-run that keeps
the same key kind, run id, message order and message bodies, within 24 hours.

A `personalizations` send becomes one message per personalization. Build each from that
personalization's own fields: `to`, `cc`, `bcc`, `subject`, `headers`, `dynamicTemplateData` (see the
template example below), `sendAt` (to `scheduledAt`, see Scheduled sends) and `customArgs` (to
`tags`, see Categories and custom args), falling back to the message-level value where the
personalization has none. Then pass the list to `sendEach`.

A single personalization that lists several `to` addresses is one shared email that every recipient
already sees. That stays one `emails.send` with a `to` array, up to 50 recipients across `to`, `cc`
and `bcc`.

On Node older than 24, the same loop uses `sendEmail` from [rest-clients.md](rest-clients.md), which
reads the API key from the environment, takes the idempotency key in its second argument, puts
`retry-after` on `MailfullyApiError.retryAfterSec` and abandons a request after 10 seconds with a
`TimeoutError`. Save the loop as `lib/mailfully-send-each.ts`, beside `lib/mailfully.ts`, which it
imports:

```ts mailfully-rest
// sendEmail (lib/mailfully.ts, from rest-clients.md) POSTs to https://api.mailfully.com/v1/emails.
import { setTimeout as sleep } from "node:timers/promises";
import { MailfullyApiError, sendEmail, type MailfullyEmail } from "./mailfully";

const MAX_ATTEMPTS = 10;
const MAX_UNKNOWN_RETRIES = 3;

export interface SendEachResult {
  sent: { index: number; id: string; status: "queued" | "canceled" }[];
  /** outcome is refused when every attempt got a 4xx, and unknown after no answer, a timeout or a 5xx. */
  stoppedAt: { index: number; outcome: "refused" | "unknown"; message: string } | null;
}

/**
 * One sendEmail call per message, one at a time, in order. runId is an id the app already has for the
 * event (the new user's id, the order id), the same on a re-run of the same job. A random runId means
 * a retried request is not deduplicated: it can send every message again.
 */
export async function sendEach(runId: string, messages: MailfullyEmail[]): Promise<SendEachResult> {
  const apiKey = process.env.MAILFULLY_API_KEY;
  if (!apiKey) throw new Error("MAILFULLY_API_KEY is not set");
  // Test and live keys share one key space per account, so the key kind is part of every key.
  const kind = apiKey.startsWith("mf_live_") ? "live" : "test";
  const result: SendEachResult = { sent: [], stoppedAt: null };
  for (const [index, message] of messages.entries()) {
    const idempotencyKey = `${kind}:${runId}:${index}`;
    let unknownRetries = 0;
    let everUnknown = false;
    for (let attempt = 1; ; attempt++) {
      try {
        const { id, status } = await sendEmail(message, { idempotencyKey });
        result.sent.push({ index, id, status });
        break;
      } catch (err) {
        const api = err instanceof MailfullyApiError ? err : null;
        const paced = api?.type === "send_rate_limited" || api?.type === "rate_limit_exceeded";
        // fetch rejects with a TypeError when no answer came back, and a TimeoutError on the timeout.
        // A 2xx whose body cannot be read also surfaces as a TypeError.
        const noAnswer = err instanceof TypeError || (err instanceof Error && err.name === "TimeoutError");
        const unknown = noAnswer || (api !== null && (api.status >= 500 || api.type === "concurrent_idempotent_requests"));
        everUnknown ||= unknown;
        if (paced && attempt < MAX_ATTEMPTS) {
          await sleep(Math.max(api?.retryAfterSec ?? 1, 1) * 1000);
          continue;
        }
        if (unknown && attempt < MAX_ATTEMPTS && unknownRetries < MAX_UNKNOWN_RETRIES) {
          unknownRetries++;
          await sleep(2 ** unknownRetries * 1000);
          continue;
        }
        result.stoppedAt = {
          index,
          outcome: everUnknown ? "unknown" : "refused",
          message: err instanceof Error ? err.message : String(err),
        };
        return result;
      }
    }
  }
  return result;
}
```

Python, before:

```python
from sendgrid.helpers.mail import Mail


def notify_archived(sg, member_emails, project_name):
    message = Mail(
        from_email="hello@example.com",
        to_emails=member_emails,
        subject=f"{project_name} was archived",
        plain_text_content=f"{project_name} was archived. You can restore it for 30 days.",
        is_multiple=True,
    )
    sg.send(message)
```

Python, after (save as `mailfully_send_each.py` beside `mailfully_client.py`, which it imports; the
app then imports `send_each` or `notify_archived` from `mailfully_send_each`):

```python mailfully-rest
# send_email and MailfullyError (mailfully_client.py, from rest-clients.md) POST to
# https://api.mailfully.com/v1/emails, take an idempotency key and carry a 429's retry-after seconds.
import http.client
import os
import time
from dataclasses import dataclass

from mailfully_client import MailfullyError, send_email

MAX_ATTEMPTS = 10
MAX_UNKNOWN_RETRIES = 3
REQUEST_TIMEOUT_SEC = 15
PACED = ("send_rate_limited", "rate_limit_exceeded")
# No answer, a timeout, a broken response, or a 2xx body that cannot be read: the outcome is unknown.
NO_CLEAR_ANSWER = (OSError, http.client.HTTPException, ValueError, KeyError, TypeError)


@dataclass
class StoppedAt:
    index: int
    outcome: str  # "refused" (every attempt got a 4xx) or "unknown" (it may have been accepted)
    message: str


def send_each(run_id, payloads):
    """One send_email call per payload, one at a time, in order.

    Returns (sent, stopped_at) and never raises once sending has started. sent is
    [(index, id, status)]. stopped_at is None, or a StoppedAt: payloads after its index were not sent.
    run_id names the job; a re-run with the same key kind, run_id, order and payloads within 24 hours
    gets back what the API already accepted instead of sending it again. Use an id the app already
    has for the event (the new user's id, the order id): a random run_id means a retried request is
    not deduplicated and can send every message again.
    """
    api_key = os.environ.get("MAILFULLY_API_KEY")
    if not api_key:
        raise RuntimeError("MAILFULLY_API_KEY is not set")  # before anything is sent
    # Test and live keys share one key space per account, so the key kind is part of every key.
    kind = "live" if api_key.startswith("mf_live_") else "test"
    sent = []
    for index, payload in enumerate(payloads):
        key = f"{kind}:{run_id}:{index}"
        attempt = 0
        unknown_retries = 0
        ever_unknown = False
        while True:
            attempt += 1
            try:
                email_id, status = send_email(
                    payload, timeout=REQUEST_TIMEOUT_SEC, idempotency_key=key
                )
            except MailfullyError as exc:
                unknown = exc.status >= 500 or exc.type == "concurrent_idempotent_requests"
                ever_unknown = ever_unknown or unknown
                if exc.type in PACED and attempt < MAX_ATTEMPTS:
                    time.sleep(max(exc.retry_after or 1, 1))
                    continue
                error = exc
            except NO_CLEAR_ANSWER as exc:
                unknown = True
                ever_unknown = True
                error = exc
            else:
                sent.append((index, email_id, status))
                break
            if unknown and attempt < MAX_ATTEMPTS and unknown_retries < MAX_UNKNOWN_RETRIES:
                unknown_retries += 1
                time.sleep(2 ** unknown_retries)
                continue
            outcome = "unknown" if ever_unknown else "refused"
            return sent, StoppedAt(index, outcome, f"{type(error).__name__}: {error}")
    return sent, None


def notify_archived(project_id, member_emails, project_name):
    return send_each(f"project-archived:{project_id}", [
        {
            "from": "Acme <hello@example.com>",
            "to": address,
            "subject": f"{project_name} was archived",
            "text": f"{project_name} was archived. You can restore it for 30 days.",
        }
        for address in member_emails
    ])
```

A Flask view that calls `notify_archived` reports the returned `stopped_at` instead of raising; if
the user retries the action, the same `project_id` makes the re-run safe.

A send loop over more than a handful of recipients belongs in the app's background job runner
(Celery, RQ, BullMQ, Sidekiq or whatever it already uses), not in the request: a hung connection
can hold one message for about a minute before it ends as unknown.

### Switch

Save the After code as its own modules (here `lib/mailfully-welcome.ts` and
`lib/mailfully-send-each.ts`), then make the file that sends choose by `EMAIL_PROVIDER`. The SendGrid
code stays exactly as it was, renamed only, and stays the default, so merging this changes nothing at
runtime. The per-recipient loop is switched the same way as the single send:

```ts
import sgMail from "@sendgrid/mail";
import { notifyArchived as notifyArchivedMailfully } from "./mailfully-send-each";
import { sendWelcome as sendWelcomeMailfully } from "./mailfully-welcome";

sgMail.setApiKey(process.env.SENDGRID_API_KEY ?? "");

// The SendGrid code, unchanged except for its names.
async function sendWelcomeSendGrid(to: string) {
  await sgMail.send({
    to,
    from: "Acme <hello@example.com>",
    replyTo: "support@example.com",
    subject: "Welcome to Acme",
    text: "Welcome aboard.",
    html: "<p>Welcome aboard.</p>",
    categories: ["Welcome Email"],
  });
}

async function notifyArchivedSendGrid(project: { name: string; memberEmails: string[] }) {
  await sgMail.send({
    to: project.memberEmails,
    from: "Acme <hello@example.com>",
    subject: `${project.name} was archived`,
    text: `${project.name} was archived. You can restore it for 30 days.`,
    isMultiple: true,
  });
}

// EMAIL_PROVIDER=mailfully selects Mailfully. Unset, or any other value, keeps SendGrid.
export async function sendWelcome(to: string): Promise<void> {
  if (process.env.EMAIL_PROVIDER === "mailfully") await sendWelcomeMailfully(to);
  else await sendWelcomeSendGrid(to);
}

export async function notifyArchived(project: { id: string; name: string; memberEmails: string[] }): Promise<void> {
  if (process.env.EMAIL_PROVIDER === "mailfully") {
    const apiKey = process.env.MAILFULLY_API_KEY;
    if (!apiKey) throw new Error("MAILFULLY_API_KEY is not set");
    const result = await notifyArchivedMailfully(apiKey, project.id, project.memberEmails, project.name);
    // Report it: messages after stoppedAt.index were not sent (see sendEach above).
    if (result.stoppedAt) console.error("Mailfully stopped sending", result.stoppedAt);
  } else {
    await notifyArchivedSendGrid(project);
  }
}
```

In Python the same check is `if os.environ.get("EMAIL_PROVIDER") == "mailfully":`, with
`notify_archived` from above in that branch and the SendGrid `sg.send(message)` code in the other.

### Dynamic templates

A SendGrid dynamic template becomes a Mailfully template ONLY when it uses flat `{{var}}`
placeholders. Mailfully templates have no logic: a template with Handlebars blocks (`{{#if}}`,
`{{#each}}`, `{{else}}`, helpers) is rendered in app code into `html` instead.

For a flat template, copy its HTML out of SendGrid and create it on the dashboard's Templates page (or
with `mailfully.templates.create({ name, html, text })` in a one-off script). Then:

- `{{{var}}}` (Handlebars raw output) becomes `{{var}}`. Mailfully HTML-escapes every value in the
  HTML body, so a value that must carry markup belongs in app-rendered `html` instead.
- `{{user.name}}` looks up the literal key `"user.name"`: flatten nested data into dotted keys.
- The template's subject does not come across. Send `subject` with each email.

Before:

```js
await sgMail.send({
  to: user.email,
  from: "Acme <hello@example.com>",
  templateId: "d-12345678901234567890123456789012",
  dynamicTemplateData: { first_name: user.firstName, reset_url: resetUrl },
});
```

After:

```ts mailfully-sdk
import { Mailfully } from "mailfully";

export async function sendPasswordReset(
  mailfully: Mailfully,
  to: string,
  variables: Record<string, string>,
): Promise<string> {
  const { data, error } = await mailfully.emails.send({
    from: "Acme <hello@example.com>",
    to,
    subject: "Reset your password",
    template: { id: "tmpl_01K6T0V1Q5H8C3D7E9F2G4J6KM", variables },
  });
  if (error) throw new Error(`${error.type ?? "error"}: ${error.message}`);
  return data.id;
}
```

Use the real `tmpl_` id from the Templates page. In Python the body is
`"template": {"id": template_id, "variables": variables}`.

For a template with logic, render it with the project's own engine (the `handlebars` package keeps the
template unchanged), then send the result:

```js
import Handlebars from "handlebars";

const render = Handlebars.compile(templateSource);
const html = render({ user, items });
// then: mailfully.emails.send({ from, to, subject, html, text })
```

### Scheduled sends

`sendAt` is Unix seconds. Mailfully takes a UTC ISO 8601 string (the `Z` form `toISOString()`
gives), up to 90 days ahead, and refuses an offset such as `+02:00`.

```ts mailfully-sdk
import { Mailfully, type SendEmailInput } from "mailfully";

export async function sendAtUnix(mailfully: Mailfully, message: SendEmailInput, sendAt: number): Promise<string> {
  const scheduledAt = new Date(sendAt * 1000).toISOString();
  const { data, error } = await mailfully.emails.send({ ...message, scheduledAt });
  if (error) throw new Error(`${error.type ?? "error"}: ${error.message}`);
  return data.id;
}
```

In Python: `datetime.fromtimestamp(send_at, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")`.

### Categories and custom args

Tag names and values allow only `A-Z`, `a-z`, `0-9`, `_` and `-`, so slugify a category before using
it as a tag value:

```ts mailfully-sdk
import type { Tag } from "mailfully";

export function categoryTags(categories: string[]): Tag[] {
  return categories
    .map((c) => c.trim().toLowerCase().replace(/[^a-z0-9_-]+/g, "-").replace(/^-+|-+$/g, ""))
    .filter((value) => value.length > 0)
    .map((value) => ({ name: "category", value }));
}
```

`customArgs` become tags the same way when the values are short ids (`{ name: "order_id", value }`).
Drop an arg whose value cannot be slugified without losing meaning (free text, URLs), and say so in the
report. Webhook events carry the tags back in `data.tags`.

### Sandbox mode

`mailSettings: { sandboxMode: { enable: true } }` becomes a test key: put an `mf_test_…` key in
`MAILFULLY_API_KEY` and drop `mailSettings`. A test key runs the real send path without delivering to
a real inbox (see Test keys in [api-essentials.md](api-essentials.md)).

## Not supported, and what to do instead

- **Any send carrying `asm` (unsubscribe groups), and Marketing Campaigns:** out of scope. Leave them
  on SendGrid and list them in the report. Their unsubscribe lists cannot be imported, so moving that
  mail risks mailing people who opted out.
- **Suppressions:** before switching live, tell the user to export SendGrid's bounce and spam report
  (complaint) lists and add those addresses on the Mailfully dashboard's Blocklist page. Without that,
  the first sends go to addresses that already bounced or complained, and a new account that keeps
  mailing dead addresses can have its sending paused. The page adds one address at a time and
  has no bulk import, so a long list is a real chore; if the list is large, suggest the user email it
  to contact@mailfully.com and ask what can be done.
- **Legacy templates with `substitutions`** (`-name-` style tags): replace them in app code before
  sending, or move them to a flat Mailfully template.
- **`batchId`, `ipPoolName`, `sections`:** no equivalent; drop them and say so in the report.
- **Open and click tracking** is set per sending domain on the dashboard's Domains page, not per
  message.

## Webhooks

The user creates the endpoint in the Mailfully dashboard (Webhooks, then Add webhook) and pastes the
new `whsec_…` secret into `MAILFULLY_WEBHOOK_SECRET`. Never create it with code.

The handler changes shape:

- SendGrid's Event Webhook POSTs a JSON ARRAY of events; Mailfully POSTs ONE event per request, an
  object `{ type, created_at, data }`. Drop the loop over the array.
- SendGrid signs with ECDSA (`X-Twilio-Email-Event-Webhook-Signature` and
  `X-Twilio-Email-Event-Webhook-Timestamp`, checked against a public key with `EventWebhook`).
  Mailfully signs with HMAC: `webhook-id`, `webhook-timestamp` and `webhook-signature`. Replace the
  check with the base64url verifier in [webhooks.md](webhooks.md) (Node and Python) and remove
  `@sendgrid/eventwebhook`. Verify the raw body, as before.
- Correlate by `data.email_id` (the `id` the send returned), not `sg_message_id`.

| SendGrid `event` | Mailfully `type` |
| --- | --- |
| `delivered` | `email.delivered` |
| `bounce` | `email.bounced`, for a hard bounce only; a soft bounce (SendGrid `type: "blocked"`) sends no event |
| `deferred` | `email.delivery_delayed` |
| `spamreport` | `email.complained` |
| `open` | `email.opened` |
| `click` | `email.clicked` |
| `dropped` | no event. A send to suppressed addresses returns `status: "canceled"` at once. For a message refused later, see `email.failed` in [webhooks.md](webhooks.md): not every failure fires it, so read `last_event` |
| `processed` | no event: the send's 202 response is the acceptance |
| `unsubscribe`, `group_unsubscribe`, `group_resubscribe` | none (marketing mail stays on SendGrid) |

## Env

- `SENDGRID_API_KEY` → `MAILFULLY_API_KEY`. The user pastes the key into the env file; add only the
  name to `.env.example`.
- The Event Webhook verification key → `MAILFULLY_WEBHOOK_SECRET`, a new secret from the Mailfully
  dashboard.
- Keep SendGrid wired in behind `EMAIL_PROVIDER`, with SendGrid as the default, until the user's
  Mailfully account is approved.
