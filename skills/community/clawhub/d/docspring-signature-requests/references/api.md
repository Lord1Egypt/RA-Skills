# Signature requests over the REST API (v2)

For app code. Send every request to `https://sync.api.docspring.com/api/v2` (EU:
`https://sync.api-eu.docspring.com/api/v2`) with HTTP Basic auth: the API token's ID as the username, its secret as
the password. The 4.x API clients read `DOCSPRING_TOKEN_ID`, `DOCSPRING_TOKEN_SECRET` and `DOCSPRING_REGION` from the
environment; `docspring-api-integration` covers setting them up.

## Contents

1. Endpoints
2. The signature request properties
3. Code: curl, Ruby, Python, JavaScript and TypeScript
4. Signing links (tokens)
5. Recording that you sent the link (events)
6. Updating authentication details
7. Errors
8. Authentication details for the audit trail
9. Existing API v1 code

## 1. Endpoints

| Operation (client method)     | Endpoint                                                 | What it does                                       |
| ----------------------------- | -------------------------------------------------------- | -------------------------------------------------- |
| `createSubmission`            | `POST /templates/{template_id}/submissions`              | Creates the submission and its signature requests. |
| `getSubmission`               | `GET /submissions/{submission_id}`                       | The submission, its signature requests and files.  |
| `expireSubmission`            | `DELETE /submissions/{submission_id}`                    | Cancels it: deletes its data, links stop working.  |
| `getSignatureRequest`         | `GET /signature_requests/{signature_request_id}`         | One signature request, with the values so far.     |
| `updateSignatureRequest`      | `PUT /signature_requests/{signature_request_id}`         | Changes its metadata or authentication details.    |
| `createSignatureRequestToken` | `POST /signature_requests/{signature_request_id}/tokens` | Makes a signing link, for a link you send.         |
| `createSignatureRequestEvent` | `POST /signature_requests/{signature_request_id}/events` | Records that you sent the link.                    |

Ruby, Python, Elixir and Rust name the methods in snake case (createSubmission becomes create_submission); JavaScript,
TypeScript, PHP and Java use the names above, and C# and Go capitalize them. In Ruby, Python, JavaScript and
TypeScript the request body is a plain hash or object with the API's snake case property names.

## 2. The signature request properties

The create request's body takes the usual submission properties (`test`, `data`, `metadata`, `expires_in`,
`password`, `field_overrides`, and the `version` query parameter), the email properties (`send_email`,
`signing_order`, `email_subject`, `email_message`, `cc`, `reply_to`, `notification_emails`, `notify_when_signed` and
`reminders`, described in `SKILL.md` section 2) and `signature_requests`, up to 100 of:

| Property                                                                                    | Required    | Notes                                                                          |
| ------------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------ |
| `fields`                                                                                    | yes         | Field names this person fills in. At least one; each field in only one list.   |
| `auth_type`                                                                                 | see notes   | Required with `send_email: false`. Otherwise always `email_link`, the default. |
| `email`                                                                                     | see notes   | Required when DocSpring emails the person. Shown on the audit trail.           |
| `name`                                                                                      | no          | In DocSpring's emails and on the audit trail.                                  |
| `send_email`                                                                                | no          | `false`: DocSpring doesn't email this person. Default: the submission's.       |
| `signing_step`                                                                              | no          | With `signing_order: sequential`: on all signature requests, or none.          |
| `role`                                                                                      | no          | `Signer 1` to `Signer 100`. All signature requests have one, or none does.     |
| `metadata`                                                                                  | no          | Your own data, such as the signer's ID in your app.                            |
| `prefilled_values_editable`                                                                 | no          | Lets the person change values that `data` has for their fields.                |
| `ignore_unknown_fields`                                                                     | no          | Drops names the template doesn't have, instead of `invalid_data`.              |
| `auth_second_factor_type`                                                                   | no          | `none`, `phone_number`, `totp`, `mobile_push`, `security_key`, `fingerprint`.  |
| `auth_provider`                                                                             | for `oauth` | The service that signed them in, such as `google`.                             |
| `auth_session_started_at`                                                                   | no          | When your app signed them in. Set for you with `email_link`.                   |
| `auth_session_id_hash`, `auth_user_id_hash`, `auth_username_hash`, `auth_phone_number_hash` | no          | Hashes for the audit trail (section 8).                                        |

`data` is optional with signature requests (required without them). `editable: true` isn't allowed.

## 3. Code

curl:

```bash
curl -s -u "$DOCSPRING_TOKEN_ID:$DOCSPRING_TOKEN_SECRET" \
  -H 'Content-Type: application/json' \
  -X POST https://sync.api.docspring.com/api/v2/templates/tpl_.../submissions \
  -d '{
    "test": true,
    "data": { "company_name": "Acme Inc." },
    "signature_requests": [
      { "name": "Jane Smith", "email": "jane@example.com", "fields": ["employee_signature"] }
    ]
  }'
```

