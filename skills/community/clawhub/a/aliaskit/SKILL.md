---
name: aliaskit
description: |
  Persistent digital identity for this agent. Provides real email, phone number,
  virtual payment card, and TOTP codes. Use this skill whenever the agent needs:
  an email address, a phone number, a name, a date of birth, a mailing address,
  a card number or payment method, to sign up for a service, to receive a
  verification code (email or SMS), to make an online purchase, to handle 2FA/MFA,
  to send an email or SMS, to prove identity, or any operation requiring a piece
  of identification material.
---

# AliasKit Identity

You have a persistent digital identity. `identity.json` is stored next to this SKILL.md file. Use the directory containing this file as the base path for all operations.

First, check for new messages by running `scripts/check-events.sh` (relative to this file's directory).

## Load your identity

Read `identity.json` from the same directory as this SKILL.md file.

If `identity.json` does not exist, run `scripts/setup.sh` (relative to this file's directory).

After loading, you have:
- `identityId` - your AliasKit identity ID (use in all SDK calls)
- `email` - your real email address (use for signups, forms, contact)
- `phone` - your real phone number (use for SMS verification, phone fields)
- `name` - your full name (use for name fields on forms)
- `dob` - your date of birth (use for DOB fields)
- `cardKey` - encryption key for virtual card operations

## What you can do

You have a complete digital identity. Use it whenever you encounter:

- **Email fields**: Use `identity.email` for any form asking for email
- **Phone fields**: Use `identity.phone` for any form asking for phone number
- **Name fields**: Use `identity.name` for any form asking for your name
- **DOB fields**: Use `identity.dob` for date of birth
- **Signup flows**: Sign up using your email, then retrieve the verification code
- **SMS verification**: Receive SMS codes at your phone number
- **Online purchases**: Reveal your virtual card details for checkout
- **2FA/MFA**: Register TOTP secrets and read current codes
- **Sending messages**: Send emails and SMS from your own address/number
- **Realtime listeners**: Subscribe to live email/SMS events via WebSocket
- **Search emails**: Full-text search across your inbox
- **Email threads**: View conversation threads
- **Attachments**: Download email attachments via signed URLs
- **Mark read/delete**: Manage inbox state

If a form asks for personal information, always read your identity file first.

## Patterns

All patterns start with loading the identity and creating the SDK client. Read `identity.json` from the same directory as this file. The API key is stored in identity.json so it persists across sessions.

```typescript
const fs = require('fs');
const path = require('path');
const { AliasKit } = require('aliaskit');

const id = JSON.parse(fs.readFileSync(path.join(SKILL_DIR, 'identity.json'), 'utf8'));

// Set API key from stored credentials (persists across sessions)
if (id.apiKey) process.env.ALIASKIT_API_KEY = id.apiKey;

const ak = new AliasKit();
```

Replace `SKILL_DIR` with the actual path to the directory containing this SKILL.md file.

### A. Identity management

```typescript
// Create a new identity (usually done once via setup.sh)
const identity = await ak.identities.create({ provisionPhone: true });

// List all identities
const all = await ak.identities.list();

// Get an identity by ID
const existing = await ak.identities.get(id.identityId);

// Provision a phone number on an existing identity
const updated = await ak.identities.provisionPhone(id.identityId, { country: 'US' });

// Delete an identity (releases email + phone)
await ak.identities.delete(id.identityId);

// List identity events (activity log)
const events = await ak.identities.listEvents(id.identityId, { limit: 20 });
```

### B. Fill a form with your details

When you encounter a form asking for personal information:

```typescript
console.log('Name:', id.name);
console.log('Email:', id.email);
console.log('Phone:', id.phone);
console.log('DOB:', id.dob);
```

Use these values to fill form fields. For address fields, ask the user.

### B. Sign up for a service (email verification)

After using `id.email` to sign up, wait for the verification email. `waitForCode` checks existing unread emails first, then subscribes via realtime WebSocket. It returns the full email, so you can read the body and extract the code yourself.

```typescript
const email = await ak.emails.waitForCode(id.identityId, { timeout: 60_000 });
console.log('From:', email.from);
console.log('Subject:', email.subject);
console.log('Body:', email.body_text);
// Read the body and extract the verification code or link from it
```

### C. SMS verification

Same pattern. Returns the full SMS message.

```typescript
const sms = await ak.sms.waitForCode(id.identityId, { timeout: 60_000 });
console.log('From:', sms.from);
console.log('Body:', sms.body);
// Read sms.body and extract the verification code from it
```

If `waitForCode` isn't working, you can use the realtime subscription directly:

```typescript
const sub = ak.realtime.subscribeToEmails(id.identityId, (email) => {
  if (email.direction === 'inbound') {
    console.log('New email:', email.from, email.subject, email.body_text);
    sub.unsubscribe();
  }
});

// For SMS:
const smsSub = ak.realtime.subscribeToSms(id.identityId, (sms) => {
  if (sms.direction === 'inbound') {
    console.log('New SMS:', sms.from, sms.body);
    smsSub.unsubscribe();
  }
});
```

### D. Add a card (setup process)

When the user wants their agent to make purchases, walk them through adding a card. Ask for these details one by one:

1. **Card number** (the 16-digit number on the card)
2. **CVC** (3-digit security code on the back)
3. **Expiry month** (1-12)
4. **Expiry year** (e.g. 2028)
5. **Cardholder's first name** (the real name on the card, NOT the identity's generated name)
6. **Cardholder's last name**
7. **Billing address line 1**
8. **Billing address line 2** (optional)
9. **City**
10. **State / region** (optional)
11. **Postal / ZIP code**
12. **Country** (e.g. GB, US)
13. **Budget limit** (optional, in your currency, e.g. "50" for a £50 cap)
14. **Card source** (where the card is from: revolut, monzo, wise, or other)

Explain to the user: "All card and billing details are encrypted on your device before anything is sent. AliasKit's servers only ever see an encrypted blob. The card key in your identity.json is used to decrypt details locally when needed. AliasKit can never see your card number, CVC, or billing details."

We recommend using a virtual card from your bank (Revolut, Monzo, Wise) with its own spending limit as a safety net.

```typescript
const ak = new AliasKit({ cardKey: id.cardKey });

const card = await ak.cards.create(id.identityId, {
  cardNumber: '4242424242424242',
  cvc: '123',
  expMonth: 12,
  expYear: 2028,
  billingFirstName: 'John',
  billingLastName: 'Doe',
  billingAddressLine1: '123 Main Street',
  billingAddressLine2: 'Flat 4B',
  billingAddressCity: 'London',
  billingAddressState: 'Greater London',
  billingAddressPostalCode: 'SW1A 1AA',
  billingAddressCountry: 'GB',
  budgetCents: 5000,       // optional, £50 limit
  cardSource: 'revolut',
  cardName: 'Shopping',
});
```

**Important distinction**: The billing details (real name, real address) belong to the card and are for checkout forms only. They are completely separate from the identity's generated name and DOB. When filling a checkout form:
- Use `card.billing_first_name` / `card.billing_last_name` for name fields (NOT `identity.name`)
- Use `card.billing_address_*` for address fields
- Use `identity.email` for email fields
- Use `identity.phone` for phone fields

### E. Make a purchase (reveal card)

When the agent needs to fill a checkout form, reveal the card to get all details:

```typescript
const ak = new AliasKit({ cardKey: id.cardKey });
const cards = await ak.cards.list(id.identityId);

if (cards.data.length === 0) {
  // No card added yet. Ask the user to add one (see pattern D above).
  console.log('No card added. Ask the user to add a bank card first.');
} else {
  const card = await ak.cards.reveal(cards.data[0].id, {
    amountCents: 1999, // declare the purchase amount for budget tracking
  });

  // Card details
  console.log('Card:', card.number);
  console.log('CVC:', card.cvc);
  console.log('Expiry:', card.exp_month + '/' + card.exp_year);

  // Billing details (use these for checkout, not identity.name)
  console.log('Name:', card.billing_first_name, card.billing_last_name);
  console.log('Address:', card.billing_address_line1);
  console.log('City:', card.billing_address_city);
  console.log('Postal:', card.billing_address_postal_code);
  console.log('Country:', card.billing_address_country);
}
```

Never log full card numbers in conversation output. Use `last4` for display.

### E. Handle TOTP 2FA

When a service shows a TOTP QR code or secret during 2FA setup:

```typescript
// Register a TOTP secret
const entry = await ak.totp.register(id.identityId, {
  secret: 'JBSWY3DPEHPK3PXP',
  serviceName: 'example.com',
});

// Get the current code
const { code, remaining_seconds } = await ak.totp.getCode(id.identityId, entry.id);
console.log('2FA code:', code, '(expires in', remaining_seconds, 's)');

// List all registered TOTP secrets
const secrets = await ak.totp.list(id.identityId);
secrets.data.forEach(t => console.log(t.service_name, t.id));

// Delete a TOTP entry
await ak.totp.delete(id.identityId, entry.id);
```

### F. Send email or SMS

```typescript
await ak.emails.send(id.identityId, {
  to: 'someone@example.com',
  subject: 'Hello',
  bodyText: 'Message from your AI agent.',
});

await ak.sms.send(id.identityId, {
  to: '+15551234567',
  body: 'Message from your AI agent.',
});
```

### G. Check inbox

```typescript
const emails = await ak.emails.list(id.identityId, { unread: true, limit: 10 });
emails.data.forEach(e => console.log(`[${e.from}] ${e.subject}`));

const sms = await ak.sms.list(id.identityId, { unread: true, limit: 10 });
sms.data.forEach(s => console.log(`[${s.from}] ${s.body}`));
```

### H. Realtime subscriptions (listen for incoming messages)

Instead of polling, you can subscribe to live events. The callback fires instantly when an email or SMS arrives.

```typescript
// Listen for incoming emails
const emailSub = ak.realtime.subscribeToEmails(id.identityId, (email) => {
  console.log('New email from:', email.from, '| Subject:', email.subject);
  // React to the email here
});

// Listen for incoming SMS
const smsSub = ak.realtime.subscribeToSms(id.identityId, (sms) => {
  console.log('New SMS from:', sms.from, '| Body:', sms.body);
  // React to the SMS here
});

// Listen for all events (emails, SMS, card authorizations, etc.)
const allSub = ak.realtime.subscribe(id.identityId, (event) => {
  console.log('Event:', event.type, event.data);
});

// When done, unsubscribe:
emailSub.unsubscribe();
smsSub.unsubscribe();
allSub.unsubscribe();
```

Use realtime subscriptions when your agent needs to react immediately to incoming messages, rather than checking on a schedule.

### I. Search emails

```typescript
const results = await ak.emails.search(id.identityId, {
  query: 'verification',       // full-text search on subject + body
  from: 'noreply@example.com', // filter by sender
  after: '2026-04-01T00:00:00Z',
  limit: 10,
});
results.data.forEach(e => console.log(e.subject));
```

### J. Email threads

```typescript
const threads = await ak.threads.list(id.identityId);
threads.data.forEach(t => console.log(t.subject, '-', t.message_count, 'messages'));

// Get a full thread with all messages
const thread = await ak.threads.get(id.identityId, threadId);
thread.messages.forEach(m => console.log(m.from, ':', m.body_text));
```

### K. Manage inbox

Messages are NOT automatically marked as read when you list or poll them. You must explicitly mark them as read after processing. This is important for workflows that check for unread messages, otherwise you will keep re-processing the same messages.

```typescript
// Mark email as read (do this after you've processed the message)
await ak.emails.markRead(id.identityId, emailId, true);

// Mark SMS as read
await ak.sms.markRead(id.identityId, smsId, true);

// Mark as unread again
await ak.emails.markRead(id.identityId, emailId, false);

// Delete an email
await ak.emails.delete(id.identityId, emailId);

// Delete an SMS
await ak.sms.delete(id.identityId, smsId);

// Get a signed URL for an email attachment
const { url } = await ak.emails.getAttachmentUrl(emailId, 0); // 0 = first attachment
```

### L. Wait for a magic link

```typescript
const link = await ak.emails.waitForMagicLink(id.identityId, {
  timeout: 60_000,
});
console.log('Magic link:', link); // https://example.com/verify?token=...
```

### M. Card management

```typescript
const ak = new AliasKit({ cardKey: id.cardKey });

// Add a new card with billing details (all encrypted before leaving your device)
const card = await ak.cards.create(id.identityId, {
  cardNumber: '4242424242424242',
  cvc: '123',
  expMonth: 12,
  expYear: 2028,
  budgetCents: 5000,         // optional spending limit
  cardSource: 'revolut',     // where the card is from
  cardName: 'Shopping',      // friendly label
  // Billing details (cardholder's real details for checkout forms)
  billingFirstName: 'John',
  billingLastName: 'Doe',
  billingAddressLine1: '123 Main Street',
  billingAddressCity: 'London',
  billingAddressPostalCode: 'SW1A 1AA',
  billingAddressCountry: 'GB',
});

// Check budget before a purchase
const budget = await ak.cards.budget(card.id);
console.log('Remaining:', budget.remaining_cents, 'cents');

// Update budget
await ak.cards.updateBudget(card.id, { budgetCents: 10000 });

// View card activity
const activity = await ak.cards.activity(card.id);
activity.data.forEach(a => console.log(a.amount_cents, a.allowed ? 'approved' : 'declined'));

// Freeze / unfreeze / cancel
await ak.cards.freeze(card.id);
await ak.cards.unfreeze(card.id);
await ak.cards.cancel(card.id); // permanent
```

### N. Unified inbox

```typescript
// Get all messages (email + SMS) in one call
const all = await ak.identities.listMessages(id.identityId, { limit: 20 });
all.data.forEach(m => console.log(m.direction, m.from || m.to));
```

## Guardrails

- **Never create a second identity.** Always use the one in your identity file.
- **Never log full card numbers.** Use `last4` for any output shown to the user.
- **Identity file is sensitive.** Never commit it to version control.
- **Card key is irrecoverable.** If lost, card data cannot be decrypted.

For the full SDK method reference, read: `references/sdk-methods.md`

For detailed documentation, guides, and examples, visit: https://www.aliaskit.com/docs

## Troubleshooting

- `ALIASKIT_API_KEY not set` - Get your key at https://aliaskit.com/dashboard
- `EmailTimeoutError` - No email arrived in 60s. Check the email address was entered correctly.
- `SmsTimeoutError` - No SMS arrived. Check the phone number was entered in E.164 format.
- `OtpNotFoundError` - An email/SMS arrived but no code was found. Try passing a `provider` hint.
- `Identity not found` - The identity may have been deleted. Run setup again.
