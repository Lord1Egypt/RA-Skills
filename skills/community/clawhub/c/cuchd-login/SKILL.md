---
name: openclaw
description: >
  Full browser automation skill for the OpenClaw platform. Use this skill whenever
  the user wants to log in to OpenClaw, navigate its portal, submit forms, retrieve
  data, or perform any browser-based interaction with OpenClaw. Trigger this skill
  even if the user only mentions "OpenClaw", "claw portal", or asks to "open the
  claw dashboard". This skill grants the agent full permission to operate the browser
  autonomously — including clicking, typing, waiting, reading page content, and
  navigating — without asking for confirmation at each step.
version: 1.0.0
permissions:
  browser: full
  navigation: allow-all
  form-input: allow
  data-read: allow
  auto-proceed: true
  confirm-each-step: false
---

# OpenClaw Browser Automation Skill

The agent is granted **full autonomous browser access** for all interactions with the
OpenClaw platform. The agent must NOT pause to ask for confirmation at each step —
it should proceed through the full flow independently and only report back at the end
(or if a blocker is encountered, such as a CAPTCHA or unexpected error).

---

## Agent Permissions (Full)

| Permission | Status |
|---|---|
| Navigate to URLs | ✅ Allowed |
| Click any element | ✅ Allowed |
| Type into fields | ✅ Allowed |
| Wait for page/element | ✅ Allowed |
| Read page content | ✅ Allowed |
| Submit forms | ✅ Allowed |
| Follow redirects | ✅ Allowed |
| Handle dynamic content | ✅ Allowed |
| Solve CAPTCHA | ❌ Not allowed — notify user |
| Store passwords | ❌ Never — security policy |

---

## Login URL

```
https://openclaw.in
```

---

## Login Flow (Two-Step)

The OpenClaw login is a **two-step process**. The password field is hidden until
the username is submitted and the page reloads. The agent must handle this sequentially.

---

### Step 1 — Navigate to Portal

```
browser: navigate to https://openclaw.in
```

- Wait for the page to **fully load** before proceeding
- Do not interact with any element until load is confirmed

---

### Step 2 — Enter Username / User ID

- Locate the username or User ID input field
  - May be labelled: `"Username"`, `"User ID"`, `"Employee ID"`, or `"Email"`
- If the field is **auto-focused**, type directly; otherwise click it first

```
browser: type "<username>" into the username field
```

- Click the **Next** button to proceed
  - May be labelled: `"Next"`, `"Continue"`, or `"Proceed"`

```
browser: click the Next / Continue button
```

- If no Next button is found → press **Enter** after typing the username

---

### Step 3 — Wait for Password Field

The page will **reload or dynamically update**. The password field is not visible
before this reload. The agent must wait until it appears.

```
browser: wait for the password field to appear (up to 15 seconds)
```

- Do not proceed until the password input is visible and interactable

---

### Step 4 — Enter Password

```
browser: type "<password>" into the password field
```

> ⚠️ **Security rule**: Never log, store, echo, or write the password anywhere.

---

### Step 5 — Submit Login

```
browser: click the Login button
```

- If no Login button is found → press **Enter** after entering the password

---

### Step 6 — Confirm Login Success

```
browser: wait for dashboard or home page to load
browser: read the page title or welcome message
```

- ✅ If logged in: report `"Login successful. Now on: <page title or URL>"`
- ❌ If error shown: report the **exact error message** displayed on screen
- ❌ If CAPTCHA appears: stop and notify the user immediately

---

## Post-Login Actions

The agent may proceed with any of the following actions autonomously after login:

### Navigate to a Section

```
browser: click "<section name>" in the navigation menu or sidebar
browser: wait for the section page to load
```

### Read / Extract Page Data

```
browser: locate the data table, list, or content area
browser: read and return all visible text and structured data
```

### Fill and Submit a Form

```
browser: locate the form on the current page
browser: fill each field in order as instructed
browser: click the Submit / Save / Confirm button
browser: confirm the success message or note any error
```

### Download a File

```
browser: locate the download link or button
browser: click it and wait for the download to begin
browser: confirm the filename and report to user
```

### Logout

```
browser: click the user profile icon or dropdown menu
browser: click Logout / Sign Out
browser: confirm redirect to login or home page
```

---

## Error Handling

| Situation | Agent Action |
|---|---|
| Login fails with error message | Report exact error text; do not retry automatically |
| CAPTCHA appears | Stop immediately; notify the user |
| Page does not load in 15s | Report timeout; ask user how to proceed |
| Element not found | Scroll the page; if still missing, describe visible UI and report |
| Session expires mid-task | Re-run login flow from Step 1 automatically |
| Unexpected popup or modal | Dismiss if safe (e.g., cookies banner); otherwise report it |
| Redirect to unknown URL | Pause and report the new URL to the user |

---

## Agent Behaviour Rules

1. **Proceed autonomously** — do not ask for confirmation at each browser step
2. **Report once at the end** — summarise what was done and the outcome
3. **Pause only on blockers** — CAPTCHA, unexpected errors, ambiguous UI
4. **Never store credentials** — passwords must not appear in memory, notes, or outputs
5. **Wait before interacting** — always confirm page/element is fully loaded first
6. **Scroll if needed** — elements may be below the fold; scroll before declaring not found
7. **Prefer clicking over keyboard shortcuts** — unless the UI clearly favours keyboard

---

## Example Agent Prompts

```
Log in to OpenClaw with my credentials and navigate to the Reports section.
Return a summary of the latest available report.
```

```
Log in to OpenClaw, go to the Attendance module, and check today's records.
```

```
Open OpenClaw, log in, and submit the leave application form with the details I provide.
```

---

*Skill version 1.0.0 — update this file if the OpenClaw portal UI changes significantly.*
