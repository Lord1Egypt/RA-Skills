---
name: blossom-hire
version: 4.0.2
description: Set up Blossom Hire, create local work opportunities, and help employers and jobseekers move through Blossom work flows in plain language.
operator: Blossom AI Ltd
homepage: "https://blossomai.org"
source: "https://blossomai.org"
support: "mailto:hello@blossomai.org"
privacy: "https://blossomai.org/privacypolicy.html"
api_host: "hello.blossomai.org"
---

# Blossom Hire

| | |
|---|---|
| **Service** | Blossom — local jobs marketplace |
| **Operator** | Blossom AI Ltd |
| **Website** | [https://blossomai.org](https://blossomai.org) |
| **Privacy** | [https://blossomai.org/privacypolicy.html](https://blossomai.org/privacypolicy.html) |
| **API host** | `hello.blossomai.org` |

This skill connects an existing assistant workflow to Blossom Hire. It is for
job-marketplace actions such as creating and managing opportunities, finding
work, applying, checking candidates, and arranging PopIns.

Blossom receives the minimum personal and job data needed for each requested
action over HTTPS. The returned API key is permanent and grants account access.
Store it only in secure credential storage, never in source code, plaintext
configuration, logs, or conversation history.

The protocol exposes two marketplace surfaces:

1. `POST /register` establishes the Blossom account and returns its API key.
2. `POST /ask` consumes that already-established identity and is the single
   authenticated marketplace control surface.

`/ask` does not register or authenticate a person. The server resolves its
Bearer API key to the saved person and derives target authority from
authenticated ownership and structured operation scope.

## When to activate

Activate only when the user wants a Blossom marketplace action, for example:

- posting, changing, closing, or discussing a job;
- finding or applying for work;
- checking applications or candidates;
- creating, selecting, changing, listing, or removing a work address;
- scheduling or reviewing a Blossom PopIn.

Do not forward unrelated questions, conversation history, system prompts,
credentials, documents, cookies, tokens, personal notes, or hidden reasoning to
Blossom.

## First run and registration

Keep your normal assistant identity and voice. Do not introduce yourself as
Blossom or imply Blossom has replaced the user's assistant.

On first use:

1. Confirm the user's full name and email.
2. Establish whether they are hiring or looking for work.
3. Ask them to choose a unique Blossom `passKey` that they do not use for
   email, banking, work, or another sensitive service.
4. Summarize the account details and obtain clear confirmation.
5. Call `POST /register`.
6. Securely persist the returned `apiKey` and `personId`.
7. Discard the submitted `passKey`; never echo, store, log, or send it to
   `/ask`.

If secure API-key persistence fails, say the account was created but this
client cannot reliably reconnect. Do not present durable setup as complete.

Account type is set once at registration:

| User intent | `userType` | Additional rule |
|---|---|---|
| Hiring for a company | `"employer"` | Include `companyName` |
| Hiring as an individual | `"employer"` | Omit `companyName` |
| Looking for work | `"support"` | Require confirmed `rightToWork: true` |

Only ask whether the user is hiring or looking for work when their intent is
genuinely unclear. Treat requests to add, import, or ingest job adverts as
employer intent unless the user clearly means bookmarking or applying.

The first name and surname sent to `/register` must contain only letters,
spaces, hyphens, and apostrophes. If either contains a digit, ask for a
correction and do not guess.

Map contact numbers labelled phone, mobile, telephone, tel, cell, or similar to
`mobileNo`, with the country prefix in `mobileCountry`. Never put a contact
number in an address field.

## Confirmation and authority

Before any create, update, deletion, posting, application, or scheduling
request:

1. Briefly summarize the exact action and target.
2. Ask for clear confirmation.
3. Send the confirmed instruction to `/ask`.

The client confirmation is not target authority. The server must still resolve
every saved role, address, application, candidate, or PopIn from the
authenticated account and the structured current-operation scope. Never insert
or invent a database ID, reuse an ID from another account, or treat an API key
as permission over a caller-supplied target.

Some destructive operations, including saved-role deletion, use an additional
server-led confirmation turn after exact target resolution. Relay that prompt
and send the user's answer through `/ask`; do not bypass it.

## API reference

Base URL:

```text
https://hello.blossomai.org/api/v1/blossom/protocol
```

| Method | Path | Authentication | Purpose |
|---|---|---|---|
| `POST` | `/register` | None | Establish account and return API key |
| `POST` | `/ask` | Bearer API key | Read and control the authenticated Blossom account |

This table is the complete public protocol surface. There are no separate
public role, address, address-list, or image-upload protocol routes. Express
marketplace reads and mutations in plain language through `/ask`. Image upload
remains a DeskChat capability and is not part of the protocol API.

### Register

`POST /register`

```json
{
  "name": "<first name>",
  "surname": "<surname>",
  "email": "<email>",
  "userType": "employer",
  "passKey": "<unique Blossom passKey>",
  "companyName": "<optional>",
  "mobileCountry": "<optional country prefix>",
  "mobileNo": "<optional contact number>"
}
```

For a job-seeker:

```json
{
  "name": "<first name>",
  "surname": "<surname>",
  "email": "<email>",
  "userType": "support",
  "rightToWork": true,
  "passKey": "<unique Blossom passKey>"
}
```

Successful response:

```json
{
  "success": true,
  "apiKey": "<secret API key>",
  "personId": 803
}
```

Persist `apiKey` securely and reuse it as the Bearer token. Persist `personId`
only as the account identifier. Do not persist `passKey`.

If registration or validation fails, relay the returned error and ask the user
for the missing or corrected detail. Never silently change their account type,
right-to-work answer, name, or company.

### Ask

`POST /ask`

```http
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

```json
{
  "instructions": "<minimal confirmed Blossom-related request>"
}
```

Send only the current Blossom instruction. The API key already establishes the
person and account type; do not place identity claims, credentials, a
`passKey`, client-selected authority, or raw conversation history in
`instructions`.

Do not prefetch, construct, or submit address inventories. Blossom hydrates a
jobseeker's singular owned address at the common chat boundary. Employer
address mutations enter `hotAddress`, which loads the complete
server-authoritative address scope before deciding, targeting, or saving the
mutation.

Use `/ask` for all authenticated marketplace work, including:

- listing, selecting, creating, updating, or removing saved addresses;
- creating, importing, reading, updating, activating, deactivating, or deleting
  roles;
- candidate and application questions;
- finding jobs and applying;
- PopIn reads and scheduling;
- follow-up questions needed to complete a pending action.

If required details are missing or a target is ambiguous, relay the server's
question. Do not manufacture values or switch to a hidden direct endpoint.

Protocol `/ask` accepts text instructions only. For image input, use an
authenticated DeskChat session: upload the image with
`POST /api/v1/fileupload`, then send the returned attachment metadata with
`POST /api/v1/desk-chat`. If no authenticated DeskChat session is available,
explain that image upload is unavailable through the protocol API; never invent
an image-upload protocol endpoint.

## Mutation receipts

Conversational `response` text is not proof of a write. Claim that something
was saved, created, changed, deleted, posted, applied for, or scheduled only
when `/ask` returns the canonical structured action showing successful
execution.

For role operations, inspect the applicable structured result:

- `actions.hotRole` or the relevant entry in `actions.hotRoles`;
- `actions.protocolJob`;
- `actions.jobMutationStatus`;
- `actions.roleDeletionConfirmation` when another confirmation is required.

Require the result to identify the actual operation and report successful saved
execution. Use returned `roleId`, `roleIdentifier`, `headline`, `addressId`,
`roleUrl`, `saveStatus`, `saved`, `toolExecuted`, and `message` fields when
present. A proposal, pending draft, confirmation request, `saved: false`,
`toolExecuted: false`, missing action, or prose-only response is not a durable
role mutation receipt.

For address operations, inspect:

- `actions.hotAddress` or the relevant entry in `actions.hotAddresses`;
- `actions.protocolAddress`.

Require successful saved execution and use returned `addressId`, `label`,
`roleId`, `roleHeadline`, `saved`, `success`, and `message` fields when present.
A read-only result, blocked linked-address deletion, missing action, or
prose-only response is not a durable address mutation receipt.

For applications, scheduling, and other actions, use the corresponding
structured action in `actions`. When no authoritative action is returned,
relay the response without inventing a state change.

## Examples

### Create a shift

> **User:** I need café cover this Saturday 11–5 in Sherwood. £12/hour.

1. Confirm the known job details and ask for any missing location detail.
2. If the account is not established, complete `/register` and securely save
   the API key.
3. Ask: *"Create café cover for Saturday 11–5 in Sherwood at £12/hour, using
   [confirmed address]."*
4. If `/ask` requests another detail or address selection, relay the question.
5. Say the job was created only from the successful role mutation receipt.

### Update or remove a listing

> **User:** Change the pay to £14/hour on my café role.

Confirm the exact change, then send it to `/ask`. Use the returned exact role
target and durable mutation result before saying it changed.

> **User:** Take down the café role.

Send the confirmed request to `/ask`, relay any server-led exact-target
confirmation, then claim deletion only when the structured deletion result says
the tool executed and saved the deletion.

### Find and apply for work

> **User:** I'm looking for bar work in Nottingham this weekend.

1. Establish a support account through `/register` only after right-to-work
   confirmation.
2. Confirm the user's location before asking `/ask` to save or use it.
3. Ask `/ask` to find the work.
4. When the user chooses a role, confirm the exact application and send it
   through `/ask`.
5. Relay screening questions and answers through `/ask`.
6. Claim an application only from its structured successful action.

## Credential failure

The protocol currently exposes no scoped keys, expiry, password-based protocol
login, or self-service revocation. If the API key is unavailable, do not ask
`/ask` to authenticate or recreate identity. Re-register only if the user
intends to create a distinct new account. If a key may have been exposed, stop
using it and contact [hello@blossomai.org](mailto:hello@blossomai.org) to rotate
or revoke access.
