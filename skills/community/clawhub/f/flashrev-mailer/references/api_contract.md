# FlashRev API Contract (v2)

This document describes the **request and response shapes** the CLI relies on.
Endpoint paths and methods are baked into `src/config.js` (`flashrev.endpoints`)
as the single source of truth; override per environment via
`.flashrev/config.json`.

Default base URL: `https://open-ai-api.flashlabs.ai`
(Test/staging URL: ask your FlashRev team or override via `flashrev-mailer init --base-url`.)

## Authentication

- Header: `X-API-Key: <FLASHREV_API_KEY>` (no `Bearer ` prefix).
- Issue keys at https://info.flashlabs.ai/settings/privateApps.
- Same key authorizes all sequence / contact / csv / mailbox / time-template
  endpoints listed below.

## Gateway path-prefix conventions

The CLI talks to three logical services through one gateway:

| Path prefix | Service |
|---|---|
| `/mailsvc/*` | mail-svc (sender mailbox + sent/inbox views) |
| `/dispatch/*` | dispatch-svc (email verification) |
| `/engage/*` | engage-svc (sequence + contact + csv + time template) |

The `/engage` prefix is critical — `/api/v1/sequence/*` alone returns 404.

## Endpoint inventory

### Sequence
| Endpoint | Method | Purpose |
|---|---|---|
| `/engage/api/v1/sequence/add` | POST | Create sequence (incl. steps + setting.properties) |
| `/engage/api/v1/sequence/edit` | POST | **Full-replace** edit (sequence id + complete steps[] + complete setting.properties) |
| `/engage/api/v1/sequence/page/list` | POST | Paginated list; supports `sources` filter |
| `/engage/api/v1/sequence/detail/{id}` | GET | Single sequence with steps + settings |
| `/engage/api/v1/sequence/start` | POST | Resume from paused (does not need to be called on add — sequences are active by default) |
| `/engage/api/v1/sequence/paused` | POST | Pause |
| `/engage/api/v1/sequence/setting/edit` | POST | **Full-replace** properties update (timeTemplateId / aiAutoReply / etc.) |
| `/engage/api/v1/sequence/config/list` | GET | Default config catalog (sequenceTypes, emailTrackList, stepDelay) |
| `/engage/api/v1/sequence/details/contacts/page/list` | POST | Contacts under a sequence (currentStep / state / scheduleTime) |
| `/engage/api/v1/sequence/details/contacts/statistics` | POST | Per-state contact counts |
| `/engage/api/v1/sequence/stats/{id}` | GET | Aggregates (emailSent / opened / clicked / replied / bounced / ...) |
| `/engage/api/v1/sequence/step/contacts/timeline` | POST | Per-contact step-by-step event log |
| `/engage/api/v1/sequence/mailbox-pool/{sequenceId}` | PUT | Update mailbox pool |

### Contact / CSV
| Endpoint | Method | Purpose |
|---|---|---|
| `/engage/contact/upload-contact` | POST (multipart) | Upload CSV → contact rows, optionally linked to a sequenceId |
| `/engage/contact/list` | POST | List import batches |
| `/engage/contact/import-record/{id}` | GET | Single import batch summary (does NOT return contactId list) |
| `/engage/api/v1/contact/property/list` | GET | Display-property whitelist for template variables |
| `/engage/csv/v1/upload/parse` | POST (multipart) | Parse CSV headers; returns mappingList |
| `/engage/csv/v1/languages/columns` | GET | Field whitelist for `mappings.field` |

### Time template (a.k.a. schedule)
| Endpoint | Method | Purpose |
|---|---|---|
| `/engage/api/v1/time/template/list` | GET | List templates; **first call on a new account lazy-creates "Default Business Hours"** |
| `/engage/api/v1/time/template/add` | POST | Create a private schedule (per-company unique name) |
| `/engage/api/v1/time/template/edit` | PUT | Modify an existing schedule (affects every sequence referencing it) |
| `/engage/api/v1/time/template/detail/{id}` | GET | Detail |