DocSpring emails Jane her link. It's a test, so Jane must be on the account's DocSpring team: a test request emails
nobody else (a 422 `not_allowed`). For a link your app sends instead, add `"send_email": false` and
`"auth_type": "email_link"` to her signature request, then make the link:

```bash
curl -s -u "$DOCSPRING_TOKEN_ID:$DOCSPRING_TOKEN_SECRET" \
  -H 'Content-Type: application/json' \
  -X POST https://sync.api.docspring.com/api/v2/signature_requests/srq_.../tokens \
  -d '{ "type": "email" }'
```

The Ruby and Python examples are for an app that sends the links itself (`send_email: false`).

Ruby (`docspring` gem, 4.x):

```ruby
require 'docspring'

client = DocSpring::Client.new # reads DOCSPRING_TOKEN_ID, DOCSPRING_TOKEN_SECRET and DOCSPRING_REGION

submission = client.create_submission('tpl_...', {
  test: true,
  data: { company_name: 'Acme Inc.' },
  send_email: false,
  signature_requests: [
    { name: 'Jane Smith', email: 'jane@example.com', fields: ['employee_signature'], auth_type: 'email_link' },
  ],
})

submission.signature_requests.each do |signature_request|
  token = client.create_signature_request_token(signature_request.id, body: { type: 'email' })
  # Email token.signature_request_url to signature_request.email from your app, then record it:
  client.create_signature_request_event(signature_request.id, {
    event_type: 'send_request', message_type: 'email', message_recipient: signature_request.email,
  })
end
```

Python (`docspring` package, 4.x):

```python
from docspring import Client

client = Client()  # reads DOCSPRING_TOKEN_ID, DOCSPRING_TOKEN_SECRET and DOCSPRING_REGION

submission = client.create_submission("tpl_...", {
    "test": True,
    "data": {"company_name": "Acme Inc."},
    "send_email": False,
    "signature_requests": [
        {"name": "Jane Smith", "email": "jane@example.com", "fields": ["employee_signature"], "auth_type": "email_link"},
    ],
})

for signature_request in submission.signature_requests:
    token = client.create_signature_request_token(signature_request.id, body={"type": "email"})
    # Email token.signature_request_url from your app, then record it:
    client.create_signature_request_event(signature_request.id, {
        "event_type": "send_request", "message_type": "email", "message_recipient": signature_request.email,
    })
```

JavaScript calls `createSubmission(templateId, body)` and `createSignatureRequestEvent(signatureRequestId, body)`, with
the same snake case bodies. Its token call takes the body in an options object, because the body is optional:
`createSignatureRequestToken(signatureRequestId, { body: { type: 'email' } })`. TypeScript passes each body directly,
as the second argument. Its enum properties take the enums (`DocSpring.SignatureRequestTokenType.Email`,
`DocSpring.SignatureRequestEventType.SendRequest`, `DocSpring.SignatureRequestMessageType.Email`,
`DocSpring.SignatureRequestAuthType.Oauth` and so on), and its times are `Date` objects.

The clients check a request against the API's schema before sending it, so a signature request without `fields`
raises a validation error with a `pointer` to it.

## 4. Signing links (tokens)

For a signature request with `send_email: false`, or when a signer asks for a new link:
`POST /signature_requests/{signature_request_id}/tokens` with `{"type": "email"}` (7 days) or no body (`api`, 24
hours). The response:

```json
{
  "id": "1234567890abcdef01",
  "signature_request_id": "srq_...",
  "type": "email",
  "secret": "ABCDEF01234567890",
  "signature_request_url": "https://app.docspring.com/signature_requests/srq_...?token_id=...&token_secret=...",
  "expires_at": "...",
  "created_at": "..."
}
```

- `signature_request_url` opens DocSpring's hosted signing page. For an embedded form, pass `id` and `secret` to the
  page as `tokenId` and `tokenSecret` (`references/embedding.md`).
- `secret` is only in this response. Make a token each time you send or show the form; don't store one to reuse.
- A signing page that opened while the link worked keeps working for 7 more days.
- 409 once the signature request is completed, declined or expired. 403 with a test API token on a live signature
  request.

## 5. Recording that you sent the link (events)

`POST /signature_requests/{signature_request_id}/events`:

```json
{
  "event_type": "send_request",
  "message_type": "email",
  "message_recipient": "jane@example.com"
}
```

- `send_request` is the only event type. `message_type` and `message_recipient` are required for it.
- `message_type`: `email`, `sms`, `fax`, `mail`, `slack`, `msteams`, `discord`, `telegram` or `whatsapp`.
- `occurred_at` defaults to now.
- The audit trail shows it as "Reported by <account> via API". DocSpring records its own emails, views, signatures,
  declines and completion itself.
- 409 once the signature request is finished. 403 with a test API token on a live one.

## 6. Updating authentication details

`PUT /signature_requests/{signature_request_id}` takes `metadata` and the `auth_*` properties, for when the person
signed in again before they opened the form. Once they've opened it, only `metadata` can change; a completed or
declined signature request can't change at all (409). `name`, `email` and `fields` can never change: expire the
submission and create a new signature request.

