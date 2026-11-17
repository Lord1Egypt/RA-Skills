# Migrating from Resend

Resend's send call and Mailfully's are close: both SDKs take camelCase input and return
`{ data, error }`. Most of the work is in the parts Mailfully does not do for you: rendering React
emails, fetching attachments by URL, and parsing natural-language schedule times.

Read [api-essentials.md](api-essentials.md) first for the send body, test keys and errors. The Node SDK
needs Node 24 or later. On an older Node, or in Python, use the helpers in
[rest-clients.md](rest-clients.md): the mapping below still holds, with snake_case wire keys.

## Detect

- npm: `resend` (`import { Resend } from "resend"`, `new Resend(...)`), often beside `@react-email/render`,
  `@react-email/components` or `react-email`, and `svix` for webhooks.
- Python: `resend` on PyPI (`import resend`, `resend.api_key = ...`, `resend.Emails.send(params)`).
- Calls: `resend.emails.send`, `resend.batch.send`, `resend.emails.update` / `cancel` (scheduled mail),
  `resend.webhooks.verify`, and anything under `resend.contacts`, `resend.audiences`,
  `resend.segments` or `resend.broadcasts`.
- Environment: `RESEND_API_KEY`, and a webhook secret (often `RESEND_WEBHOOK_SECRET`).

## Field map

| Resend (Node) | Mailfully SDK | Wire |
| --- | --- | --- |
| `from` | `from` | `from` |
| `to` (up to 50) | `to` | `to` (up to 50 across `to`, `cc` and `bcc`) |
| `cc`, `bcc` | `cc`, `bcc` | `cc`, `bcc` |
| `replyTo` (Python `reply_to`) | `replyTo` | `reply_to` |
| `subject` | `subject` | `subject` |
| `html`, `text` | `html`, `text` | `html`, `text` |
| `react` | none: render to `html` and `text` first | `html`, `text` |
| `headers` | `headers` | `headers` |
| `tags` (`{ name, value }`) | `tags`, unchanged | `tags` |
| `attachments[].content` (string or Buffer) | `attachments[].content`, a base64 string | `content` |
| `attachments[].path` (URL) | fetch it, then base64 into `content` | `content` |
| `attachments[].contentType` | `contentType` | `contentType` |
| `attachments[].contentId` | `cid` | `cid` |
| `scheduledAt` (ISO or "in 1 hour") | `scheduledAt`, a UTC ISO string only | `scheduled_at` |
| `template: { id, variables }` | `template: { id, variables }` with a Mailfully `tmpl_` id | `template` |
| `data.id` | `data.id` (a ULID such as `01K6T0V1Q5H8C3D7E9F2G4J6KM`), plus `data.status` | `id`, `status` |
| `error.name` | `error.type` | `error.type` |
| `error.statusCode`, `error.message` | `error.statusCode`, `error.message` | HTTP status, `error.message` |

Two differences to carry through every call site:

- Resend builds a text part from `html` when `text` is missing. Mailfully sends the parts you pass,
  so pass `text` too.
- A Mailfully send can return `status: "canceled"`: every recipient was suppressed and nothing will be
  sent. Log it or report it; never count it as sent.

## Before and after

### A single send

Before:

```ts
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

export async function sendWelcome(to: string) {
  const { data, error } = await resend.emails.send({
    from: "Acme <hello@example.com>",
    to: [to],
    replyTo: "support@example.com",
    subject: "Welcome to Acme",
    html: "<p>Welcome aboard.</p>",
  });
  if (error) throw new Error(`${error.name} (${error.statusCode}): ${error.message}`);
  return data.id;
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
    to: [to],
    replyTo: "support@example.com",
    subject: "Welcome to Acme",
    html: "<p>Welcome aboard.</p>",
    text: "Welcome aboard.",
  });
  // statusCode is null when the request never reached the API.
  if (error) throw new Error(`${error.type ?? "error"} (${String(error.statusCode)}): ${error.message}`);
  if (data.status === "canceled") console.warn(`Mailfully sent nothing for ${data.id}: every recipient is suppressed`);
  return data.id;
}
```

