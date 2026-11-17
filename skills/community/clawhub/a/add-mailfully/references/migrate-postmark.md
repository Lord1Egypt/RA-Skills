# Migrating from Postmark

Postmark's message object uses PascalCase keys (`From`, `HtmlBody`), comma-separated address strings
and arrays of `{ Name, Value }` headers. Mailfully takes camelCase keys, address arrays and a headers
object, so most of the work is a small converter. Message streams, per-message tracking flags and
Mustachio templates need a decision each.

Read [api-essentials.md](api-essentials.md) first for the send body, test keys and errors. The Node SDK
needs Node 24 or later. On an older Node, or in Python, use the helpers in
[rest-clients.md](rest-clients.md): the mapping below still holds, with snake_case wire keys.

## Detect

- npm: `postmark` (`import { ServerClient } from "postmark"`, `new postmark.ServerClient(token)`), and
  `postmark.Models.Message`, `postmark.Models.Attachment` or `postmark.Models.TemplatedMessage`.
- Calls: `client.sendEmail`, `client.sendEmailBatch`, `client.sendEmailWithTemplate`,
  `client.sendEmailBatchWithTemplates`, and error checks against `postmark.Errors`.
- Raw API calls to `https://api.postmarkapp.com/email`, `/email/batch` or `/email/withTemplate`, with
  an `X-Postmark-Server-Token` header (any language).
- Other stacks: a Postmark package in `requirements.txt`, `Gemfile` or `composer.json`
  (`wildbit/postmark-php`), or a framework mail driver set to Postmark. A Django or Rails app moves to
  the adapters in [rest-clients.md](rest-clients.md); anything else uses that file's helper for its
  language.
- `MessageStream` values in the code. `"outbound"` is the default transactional stream; anything else
  needs the check in Message streams below.
- Environment: `POSTMARK_SERVER_TOKEN` (also spelled `POSTMARK_API_TOKEN` or `POSTMARK_API_KEY`), and
  any Basic Auth user and password the webhook handler checks.

## Field map

| Postmark | Mailfully SDK | Wire |
| --- | --- | --- |
| `From` | `from` | `from` |
| `To` (comma-separated string, up to 50) | `to`, an array of single addresses | `to` (up to 50 across `to`, `cc` and `bcc`) |
| `Cc`, `Bcc` (comma-separated strings) | `cc`, `bcc` (arrays) | `cc`, `bcc` |
| `ReplyTo` | `replyTo` | `reply_to` |
| `Subject` | `subject` | `subject` |
| `HtmlBody`, `TextBody` | `html`, `text` | `html`, `text` |
| `Headers: [{ Name, Value }]` | `headers: { [Name]: Value }` | `headers` |
| `Attachments[].Name` | `filename` | `filename` |
| `Attachments[].Content` (base64) | `content`, unchanged | `content` |
| `Attachments[].ContentType` | `contentType` | `contentType` |
| `Attachments[].ContentID` (`cid:logo.png`) | `cid`, without the `cid:` prefix (`logo.png`) | `cid` |
| `Tag` | `tags: [{ name: "tag", value }]` | `tags` |
| `Metadata` | `tags`, for keys and values that fit `[A-Za-z0-9_-]`; drop the rest | `tags` |
| `MessageStream: "outbound"` | omit it (transactional is the default) | |
| `MessageStream` for a broadcast stream | out of scope, stays on Postmark | |
| `TrackOpens`, `TrackLinks` | per sending domain, not per message (see below) | |
| `TemplateAlias` / `TemplateId` + `TemplateModel` | `template: { id, variables }` with a Mailfully `tmpl_` id and flat keys | `template` |
| `InlineCss` | drop it | |
| `MessageID` in the response | `data.id` (a ULID such as `01K6T0V1Q5H8C3D7E9F2G4J6KM`), plus `data.status` | `id`, `status` |
| `ErrorCode`, `Message` in an error | `error.type`, `error.message` | `error.type`, `error.message` |