### User profile + timezone (engage-svc, for schedule defaults)
| Endpoint | Method | Purpose |
|---|---|---|
| `/engage/api/v1/user/setting/profile` | GET | Current user profile (returns `{userId, firstName, lastName, email, timezoneId, timezoneDisplayName, company, ...}`). CLI reads `timezoneId` as the default for schedule creation. Cached 24h at `.flashrev/profile-cache.json`. |
| `/engage/api/v1/timezone/list` | GET | All IANA timezones (~141 entries). Each item: `{id, name, zoneId, displayName, offset, formattedOffset}`. CLI uses for `--timezone` validation + id↔zoneId lookup. Cached permanently at `.flashrev/timezone-list.json`. |

**Timezone resolution priority (CLI side):**
1. `--timezone <id|zoneId>` explicit input → must be present in `timezone/list` or CLI throws with candidate examples.
2. `profile.timezoneId` (auto-fetched on first `send --live`).
3. Fallback `id=22 America/New_York`.

`timeTemplate.properties.defaultTimezone.id` **must** be a valid timezone-list id — backend uses this to compute send-time windows. Never pass an arbitrary IANA string without first resolving via `timezone/list`.

### Mailbox / mail views (mail-svc)
| Endpoint | Method | Purpose |
|---|---|---|
| `/mailsvc/mail-address/v2/list` | POST | List sender mailboxes |
| `/mailsvc/mail-address/smtp-credential/{id}` | GET | (v1 nodemailer fallback) per-mailbox SMTP credentials |
| `/dispatch/api/v2/email-verify` | GET | Pre-flight email deliverability check |
| `/mailsvc/mail-box/v2/sent` | POST | Outbox; supports `sequenceId` filter; per-row labels + open/click/reply counts |
| `/mailsvc/mail-box/v2/inbox` | POST | Prospect-reply view |
| `/mailsvc/mail-box/read/{summaryId}` | POST | Mark a single mail as read |
| `/mailsvc/mail-box/operate-timeline/{summaryId}` | GET | Per-message event timeline |
| `/mailsvc/mail/reply-mail` | POST | Send a thread-preserving reply to an inbox message |

## Identifier conventions

