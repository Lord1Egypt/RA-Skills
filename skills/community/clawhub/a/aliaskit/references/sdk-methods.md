# AliasKit SDK Method Reference

## Constructor

```typescript
const { AliasKit } = require('aliaskit');
const ak = new AliasKit({ apiKey?, baseUrl?, cardKey? });
```

- `apiKey`: defaults to `ALIASKIT_API_KEY` env var
- `baseUrl`: defaults to `https://www.aliaskit.com/api/v1`
- `cardKey`: required for card operations, defaults to `ALIASKIT_CARD_KEY`

## ak.identities

| Method | Returns | Notes |
|--------|---------|-------|
| `create(params?)` | `Identity` | params: `name?`, `emailDomain?`, `emailUsername?`, `provisionPhone?`, `metadata?` |
| `list()` | `{ data: Identity[] }` | All identities for this API key |
| `get(id)` | `Identity` | |
| `delete(id)` | `void` | Releases email + phone resources |
| `provisionPhone(id, { country? })` | `Identity` | country: `'US'` or `'GB'` |
| `listEvents(id, params?)` | `{ data: Event[] }` | Identity activity log |
| `listMessages(id, params?)` | `{ data: Message[] }` | Unified inbox (email + SMS) |

## ak.emails

| Method | Returns | Notes |
|--------|---------|-------|
| `list(identityId, { limit?, offset?, unread? })` | `{ data: EmailMessage[] }` | |
| `get(identityId, emailId)` | `EmailMessage` | Full body + headers |
| `send(identityId, { to, subject?, bodyText?, bodyHtml? })` | `EmailMessage` | |
| `search(identityId, { query?, from?, after?, before? })` | `{ data: EmailMessage[] }` | At least one filter required |
| `markRead(identityId, emailId, read)` | `EmailMessage` | |
| `delete(identityId, emailId)` | `void` | |
| `waitForCode(identityId, opts?)` | `string` | Polls for OTP code. opts: `timeout?`, `interval?`, `provider?`, `after?` |
| `waitForMagicLink(identityId, opts?)` | `string` | Polls for verification URL |
| `getAttachmentUrl(emailId, index)` | `{ url: string }` | Signed download URL |

## ak.sms

| Method | Returns | Notes |
|--------|---------|-------|
| `list(identityId, { limit?, offset?, unread? })` | `{ data: SmsMessage[] }` | |
| `send(identityId, { to, body })` | `SmsMessage` | `to` in E.164 format |
| `markRead(identityId, smsId, read)` | `SmsMessage` | |
| `delete(identityId, smsId)` | `void` | |
| `waitForCode(identityId, opts?)` | `string` | opts: `timeout?`, `interval?`, `after?` |

## ak.cards

| Method | Returns | Notes |
|--------|---------|-------|
| `create(identityId, params)` | `Card` | params: `cardNumber`, `cvc`, `expMonth`, `expYear`, `budgetCents?`, `cardSource?`, `cardName?`. Encrypted client-side. |
| `list(identityId)` | `{ data: Card[] }` | Metadata only (no plaintext) |
| `reveal(cardId, { amountCents? })` | `CardRevealResponse` | Returns `number`, `cvc`, `exp_month`, `exp_year`. Decrypted client-side. |
| `freeze(cardId)` | `Card` | Temporary |
| `unfreeze(cardId)` | `Card` | |
| `cancel(cardId)` | `Card` | Permanent, cannot undo |
| `budget(cardId)` | `CardBudget` | `budget_cents`, `spent_cents`, `remaining_cents` |
| `updateBudget(cardId, { budgetCents?, resetSpend? })` | `CardBudget` | |
| `activity(cardId)` | `{ data: CardActivity[] }` | Transaction history |

Requires `cardKey` in constructor. Generate once: `const key = AliasKit.generateCardKey()`.

## ak.totp

| Method | Returns | Notes |
|--------|---------|-------|
| `register(identityId, { secret, serviceName?, algorithm?, digits?, period? })` | `TotpEntry` | |
| `list(identityId)` | `{ data: TotpEntry[] }` | |
| `getCode(identityId, totpId)` | `{ code, remaining_seconds }` | Current 6-digit code |
| `delete(identityId, totpId)` | `void` | |

## ak.realtime

| Method | Returns | Notes |
|--------|---------|-------|
| `subscribeToEmails(identityId, callback)` | `{ unsubscribe() }` | Live email events |
| `subscribeToSms(identityId, callback)` | `{ unsubscribe() }` | Live SMS events |
| `subscribe(identityId, callback)` | `{ unsubscribe() }` | All agent events |

## OTP Provider Presets

```typescript
ak.emails.waitForCode(id, { provider: 'supabase' })
ak.emails.waitForCode(id, { provider: 'clerk' })
ak.emails.waitForCode(id, { provider: 'auth0' })

// Custom extractor:
ak.emails.waitForCode(id, {
  provider: {
    id: 'my-service',
    name: 'My Service',
    detect: (email) => email.from.includes('myservice.com'),
    extractCode: (text) => text.match(/code: (\d{6})/)?.[1] ?? null,
  },
})
```

## Error Classes

| Error | When |
|-------|------|
| `AliasKitError` | Base error class, has `code` property |
| `AuthError` | Missing or invalid API key |
| `ApiError` | HTTP 4xx/5xx, has `status`, `endpoint`, `responseBody` |
| `EmailTimeoutError` | No email arrived within timeout, has `timeoutMs` |
| `SmsTimeoutError` | No SMS arrived within timeout, has `timeoutMs` |
| `OtpNotFoundError` | Message arrived but no code found, has `emailSubject?`, `emailFrom?` |
| `BillingError` | 402 plan limit errors, has `requiredPlan` |

```typescript
const { AliasKit, EmailTimeoutError, OtpNotFoundError, ApiError } = require('aliaskit');
```