## 7. Errors

The create request checks the request's shape first. These are 422 `validation_failed`, and nothing is saved:

| `details[].code` | `pointer`                             | Cause                                                                     |
| ---------------- | ------------------------------------- | ------------------------------------------------------------------------- |
| `duplicate`      | `/signature_requests/1/fields/0`      | The field is in another signature request's `fields`.                     |
| `duplicate`      | `/signature_requests/1/role`          | Another signature request has this role.                                  |
| `prefilled`      | `/signature_requests/0/fields/2`      | `data` has a value for it: set `prefilled_values_editable`.               |
| `required`       | `/signature_requests/0/role`          | Some signature requests have a role and this one doesn't.                 |
| `invalid`        | `/signature_requests/0/role`          | Not `Signer 1` to `Signer 100`.                                           |
| `other_signer`   | `/signature_requests/0/fields/1`      | Another signer's formula or show/hide rule uses this field.               |
| `not_allowed`    | `/editable`                           | `editable: true` with signature requests.                                 |
| `not_allowed`    | `/signature_requests`                 | The template is an HTML template.                                         |
| `required`       | `/signature_requests/0/email`         | DocSpring emails this person, so it needs their address.                  |
| `required`       | `/signature_requests/0/auth_type`     | `send_email: false` and no `auth_type`.                                   |
| `not_allowed`    | `/signature_requests/0/auth_type`     | Not `email_link` for a person DocSpring emails.                           |
| `not_allowed`    | `/send_email`                         | `true` for a form library template, whose signers DocSpring never emails. |
| `not_allowed`    | `/signature_requests/0/signing_step`  | `signing_step` without `signing_order: sequential`.                       |
| `required`       | `/signature_requests/1/signing_step`  | Some signature requests have a step and this one doesn't.                 |
| `not_allowed`    | `/signature_requests/0/email`         | A test request, and the address isn't a team member's.                    |
| `not_allowed`    | `/reply_to`, `/notification_emails/0` | Not a team member's address or at a verified domain.                      |
| `not_allowed`    | `/cc`, `/reminders`, ...              | An email option on a request that DocSpring emails nobody.                |
| `invalid`        | `/email_subject`, `/email_message`    | A variable or tag they can't use.                                         |

Errors that depend on the template save the submission as `invalid_data` and return a 422 `invalid_data` with its
`submission_id`: a field name the template doesn't have, a signature or initials value in `data` or in a field
override's `default`, or a required field that neither `data` nor any signer fills in. Nobody can sign it: fix the
request and create a new one.

Other statuses: 403 when a demo API token creates signature requests or a test API token acts on a live signature
request; 403 `upgrade_required` for a live signature request before the account's first payment (a credit pack or a
paid plan); 404 for an ID from another account or region; 409 for a finished signature request.

A request that DocSpring would email saves nothing and returns:

- 402 `insufficient_credits_to_send`: the account's credits can't cover the live submission.
- 403: while the account's emails are paused, or before its owner has confirmed their email address.
- 409: the template's draft is still being set up. Send it again in a minute.
- 429 `daily_email_limit_reached`: over the account's daily email limit. Try again after the `Retry-After` header's
  seconds.

Each message says what to do, and sending the links yourself (`send_email: false`) avoids all of them.

## 8. Authentication details for the audit trail

The audit trail's **Signer Authentication** section shows what you send, as reported by the account. Send as much as
is true:

- `email_link`: you or DocSpring emailed the person a link and they opened it. DocSpring sets `auth_session_started_at`
  when they first open it. When the link was one DocSpring emailed, the section shows that as DocSpring's own record.
- Your app signed them in and shows the embedded form: their sign-in method as `auth_type` (with `auth_provider` for
  `oauth`), `auth_session_started_at`, and `auth_second_factor_type` if they used one.
- `auth_user_id_hash`, `auth_username_hash`, `auth_session_id_hash`, `auth_phone_number_hash`: a SHA-256 hash of a
  salt and the value. Never send a plaintext session ID. Use one salt for all of them and keep it, or the hashes
  can't be matched to your records later. Salt incrementing user IDs.

## 9. Existing API v1 code

API v1 and the 3.x clients use the old names for the same records. Write new code against API v2 and keep the names
customers see as "signature requests":

| API v1                                     | API v2                            |
| ------------------------------------------ | --------------------------------- |
| `data_requests` in the create body         | `signature_requests`              |
| `/data_requests/{id}`                      | `/signature_requests/{id}`        |
| `data_request_url` on a token              | `signature_request_url`           |
| state `waiting_for_data_requests`          | `waiting_for_signature_requests`  |
| webhook events `submission_data_request.*` | `signature_request.*` (version 4) |

The IDs are the same in both APIs: `srq_...` for new signature requests, `drq_...` for older ones.

API v1 never emails signers; API v2 does unless `send_email` is `false`. Code moved from v1 that sends its own
links needs `send_email: false`.

Moving to v2: https://docspring.com/docs/api-guide/migrating-to-api-v2/
