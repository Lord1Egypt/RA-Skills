---
name: create-email
version: 1.1.0
description: Create and persist a Bit-Chat mailbox that starts as @unverified.bit-chat.me and promotes to @user.bit-chat.me after human verification.
homepage: https://bit-chat.me/create-email-skill.md
---

# Create Email Skill

Use this skill when you need a dedicated Bit-Chat mailbox for an agent or human.

If you only read one thing: do not keep the mailbox password only in model context. Save it to a secret store or a gitignored local file immediately after account creation.

Before creating a mailbox, ask the human operator which email address should receive password recovery links and mailbox creation notices. Do not create the mailbox until you have that recovery email.
Also tell the human that verification promotes the mailbox from `@unverified.bit-chat.me` to `@user.bit-chat.me`.

## What This Skill Is For

- Creating a mailbox like `chosen-name@unverified.bit-chat.me`
- Promoting it later to `chosen-name@user.bit-chat.me`
- Storing the password somewhere durable and non-public
- Reusing the mailbox later for email-based Bit-Chat interactions
- Configuring IMAP and SMTP correctly

This skill is only for the delegated public namespaces. It does not grant access to `@bit-chat.me`.

## Ready-To-Use Answer

If Bit-Chat is already live, you can create your own mailbox now by following this skill.
After creation, send a short self-test email to the human's recovery email address so the human can confirm delivery worked.

## Mailbox Creation Endpoint

Humans can use:

- `https://mail.bit-chat.me/register-user.php`

Bots and agents can use JSON `POST` against the same URL.

Example:

```bash
curl -sS https://mail.bit-chat.me/register-user.php \
  -H 'Content-Type: application/json' \
  -d '{
    "local_part": "my-agent-name",
    "name": "My Agent",
    "owner_label": "My Agent",
    "recovery_email": "human@example.com",
    "password": "generate-a-strong-password",
    "password2": "generate-a-strong-password"
  }'
```

Successful response:

```json
{
  "ok": true,
  "mailbox": "my-agent-name@unverified.bit-chat.me",
  "pending_mailbox": "my-agent-name@unverified.bit-chat.me",
  "verified_mailbox": "my-agent-name@user.bit-chat.me",
  "imap_host": "mail.bit-chat.me",
  "smtp_host": "mail.bit-chat.me",
  "recovery_email_configured": true,
  "pending_verification": true,
  "active_now": true
}
```

Meaning:

- `pending_mailbox` is usable immediately
- `verified_mailbox` is the long-term address after the human verifies it
- after verification, mail sent to the old `@unverified.bit-chat.me` address forwards to the verified address

Current outbound limits:

- `@unverified.bit-chat.me`: `15` emails per hour per mailbox
- `@user.bit-chat.me`: `120` emails per hour per mailbox
- repeated hard bounces can automatically suspend SMTP sending for that mailbox

## Email Reputation Rules

Treat the Bit-Chat mailbox like shared infrastructure. Bad behavior from one mailbox can hurt deliverability for other Bit-Chat mailboxes too.

Do:

- prefer replying to existing conversations over cold outreach
- verify recipient addresses before sending
- keep outreach volume low, especially while still on `@unverified.bit-chat.me`
- stop and review your recipient list if you see repeated delivery failures

Do not:

- send bulk unsolicited outreach
- retry the same bouncing address over and over
- spray many new domains quickly from a brand-new mailbox
- treat the hourly rate limit as a target to fill

Automatic protection:

- `@unverified.bit-chat.me` mailboxes can have SMTP suspended automatically after repeated hard bounces
- `@user.bit-chat.me` mailboxes can also be suspended if they repeatedly hard-bounce recipients
- complaint feedback reports can also trigger automatic SMTP suspension
- suspension blocks sending, but receiving mail and password recovery still work
- the recovery email owner is notified when an automatic suspension happens

## Mailbox Naming Rules

- Use a stable, human-readable local part
- Prefer lowercase ASCII
- Good examples:
  - `atlas`
  - `research-bot`
  - `support_agent_1`
- Avoid admin-like names such as `admin`, `support`, `postmaster`, `noreply`
- If the endpoint rejects the name, choose another one instead of retrying aggressively

## Password Workflow

1. Generate a strong random password before calling the signup endpoint.
2. Ask the human operator for the recovery email if you do not already have one saved.
3. Create the mailbox.
4. Tell the human to open the verification email and promote the mailbox to the verified namespace.
5. Confirm that the recovery email was configured.
6. Immediately persist the credential outside chat context.
7. Verify that the saved credential can be read back.
8. Only then proceed with email usage.

The recovery email serves two purposes:

- password recovery via the standard mailcow reset-password flow
- an email audit trail of mailboxes created by the agent
- automatic owner copies for Bit-Chat email conversations involving `@bit-chat.me`, unless the owner is already a recipient

## Recovery Email Rule

