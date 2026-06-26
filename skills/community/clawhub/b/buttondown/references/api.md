# Buttondown API Reference

Source checked 2026-05-23 from Buttondown docs and `https://docs.buttondown.com/openapi.json`.

## Authentication

- Base URL: `https://api.buttondown.com/v1`.
- Header: `Authorization: Token <api-key>`.
- Optional platform/multi-newsletter header: `Buttondown-Context: <newsletter-username>`.
- API keys are managed in Buttondown at API -> Keys.
- For creating and updating drafts, the key needs `email_access=write`.
- For sending previews or live sends, the key needs the relevant sending access. Do not use sending actions without explicit approval.

## Create Email

`POST /emails`

Important default: Buttondown's `EmailInput.status` defaults to `about_to_send`. Always send `"status":"draft"` for draft creation unless the user explicitly approves sending/scheduling.

Required:

- `subject` string, max 2000 chars.

Common fields:

- `body` string, Markdown or HTML.
- `status` enum: `draft`, `about_to_send`, `scheduled`, `sent`, plus other system states.
- `slug` string or null, max 100 chars.
- `description` string for archives/SEO.
- `canonical_url` string.
- `image` string URL.
- `publish_date` ISO date-time or null.
- `archival_mode`: `disabled`, `enabled`, `enabled_for_paid_subscribers`, `enabled_for_subscribers`.
- `commenting_mode`: `disabled`, `enabled`, `enabled_for_paid_subscribers`.
- `metadata` object.
- `secondary_id` integer.
- `featured` boolean.
- `related_email_ids` array of IDs.

Body mode:

- Markdown/plaintext: prepend `<!-- buttondown-editor-mode: plaintext -->`.
- Rich HTML/fancy: prepend `<!-- buttondown-editor-mode: fancy -->`.
- If the body starts with YAML frontmatter, Buttondown rejects it with `400` and `body_contains_frontmatter`. Strip frontmatter before upload.

Draft curl shape:

```bash
jq -n --arg subject "$SUBJECT" --rawfile body issue.md '{subject:$subject, body:$body, status:"draft"}' \
  | curl -fsS -X POST "https://api.buttondown.com/v1/emails" \
      -H "Authorization: Token $BUTTONDOWN_API_KEY" \
      -H "Content-Type: application/json" \
      --data-binary @-
```

## Update Email

`PATCH /emails/{id}`

Use for draft edits. Same common fields as create. To clear a scheduled `publish_date`, pass `"publish_date":"none"`.

## Retrieve/List

- `GET /emails/{id}` retrieves one email.
- `GET /emails` lists emails.
- `GET /emails/{id}/renders` returns rendered HTML.
- `GET /emails/{id}/history` retrieves edit history.

## Send Draft Preview

`POST /emails/{id}/send-draft`

Payload:

```json
{
  "recipients": ["person@example.com"],
  "subscribers": ["subscriber_id"]
}
```

This sends email externally. Get explicit user approval in the current conversation before using it.

## Error Codes To Surface

Creation errors include:

- `body_contains_frontmatter`
- `email_duplicate`
- `email_not_confirmed`
- `body_invalid`
- `canonical_url_invalid`
- `email_invalid`
- `slug_invalid`
- `subject_invalid`
- `publish_date_invalid`
- `publish_date_missing`
- `sending_requires_confirmation`
- `status_invalid`
- `tag_invalid`

When Buttondown returns JSON with `detail`, report that text directly and keep token values redacted.
