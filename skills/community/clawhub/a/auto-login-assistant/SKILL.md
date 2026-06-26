---
name: auto-login-assistant
description: Help the agent recover from login walls on websites by detecting sign-in states, collecting user-approved credentials, filling common login forms, and handling verification codes safely. Use when browsing is blocked by authentication and the user wants guided sign-in rather than manual step-by-step help.
metadata:
  short-description: Detect login walls, fill credentials, and handle OTP safely.
---

# Auto Login Assistant

## Overview

Use this skill when the agent is navigating a website and progress is blocked by a login screen, expired session, or verification-code challenge. The skill provides a conservative workflow for sign-in assistance: detect the login wall, collect user-approved credentials, fill the form, and handle one-time codes with clear consent boundaries.

This skill is intentionally not a bypass tool. It should never attempt to break captchas, defeat anti-bot systems, or infer secrets the user did not explicitly provide.

## When To Use

Trigger this skill when any of the following are true:

- The page redirects to a login, sign-in, or session-expired screen.
- The user asks the agent to sign in to a website, mailbox, SaaS product, or admin console.
- A workflow such as reading email, sending mail, checking dashboards, or accessing settings is blocked by authentication.
- The user wants the agent to help retrieve or place a verification code after they approve the flow.

Do not use this skill for:

- Captcha solving, QR login bypass, hardware key prompts, payment approval, or biometric confirmation
- Guessing usernames, passwords, security questions, or backup codes
- Reading email or messages unless the user explicitly authorizes it for the current task

## Workflow

### 1. Confirm It Is A Login Barrier

First verify that the page is actually asking for authentication. Look for signals such as:

- URL patterns like `login`, `signin`, `auth`, `session-expired`, `verify`
- Password fields, OTP fields, or email/username inputs
- Buttons or headings such as "Sign in", "Log in", "Continue with email", "Enter code"

If the page is ambiguous, say so and ask the user whether you should treat it as a login flow before entering any credentials.

### 2. Choose Credential Source

Credential priority order:

1. Credentials the user provides in the current conversation
2. A local file path the user explicitly points to
3. Environment variables the user explicitly names

Never scan the filesystem broadly for secrets. Never assume a saved credential source without user direction.

If the user gives a file path or env var name, use `scripts/read_credentials.py` to normalize it into a consistent structure.

Supported normalized fields:

- `site`
- `login_url`
- `username`
- `email`
- `phone`
- `password`
- `otp_email`
- `otp_mode`
- `notes`

See `references/config-example.md` for examples.

### 3. Fill The Login Form Conservatively

Use the website's visible login flow rather than forcing a direct post.

Preferred field mapping order:

- User identifier: `email`, `username`, `account`, `phone`
- Secret: `password`
- Verification: `otp`, `code`, `verification code`, `security code`

Before submitting:

- Confirm the target site with the user if multiple accounts could apply
- Mask secrets in your explanation
- Avoid clicking "remember this device" or equivalent unless the user explicitly asks

### 4. Handle Verification Codes

Default behavior: ask the user to provide the verification code manually.

Only enter the email-reading branch if the user explicitly authorizes it for the current task and provides the mailbox access path. When allowed:

- Read only the minimum mailbox content needed to locate the latest relevant code
- Extract likely codes with `scripts/extract_verification_code.py`
- Present the candidate briefly if confidence is low
- If multiple codes are plausible, ask before submitting

If email access fails or is unavailable, fall back to asking the user to paste the code.

### 5. Validate Success

After submit, confirm login success using page evidence:

- User avatar, account menu, inbox, dashboard, or "sign out" control
- Removal of login prompt
- Successful navigation to the requested feature

If the flow fails, stop after a small number of attempts and explain the blocker clearly. Do not loop forever on retries.

## Safety Rules

- Treat credentials as ephemeral unless the user explicitly asks for a reusable local config.
- Do not store credentials in the skill folder.
- Do not broaden permissions, change MFA settings, or approve trusted-device prompts without explicit user permission.
- Refuse flows that amount to bypassing authentication or anti-abuse protections.
- If the website requests a captcha, QR scan, physical token, or passkey confirmation, hand control back to the user.

## Suggested Interaction Pattern

Use short, direct prompts like these:

- "This page appears to require login. Do you want me to sign in with credentials you provide now, or a local config you specify?"
- "I found a password field and an email field. Please provide the account for this site, or point me to the config path."
- "The site is asking for a verification code. If you want, paste the code here. I can only read email for this if you explicitly authorize that mailbox for this task."

## Resources

### `references/config-example.md`

Load this when the user wants a reusable local credential format or wants to see supported fields.

### `scripts/read_credentials.py`

Run this to normalize credentials from a JSON file or environment variables into a consistent schema.

### `scripts/extract_verification_code.py`

Run this to extract likely one-time codes from email text or copied verification messages after the user authorizes that step.
