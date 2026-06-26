---
name: cdp-gmail-delivery
description: "Send Gmail messages from an operator-controlled Chrome debug session using Gmail CDP automation. Use when the user asks to send email from the local machine, with or without an attachment. Default assumption: Chrome CDP is already installed and available. If the CDP endpoint is unavailable, ask the human operator to help restart the debug Chrome session, then send, and verify in Sent by unique subject."
metadata: {"openclaw":{"requires":{"bins":["node","npm"]}}}
---

# Gmail CDP Delivery

Use this workflow when a user asks to send email by Gmail from the local machine, with or without an attachment.

Current limitation: this skill supports plain-text Gmail body content plus attachments. It does not reliably support sending raw HTML as inline Gmail body content.

## Required Inputs

- Recipient email
- Optional file path or paths
- Optional body text

## Environment Assumptions

- Chrome with remote debugging support is already installed and expected to be available
- Chrome debug launcher exists in your repo/workspace when restart help is needed:
  - `scripts/restart_debug_chrome.sh`
- Chrome DevTools endpoint is `http://127.0.0.1:9222`
- Node and npm are available
- This skill's runtime dependency is installed once with the bundled installer into `skills/cdp-gmail-delivery/.runtime/pupp-mail`

## Preflight Checklist

- If attaching a file, confirm target file exists and is readable
- If attaching files for a personal Gmail account, keep total size at or under 25 MB
- Reject obviously blocked Gmail attachment classes before send:
  - executable/script-heavy file types like `.exe`, `.dll`, `.js`, `.jar`, `.bat`, `.cmd`, `.msi`, `.iso`, and similar blocked extensions
  - blocked files inside archives, including compressed forms or nested archives
  - password-protected archives
  - documents with malicious macros
- Confirm recipient email is explicit
- Confirm CDP endpoint responds (`http://127.0.0.1:9222/json/version`)
- Confirm user login state in visible debug Chrome session

If a requested attachment appears blocked or too large for Gmail, stop and ask the human operator for another delivery path. Do not keep retrying the same blocked upload.

If the user wants an HTML newsletter or raw HTML email body, treat inline HTML body delivery as unsupported for this skill under the current Gmail compose + CDP model. Use plain-text summary/body plus an `.html` attachment instead, or use a future Gmail API / MIME-based workflow.

For detectable cases, `scripts/send_via_cdp.js` should fail before opening Gmail and print a limitation result instead of pretending the upload might work.

## Workflow

1. Assume Chrome CDP is already available and try the send flow first.
2. If the CDP endpoint is unavailable, run `scripts/restart_debug_chrome.sh` from repo/workspace root.
3. If CDP is still unavailable after restart, ask the human operator to help restore the visible debug Chrome session.
4. If Gmail is not already authenticated in that visible Chrome window, ask the operator to sign in manually.
5. Send mail over CDP with `scripts/send_via_cdp.js`.
6. Verify send in Sent folder by a unique subject.

## Non-negotiable Validation

Before clicking Send, validate all of the following in the live compose draft:

- To field contains intended recipient
- Subject is non-empty and unique
- If attaching files, the compose draft shows all requested filenames before send

If any check fails, stop and repair draft fields before send.

## Gmail Attachment Constraints

- Personal Gmail sending limit: 25 MB total attachment size
- Google Workspace accounts may use admin-defined limits instead
- Gmail blocks many risky attachment types, including executable and script-like formats such as:
  - `.ade`, `.adp`, `.apk`, `.appx`, `.appxbundle`, `.bat`, `.cab`, `.chm`, `.cmd`, `.com`, `.cpl`, `.diagcab`, `.diagcfg`, `.diagpkg`, `.dll`, `.dmg`, `.ex`, `.ex_`, `.exe`, `.hta`, `.img`, `.ins`, `.iso`, `.isp`, `.jar`, `.jnlp`, `.js`, `.jse`, `.lib`, `.lnk`, `.mde`, `.mjs`, `.msc`, `.msi`, `.msix`, `.msixbundle`, `.msp`, `.mst`, `.nsh`, `.pif`, `.ps1`, `.scr`, `.sct`, `.shb`, `.sys`, `.vb`, `.vbe`, `.vbs`, `.vhd`, `.vxd`, `.wsc`, `.wsf`, `.wsh`, `.xll`
- Gmail can also block:
  - compressed forms of blocked files
  - blocked files found inside archives like `.zip` or `.tgz`
  - password-protected archives
  - documents with malicious macros

Use these constraints as preflight filters. If the file is likely to be blocked, do not claim it can be mailed successfully.

## HTML Email Limitation

- Do not promise raw HTML body delivery through Gmail compose DOM automation
- Gmail compose currently behaves like a plain-text/body-editor automation target for this skill, not a reliable raw HTML injection target
- Treat HTML email as a limitation of this skill, not a temporary success path
- Current supported workaround:
  - put a plain-text summary or intro in the email body
  - attach the full `.html` file
- Future upgrade path for true inline HTML email:
  - Gmail API
  - raw MIME message assembly

## Install (one-time)

From the workspace root, run:

```bash
bash skills/cdp-gmail-delivery/scripts/install_runtime.sh
```

What it does:
- Creates `skills/cdp-gmail-delivery/.runtime/pupp-mail`
- Initializes a minimal npm runtime there
- Installs pinned `puppeteer-core@24`

This keeps the runtime local to the skill instead of using an ad hoc `/tmp` path.

## Send Command

```bash
node skills/cdp-gmail-delivery/scripts/send_via_cdp.js \
  --to "recipient@example.com" \
  --body "Optional message"
```

With attachment:

```bash
node skills/cdp-gmail-delivery/scripts/send_via_cdp.js \
  --to "recipient@example.com" \
  --file "/absolute/path/to/file.txt" \
  --body "Optional message"
```

With multiple attachments:

```bash
node skills/cdp-gmail-delivery/scripts/send_via_cdp.js \
  --to "recipient@example.com" \
  --file "/absolute/path/to/file-a.txt" \
  --file "/absolute/path/to/file-b.txt" \
  --body "Optional message"
```

## Success Output

The script prints:

- `EMAIL_SENT_OK`
- `SUBJECT=<unique-subject>`
- `TO=<recipient>`
- `FILE_NAME=<basename-only>` for each attached file

Report success only after these outputs and Sent verification succeed. Do not expose absolute local filesystem paths in success messages.

When local preflight detects a Gmail attachment limitation, the script should print:

- `LIMITATION_GMAIL_ATTACHMENT`
- `REASON=<limitation-type>`
- `DETAILS=<detected-context>` when available
- `ACTION=...` telling the human operator this is a limitation of Gmail attachment sending for this skill

## When to read extra references

- If send flow fails or behaves unexpectedly: read `references/troubleshooting.md`
- If you need incident evidence/context: read `references/receipts.md`

## References

- Runtime model:
  - This workflow uses direct Chrome CDP automation (Puppeteer), not agent-browser.
- Browser runtime/bootstrap foundation:
  - `https://github.com/joustonhuang/chrome_for_openclaw`
  - Script references: `chrome_for_openclaw.sh`, `scripts/restart_debug_chrome.sh`
- Historical script context:
  - `scripts/xrdp_chrome_debug_setup.sh`
- Git repo context: `https://github.com/joustonhuang/unifai`
- Incident receipts:
  - `references/receipts.md`
- Troubleshooting:
  - `references/troubleshooting.md`