| ID | Source | Used by |
|---|---|---|
| `summaryId` | mail-svc `mail_summary.id` | CLI exposes as `MAIL_ID`. Stable across CLI runs (cached in `.flashrev/inbox-cache.json`) |
| `messageId` | SMTP `Message-ID` header (numeric in FlashRev DB) | Required by `mail/reply-mail` input; the CLI resolves it from cache by `MAIL_ID` |
| `sequenceId` | base_sequences.id | All sequence/* endpoints + outbox/inbox filter |
| `contactId` | engage contacts.id | Returned by sequence/details/contacts/page/list; exposed as `CONTACT_ID` in CLI output |
| `feid` | client-generated epoch ms | Used to link reply steps (`parentFeid`) inside a single sequence/add call |
| `importId` | contact import batch id | **Cannot be reverse-mapped to contactId** via any HTTP endpoint |
| `peopleId` | FlashRev global people library | Required by `/v2/contact/add`; CLI does not use this path |

## sequence/add request shape

```jsonc
{
  "name": "launch-001",
  "sources": "ai_mailer",                  // mark the CLI-origin for list filtering
  "steps": [
    {
      "delayMinutes": 0,             // step 1: usually 0 with --send-now
      "emailType": "new_thread",     // or "reply" for follow-up steps
      "feid": 1779380515660,         // client-generated, unique within request
      "parentFeid": 0,               // 0 for new_thread; <step N's feid> for reply
      "stepType": "Email",
      "taskType": "",                // ⚠️ MUST be empty string, NOT "automatic_email"
      "weight": 1,                   // step order, 1-based
      "active": true,
      "abTest": false,
      "groups": "",                  // empty string (NOT null)
      "groupsWeight": 0,
      "tasks": [{
        "subject": "Hi {{ FirstName }}",   // empty when emailType=reply
        "content": "<p>...</p>",
        "preHeader": "",
        "mailCcList": [],
        "mailBccList": [],
        "contentServer": "<!DOCTYPE html>...{{openedUrl}}...",  // full HTML wrapper with tracking pixel
        "contentMode": "email"
      }]
    }
  ],
  "setting": {
    "type": "owner",                 // or "all"
    "properties": {
      "timeTemplateId": 135509,      // required
      "autoMatchEmailProvider": false,
      "importSettings": { "callVerifiedTypeToUse": "all type", "emailVerifiedTypeToUse": "all type" },
      "emailTrack": {
        "trackType": "general",
        "emailUnsubscribe": true,
        "trackOpen": true,
        "trackLinkClick": true,
        "unsubscribeTemplate": "Don't want to get emails like this? <%Unsubscribe from our emails%>"
      },
      "markedContactFinished": {
        "prospectRepliesEnabled": 1,       // stop sequence on prospect reply
        "sameCompanyContactEnabled": 0,
        "callLoggedAnsweredEnabled": 1,
        "callNoFinishAnsweredEnabled": 0,
        "doNotReplyAfterLastStepNumberOfDays": 7
      },
      "markedContactPaused": {
        "outOfOfficeReplyEnabled": 1,
        "resumeDays": 7,
        "entersCallStepAndCallNotDialed": 1,
        "emailVerificationUsedUp": 0
      },
      "emailRealValid": {                // REQUIRED, even if not using real-time validation
        "enabled": true,
        "rules": ["valid", "catchall"],
        "sources": ["FlashInfo"]
      },
      "aiAutoReplyEnabled": false,
      "aiAutoReplyPrompt": "",
      "emailTextOnly": false,
      "allowOtherUserAsOwner": false,
      "deduplicateContact": false,
      "smsThrottle": false,
      "maxDailySmsCount": 10000
    }
  }
}
```

Response: `{"code": 200, "data": {"sequenceId": 2268, "sequenceReachLimit": false}}`

## contact/upload-contact (multipart) request

```
file:           <CSV bytes>            // Content-Type MUST be "text/csv"
filename:       "campaign.csv"
importType:     1                       // 1=link to sequence, 2=pure import
sequenceId:     2268                    // when importType=1
sendMailType:   "designated"            // or "rotation" / "mailbox_pool"
addressId:      1479                    // when sendMailType=designated
ignoreStepDelay: 1                      // 1 = fire step 1 immediately, skip delay + window + holidays
mappings:       "[{\"csvHeader\":\"First Name\",\"csvColIndex\":0,\"field\":\"First Name\"},...]"
importLimit:    "false"                 // "true" forces deliverable email gating
```

`mappings.field` values come from `/csv/v1/languages/columns` (e.g.
"First Name", "Last Name", "Email Address", "Company Name").

Response: `{"code": 200, "data": <importId>, "msg": "Operation successful!"}`
Note: this importId **cannot be reversed back to a list of contactIds** via
any public endpoint. The CLI infers contactIds from `sequence/details/contacts/page/list`
on the same sequence after upload.

## sequence/edit (Full-Replace) workflow

`sequence/edit` is **not** a patch endpoint. Send the entire `steps[]` array
and the entire `setting.properties` object. The CLI does this in three steps:

1. `GET /sequence/detail/{id}` to fetch current state
2. In memory, modify only the fields you want changed (keep others as-is;
   step.id from remote is preserved for matched steps; new steps have no id;
   steps not in the payload are deleted)
3. `POST /sequence/edit` with the full reconstructed payload

The same Full-Replace rule applies to `sequence/setting/edit` for properties
updates (timeTemplateId / aiAutoReply / etc.).

## Field traps (13 commonly hit)

These tripped earlier integrations. The CLI now handles each correctly:

1. **`steps[].taskType = ""`** (empty string) — NOT `"automatic_email"`.
   Backend rejects `taskType="automatic_email"` with `code: 400, msg: "Unknown error !"`.
2. **`steps[].feid` is required** and must be unique within the request.
3. **`steps[].parentFeid = 0`** for new_thread; **= <step N feid>** for reply.
4. **`steps[].groups = ""`** (empty string), **`groupsWeight = 0`** even
   when no AB test.
5. **`tasks[].contentServer` is required** and must be a full HTML document
   with `{{openedUrl}}` pixel for open-tracking.
6. **`tasks[].subject` must be empty when `emailType="reply"`** — backend
   auto-sets `"Re: " + parent.subject`. Including a custom subject is silently
   overwritten.
7. **`setting.properties.emailRealValid` is required** even when not using
   real-time validation (set `enabled: true, rules: ["valid","catchall"]`).
8. **Template variable syntax is `{{ FirstName }}` / `{{ Company }}`** — uses
   the `displayProperty` value from `/contact/property/list`, NOT
   `{{first_name}}` snake_case.
9. **CSV file upload MUST declare `Content-Type: text/csv`** in the multipart
   part header (the CLI does this via `Blob({type: "text/csv"})`).
10. **`mappings` requires "First Name" + "Last Name"** (or single "Full Name").
    Backend rejects upload otherwise. Other fields are optional.
11. **`ignoreStepDelay=1` only affects step 1** — subsequent steps still
    obey their `delayMinutes` and the working-time-window.
12. **Reply auto-detection lag** — when a prospect replies, the backend
    takes 10-30s to mark the sequence as `stopped` for that contact. If a
    follow-up step has `delayMinutes` shorter than ~30s, it may still fire
    before the stop signal lands. Recommend ≥ 1 hour delay between steps.
13. **`aiAutoReplyEnabled=true` requires `aiAutoReplyPrompt` non-empty and
    ≤ 2000 chars.** Backend rejects with code 50070 / 50071 otherwise.

## Pagination conventions

All list endpoints (`sequence/page/list`, `contacts/page/list`,
`mail-box/v2/sent|inbox`, `time/template/list`) accept `{page, size}` in body
(GET endpoints use querystring).

- CLI defaults: `page=1, size=25` per call.
- CLI caps `--limit` at 100.
- For full export, the CLI streams pages and writes to file, with a soft cap
  of 1000 rows (advise user to add more filters past that).

## Response envelope

All endpoints return:

```json
{ "code": 200, "data": <payload>, "msg": "Operation successful!" }
```

Non-200 `code` values seen so far:

| code | Meaning |
|---|---|
| 400 | "Unknown error !" — backend swallowed the real exception (see Field traps) |
| 203 | "Data is empty" — required field missing |
| 50006 | "CSV file is empty" |
| 50007 | "CSV format error" — usually missing `Content-Type: text/csv` |
| 50003 | Sequence not found |
| 50070 | aiAutoReplyPrompt required when enabled |
| 50071 | aiAutoReplyPrompt exceeds 2000 chars |
| 403 | Sequence detail accessed by non-owner |

## Sample inbox/outbox response row

```jsonc
{
  "summaryId": 150479,                 // MAIL_ID for CLI
  "messageId": 38146,                  // needed for mail/reply-mail
  "contactId": 2049119,                // CONTACT_ID for CLI
  "addressId": 1479,                   // sender mailbox
  "sequenceId": 2266,
  "subject": "Re: CLI verify step1 - hi",
  "targetMail": "prospect@example.com",
  "name": "Prospect Display Name",
  "time": "18:44, May 21, 2026 (UTC+08:00)",
  "labels": ["delivered", "opened", "replied", "positive", "human_rep"],
  "openCnt": 1, "clickCnt": 0, "replyCnt": 1,
  "sentiment": "positive",             // AI-detected
  "recipientIntent": "Interested",     // AI-detected
  "snippet": "Thanks, can you tell me more about..."
}
```

The CLI persists the `summaryId → {messageId, addressId, contactId,
sequenceId, to, subject}` map at `.flashrev/inbox-cache.json` so that
`reply --mail-id <MAIL_ID>` can resolve the required fields without an extra
detail call.