Two differences to carry through every call site:

- Postmark refuses a send to an inactive (bounced or complained) recipient with an `ApiInputError`.
  Mailfully accepts it with HTTP 202 and `status: "canceled"` when every recipient is suppressed:
  nothing will be sent. Log it or report it; never count it as sent.
- Each Mailfully address string must hold exactly ONE mailbox. Split Postmark's comma lists into
  arrays, keeping a comma inside a quoted display name (`"Doe, Jane" <jane@example.com>`) with its
  address.

## Before and after

### A single send

Before:

```ts
import { ServerClient } from "postmark";

const client = new ServerClient(process.env.POSTMARK_SERVER_TOKEN ?? "");

export async function sendWelcome(to: string) {
  const result = await client.sendEmail({
    From: "Acme <hello@example.com>",
    To: to,
    ReplyTo: "support@example.com",
    Subject: "Welcome to Acme",
    HtmlBody: "<p>Welcome aboard.</p>",
    TextBody: "Welcome aboard.",
    Tag: "welcome",
    MessageStream: "outbound",
  });
  return result.MessageID;
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
    html: "<p>Welcome aboard.</p>",
    text: "Welcome aboard.",
    tags: [{ name: "tag", value: "welcome" }],
  });
  // The SDK never throws. statusCode is null when the request never reached the API.
  if (error) throw new Error(`${error.type ?? "error"} (${String(error.statusCode)}): ${error.message}`);
  if (data.status === "canceled") console.warn(`Mailfully sent nothing for ${data.id}: every recipient is suppressed`);
  return data.id;
}
```

