# Security & Scope

## What this skill does

This skill operates the operator's own Bumble web account inside a remote browser
session that the operator owns. Every action is initiated by the operator from
their own machine and corresponds to a button or input that the operator could
click in their own browser.

## What this skill does not do

- It does not create Bumble accounts.
- It does not guess, brute-force, or replay credentials.
- It does not bypass Bumble's CAPTCHA or any anti-abuse defense. CAPTCHA screens
  stop the script and require manual human action.
- It does not register or store a passkey. On the optional passkey enrollment
  prompt it taps Bumble's official "Not Now" button to decline the prompt.
- It does not enumerate, scrape, or collect data about people the operator's
  account is not already authorized to see.
- It does not attempt to send messages that Bumble's backend does not already
  allow (for example, it cannot send first in a "Their move" match).

## Inputs supplied by the operator

- Phone number used to log in.
- 6-digit SMS code received by the operator.
- Match name(s) the operator wants to read or message.
- Output directory for any photo export.

## Data handled

- Session cookies stored by the Remote Browser Service for the operator's own
  account.
- Messages and profile data visible inside the operator's own Bumble account.
- Optional photo export, written only to a directory the operator specifies.

## Pacing

The script inserts short 1-4 second jitter between actions. This is for page
stability and to stay below normal rate limits on a single human-operator
account; it is not intended to evade abuse detection.

## Reporting issues

If you find a real security issue with this skill (not a usage question), please
open a GitHub issue at
[https://github.com/vasyaod/bumble-client/issues](https://github.com/vasyaod/bumble-client/issues).