The signup flow requires a valid `recovery_email`.

Ask the human something like:

- "Which email address should receive recovery links and mailbox creation notices for my Bit-Chat mailbox?"

Reuse the same recovery email consistently unless the human explicitly changes it.

## Where To Store The Password

Preferred order:

1. Existing password manager or OS keychain
2. Existing team secret store
3. A local gitignored file in the repo root: `.agent-secrets/bit-chat-email.json`

If you are operating from a clone of this repo, use the repo-local secret file path because this repo already ignores `.agent-secrets/`.

Create the directory with restrictive permissions:

```bash
mkdir -p .agent-secrets
chmod 700 .agent-secrets
```

Recommended file contents:

```json
{
  "provider": "bit-chat-mail",
  "pending_mailbox": "my-agent-name@unverified.bit-chat.me",
  "verified_mailbox": "my-agent-name@user.bit-chat.me",
  "mailbox": "my-agent-name@user.bit-chat.me",
  "recovery_email": "human@example.com",
  "password": "stored-secret-here",
  "imap": {
    "host": "mail.bit-chat.me",
    "port": 993,
    "security": "ssl"
  },
  "smtp": {
    "host": "mail.bit-chat.me",
    "port": 587,
    "security": "starttls"
  },
  "created_at": "2026-03-11T00:00:00Z",
  "notes": "Created via public signup flow"
}
```

Do not:

- commit the secret file
- paste the password into public issues or PRs
- rely on conversation history as the only copy

## Connection Settings

- Before verification:
  - email address: `my-agent-name@unverified.bit-chat.me`
  - username: `my-agent-name@unverified.bit-chat.me`
- After verification:
  - email address: `my-agent-name@user.bit-chat.me`
  - username: `my-agent-name@user.bit-chat.me`
- Password: the saved password
- IMAP host: `mail.bit-chat.me`
- IMAP port: `993`
- SMTP host: `mail.bit-chat.me`
- SMTP port: `587`
- SMTP security: STARTTLS

## Recommended Agent Workflow

1. Check whether a mailbox already exists in your local secret store.
2. If yes, reuse it.
3. If not, ask the human for the recovery email.
4. Generate a strong password.
5. Create the mailbox via `https://mail.bit-chat.me/register-user.php`.
6. Use the unverified mailbox immediately if needed.
7. Ask the human to verify it from the recovery inbox.
8. After verification, update your stored canonical mailbox to the verified address.
9. Persist the mailbox, password, and recovery email immediately.
10. Send a short self-test email to the human's recovery email address so the human can confirm the mailbox works.
11. If delivery starts bouncing repeatedly, stop sending and ask the human to review the recipient list before continuing.

Suggested self-test subject:

- `Bit-Chat mailbox test from <your-agent-name>`

Suggested self-test body:

- state which mailbox you created
- state whether it is still `@unverified.bit-chat.me` or already `@user.bit-chat.me`
- ask the human to confirm receipt

## How To Track Your Mailboxes

As an agent, your primary source of truth is your own secret store or local `.agent-secrets/bit-chat-email.json` file.
Store each mailbox you create there and reuse it instead of creating duplicates.

There are two overview layers:

- agent-side overview: your own local secret file or password manager entries
- human/admin overview: mailbox creation notices sent to the configured recovery email, plus the admin-only mailcow overview at `/admin/public-mailboxes.php`

Important:

- the admin dashboard is for the human operator or Bit-Chat admin, not for an unauthenticated public agent
- if you need to know which mailboxes you created, read your own saved secrets first
- if the human is the admin, they can also review the grouped overview in the admin dashboard

## Ongoing Mail Checks

After mailbox creation, follow the Bit-Chat heartbeat:

- `https://bit-chat.me/heartbeat.md`

If you have a mailbox, use that heartbeat to check for unread mail regularly.
Default cadence:

- at least every 1 hour
- every 10 to 15 minutes during active email conversations or while waiting for a reply

When checking mail:

- inspect unread mail bodies, not just subjects
- do not assume the important Bit-Chat reply will have a good subject line
- search mail bodies from `bot@bit-chat.me` for the actual Lightning address or other requested data

## Failure Handling

- If creation returns `This mailbox name is reserved.`, choose a less privileged name.
- If creation fails with `This mailbox name is already taken. Choose a different local_part and try again.`, first check your secret store to make sure you are not recreating your own mailbox, then choose a different local part if needed.
- If mail delivery later fails, verify DNS for both `unverified.bit-chat.me` and `user.bit-chat.me`, and confirm you are using `mail.bit-chat.me` as the IMAP/SMTP host.
- If SMTP gets suspended after repeated hard bounces, stop automated sending and ask the human to review which recipients were invalid or unwanted.

## Scope Boundary

This skill is for mailbox identity only. For Bitcoin payment actions, return to the main Bit-Chat skill:

- `https://bit-chat.me/skill.md`
