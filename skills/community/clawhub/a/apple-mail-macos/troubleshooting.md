# Troubleshooting - Apple Mail (MacOS)

## Mail Automation Permission Denied

Symptoms:
- `osascript` returns permission errors.

Fix:
1. Open System Settings -> Privacy and Security -> Automation.
2. Allow your terminal app to control Mail.
3. Re-run a read-only probe before attempting writes.

## Shortcut Not Found

Symptoms:
- `shortcuts run` fails with missing shortcut name.

Fix:
1. Confirm exact shortcut name with `shortcuts list`.
2. Update command to the exact name.
3. Keep a fallback path with `osascript`.

## Message Not Found for Write

Symptoms:
- Move, reply, or delete targets do not resolve.

Fix:
1. Expand search window slightly.
2. Disambiguate using sender plus date, not subject only.
3. Retry with explicit mailbox scope.

## Duplicate Send Risk Detected

Symptoms:
- Operation looks like a repeat send.

Fix:
1. Compare operation ID with recent sent records.
2. Ask user whether this is intentional resend.
3. Proceed only with explicit confirmation.

## Provider Sync Delay

Symptoms:
- Write succeeds locally but remote state appears delayed.

Fix:
1. Wait a short sync interval.
2. Re-read mailbox window.
3. If still inconsistent, report provider sync latency and keep logs.

## Proton Bridge Offline

Symptoms:
- Proton-connected account fails read or send unexpectedly.

Fix:
1. Verify Proton Mail Bridge is running and unlocked.
2. Re-run account read probe.
3. Keep send actions blocked until probe succeeds.
