# Migrating from Nodemailer and SMTP

Mailfully is API-only today: there is no SMTP host to point an existing transport at. So an app that
sends through SMTP (Nodemailer, Python `smtplib`, Django, Rails or Laravel set to SMTP) moves to an
HTTP call. In Node, a small `sendMail` wrapper with Nodemailer's option names keeps every call site
unchanged; other stacks use the adapters and helpers in [rest-clients.md](rest-clients.md).

Read [api-essentials.md](api-essentials.md) first for the send body, test keys and errors. The Node SDK
needs Node 24 or later; on an older Node, see the end of Switch below.

## Detect

- npm: `nodemailer` (`nodemailer.createTransport({ host, port, secure, auth })`, or an `smtp://` /
  `smtps://` URL), and calls to `transporter.sendMail(...)`. Also a framework mailer configured with
  an SMTP host, port, user and password, since most of them wrap Nodemailer.
- Python: `smtplib` (`smtplib.SMTP(...)`, `server.send_message(msg)`, `server.sendmail(...)`) with
  `email.message.EmailMessage` or `email.mime`.
- Django: `EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"` (or no `EMAIL_BACKEND` with
  `EMAIL_HOST` set), plus `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
  `EMAIL_USE_TLS`.
- Rails: `config.action_mailer.delivery_method = :smtp` and `config.action_mailer.smtp_settings`.
- Laravel: `MAIL_MAILER=smtp`, with `MAIL_HOST`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`,
  `MAIL_ENCRYPTION`.
- Environment: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` (or `SMTP_PASSWORD`),
  `SMTP_SECURE`, `SMTP_URL`, `EMAIL_SERVER`, `MAIL_*`, and any provider credentials behind them.

## Field map

| Nodemailer `sendMail` option | Mailfully SDK | Wire |
| --- | --- | --- |
| `from` (string or `{ name, address }`) | `from`, a single `"Name <address>"` string | `from` |
| `to`, `cc`, `bcc` (string, comma list, object or array) | arrays of single `"Name <address>"` strings | `to`, `cc`, `bcc` (up to 50 across all three) |
| `replyTo` | `replyTo` | `reply_to` |
| `subject` | `subject` | `subject` |
| `text`, `html` (string, or a Buffer read as UTF-8; a path, URL or stream is refused) | `text`, `html` (strings) | `text`, `html` |
| `headers` (object, or an array of `{ key, value }`) | `headers`, one string value per name | `headers` |
| `inReplyTo`, `references` | `headers["In-Reply-To"]`, `headers["References"]` | `headers` |
| `attachments[].filename` | `filename` | `filename` |
| `attachments[].content` (string or Buffer) | `content`, as bare base64 | `content` |
| `attachments[].path` (a file) | read the file, then base64 into `content` | `content` |
| `attachments[].path` or `href` (a URL) | fetch it, then base64 into `content` | `content` |
| `attachments[].contentType` | `contentType` | `contentType` |
| `attachments[].cid` | `cid`, unchanged | `cid` |
| `info.messageId` | `data.id` (a ULID such as `01K6T0V1Q5H8C3D7E9F2G4J6KM`), plus `data.status` | `id`, `status` |
| transport `auth`, `host`, `port`, `pool`, `rateLimit` | none: the API key replaces them | |

Rules the wrapper below enforces, because the API would refuse the message otherwise:

- Every address string holds exactly ONE mailbox. A `{ name, address }` object becomes
  `"Name <address>"`, and a name with a comma, a period or another special character is quoted
  (`"Doe, Jane" <jane@example.com>`).
- A display name may not contain `<` or `>`, and a quoted local part (`"john doe"@example.com`) is
  refused.
- Headers are a flat object of strings. `From`, `Sender`, `Return-Path`, `X-Mailfully-Mid` and
  `X-SES-*`-prefixed headers are reserved and refused with a 422, case-insensitively, and so is a
  header name with a space or a colon. A header given twice (an array value, or one name twice in a
  `headers` array, in any letter case) is refused, since the API takes one value per name.

A Mailfully send can return `status: "canceled"`: every recipient was suppressed and nothing will be
sent. SMTP would have refused those recipients, and Nodemailer rejects with `EENVELOPE` when every
recipient is refused, so the wrapper throws in that case too. Never count a canceled send as sent.

## Before and after

### The wrapper

Before:

```js
const nodemailer = require("nodemailer");

const transporter = nodemailer.createTransport(
  {
    host: process.env.SMTP_HOST,
    port: Number(process.env.SMTP_PORT),
    secure: false,
    auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
  },
  { from: { name: "Acme", address: "hello@example.com" } },
);

