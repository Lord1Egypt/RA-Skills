# Drafts, Identities, Attachments, and Sending

Sending is two objects: an `Email` in Drafts and an `EmailSubmission` that hands it to the mail system. Doing it in one request is what keeps Drafts and Sent honest.

**Before composing**, read `## Identities` in `~/Clawic/data/fastmail-api/memory.md` and `default_identity` from config — the From address is a decision, and the wrong one is visible to the recipient forever. **After a new identity appears, a custom domain is verified, or a send fails in an instructive way**, write the identity row, the domain row in the shared `~/Clawic/data/domains/domains.md`, and the failure in `## Pain Points` (`memory-template.md`).

**Contents:** [Identities](#identities) · [The Draft](#the-draft) · [Attachments](#attachments) · [Submission in One Request](#submission-in-one-request) · [Envelope Versus Headers](#envelope-versus-headers) · [Undo Send](#undo-send) · [Replies and Threading](#replies-and-threading) · [When a Send Fails](#when-a-send-fails) · [Custom Domains](#custom-domains) · [Bulk Sending](#bulk-sending)

## Identities

`Identity/get` returns every address this account may send as: `id`, `name`, `email`, `replyTo`, `bcc`, `textSignature`, `htmlSignature`, `mayDelete`.

- **`identityId` and the `from` header must agree.** Sending with an identity that does not own the From address is rejected with `forbiddenFrom` — a permissions answer to what looks like a content problem.
- Aliases and custom-domain addresses appear as their own identities once configured on the account. If the address the user wants is not in `Identity/get`, it does not exist yet; no request shape creates it.
- Signatures live on the identity. A draft that pastes a signature into the body will produce two of them in clients that append the identity's own.
- Wildcard or catch-all addresses on a custom domain can receive without being sendable. Receiving works, sending returns `forbiddenFrom`, and the difference surprises people.

Record `identityId` → address → domain in `## Identities` the first time you resolve it.

## The Draft

Create the `Email` with `$draft` set, in the `drafts`-role mailbox:

```json
["Email/set", {"accountId": "u1a2b3c4", "create": {
  "draft": {
    "mailboxIds": {"<drafts>": true},
    "keywords": {"$draft": true},
    "from": [{"name": "Me", "email": "me@example.com"}],
    "to": [{"name": "Marta", "email": "marta@acme.example"}],
    "subject": "Invoice 2026-114",
    "bodyValues": {"b1": {"value": "Text body here.\n", "charset": "utf-8"}},
    "textBody": [{"partId": "b1", "type": "text/plain"}]
  }}}, "c0"]
```

- `bodyValues` holds the content, keyed by `partId`; `textBody` and `htmlBody` reference those parts. For both formats, define two body values and list one in each — the client picks.
- Omitting `$draft` produces a message sitting in Drafts that clients will not treat as editable.
- `receivedAt` and message ids are server-assigned. Do not invent them.
- Verify recipients before submission, not after. `to`, `cc` and `bcc` are lists of `{name, email}` objects, and a typo in an address is not an error at any layer — it is a delivery to someone else.

## Attachments

Three steps, in order:

1. **Upload the blob** — POST the bytes to the session's `uploadUrl` with `{accountId}` filled in and the correct `Content-Type`. The response gives `blobId`, `type`, `size`.
2. **Reference it** in the email's `attachments`: `{"blobId": "<id>", "type": "application/pdf", "name": "invoice.pdf", "disposition": "attachment"}`.
3. **Create the email in the same session**, promptly. An uploaded blob that is never referenced by an object is eventually reaped by the server; a blobId from last week may be gone.

Sizing:

```
base64_bytes ≈ raw_bytes × 1.33
budget base64_bytes for all attachments against maxSizeAttachmentsPerEmail
each upload against maxSizeUpload, parallel uploads against maxConcurrentUpload
```

A 20 MB file is ~27 MB of message. Checking the raw size against the limit is the standard way to build an email that fails at submission after everything else worked.

`disposition: "inline"` plus a `cid` reference in the HTML body embeds an image; `"attachment"` lists it. Inline images generally do not make `hasAttachment` true in a later search (`search.md`).

## Submission in One Request

Create the draft and submit it in one envelope, with the submission cleaning up the draft on success:

```json
["EmailSubmission/set", {"accountId": "u1a2b3c4",
  "create": {"sendIt": {"emailId": "#draft", "identityId": "I77a"}},
  "onSuccessUpdateEmail": {"#sendIt": {
    "mailboxIds/<drafts>": null,
    "mailboxIds/<sent>": true,
    "keywords/$draft": null,
    "keywords/$seen": true
  }}}, "c1"]
```

- `"#draft"` is the creation id from the `Email/set` earlier in the same envelope (`requests.md`).
- `onSuccessUpdateEmail` is keyed by `#<submissionCreationId>` and applies **only if the submission succeeded**. This is what makes "sent" and "not in drafts" a single atomic outcome.
- `onSuccessDestroyEmail` exists for the case where no Sent copy is wanted. Rare, and irreversible.
- Doing this as two separate requests is the standard way to end up with a message both sent and still in Drafts, or sent twice after a retry.
- The submission response carries `undoStatus`, `sendAt`, and `deliveryStatus` per recipient once known.

## Envelope Versus Headers

Two different things, and only one of them decides delivery:

| | What it is | Who sees it |
|---|---|---|
| `envelope.mailFrom` / `envelope.rcptTo` | The SMTP envelope — where the message actually goes | The mail systems; bounces go to `mailFrom` |
| `from` / `to` / `cc` / `bcc` headers | Display | The recipient |

- Omit `envelope` and the server derives it from the headers, which is correct almost always.
- **Bcc works by envelope**: the address is in `rcptTo` and absent from the headers. Putting an address in the `bcc` header and expecting the server to strip it is provider-dependent behaviour to not rely on.
- A custom `mailFrom` (for bounce handling on a separate address) must be an address the identity is allowed to use, or the submission is rejected.

## Undo Send

If the account has a delayed-send window configured, the submission sits with `undoStatus: "pending"` until it expires.

- Cancel with `EmailSubmission/set` update: `{"<submissionId>": {"undoStatus": "canceled"}}`.
- Once `undoStatus` is `final`, the message is gone. There is no recall, no unsend, and no support path.
- Say the window out loud when sending something consequential — "cancellable for the next N seconds" is actionable; "sent" is not.
- With no delayed-send configured, the window is zero. Verify recipients before submitting rather than planning to catch it after.

## Replies and Threading

- Set `inReplyTo` to the parent's `Message-ID` header value and `references` to the parent's `references` plus that value. Threading in the recipient's client depends on those headers, not on your `threadId`.
- `threadId` is the server's local grouping and is read-only; it cannot be set to force a thread.
- Mark the parent `$answered` in the same envelope — it is a one-line patch and it is what makes "unanswered threads" searches work later (`search.md`).
- Quoting: include the quoted text in the body you build. Nothing quotes automatically.

## When a Send Fails

| Signal | Cause | Move |
|---|---|---|
| `forbiddenFrom` | Identity does not own the From address | Re-read `Identity/get`; the address may exist for receiving only |
| `invalidEmail` in `notCreated` | Malformed recipient address | Fix the address; every other recipient still needs re-checking |
| `tooManyRecipients` | Per-message recipient cap | Split the send; a large recipient list is a mailing job, not an email (`Bulk Sending`) |
| `tooLarge` | Attachment budget exceeded | Recompute with the `× 1.33` factor; link instead of attach |
| `overQuota` | Mailbox full — the Sent copy cannot be stored | Free space; the send itself may partially succeed while the copy fails |
| `rateLimit` | Sending rate cap | Back off; sending faster is not a thing to retry into |
| Accepted, then a bounce arrives | Recipient-side rejection | The bounce message carries the reason; DNS and reputation issues are `dns` territory |
| `deliveryStatus` shows a recipient not delivered | Per-recipient outcome | Report per recipient — a partially delivered send is not a failed send |

## Custom Domains

Sending from your own domain is a DNS fact before it is a JMAP fact:

- SPF, DKIM and DMARC records must exist and validate; until they do, mail sends and lands in spam, which reads as a delivery bug and is not one.
- Record the domain, its registrar, its expiry, and the DKIM **selector plus verification date** in the shared `~/Clawic/data/domains/domains.md` — never the private key (`memory-template.md`).
- Domain expiry silently kills both sending and receiving. Its `## Due` row is the reason to write it down at all.
- Record shape, precise values, and migration order live in `dns`.

## Bulk Sending

Personalized mail to a list is a different job with different failure modes: recipient caps, rate limits, reputation, unsubscribe handling, and the fact that a mistake is unrecallable per recipient. Through this API, keep it to a size where each message is verifiable, cap the batch well below the account's limits, and log the run in `operations/<year>.md`.

Above that scale the honest answer is a sending platform, not a loop over `EmailSubmission/set`: a personal mailbox has no unsubscribe handling, no bounce processing, and one reputation to lose. Transport-level tuning and deliverability testing belong in `smtp`.