Postmark rejects with an error from `postmark.Errors` carrying `code` (Postmark's `ErrorCode`) and
`statusCode`. Mailfully returns `error.statusCode`, `error.type` and `error.message`. Branch on
`error.type`, using the Errors table in [api-essentials.md](api-essentials.md).

### Switch

Save the After code as its own module (here `lib/mailfully-welcome.ts`), then make the file that sends
choose by `EMAIL_PROVIDER`. The Postmark function stays exactly as it was, renamed only, and stays the
default, so merging this changes nothing at runtime. Every call site keeps calling `sendWelcome`:

```ts
import { ServerClient } from "postmark";
import { sendWelcome as sendWelcomeMailfully } from "./mailfully-welcome";

const client = new ServerClient(process.env.POSTMARK_SERVER_TOKEN ?? "");

// The Postmark code, unchanged except for its name.
async function sendWelcomePostmark(to: string) {
  const result = await client.sendEmail({
    From: "Acme <hello@example.com>",
    To: to,
    ReplyTo: "support@example.com",
    Subject: "Welcome to Acme",
    HtmlBody: "<p>Welcome aboard.</p>",
    TextBody: "Welcome aboard.",
    Tag: "welcome",
    MessageStream: "outbound",
  });
  return result.MessageID;
}

// EMAIL_PROVIDER=mailfully selects Mailfully. Unset, or any other value, keeps Postmark.
export function sendWelcome(to: string) {
  return process.env.EMAIL_PROVIDER === "mailfully" ? sendWelcomeMailfully(to) : sendWelcomePostmark(to);
}
```

The converter, templates and batches below go behind the same check: `client.sendEmail(message)`
stays in the default branch, and `sendPostmarkMessage(getMailfully(), message)` goes in the
`mailfully` one.

### Many call sites: a converter

When the app builds Postmark message objects in many places, convert them in one function instead of
rewriting each one. Save as `lib/mailfully-postmark.ts`:

```ts mailfully-sdk
import { Mailfully, type SendEmailInput, type Tag } from "mailfully";

/** The Postmark message fields the converter reads. */
export interface PostmarkMessage {
  From: string;
  To: string;
  Cc?: string;
  Bcc?: string;
  ReplyTo?: string;
  Subject?: string;
  HtmlBody?: string;
  TextBody?: string;
  Headers?: { Name: string; Value: string }[];
  Attachments?: { Name: string; Content: string; ContentType: string; ContentID?: string | null }[];
  Tag?: string;
  Metadata?: Record<string, string>;
  MessageStream?: string;
  TrackOpens?: boolean;
  TrackLinks?: string;
}

const TAG_TOKEN = /^[A-Za-z0-9_-]+$/;

/** Split a comma-separated address list, keeping commas inside quotes, (comments) or <angle brackets>. */
export function splitAddressList(list: string): string[] {
  const out: string[] = [];
  let current = "";
  let quoted = false;
  let angle = false;
  let comment = 0;
  let escaped = false;
  for (const ch of list) {
    if (escaped) escaped = false;
    else if ((quoted || comment > 0) && ch === "\\") escaped = true;
    else if (comment === 0 && ch === '"') quoted = !quoted;
    else if (!quoted && ch === "(") comment++;
    else if (!quoted && ch === ")" && comment > 0) comment--;
    else if (!quoted && comment === 0 && ch === "<") angle = true;
    else if (!quoted && comment === 0 && ch === ">") angle = false;
    else if (ch === "," && !quoted && !angle && comment === 0) {
      if (current.trim() !== "") out.push(current.trim());
      current = "";
      continue;
    }
    current += ch;
  }
  if (current.trim() !== "") out.push(current.trim());
  return out;
}

/** A Postmark Tag as a tag value: kept as is when valid, else each run of other characters becomes "-". */
function tagValueFor(tag: string): string {
  const trimmed = tag.trim();
  if (TAG_TOKEN.test(trimmed)) return trimmed;
  return trimmed.replace(/[^A-Za-z0-9_-]+/g, "-").replace(/^-+|-+$/g, "");
}

/**
 * Converts one Postmark message. `dropped` names the Metadata keys (and "Tag", for a Tag with no
 * usable characters) that could not become tags, so the caller can log them and the migration report
 * can list them.
 */
export function fromPostmark(message: PostmarkMessage): { input: SendEmailInput; dropped: string[] } {
  if (message.MessageStream !== undefined && message.MessageStream !== "outbound") {
    // Broadcast streams stay on Postmark. Remove this check only for a stream the user confirmed is
    // transactional (see Message streams).
    throw new Error(`MessageStream "${message.MessageStream}" is not migrated to Mailfully`);
  }
  const tags: Tag[] = [];
  const dropped: string[] = [];
  if (message.Tag !== undefined && message.Tag.trim() !== "") {
    const value = tagValueFor(message.Tag);
    if (value === "") dropped.push("Tag");
    else tags.push({ name: "tag", value });
  }
  for (const [name, value] of Object.entries(message.Metadata ?? {})) {
    if (TAG_TOKEN.test(name) && TAG_TOKEN.test(value) && name !== "tag") tags.push({ name, value });
    else dropped.push(name);
  }
  const input: SendEmailInput = {
    from: message.From,
    to: splitAddressList(message.To),
    ...(message.Cc ? { cc: splitAddressList(message.Cc) } : {}),
    ...(message.Bcc ? { bcc: splitAddressList(message.Bcc) } : {}),
    ...(message.ReplyTo ? { replyTo: splitAddressList(message.ReplyTo) } : {}),
    ...(message.Subject !== undefined ? { subject: message.Subject } : {}),
    ...(message.HtmlBody !== undefined ? { html: message.HtmlBody } : {}),
    ...(message.TextBody !== undefined ? { text: message.TextBody } : {}),
    ...(message.Headers && message.Headers.length > 0
      ? { headers: Object.fromEntries(message.Headers.map((h) => [h.Name, h.Value])) }
      : {}),
    ...(message.Attachments && message.Attachments.length > 0
      ? {
          attachments: message.Attachments.map((a) => ({
            filename: a.Name,
            content: a.Content,
            contentType: a.ContentType,
            ...(a.ContentID ? { cid: a.ContentID.replace(/^cid:/i, "") } : {}),
          })),
        }
      : {}),
    ...(tags.length > 0 ? { tags } : {}),
  };
  // TrackOpens and TrackLinks are not per message in Mailfully; they are read here and ignored.
  return { input, dropped };
}

/** Sends one Postmark-shaped message through Mailfully and returns the Mailfully id. */
export async function sendPostmarkMessage(mailfully: Mailfully, message: PostmarkMessage): Promise<string> {
  const { input, dropped } = fromPostmark(message);
  if (dropped.length > 0) console.warn(`Mailfully: not sent as tags: ${dropped.join(", ")}`);
  const { data, error } = await mailfully.emails.send(input);
  if (error) throw new Error(`${error.type ?? "error"} (${String(error.statusCode)}): ${error.message}`);
  if (data.status === "canceled") console.warn(`Mailfully sent nothing for ${data.id}: every recipient is suppressed`);
  return data.id;
}
```

Then `client.sendEmail(message)` becomes `sendPostmarkMessage(getMailfully(), message)`. Code that read
`result.MessageID` reads the returned id instead.

Notes on the converter:

- **Headers.** Postmark allows the same `Name` twice; a headers object keeps the last one. `From`,
  `Sender`, `Return-Path` and `X-Mailfully-Mid` are reserved and refused with a 422 (the full list is
  in [migrate-nodemailer.md](migrate-nodemailer.md)), and so is a header name with a space or a colon.
- **Attachments.** Postmark's `Content` is already bare base64, so it passes through. A `ContentID`
  loses its `cid:` prefix; the HTML keeps its `src="cid:logo.png"` reference unchanged.
- **Tag and Metadata.** Tag names and values allow only `A-Z`, `a-z`, `0-9`, `_` and `-`. A Tag that
  already fits is kept exactly, case included (`WelcomeEmail` stays `WelcomeEmail`); any other run of
  characters becomes `-` (`Welcome Email` becomes `Welcome-Email`). A Tag with nothing usable left, and
  a Metadata entry whose key or value does not fit (free text, URLs, email addresses), is dropped and
  named in `dropped`; list each one in the report, and tell the user when a Tag changed, since reports
  filtered on the old value will not match. Webhook events carry the tags back in `data.tags`.
- **Address lists.** A comma inside a quoted display name or a `(comment)` stays with its address
  (`Acme (Sales, EU) <sales@example.com>` is one address).

### Message streams

`MessageStream: "outbound"` is Postmark's default transactional stream: remove the field. A
**broadcast** stream (often named `broadcast`, `newsletter` or `marketing`) carries bulk mail and is
out of scope: leave those call sites on Postmark and list them in the report. Its unsubscribe list
cannot be imported, so moving that mail risks mailing people who opted out (see Marketing in
[api-essentials.md](api-essentials.md)).

A stream name that is neither `outbound` nor clearly bulk may still be a second transactional stream.
Ask the user which type each stream is in Postmark. Migrate only the ones they confirm are
transactional, and drop the field (or keep the name as a tag, `{ name: "stream", value }`).

### Open and click tracking

`TrackOpens` and `TrackLinks` are per message in Postmark. In Mailfully, open and click tracking is
one switch per sending domain, and it is ON by default for a new domain: Mailfully adds an open pixel
and rewrites links, including password-reset and sign-in links. Drop both fields from every call, then
decide the domain's switch from what the app did on Postmark:

- **The app never tracked** (`TrackOpens: false` and `TrackLinks: "None"` on all its mail): turn
  tracking off for the domain with `--disable`. A field that is absent inherits the Postmark server's
  own tracking setting, which the code does not show, so when either field is missing anywhere, ask
  the user whether that server tracked opens or links before deciding.
- **The app tracked:** leave the default on. `--enable` is needed only if someone turned it off.
- **It tracked only opens, or only links:** the one switch covers both, so ask the user which way to
  set it.

Set it with the domain's Tracking switch in the dashboard. A key the user pasted from the dashboard
(not one from the browser sign-in, which is refused here) can use the CLI instead; the domain id is
the `dom_…` value from `domains list`:

```bash
npx -y mailfully@1.4.0 domains list
npx -y mailfully@1.4.0 domains tracking <domain-id> --disable
npx -y mailfully@1.4.0 domains tracking <domain-id> --enable
```

If the app tracks some messages and not others from the same domain, say so in the report: Mailfully
cannot split them. Say in the report which way the switch was set, and why.

### Templates

A Postmark template becomes a Mailfully template ONLY when it uses plain `{{var}}` placeholders.
Mailfully templates have no logic, so a template with Mustachio blocks (`{{#each items}}`,
`{{#section}}…{{/section}}`, `{{^section}}`) or a layout (`LayoutTemplate`) is rendered in app code
into `html` and `text` instead.

For a flat template, copy its HTML and text out of Postmark and create it on the dashboard's Templates
page (or with `mailfully.templates.create({ name, html, text })` in a one-off script run with a key
made in the dashboard; a key from the browser sign-in cannot change templates). Then:

- `{{{var}}}` (raw output) becomes `{{var}}`. Mailfully HTML-escapes every value in the HTML body, so
  a value that must carry markup belongs in app-rendered `html` instead.
- `{{user.name}}` looks up the literal key `"user.name"`: flatten a nested `TemplateModel` into
  dotted keys (below).
- The template's subject does not come across. Send `subject` with each email; a subject with
  placeholders is built in app code.
- Keep a map from each Postmark alias to its new `tmpl_` id.

Before:

```ts
await client.sendEmailWithTemplate({
  From: "Acme <hello@example.com>",
  To: user.email,
  TemplateAlias: "password-reset",
  TemplateModel: { user: { name: user.name }, action_url: resetUrl },
  MessageStream: "outbound",
});
```

After:

```ts mailfully-sdk
import { Mailfully } from "mailfully";

/** Postmark alias to Mailfully template id. Use the real ids from the Templates page. */
const TEMPLATE_IDS: Record<string, string> = {
  "password-reset": "tmpl_01K6T0V1Q5H8C3D7E9F2G4J6KM",
};

/** Flattens a TemplateModel into dotted keys: { user: { name } } becomes { "user.name": name }. */
export function flattenModel(model: Record<string, unknown>, prefix = ""): Record<string, string> {
  const out: Record<string, string> = {};
  for (const [key, value] of Object.entries(model)) {
    const path = prefix === "" ? key : `${prefix}.${key}`;
    if (Array.isArray(value)) {
      throw new Error(`TemplateModel.${path} is a list: the template loops, so render it in app code`);
    }
    if (value !== null && typeof value === "object") Object.assign(out, flattenModel(value as Record<string, unknown>, path));
    else if (value !== undefined && value !== null) out[path] = String(value);
  }
  return out;
}

export async function sendPasswordReset(
  mailfully: Mailfully,
  to: string,
  model: Record<string, unknown>,
): Promise<string> {
  const id = TEMPLATE_IDS["password-reset"];
  if (!id) throw new Error("no Mailfully template for password-reset");
  const { data, error } = await mailfully.emails.send({
    from: "Acme <hello@example.com>",
    to,
    subject: "Reset your password",
    template: { id, variables: flattenModel(model) },
  });
  if (error) throw new Error(`${error.type ?? "error"}: ${error.message}`);
  if (data.status === "canceled") console.warn(`Mailfully sent nothing for ${data.id}: every recipient is suppressed`);
  return data.id;
}
```

`TemplateId` (a number) maps the same way as `TemplateAlias`. In Python the body is
`"template": {"id": template_id, "variables": variables}`, with the same flat keys.

For a template with logic, render it in app code with the project's own template engine, porting
the Mustachio blocks and the layout by hand, then send the result as `html` and `text`. Check each
ported template against a test send.

### Batch

Before:

```ts
const results = await client.sendEmailBatch(messages);
for (const r of results) {
  if (r.ErrorCode !== 0) console.error(`not sent to ${r.To}: ${r.Message}`);
}
```

After:

```ts mailfully-sdk
import { Mailfully, type AcceptedEmail, type SendEmailInput } from "mailfully";

export async function sendBatch(mailfully: Mailfully, inputs: SendEmailInput[]): Promise<AcceptedEmail[]> {
  if (inputs.length > 100) throw new Error("a Mailfully batch takes up to 100 messages");
  const { data, error } = await mailfully.emails.batch(inputs);
  if (error) throw new Error(`${error.type ?? "error"} (${String(error.statusCode)}): ${error.message}`);
  for (const sent of data.data) {
    if (sent.status === "canceled") console.warn(`Mailfully sent nothing for ${sent.id}: every recipient is suppressed`);
  }
  // One accepted message per input, in input order.
  return data.data;
}
```

Build `inputs` with `fromPostmark(message).input` from the converter above. The differences:

- Postmark takes up to 500 messages per call and answers per message, so some can fail while others
  send. A Mailfully batch takes up to 100 messages and is all or nothing: one invalid message refuses
  the whole request, and `error.param` names the index (`[3].to`). Drop the per-message `ErrorCode`
  loop; check each entry's `status` for `canceled` instead.
- A Postmark batch is usually per-recipient mail (one notification per user). On a new account,
  pacing counts every recipient in a batch together, so a batch like that gets 422
  `young_sender_batch_too_large`. Send per-recipient mail, and any list over 100, one message at a
  time with `sendEach` from [migrate-sendgrid.md](migrate-sendgrid.md). It waits out `retry-after` on
  a 429, gives each message a key so a re-run with the same run id, order and messages within 24
  hours does not send a message twice, and reports a message whose outcome is unknown instead of
  calling it not sent. Never merge the recipients into one `to` array: every recipient would see
  every other recipient's address.
- `sendEmailBatchWithTemplates` maps the same way, with `template` on each message.

### Python

Before (Postmark's HTTP API, here with `requests`):

```python
import os

import requests


def send_welcome(to):
    response = requests.post(
        "https://api.postmarkapp.com/email",
        headers={"X-Postmark-Server-Token": os.environ["POSTMARK_SERVER_TOKEN"]},
        json={
            "From": "Acme <hello@example.com>",
            "To": to,
            "Subject": "Welcome to Acme",
            "HtmlBody": "<p>Welcome aboard.</p>",
            "TextBody": "Welcome aboard.",
            "MessageStream": "outbound",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["MessageID"]
```

After (with `send_email` from the Python helper in [rest-clients.md](rest-clients.md)):

```python mailfully-rest
# send_email (mailfully_client.py, from rest-clients.md) POSTs to https://api.mailfully.com/v1/emails.
import logging

from mailfully_client import send_email

logger = logging.getLogger(__name__)


def send_welcome(to):
    email_id, status = send_email({
        "from": "Acme <hello@example.com>",
        "to": [to],
        "subject": "Welcome to Acme",
        "html": "<p>Welcome aboard.</p>",
        "text": "Welcome aboard.",
    })
    if status == "canceled":
        logger.warning("Mailfully sent nothing for %s: every recipient is suppressed", email_id)
    return email_id
```

A Postmark Python client maps the same way: the PascalCase keys become the wire keys in the Field map.
`requests.HTTPError` becomes the helper's `MailfullyError`, with `.type`, `.status` and `.param`.

## Not supported, and what to do instead

- **Broadcast streams:** out of scope (see Message streams). Leave them on Postmark and list them in
  the report.
- **Suppressions (inactive recipients):** before switching live, tell the user to export Postmark's
  suppression list for each transactional stream and add those addresses on the Mailfully dashboard's
  Blocklist page. Without that, the first sends go to addresses that already bounced or complained,
  and a new account that keeps mailing dead addresses can have its sending paused.
  The page adds one address at a time and has no bulk import; if the list is large, suggest the user
  email it to contact@mailfully.com and ask what can be done.
- **Templates with logic, and layouts:** render them in app code (see Templates).
- **Per-message `TrackOpens` / `TrackLinks`:** one switch per sending domain (see Open and click
  tracking).
- **Inbound mail** (an inbound stream and its webhook): not covered by this migration. Leave it on
  Postmark and list it in the report.
- **Bounce and message APIs** (`getBounces`, `activateBounce`, `getOutboundMessageDetails`): no
  equivalent for bounces. Read a message's state with `mailfully.emails.get(id)` (its `last_event`
  uses status words such as `delivered` and `bounced`; see [api-essentials.md](api-essentials.md)).
- **Sender signatures and domains:** the sending domain is added and verified in Mailfully
  separately; see the main skill's go-live phase.

## Webhooks

The user creates the endpoint in the Mailfully dashboard (Webhooks, then Add webhook) and pastes the
new `whsec_…` secret into `MAILFULLY_WEBHOOK_SECRET`. Never create it with code.

The handler changes shape:

- Postmark does not sign its webhooks; a handler usually checks Basic Auth credentials in the URL or
  an IP allowlist. Mailfully signs every delivery with HMAC (`webhook-id`, `webhook-timestamp`,
  `webhook-signature`). Verify the raw body with `verifyMailfullyWebhook` (Node) or
  `verify_mailfully_webhook` (Python) from [webhooks.md](webhooks.md), and reject anything that
  fails. The Basic Auth check
  and the IP allowlist can go once the verifier is in place.
- Postmark's body is a flat PascalCase object with `RecordType`. Mailfully's is
  `{ type, created_at, data }`. Switch on `type`, and correlate by `data.email_id` (the `id` the send
  returned) instead of `MessageID`. The recipient list is `data.to`.
- Postmark's `Tag` and `Metadata` come back as `data.tags`, an array of `{ name, value }`.

| Postmark `RecordType` | Mailfully `type` |
| --- | --- |
| `Delivery` | `email.delivered` |
| `Bounce` with `Type: "HardBounce"` | `email.bounced` (hard bounces only; details in `data.bounce`) |
| `Bounce` with any other `Type` (`SoftBounce`, `Transient`, ...) | no event |
| `SpamComplaint` | `email.complained` (details in `data.complaint`) |
| `Open` | `email.opened` (only when tracking is on for the domain) |
| `Click` | `email.clicked` |
| `SubscriptionChange` | none (use the dashboard's Blocklist page) |
| none | `email.delivery_delayed`, `email.failed`: subscribe if the app wants them |

An address Postmark already marked inactive is refused at send time there; in Mailfully the send
returns `status: "canceled"` at once and no webhook follows. For a message refused later, see
`email.failed` in [webhooks.md](webhooks.md): not every failure fires it, so read `last_event`.

## Env

- `POSTMARK_SERVER_TOKEN` → `MAILFULLY_API_KEY`. The user pastes the key into the env file; add only
  the name to `.env.example`.
- `POSTMARK_API_TEST` (Postmark's test token) → a test key (`mf_test_…`). A test key runs the real
  send path without delivering to a real inbox (see Test keys in [api-essentials.md](api-essentials.md)).
- Any webhook Basic Auth user and password → `MAILFULLY_WEBHOOK_SECRET`, a new secret from the
  Mailfully dashboard. Remove the old variables once the verifier is live, and list them in the report.
- Keep Postmark wired in behind `EMAIL_PROVIDER`, with Postmark as the default, until the user's
  Mailfully account is approved.