async function sendReset(user, resetUrl) {
  const info = await transporter.sendMail({
    to: { name: user.name, address: user.email },
    subject: "Reset your password",
    text: `Reset it here: ${resetUrl}`,
    html: `<p><a href="${resetUrl}">Reset your password</a></p>`,
    attachments: [
      { filename: "terms.pdf", path: "./assets/terms.pdf" },
      { filename: "logo.png", path: "./assets/logo.png", cid: "logo" },
      { filename: "note.txt", content: Buffer.from("hi") },
    ],
  });
  return info.messageId;
}
```

After: save the wrapper next to the code that sends, then put the line that builds `transporter`
behind `EMAIL_PROVIDER` (shown after the wrapper), keeping the SMTP transport as the default. In a
TypeScript project, save this as `lib/mailer.ts`:

```ts mailfully-sdk
import { readFile } from "node:fs/promises";
import { basename } from "node:path";
import { Mailfully, type MailfullyError, type SendEmailInput } from "mailfully";

export type Address = string | { name?: string; address: string };
export type AddressList = Address | Address[];
type HeaderValue = string | number | boolean | { prepared?: boolean; value: string } | null | undefined;

export interface MailAttachment {
  filename?: string;
  content?: string | Buffer;
  /** How a string `content` is encoded, for example "base64". Plain text when absent. */
  encoding?: BufferEncoding;
  path?: string;
  href?: string;
  contentType?: string;
  cid?: string;
}

/** The Nodemailer message options this wrapper maps. Any other option is refused, never dropped. */
export interface MailOptions {
  from?: Address;
  to?: AddressList;
  cc?: AddressList;
  bcc?: AddressList;
  replyTo?: AddressList;
  subject?: string;
  text?: string | Buffer;
  html?: string | Buffer;
  headers?: Record<string, HeaderValue> | { key: string; value: HeaderValue }[];
  attachments?: MailAttachment[];
  inReplyTo?: string;
  references?: string | string[];
  [option: string]: unknown;
}

export interface SentInfo {
  /** The Mailfully email id. */
  messageId: string;
  status: "queued";
}

export type Callback<T> = (err: Error | null, result?: T) => void;

export class MailfullySendError extends Error {
  readonly statusCode: number | null;
  readonly type: string | null;
  readonly param: string | null;

  constructor(message: string, statusCode: number | null, type: string | null, param: string | null) {
    super(message);
    this.name = "MailfullySendError";
    this.statusCode = statusCode;
    this.type = type;
    this.param = param;
  }
}

const MAPPED = new Set([
  "from", "to", "cc", "bcc", "replyTo", "subject", "text", "html",
  "headers", "attachments", "inReplyTo", "references",
]);
const NAME_SPECIALS = /[()<>[\]:;@\\,."]/;

/** Splits a comma list into single addresses, keeping commas inside quotes, (comments) or <angle brackets>. */
function splitAddressList(list: string): string[] {
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

function formatAddress(a: { name?: string; address: string }): string {
  const address = a.address.trim();
  if (address.startsWith('"')) throw new Error(`quoted local parts are refused: ${address}`);
  const name = (a.name ?? "").trim();
  if (name === "") return address;
  if (/[<>]/.test(name)) throw new Error(`a display name may not contain < or >: ${name}`);
  const shown = NAME_SPECIALS.test(name) ? `"${name.replace(/["\\]/g, "\\$&")}"` : name;
  return `${shown} <${address}>`;
}

function addressList(list: AddressList | undefined): string[] {
  if (list === undefined) return [];
  return (Array.isArray(list) ? list : [list]).flatMap((a) =>
    typeof a === "string" ? splitAddressList(a) : [formatAddress(a)],
  );
}

/** One header value as a string, or undefined to skip it. Anything else is refused. */
function headerValue(name: string, value: unknown): string | undefined {
  if (value === null || value === undefined) return undefined;
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  if (typeof value === "object" && !Array.isArray(value) && typeof (value as { value?: unknown }).value === "string") {
    return (value as { value: string }).value;
  }
  throw new Error(`header ${name}: Mailfully takes one string value per header`);
}

function headerRecord(options: MailOptions): Record<string, string> {
  const out: Record<string, string> = {};
  const add = (name: string, value: unknown): void => {
    const text = headerValue(name, value);
    if (text === undefined) return;
    if (Object.keys(out).some((k) => k.toLowerCase() === name.toLowerCase())) {
      throw new Error(`header ${name} is repeated: Mailfully takes each header once`);
    }
    out[name] = text;
  };
  const headers: unknown = options.headers;
  if (Array.isArray(headers)) {
    for (const entry of headers as unknown[]) {
      const key = (entry as { key?: unknown } | null)?.key;
      if (typeof key !== "string") throw new Error("headers: each array entry needs a string key");
      add(key, (entry as { value?: unknown }).value);
    }
  } else if (headers !== null && typeof headers === "object") {
    for (const [name, value] of Object.entries(headers)) add(name, value);
  } else if (headers !== undefined) {
    throw new Error("headers: pass an object or an array of { key, value }");
  }
  if (options.inReplyTo) add("In-Reply-To", options.inReplyTo);
  if (options.references) {
    add("References", Array.isArray(options.references) ? options.references.join(" ") : options.references);
  }
  return out;
}

/** text and html: a string, or a Buffer read as UTF-8. Paths, URLs and streams are refused. */
function bodyPart(field: "text" | "html", value: unknown): string | undefined {
  if (value === undefined) return undefined;
  if (typeof value === "string") return value;
  if (Buffer.isBuffer(value)) return value.toString("utf8");
  throw new Error(`${field}: pass a string or a Buffer; read a file, URL or stream into a string first`);
}

async function base64FromUrl(url: string): Promise<string> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`could not fetch attachment ${url}: HTTP ${res.status}`);
  return Buffer.from(await res.arrayBuffer()).toString("base64");
}