Code that branches on `error.name` now branches on `error.type`. The type names differ in places
(Mailfully's validation errors are 422 `validation_error`); the full list is the Errors table in
[api-essentials.md](api-essentials.md).

### Switch

Save the After code as its own module (here `lib/mailfully-welcome.ts`), then make the file that sends
choose by `EMAIL_PROVIDER`. The Resend function stays exactly as it was, renamed only, and stays the
default, so merging this changes nothing at runtime. Every call site keeps calling `sendWelcome`:

```ts
import { Resend } from "resend";
import { sendWelcome as sendWelcomeMailfully } from "./mailfully-welcome";

const resend = new Resend(process.env.RESEND_API_KEY);

// The Resend code, unchanged except for its name.
async function sendWelcomeResend(to: string) {
  const { data, error } = await resend.emails.send({
    from: "Acme <hello@example.com>",
    to: [to],
    replyTo: "support@example.com",
    subject: "Welcome to Acme",
    html: "<p>Welcome aboard.</p>",
  });
  if (error) throw new Error(`${error.name} (${error.statusCode}): ${error.message}`);
  return data.id;
}

// EMAIL_PROVIDER=mailfully selects Mailfully. Unset, or any other value, keeps Resend.
export function sendWelcome(to: string) {
  return process.env.EMAIL_PROVIDER === "mailfully" ? sendWelcomeMailfully(to) : sendWelcomeResend(to);
}
```

Every other send below (batch, React Email, attachments, scheduled) goes behind the same check, with
the Resend call left as it was in the other branch.

### Python

Before:

```python
import os

import resend

resend.api_key = os.environ["RESEND_API_KEY"]


def send_welcome(to):
    params = {
        "from": "Acme <hello@example.com>",
        "to": [to],
        "reply_to": "support@example.com",
        "subject": "Welcome to Acme",
        "html": "<p>Welcome aboard.</p>",
    }
    return resend.Emails.send(params)["id"]
```

After (with `send_email` from the Python helper in [rest-clients.md](rest-clients.md)). Resend's
Python keys are already the wire keys:

```python mailfully-rest
# send_email (mailfully_client.py, from rest-clients.md) POSTs to https://api.mailfully.com/v1/emails.
import logging

from mailfully_client import send_email

logger = logging.getLogger(__name__)


def send_welcome(to):
    email_id, status = send_email({
        "from": "Acme <hello@example.com>",
        "to": [to],
        "reply_to": "support@example.com",
        "subject": "Welcome to Acme",
        "html": "<p>Welcome aboard.</p>",
        "text": "Welcome aboard.",
    })
    if status == "canceled":
        logger.warning("Mailfully sent nothing for %s: every recipient is suppressed", email_id)
    return email_id
```

`resend.exceptions.ResendError` becomes the helper's `MailfullyError`, with `.type`, `.status` and
`.param`.

### Batch

Before:

```ts
const { data, error } = await resend.batch.send([
  { from: "Acme <hello@example.com>", to: ["a@example.com"], subject: "Your receipt", html: receiptA },
  { from: "Acme <hello@example.com>", to: ["b@example.com"], subject: "Your receipt", html: receiptB },
]);
```

After:

```ts mailfully-sdk
import { Mailfully, type AcceptedEmail, type SendEmailInput } from "mailfully";

export async function sendReceipts(mailfully: Mailfully, receipts: SendEmailInput[]): Promise<AcceptedEmail[]> {
  const { data, error } = await mailfully.emails.batch(receipts);
  if (error) throw new Error(`${error.type ?? "error"} (${String(error.statusCode)}): ${error.message}`);
  // One accepted message per input, in input order.
  return data.data;
}
```

- Up to 100 messages per request. The batch is all or nothing: one invalid message refuses the whole
  request, and `error.param` names the index (`[3].to`). There is no permissive mode.
- New-account pacing counts every recipient in a batch together. A batch of per-recipient mail on a
  new account gets 422 `young_sender_batch_too_large`, so send that mail one message at a time
  instead, with `sendEach` from [migrate-sendgrid.md](migrate-sendgrid.md). It works for any
  provider: it waits out `retry-after` on a 429 and gives each message a key, so a re-run with the
  same run id, the same order and the same bodies within 24 hours does not send a message twice.

### React Email

Before:

```tsx
import { WelcomeEmail } from "./emails/welcome";

await resend.emails.send({
  from: "Acme <hello@example.com>",
  to: [user.email],
  subject: "Welcome to Acme",
  react: <WelcomeEmail name={user.name} />,
});
```

After, with the SDK: render first, then send `html` and `text`. Keep this part in a `.tsx` file
(the `fetch` helper version below shows the `.ts` form):

```tsx
import { render } from "@react-email/render";
import { WelcomeEmail } from "./emails/welcome";
import { getMailfully } from "./lib/mailfully"; // the client module from api-essentials.md

const html = await render(<WelcomeEmail name={user.name} />);
const text = await render(<WelcomeEmail name={user.name} />, { plainText: true });
await sendRendered(getMailfully(), user.email, html, text);
```

```ts mailfully-sdk
import { Mailfully } from "mailfully";

export async function sendRendered(mailfully: Mailfully, to: string, html: string, text: string): Promise<string> {
  const { data, error } = await mailfully.emails.send({
    from: "Acme <hello@example.com>",
    to,
    subject: "Welcome to Acme",
    html,
    text,
  });
  if (error) throw new Error(`${error.type ?? "error"}: ${error.message}`);
  return data.id;
}
```

If the project imports `render` from `react-email` or `@react-email/components`, keep that import; it
is the same function.

On the `fetch` helper (Node older than 24, or a CommonJS project), the rendering is the same and the
result goes to `sendEmail` from [rest-clients.md](rest-clients.md):

- `@react-email/render` must be a direct dependency. Resend lists it only as an optional peer, so it
  may be installed only under `resend`. If `package.json` does not name it (or `react-email` or
  `@react-email/components`), install it with the project's package manager
  (`npm install @react-email/render`).
- `render` is async: `await` both calls, the HTML one and the `{ plainText: true }` text one.
- In a `.ts` file, where JSX is not allowed, call the component as a function
  (`WelcomeEmail({ name })`) instead of writing `<WelcomeEmail name={name} />`. The Resend code may
  already do this when it passes `react: WelcomeEmail({ name })`.

```ts mailfully-rest
// sendEmail (lib/mailfully.ts, from rest-clients.md) POSTs to https://api.mailfully.com/v1/emails.
import { render } from "@react-email/render";
import { WelcomeEmail } from "./emails/welcome";
import { sendEmail } from "./lib/mailfully";

export async function sendWelcomeMailfully(to: string, name: string): Promise<string> {
  const email = WelcomeEmail({ name });
  const html = await render(email);
  const text = await render(email, { plainText: true });
  const { id, status } = await sendEmail({ from: "Acme <hello@example.com>", to, subject: "Welcome to Acme", html, text });
  if (status === "canceled") console.warn(`Mailfully sent nothing for ${id}: every recipient is suppressed`);
  return id;
}
```

### Attachments

Before:

```ts
await resend.emails.send({
  from: "Acme <billing@example.com>",
  to: [customer.email],
  subject: "Your invoice",
  html: "<p>Your invoice is attached.</p>",
  attachments: [
    { filename: "invoice.pdf", path: "https://files.example.com/invoices/42.pdf" },
    { filename: "terms.pdf", content: termsBuffer },
  ],
});
```

After: Mailfully takes bare base64 in `content` (never a `data:` URI) and does not fetch URLs.

```ts mailfully-sdk
import { Mailfully } from "mailfully";

async function base64FromUrl(url: string): Promise<string> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`could not fetch attachment ${url}: HTTP ${res.status}`);
  return Buffer.from(await res.arrayBuffer()).toString("base64");
}

export async function sendInvoice(mailfully: Mailfully, to: string, termsBuffer: Buffer): Promise<string> {
  const { data, error } = await mailfully.emails.send({
    from: "Acme <billing@example.com>",
    to,
    subject: "Your invoice",
    html: "<p>Your invoice is attached.</p>",
    text: "Your invoice is attached.",
    attachments: [
      {
        filename: "invoice.pdf",
        content: await base64FromUrl("https://files.example.com/invoices/42.pdf"),
        contentType: "application/pdf",
      },
      { filename: "terms.pdf", content: termsBuffer.toString("base64"), contentType: "application/pdf" },
    ],
  });
  if (error) throw new Error(`${error.type ?? "error"}: ${error.message}`);
  return data.id;
}
```

An inline image keeps its `cid:` reference in the HTML; rename the attachment's `contentId` to `cid`.

### Scheduled sends

Before:

```ts
await resend.emails.send({ ...reminder, scheduledAt: "in 1 hour" });
```

After: compute the time. Mailfully takes a UTC ISO 8601 string (the `Z` form `toISOString()` gives),
refuses an offset such as `+02:00` and natural language, and allows up to 90 days ahead.

```ts mailfully-sdk
import { Mailfully, type SendEmailInput } from "mailfully";

export async function sendInOneHour(mailfully: Mailfully, reminder: SendEmailInput): Promise<string> {
  const scheduledAt = new Date(Date.now() + 60 * 60 * 1000).toISOString();
  const { data, error } = await mailfully.emails.send({ ...reminder, scheduledAt });
  if (error) throw new Error(`${error.type ?? "error"}: ${error.message}`);
  return data.id;
}
```

`resend.emails.update({ id, scheduledAt })` becomes `mailfully.emails.reschedule(id, { scheduledAt })`,
and `resend.emails.cancel(id)` becomes `mailfully.emails.cancel(id)`. Stored Resend ids do not carry
over: only messages sent through Mailfully can be changed there.

## Not supported, and what to do instead

- **Audiences (now Segments), Contacts and Broadcasts:** out of scope. Leave them on Resend and list
  them in the report. Their unsubscribe lists cannot be imported, so moving that mail risks mailing
  people who opted out.
- **Marketing mail sent with `emails.send`** (newsletters, list sends): leave it on Resend too, for
  the same reason (see Marketing in [api-essentials.md](api-essentials.md)).
- **Suppressions:** before switching live, tell the user to export Resend's suppressed addresses (its
  bounce and complaint lists) and add them on the Mailfully dashboard's Blocklist page. Without that,
  the first sends go to addresses that already bounced or complained, and a new account that keeps
  mailing dead addresses can have its sending paused. The page adds one address at a time and has no
  bulk import; if the list is large, suggest the user email it to contact@mailfully.com and ask what
  can be done.
