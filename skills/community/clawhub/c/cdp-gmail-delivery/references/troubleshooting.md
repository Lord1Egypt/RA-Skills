# Troubleshooting

## Runtime dependency missing (`Unable to load puppeteer-core`)

Symptoms:
- send script exits before connecting to Chrome

Actions:
1. Run `bash skills/cdp-gmail-delivery/scripts/install_runtime.sh`
2. Confirm `skills/cdp-gmail-delivery/.runtime/pupp-mail/node_modules/puppeteer-core` exists
3. Retry the send command

## CDP endpoint unreachable (`ECONNREFUSED 127.0.0.1:9222`)

Symptoms:
- send script fails before opening Gmail

Actions:
1. Run `scripts/restart_debug_chrome.sh`
2. Confirm endpoint:
   - `curl -fsS http://127.0.0.1:9222/json/version`
3. If the endpoint is still unavailable, ask the human operator to help restore the visible debug Chrome session
4. Retry send command

## Gmail still opens Sign-in page in automation

Symptoms:
- browser automation sees Google login page

Actions:
1. Use visible desktop Chrome session started by `restart_debug_chrome.sh`
2. Ask user to log in manually there
3. Re-run send script after login

## Validation failed: duplicate attachment

Symptoms:
- error includes `attachmentOk:false` / occurrence > 1

Actions:
1. Discard existing draft in Gmail
2. Re-open fresh compose
3. Attach only once and retry

## Attachment blocked by Gmail for security reasons

Symptoms:
- Gmail blocks the draft or send step
- Gmail reports a security or harmful-content issue

Common causes:
- executable or script-like attachment types
- blocked files inside archives
- password-protected archives
- documents with malicious macros

Actions:
1. Stop retrying the same blocked file
2. Confirm whether the file type or archive contents match Gmail's blocked classes
3. Tell the human operator this is a limitation of Gmail attachment sending for this skill
4. Ask for another delivery path or a safer export format

## Attachment too large for Gmail

Symptoms:
- attachment cannot be added normally
- Gmail moves large content out of the normal attachment path

Actions:
1. For personal Gmail, keep total attachment size at or under 25 MB
2. For Workspace accounts, remember admin-defined limits may differ
3. Tell the human operator this is a limitation of Gmail attachment sending for this skill
4. Ask for another delivery path

## Raw HTML email body requested

Symptoms:
- the user wants a true HTML email body or newsletter rendered inline in Gmail

Reality:
- this skill does not reliably support raw HTML body injection into Gmail compose
- treat this as a limitation of the current Gmail CDP compose workflow

Actions:
1. Do not claim inline HTML email body support
2. Tell the human operator this is a limitation of this skill
3. Send plain-text summary/body plus `.html` attachment when acceptable
4. If true inline HTML is required, route the request to a future Gmail API / MIME-based workflow

## Send toast not shown but maybe sent

Symptoms:
- script times out waiting for "Message sent"

Actions:
1. Search Sent folder by unique subject
2. If found in Sent, treat as sent
3. If not found, retry from fresh compose