async function toAttachment(a: MailAttachment, index: number) {
  const url = a.href ?? (a.path && /^https?:\/\//i.test(a.path) ? a.path : undefined);
  let content: string;
  if (a.content !== undefined) {
    if (typeof a.content === "string") content = Buffer.from(a.content, a.encoding ?? "utf8").toString("base64");
    else if (Buffer.isBuffer(a.content)) content = a.content.toString("base64");
    else throw new Error(`attachment ${index}: stream content is not supported; read it into a Buffer first`);
  } else if (url !== undefined) {
    content = await base64FromUrl(url);
  } else if (a.path !== undefined && !a.path.startsWith("data:")) {
    content = (await readFile(a.path)).toString("base64");
  } else {
    throw new Error(`attachment ${index}: needs content, a file path or a URL`);
  }
  const filename = a.filename ?? (a.path && !url ? basename(a.path) : `attachment-${index + 1}`);
  return {
    filename,
    content,
    ...(a.contentType ? { contentType: a.contentType } : {}),
    ...(a.cid ? { cid: a.cid } : {}),
  };
}

/** Converts Nodemailer options to a Mailfully send. Also used to build the list for a send loop. */
export async function toSendEmailInput(options: MailOptions): Promise<SendEmailInput> {
  const unsupported = Object.keys(options).filter((k) => !MAPPED.has(k) && options[k] !== undefined);
  if (unsupported.length > 0) throw new Error(`Nodemailer options not supported by Mailfully: ${unsupported.join(", ")}`);
  if (options.from === undefined) throw new Error("from is required");
  const from = addressList(options.from);
  if (from.length !== 1) throw new Error("from must be exactly one address");
  const text = bodyPart("text", options.text);
  const html = bodyPart("html", options.html);
  const headers = headerRecord(options);
  const cc = addressList(options.cc);
  const bcc = addressList(options.bcc);
  const replyTo = addressList(options.replyTo);
  const attachments = await Promise.all((options.attachments ?? []).map(toAttachment));
  return {
    from: from[0] ?? "",
    to: addressList(options.to),
    ...(cc.length > 0 ? { cc } : {}),
    ...(bcc.length > 0 ? { bcc } : {}),
    ...(replyTo.length > 0 ? { replyTo } : {}),
    ...(options.subject !== undefined ? { subject: options.subject } : {}),
    ...(text !== undefined ? { text } : {}),
    ...(html !== undefined ? { html } : {}),
    ...(Object.keys(headers).length > 0 ? { headers } : {}),
    ...(attachments.length > 0 ? { attachments } : {}),
  };
}

let client: Mailfully | undefined;
/** A request with no answer gives up after 10 seconds (see api-essentials.md). */
const timedFetch: typeof fetch = (input, init) =>
  fetch(input, { ...init, signal: init?.signal ?? AbortSignal.timeout(10_000) });
function mailfully(): Mailfully {
  if (client) return client;
  const apiKey = process.env.MAILFULLY_API_KEY;
  if (!apiKey) throw new Error("MAILFULLY_API_KEY is not set");
  client = new Mailfully({ apiKey, fetch: timedFetch });
  return client;
}

function sendError(error: MailfullyError): MailfullySendError {
  return new MailfullySendError(
    `Mailfully ${error.type ?? "error"} (${String(error.statusCode)}): ${error.message}`,
    error.statusCode,
    error.type,
    error.param,
  );
}

/** Same name and options as Nodemailer's sendMail (promise form). Resolves with the Mailfully id as messageId. */
export async function sendMail(options: MailOptions): Promise<SentInfo> {
  const { data, error } = await mailfully().emails.send(await toSendEmailInput(options));
  if (error) throw sendError(error);
  if (data.status === "canceled") {
    throw new MailfullySendError(`Mailfully sent nothing for ${data.id}: every recipient is suppressed`, 202, "canceled", null);
  }
  return { messageId: data.id, status: data.status };
}

/** Checks the API key with one read. A key limited to sending still counts as working. */
async function verifyKey(): Promise<true> {
  const { error } = await mailfully().domains.list();
  if (error === null || (error.statusCode === 403 && error.type === "insufficient_scope")) return true;
  throw sendError(error);
}

function settle<T>(promise: Promise<T>, callback: Callback<T>): void {
  void promise.then(
    (result) => callback(null, result),
    (err: unknown) => callback(err instanceof Error ? err : new Error(String(err))),
  );
}

/** Stands in for the transporter nodemailer.createTransport returns. */
export class MailfullyTransport {
  readonly #defaults: MailOptions;

  constructor(defaults: MailOptions = {}) {
    this.#defaults = defaults;
  }

  /** Promise form, or Nodemailer's callback form `(err, info)`. */
  sendMail(options: MailOptions): Promise<SentInfo>;
  sendMail(options: MailOptions, callback: Callback<SentInfo>): void;
  sendMail(options: MailOptions, callback?: Callback<SentInfo>): Promise<SentInfo> | void {
    const sent = sendMail({ ...this.#defaults, ...options });
    if (!callback) return sent;
    settle(sent, callback);
  }

  /** Like Nodemailer's verify: resolves true when the API key works. */
  verify(): Promise<true>;
  verify(callback: Callback<true>): void;
  verify(callback?: Callback<true>): Promise<true> | void {
    const checked = verifyKey();
    if (!callback) return checked;
    settle(checked, callback);
  }

  /** Nothing to close: there is no connection pool. */
  close(): void {}

  /** Nodemailer plugins do not run here; refuse rather than send mail the plugin never touched. */
  use(step: string): never {
    throw new Error(`Nodemailer plugins (use("${step}")) do not run with Mailfully: build the message before sendMail`);
  }
}

/** Stands in for nodemailer.createTransport(transport, defaults): `defaults` fills unset options. */
export function createTransport(defaults: MailOptions = {}): MailfullyTransport {
  return new MailfullyTransport(defaults);
}
```

In a JavaScript project, save the same wrapper without types as `lib/mailer.mjs`. The `.mjs` extension
makes it an ES module whatever the project's `"type"` is:

```js
import { readFile } from "node:fs/promises";
import { basename } from "node:path";
import { Mailfully } from "mailfully";

export class MailfullySendError extends Error {
  constructor(message, statusCode, type, param) {
    super(message);
    this.name = "MailfullySendError";
    this.statusCode = statusCode;
    this.type = type;
    this.param = param;
  }
}

const MAPPED = new Set([
  "from", "to", "cc", "bcc", "replyTo", "subject", "text", "html",
  "headers", "attachments", "inReplyTo", "references",
]);
const NAME_SPECIALS = /[()<>[\]:;@\\,."]/;

/** Splits a comma list into single addresses, keeping commas inside quotes, (comments) or <angle brackets>. */
function splitAddressList(list) {
  const out = [];
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

function formatAddress(a) {
  const address = a.address.trim();
  if (address.startsWith('"')) throw new Error(`quoted local parts are refused: ${address}`);
  const name = (a.name ?? "").trim();
  if (name === "") return address;
  if (/[<>]/.test(name)) throw new Error(`a display name may not contain < or >: ${name}`);
  const shown = NAME_SPECIALS.test(name) ? `"${name.replace(/["\\]/g, "\\$&")}"` : name;
  return `${shown} <${address}>`;
}

function addressList(list) {
  if (list === undefined) return [];
  return (Array.isArray(list) ? list : [list]).flatMap((a) =>
    typeof a === "string" ? splitAddressList(a) : [formatAddress(a)],
  );
}

/** One header value as a string, or undefined to skip it. Anything else is refused. */
function headerValue(name, value) {
  if (value === null || value === undefined) return undefined;
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  if (typeof value === "object" && !Array.isArray(value) && typeof value.value === "string") return value.value;
  throw new Error(`header ${name}: Mailfully takes one string value per header`);
}

function headerRecord(options) {
  const out = {};
  const add = (name, value) => {
    const text = headerValue(name, value);
    if (text === undefined) return;
    if (Object.keys(out).some((k) => k.toLowerCase() === name.toLowerCase())) {
      throw new Error(`header ${name} is repeated: Mailfully takes each header once`);
    }
    out[name] = text;
  };
  const headers = options.headers;
  if (Array.isArray(headers)) {
    for (const entry of headers) {
      if (typeof entry?.key !== "string") throw new Error("headers: each array entry needs a string key");
      add(entry.key, entry.value);
    }
  } else if (headers !== null && typeof headers === "object") {
    for (const [name, value] of Object.entries(headers)) add(name, value);
  } else if (headers !== undefined) {
    throw new Error("headers: pass an object or an array of { key, value }");
  }
  if (options.inReplyTo) add("In-Reply-To", options.inReplyTo);
  if (options.references) {
    add("References", Array.isArray(options.references) ? options.references.join(" ") : options.references);
  }
  return out;
}

/** text and html: a string, or a Buffer read as UTF-8. Paths, URLs and streams are refused. */
function bodyPart(field, value) {
  if (value === undefined) return undefined;
  if (typeof value === "string") return value;
  if (Buffer.isBuffer(value)) return value.toString("utf8");
  throw new Error(`${field}: pass a string or a Buffer; read a file, URL or stream into a string first`);
}

async function base64FromUrl(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`could not fetch attachment ${url}: HTTP ${res.status}`);
  return Buffer.from(await res.arrayBuffer()).toString("base64");
}

async function toAttachment(a, index) {
  const url = a.href ?? (a.path && /^https?:\/\//i.test(a.path) ? a.path : undefined);
  let content;
  if (a.content !== undefined) {
    if (typeof a.content === "string") content = Buffer.from(a.content, a.encoding ?? "utf8").toString("base64");
    else if (Buffer.isBuffer(a.content)) content = a.content.toString("base64");
    else throw new Error(`attachment ${index}: stream content is not supported; read it into a Buffer first`);
  } else if (url !== undefined) {
    content = await base64FromUrl(url);
  } else if (a.path !== undefined && !a.path.startsWith("data:")) {
    content = (await readFile(a.path)).toString("base64");
  } else {
    throw new Error(`attachment ${index}: needs content, a file path or a URL`);
  }
  const filename = a.filename ?? (a.path && !url ? basename(a.path) : `attachment-${index + 1}`);
  return {
    filename,
    content,
    ...(a.contentType ? { contentType: a.contentType } : {}),
    ...(a.cid ? { cid: a.cid } : {}),
  };
}

/** Converts Nodemailer options to a Mailfully send. Also used to build the list for a send loop. */
export async function toSendEmailInput(options) {
  const unsupported = Object.keys(options).filter((k) => !MAPPED.has(k) && options[k] !== undefined);
  if (unsupported.length > 0) throw new Error(`Nodemailer options not supported by Mailfully: ${unsupported.join(", ")}`);
  if (options.from === undefined) throw new Error("from is required");
  const from = addressList(options.from);
  if (from.length !== 1) throw new Error("from must be exactly one address");
  const text = bodyPart("text", options.text);
  const html = bodyPart("html", options.html);
  const headers = headerRecord(options);
  const cc = addressList(options.cc);
  const bcc = addressList(options.bcc);
  const replyTo = addressList(options.replyTo);
  const attachments = await Promise.all((options.attachments ?? []).map(toAttachment));
  return {
    from: from[0],
    to: addressList(options.to),
    ...(cc.length > 0 ? { cc } : {}),
    ...(bcc.length > 0 ? { bcc } : {}),
    ...(replyTo.length > 0 ? { replyTo } : {}),
    ...(options.subject !== undefined ? { subject: options.subject } : {}),
    ...(text !== undefined ? { text } : {}),
    ...(html !== undefined ? { html } : {}),
    ...(Object.keys(headers).length > 0 ? { headers } : {}),
    ...(attachments.length > 0 ? { attachments } : {}),
  };
}

let client;
/** A request with no answer gives up after 10 seconds (see api-essentials.md). */
const timedFetch = (input, init) =>
  fetch(input, { ...init, signal: init?.signal ?? AbortSignal.timeout(10_000) });
function mailfully() {
  if (client) return client;
  const apiKey = process.env.MAILFULLY_API_KEY;
  if (!apiKey) throw new Error("MAILFULLY_API_KEY is not set");
  client = new Mailfully({ apiKey, fetch: timedFetch });
  return client;
}

function sendError(error) {
  return new MailfullySendError(
    `Mailfully ${error.type ?? "error"} (${String(error.statusCode)}): ${error.message}`,
    error.statusCode,
    error.type,
    error.param,
  );
}

/** Same name and options as Nodemailer's sendMail (promise form). Resolves with the Mailfully id as messageId. */
export async function sendMail(options) {
  const { data, error } = await mailfully().emails.send(await toSendEmailInput(options));
  if (error) throw sendError(error);
  if (data.status === "canceled") {
    throw new MailfullySendError(`Mailfully sent nothing for ${data.id}: every recipient is suppressed`, 202, "canceled", null);
  }
  return { messageId: data.id, status: data.status };
}

/** Checks the API key with one read. A key limited to sending still counts as working. */
async function verifyKey() {
  const { error } = await mailfully().domains.list();
  if (error === null || (error.statusCode === 403 && error.type === "insufficient_scope")) return true;
  throw sendError(error);
}

function settle(promise, callback) {
  void promise.then(
    (result) => callback(null, result),
    (err) => callback(err instanceof Error ? err : new Error(String(err))),
  );
}

/** Stands in for the transporter nodemailer.createTransport returns. */
export class MailfullyTransport {
  #defaults;

  constructor(defaults = {}) {
    this.#defaults = defaults;
  }

  /** Promise form, or Nodemailer's callback form `(err, info)`. */
  sendMail(options, callback) {
    const sent = sendMail({ ...this.#defaults, ...options });
    if (!callback) return sent;
    settle(sent, callback);
  }

  /** Like Nodemailer's verify: resolves true when the API key works. */
  verify(callback) {
    const checked = verifyKey();
    if (!callback) return checked;
    settle(checked, callback);
  }

  /** Nothing to close: there is no connection pool. */
  close() {}

  /** Nodemailer plugins do not run here; refuse rather than send mail the plugin never touched. */
  use(step) {
    throw new Error(`Nodemailer plugins (use("${step}")) do not run with Mailfully: build the message before sendMail`);
  }
}

/** Stands in for nodemailer.createTransport(transport, defaults): `defaults` fills unset options. */
export function createTransport(defaults = {}) {
  return new MailfullyTransport(defaults);
}
```

Copy whichever wrapper block fits exactly as written, the whole fenced block; never retype or
paraphrase it.

### Switch

In the file from the "before" example, choose the transport by `EMAIL_PROVIDER`. The SMTP transport
stays exactly as it was and stays the default, so merging this changes nothing at runtime. Every
`transporter.sendMail(...)` call stays as it was, and so does its error handling: the wrapper's
`sendMail` throws `MailfullySendError` (with `type: "canceled"` when every recipient is suppressed)
where Nodemailer threw its own error.

In an ES module file (one that uses `import`), with each call passing its own `from` and no transport
defaults:

```js
import nodemailer from "nodemailer";
import { createTransport as mailfullyTransport } from "./lib/mailer.mjs";

// EMAIL_PROVIDER=mailfully selects Mailfully. Unset, or any other value, keeps the SMTP transport.
const transporter =
  process.env.EMAIL_PROVIDER === "mailfully"
    ? mailfullyTransport()
    : nodemailer.createTransport({
        host: process.env.SMTP_HOST,
        port: Number(process.env.SMTP_PORT),
        secure: false,
        auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
      });
// every transporter.sendMail({ from, to, ... }) call stays as it was
```

In CommonJS with transport defaults, as in the "before" example, pass the same defaults to both:

```js
const nodemailer = require("nodemailer");
const { createTransport: mailfullyTransport } = require("./lib/mailer.mjs");

const defaults = { from: { name: "Acme", address: "hello@example.com" } };

// EMAIL_PROVIDER=mailfully selects Mailfully. Unset, or any other value, keeps the SMTP transport.
const transporter =
  process.env.EMAIL_PROVIDER === "mailfully"
    ? mailfullyTransport(defaults)
    : nodemailer.createTransport(
        {
          host: process.env.SMTP_HOST,
          port: Number(process.env.SMTP_PORT),
          secure: false,
          auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
        },
        defaults,
      );
// every transporter.sendMail(...) call stays as it was
```

On Node 24, the SDK's minimum, `require("./lib/mailer.mjs")` works: Node loads that relative ES
module through `require`, and the wrapper's own `import` of `mailfully` resolves. Never write
`require("mailfully")` itself: the package exports only an `import` condition, so that line fails
with `ERR_PACKAGE_PATH_NOT_EXPORTED` on every Node version. In TypeScript, import from `./lib/mailer`
(or `./lib/mailer.js` under NodeNext) instead of `./lib/mailer.mjs`. A handler that turns a send
error into its response keeps doing so for `MailfullySendError`; see Replacing an existing send path
in [api-essentials.md](api-essentials.md) for keeping the response shape.

What changes for callers:

- `transporter.sendMail(options)` returns a promise, and `transporter.sendMail(options, callback)`
  calls `callback(err, info)` and returns nothing, as in Nodemailer. Both forms keep working.
- `info.messageId` is the Mailfully id. `info.accepted`, `info.rejected`, `info.response` and
  `info.envelope` do not exist; change any code that reads them, and say so in the report.
- A failure rejects (or reaches the callback) with `MailfullySendError` (`statusCode`, `type`,
  `param`) instead of a Nodemailer error with `code` and `responseCode`. A canceled send fails with
  `type: "canceled"`.
- `transporter.verify()` (promise or callback) checks the API key with one read instead of opening an
  SMTP connection. It is a network call, so keep it at startup, never per message.
  `transporter.close()` does nothing.
- `transporter.use(...)` throws: a Nodemailer plugin (such as a template engine on `compile`) does
  not run here. Render the message before `sendMail` and remove the `use` call.
- `text` and `html` must be strings or Buffers (a Buffer is read as UTF-8). A `{ path }`, `{ href }`
  or stream body is refused; read it into a string first.
- Before switching, search the code for:
  - options outside the Field map (`raw`, `envelope`, `icalEvent`, `alternatives`, `amp`, `list`,
    `priority`, `messageId`, `date`, `dkim`, `attachDataUrls`). The wrapper refuses them instead of
    dropping them silently, so remove or replace each one at migration time; a `list` option usually
    means newsletter mail, which stays on the old setup (see Not supported);
  - the reserved headers in the rules above (`From`, `Sender`, `Return-Path`, `X-Mailfully-Mid` and
    the prefixed ones), set in `headers`, which the API refuses with a 422;
  - a header set twice, or a `headers` value that is an array;
  - `transporter.use(` plugin registrations and `sendMail` calls with a callback, to confirm each one
    still behaves as described above.
- A `data:` URI used as an attachment `path` is refused; decode it into `content` with
  `encoding: "base64"` instead.

On Node older than 24 the SDK will not run. Keep the conversion functions, replace `SendEmailInput`
with `MailfullyEmail` and the `mailfully()` call with `sendEmail` from the `fetch` helper in
[rest-clients.md](rest-clients.md), and rename `replyTo` to `reply_to` in `toSendEmailInput` (it
builds the wire body there). `sendEmail` throws `MailfullyApiError` on a non-2xx and returns
`{ id, status }`, so `sendError` goes. The helper has no read call, so `verify` resolves `true`
without a request there. Where `require()` of an ES module fails on that Node, load the wrapper with
`await import("./lib/mailer.mjs")`. A CommonJS project on Node 24 or later follows this paragraph
too unless it keeps the wrapper as the `.mjs` file above: compiled to CommonJS, the wrapper's
`import { Mailfully } from "mailfully"` becomes `require("mailfully")`, which fails.

### A loop that sends one email per recipient

SMTP code often loops over users and calls `sendMail` once per user. That stays one message per
recipient: never merge the recipients into one `to` array, or every recipient sees every other
recipient's address. On a new account, live mail is paced per minute, so a loop of plain `sendMail`
calls gets 429 `send_rate_limited`.

Build the messages with `toSendEmailInput` and send them with `sendEach` from
[migrate-sendgrid.md](migrate-sendgrid.md). It sends one at a time, waits out `retry-after` on a 429,
gives each message a key so a re-run with the same run id, order and messages within 24 hours does
not send a message twice, and reports a message whose outcome is unknown instead of calling it not
sent:

```ts
import { toSendEmailInput } from "./lib/mailer";
import { sendEach } from "./lib/mailfully-send-each";

const messages = await Promise.all(
  users.map((user) =>
    toSendEmailInput({
      from: { name: "Acme", address: "hello@example.com" },
      to: { name: user.name, address: user.email },
      subject: "Your weekly summary",
      text: summaryText(user),
    }),
  ),
);
const result = await sendEach(apiKey, `weekly-summary:${weekId}`, messages);
```

Report `result.stoppedAt` and any `canceled` entry in `result.sent` to the user, as that section
describes. A loop over more than a handful of recipients belongs in the app's background job runner,
not in a request.

### Python `smtplib`

Before:

```python
import os
import smtplib
from email.message import EmailMessage


def send_welcome(to):
    msg = EmailMessage()
    msg["From"] = "Acme <hello@example.com>"
    msg["To"] = to
    msg["Subject"] = "Welcome to Acme"
    msg.set_content("Welcome aboard.")
    msg.add_alternative("<p>Welcome aboard.</p>", subtype="html")
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        server.send_message(msg)
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
        "text": "Welcome aboard.",
        "html": "<p>Welcome aboard.</p>",
    })
    if status == "canceled":
        logger.warning("Mailfully sent nothing for %s: every recipient is suppressed", email_id)
    return email_id
```

`smtplib.SMTPException` becomes the helper's `MailfullyError`, with `.type`, `.status` and `.param`.
An attachment added with `msg.add_attachment(data, maintype, subtype, filename=...)` becomes
`{"filename": ..., "content": base64.b64encode(data).decode("ascii"), "contentType": "maintype/subtype"}`
in `"attachments"`. A per-recipient loop uses `send_each` from [migrate-sendgrid.md](migrate-sendgrid.md).

### Django, Rails and Laravel

- **Django:** add the Mailfully email backend in [rest-clients.md](rest-clients.md) and select it
  with the `EMAIL_PROVIDER` block shown there, after the existing SMTP settings, which stay the
  default. Every `send_mail`, `EmailMessage` and `EmailMultiAlternatives` call stays as it is.
  `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` and `EMAIL_USE_TLS` become
  removable after the switch (see Env).
- **Rails:** add the Action Mailer delivery method in [rest-clients.md](rest-clients.md) and select it
  with the `EMAIL_PROVIDER` line shown there, after the existing `delivery_method`, which stays the
  default. Mailers and views stay as they are, and `smtp_settings` becomes removable after the switch
  (see Env).
- **Laravel and anything else:** there is no ready-made driver. Call the PHP helper
  (`mailfully_send` in [rest-clients.md](rest-clients.md)) from the place that sends, such as a
  queued job, only when `EMAIL_PROVIDER` is `mailfully`; the existing mailer stays the default. Pass
  the rendered view as `html` (`view('emails.welcome', $data)->render()`) and a `text` part. Use the
  matching helper in that file for Ruby without Rails or Go. `MAIL_HOST`, `MAIL_PORT`,
  `MAIL_USERNAME`, `MAIL_PASSWORD` and `MAIL_ENCRYPTION` become removable after the switch (see Env).

## Not supported, and what to do instead

- **An SMTP endpoint:** Mailfully is API-only today. A device or third-party tool that can only speak
  SMTP (a printer, a hosted form builder, a CMS plugin with no HTTP option) cannot move to Mailfully;
  list it in the report and leave it on its current SMTP server.
- **Newsletter and list mail** (`list` headers such as `List-Unsubscribe`, mail to a mailing list):
  out of scope. Leave it on the old setup and list it in the report. An unsubscribe list cannot be
  imported, so moving that mail risks mailing people who opted out (see Marketing in
  [api-essentials.md](api-essentials.md)).
- **Suppressions:** before switching live, tell the user to export the bounce and complaint lists
  from the SMTP relay or the provider behind it (a mailbox that collects bounces counts too) and add
  those addresses on the Mailfully dashboard's Blocklist page. Without that, the first sends go to
  addresses that already bounced or complained, and a new account that keeps mailing dead addresses
  can have its sending paused. The page adds one address at a time and has no bulk import; if the
  list is large, suggest the user email it to contact@mailfully.com and ask what can be done.
- **`raw` messages and `envelope`:** Mailfully builds the MIME message itself and sends to the
  `to`, `cc` and `bcc` you pass. Rebuild such a send from its parts.
- **Calendar invites (`icalEvent`), `amp`, `watchHtml` and extra `alternatives`:** not supported. An
  `.ics` file can still go as an ordinary attachment with `contentType: "text/calendar"`.
- **DKIM options (`dkim`):** Mailfully signs mail for a verified sending domain; drop the option and
  the private key, and set the domain up in the main skill's go-live phase.
- **Stream attachments, and `text` or `html` given as a path, URL or stream:** read them into a
  Buffer or a string first.
- **Transport pooling and rate limits (`pool`, `maxConnections`, `rateLimit`):** gone with the
  transport. Pacing is handled by `sendEach` above.

## Open and click tracking

Open and click tracking is ON by default for a new Mailfully domain: Mailfully adds an open pixel and
rewrites links in `html`, including password-reset and sign-in links. SMTP sends tracked nothing
unless the old provider added it, so ask the user whether the old setup tracked opens or clicks. If it
did not, turn tracking off with the domain's Tracking switch in the dashboard. A key the user pasted
from the dashboard (not one from the browser sign-in, which is refused here) can use the CLI instead
(the domain id is the `dom_…` value from `domains list`):

```bash
npx -y mailfully@1.4.0 domains list
npx -y mailfully@1.4.0 domains tracking <domain-id> --disable
```

Say in the report which way the switch was set, and why.

## Webhooks

SMTP gives no delivery events after the server accepts a message, so most of these apps have no
webhook handler to migrate. To learn about bounces and complaints, add one: the user creates the
endpoint in the Mailfully dashboard (Webhooks, then Add webhook) and pastes the new `whsec_…` secret
into `MAILFULLY_WEBHOOK_SECRET`. Never create it with code. Write the handler with the verifier
(`verifyMailfullyWebhook` in Node, `verify_mailfully_webhook` in Python) and event names in
[webhooks.md](webhooks.md), and correlate events by `data.email_id`, the `messageId`
the wrapper returns.

If the app parsed bounce emails from a mailbox (a bounce address it reads over IMAP), the
`email.bounced` and `email.complained` events replace that; list the mailbox reader in the report as
removable.

## Env

- List every SMTP setting in the report as removable: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`,
  `SMTP_PASS`, `SMTP_SECURE`, `SMTP_URL`, `EMAIL_SERVER`, or the framework's `EMAIL_*` / `MAIL_*`
  names, by the exact names the app uses.
- Add `MAILFULLY_API_KEY`. The user pastes the key into the env file; add only the name to
  `.env.example`.
- Add `MAILFULLY_WEBHOOK_SECRET` only if the app gets a webhook handler.
- Keep the SMTP transport wired in behind `EMAIL_PROVIDER`, with SMTP as the default, until the
  user's Mailfully account is approved. The SMTP settings are removed after the switch, when nothing
  reads them any more; the user does that, not the migration.