- **Resend templates:** Mailfully cannot read them. Recreate each one on the dashboard's Templates
  page, check its placeholders use `{{ name }}` with flat keys, and send the subject with the email
  (Mailfully templates carry no subject). A template that needs loops or conditionals is rendered in
  app code into `html` and `text` instead.
- **Inbound mail** (`resend.emails.receiving`, `email.received` handlers): not covered by this
  migration. Leave it on Resend and list it in the report.
- **`resend.domains.*`:** the sending domain is added and verified in Mailfully separately; see the
  main skill's go-live phase.

## Webhooks

The user creates the endpoint in the Mailfully dashboard (Webhooks, then Add webhook) and pastes the
new `whsec_…` secret into `MAILFULLY_WEBHOOK_SECRET`. Never create it with code.

| Resend | Mailfully |
| --- | --- |
| `svix-id` | `webhook-id` |
| `svix-timestamp` | `webhook-timestamp` |
| `svix-signature` | `webhook-signature` |
| `resend.webhooks.verify(...)` or the `svix` package | `verifyMailfullyWebhook` from [webhooks.md](webhooks.md) |

Replace the verification call with the base64url verifier in [webhooks.md](webhooks.md) (Node and
Python). Do not keep the `svix` library: it decodes standard base64 and rejects most Mailfully
secrets. Verify the raw body exactly as before.

Event names:

| Resend | Mailfully |
| --- | --- |
| `email.delivered` | `email.delivered` |
| `email.bounced` | `email.bounced` (hard bounces only) |
| `email.complained` | `email.complained` |
| `email.delivery_delayed` | `email.delivery_delayed` |
| `email.failed` | `email.failed`, which does not fire for every failure (see [webhooks.md](webhooks.md)); read `last_event` (`failed`, `rejected`) for the rest |
| `email.opened` | `email.opened` |
| `email.clicked` | `email.clicked` |
| `email.sent`, `email.scheduled` | no event: the send's 202 response is the acceptance |
| `email.suppressed` | no event to build on: check `status: "canceled"` on the send response |
| `contact.*`, `domain.*` | none |

The body keeps the `{ type, created_at, data }` shape and `data.email_id`, but the id is now a
Mailfully id (a ULID), and `data.tags` is an array of `{ name, value }` (Resend sends an object).

## Env

- `RESEND_API_KEY` → `MAILFULLY_API_KEY`. The user pastes the key into the env file; add only the name
  to `.env.example`.
- The Resend webhook secret → `MAILFULLY_WEBHOOK_SECRET`, a new secret from the Mailfully dashboard.
- Keep Resend wired in behind `EMAIL_PROVIDER`, with Resend as the default, until the user's Mailfully
  account is approved.
