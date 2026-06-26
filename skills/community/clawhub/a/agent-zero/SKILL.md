---
name: agent-zero
description: Interact with the AgentZero real estate listing tracker (local Rust/Axum backend at http://localhost:8000). Use when asked to add a property listing by URL, refresh an existing listing, or list search profiles/scenarios. AgentZero parses Redfin and REW.ca URLs; Zillow and Realtor.ca are blocked (saves stub only). When a listing is added via agent-suggest, the backend automatically triages it with Claude (assigns a search profile or skips it) — no manual profile selection needed. The Daily Email Scan workflow reads Redfin alert emails via himalaya (IMAP) and opens Gmail in the openclaw browser to extract listing URLs — explicit user consent and himalaya configuration are required before use. After any action, log a summary to agent_zero_logs/YYYY-MM-DD.md in the workspace.
metadata:
  openclaw:
    requires:
      bins:
        - himalaya
        - openclaw
        - cargo
        - node
        - npm
        - sqlite3
      localServices:
        - name: AgentZero backend
          url: "http://localhost:8000"
          note: "Rust/Axum server — must be running before invoking any listing API workflows"
        - name: AgentZero frontend (optional)
          url: "http://localhost:5173"
          note: "Vite/TypeScript UI — optional, used for reviewing listings"
    credentials:
      - name: ANTHROPIC_API_KEY
        description: >
          Required for the backend's automatic listing triage. When a listing is added via agent-suggest,
          the backend calls the Anthropic Claude API (claude-haiku-4-5) to match it against search profiles.
          Set this environment variable before starting the backend — it will fail to start without it.
          Obtain your key at https://console.anthropic.com.
        envVar: ANTHROPIC_API_KEY
        keychain: false
      - name: himalaya Gmail config
        description: >
          himalaya must be configured with an IMAP/SMTP account pointing to the user's Gmail inbox.
          The app password or OAuth token must be stored in the system keychain or himalaya config file.
          Without this, the Daily Email Scan workflow will fail.
        configPath: "~/.config/himalaya/config.toml"
        keychain: true
    privacy:
      emailAccess: true
      browserAutomation: true
      note: >
        The Daily Email Scan workflow is explicitly opt-in (user-triggered via cron or manual invocation)
        and is scoped to Redfin sender emails only (from:redfin.com).

        Email access: himalaya reads envelope metadata only (sender, subject, ID) via IMAP — no email
        body text is read or stored. The only data logged is the listing URLs extracted from Redfin
        emails and the processed email IDs (to avoid re-processing).

        Browser automation: the openclaw browser is used exclusively to open Redfin listing URLs
        (redfin.ca / redfin.com) — it does NOT browse Gmail or any other site. Gmail is only opened
        briefly to search for and click through to the Redfin listing link; no Gmail session data,
        cookies, or body content is recorded.

        HTML snapshots (backend/html_snapshots/): these are snapshots of Redfin property listing pages
        only — not Gmail or any user account pages. They are cached locally by the backend to avoid
        re-fetching listing data. No session tokens or authentication artifacts are stored in these files.

        Local scripts: scripts/run_backend.sh builds and starts the Rust/Axum backend (cargo build +
        ./target/release/backend). scripts/run_frontend.sh runs `npm install && npm run dev` for the
        Vite frontend. Both scripts are included in full in this repository and can be reviewed before
        execution. They do not make outbound network calls beyond fetching Rust crates (cargo) and
        npm packages on first build.
    writes:
      - "~/.openclaw/<WORKSPACE>/skills/agent-zero/agent_zero_claw_logs/YYYY-MM-DD.md"
      - "~/.openclaw/<WORKSPACE>/skills/agent-zero/agent_zero_claw_logs/processed_emails.json"
      - "<project>/backend/listings.db"
      - "<project>/backend/html_snapshots/"
      - "/tmp/agent_zero_backend.log"
    install:
      - type: shell
        label: "Build and start Rust backend"
        script: "./scripts/run_backend.sh"
        note: "Requires Rust/Cargo toolchain. Builds the Axum backend and starts it at http://localhost:8000."
      - type: shell
        label: "Build and start TypeScript frontend (optional)"
        script: "./scripts/run_frontend.sh"
        note: "Requires Node/npm. Starts the Vite UI at http://localhost:5173."
---

# AgentZero Skill

AgentZero is a personal real estate listing tracker. Backend at `http://localhost:8000`.

## Prerequisites

Before using this skill, ensure the following are in place:

| Requirement | Details |
|---|---|
| **AgentZero backend** | Must be running at `http://localhost:8000` (Rust/Axum). Start with `./scripts/run_backend.sh` in the project directory. |
| **ANTHROPIC_API_KEY** | Required for automatic listing triage. Set in your environment before starting the backend. Get your key at console.anthropic.com. |
| **himalaya** | CLI email client — must be installed (`brew install himalaya` or similar) and configured with your Gmail account via IMAP. Config at `~/.config/himalaya/config.toml`. |
| **himalaya credentials** | Gmail app password or OAuth token stored in keychain. Required for the Daily Email Scan workflow. |
| **openclaw browser** | Used by the Daily Email Scan to open Gmail and click listing links. Start with `openclaw browser --browser-profile openclaw start`. |
| **AgentZero frontend** *(optional)* | Vite UI at `http://localhost:5173` for reviewing listings. Start with `./scripts/run_frontend.sh`. |

### Privacy & Email Access

The **Daily Email Scan** workflow accesses your Gmail inbox. Specifically it:
- Reads envelope metadata (subject, sender, ID) of Redfin alert emails via `himalaya envelope list`
- Opens Gmail in the openclaw browser to click through listing links (no email body text is read or stored)
- Records processed email IDs and listing URLs in `~/.openclaw/<WORKSPACE>/skills/agent-zero/agent_zero_claw_logs/`

The scan only runs when explicitly triggered (cron or manual) and is scoped to `from:redfin.com` emails only. 

---

## Key APIs

| Action | Method | Endpoint | Body / Params |
|---|---|---|---|
| Add listing (AI) | POST | `/api/listings/agent-suggest` | `{"url": "..."}` |
| List all listings | GET | `/api/listings` | `?status=...` |
| Get single listing | GET | `/api/listings/:id` | — |

Responses are JSON `Property` objects (see field list below).

## Workflow: Add a Listing by URL

1. **POST** `/api/listings/agent-suggest` with `{"url": "<url>"}`.
2. On `409 CONFLICT` response: the listing already exists. Parse the JSON body for `existing_id` and `existing_title` and report to user.
3. On success: the listing is saved as `AgentPending`. The backend agent will further review i.
4. Log a summary to the daily notes file (see Logging section).

## Logging — agent_zero_claw_logs/

After every action (add, refresh, skip), append a summary to:

```
~/.openclaw/<WORKSPACE>/skills/agent-zero/agent_zero_claw_logs/YYYY-MM-DD.md
```

Here `<WORKSPACE>` is the name of your OpenClaw workspace for the specific agent; it can be `workspace` if it is the default agent; or `workspace` followed by the agent name.

Create the folder and file if they don't exist.

**Format:**
```markdown
## HH:MM — Added listing #38
- **Email:** https://mail.google.com/mail/u/0/#inbox/<thread_id>
- **Title:** 7778 Nanaimo St, Vancouver - 6 beds/3.5 baths
- **URL:** https://www.redfin.ca/...
- **Price:** $2,198,000
- **Status:** AgentPending (agent review running in background)

## HH:MM — Skipped listing
- **Email:** https://mail.google.com/mail/u/0/#inbox/<thread_id>
- **URL:** https://...
- **Reason:** No search profile matches — listing is in Burnaby, all profiles target Vancouver.
```

The `thread_id` is the hex ID visible in the Gmail URL after opening the email in the browser.

## Workflow: Daily Email Scan (Cron)

This is the workflow for the scheduled daily cron task.

> **Requires:** himalaya configured with Gmail + openclaw browser running. See Prerequisites above.

### Step-by-step

1. **Notify your user** (via whatever messaging channel is configured): "🏠 AgentZero daily scan starting — checking Redfin emails..."

2. **Write scan-start entry** to `~/.openclaw/<WORKSPACE>/skills/agent-zero/agent_zero_claw_logs/YYYY-MM-DD.md` immediately (create file/folder if needed):
   ```markdown
   ## HH:MM — Scan started
   - Checking Redfin emails...
   ```

3. **Load state file** `~/.openclaw/<WORKSPACE>/skills/agent-zero/agent_zero_claw_logs/processed_emails.json`
   - If missing, treat as `{"processed_ids": [], "date_counts": {}}`
   - Format: `{"processed_ids": ["57471", ...], "date_counts": {"2026-03-09": 2}}`
   - `processed_ids` are himalaya envelope IDs (sequential integers) — used to avoid re-processing emails already handled in previous scans
   - **Append to log:**
     ```markdown
     ## HH:MM — Loaded state
     - Already processed IDs: 57471, 57457
     - Processed today: 1
     ```

4. **Check daily limit:** count how many emails were processed today (from `date_counts[today]`). If ≥ 3, append to log and notify your user:
   ```markdown
   ## HH:MM — Skipped scan
   - Reason: Daily limit (3) already reached.
   ```

5. **List emails** via himalaya:
   ```bash
   himalaya envelope list --output json 2>/dev/null
   ```
   Filter to emails where `from.addr` contains `redfin.com` and ID is NOT in `processed_ids`. Take up to `3 - already_processed_today`.

   **Append to log immediately:**
   ```markdown
   ## HH:MM — Found N new Redfin email(s)
   - Email IDs: 57493, 57490
   - Already processed today: 1 (limit: 3)
   ```

6. **For each email:**

   a. **Append to log before opening:**
      ```markdown
      ## HH:MM — Processing email <id>: "<subject>"
      - Opening in Gmail...
      ```

   b. Open the email in Gmail via browser (run `openclaw browser --browser-profile openclaw start` if not already running):
      - Navigate to Gmail and search using the subject and sender from the himalaya envelope (e.g. `from:listings@redfin.com subject:"<subject from step 5>"`)
      - Click the matching email to open it

   c. For each listing link visible in the email body:
      - **Skip** "Go tour it", "Tour home", "Schedule a Tour", and "View all saved open houses" links — these go to booking pages, not listings
      - **Skip** full address links (e.g. "930 Cambie St, Vancouver, BC, V6B 5X6") — these go to Google Maps
      - **Click** the short property name links (e.g. "7778 Nanaimo St" or "2094 E 7th Ave") — these are the actual Redfin listing links
      - Read the final URL from the new tab (e.g. `https://www.redfin.ca/bc/vancouver/.../home/200788210`)
      - Close the tab
      - **⚠️ Never construct or guess URLs.** Only use URLs extracted directly by clicking through the email. Do not derive URLs from propertyId params or address strings.
      - **Append to log before submitting:**
        ```markdown
        - Found listing URL: https://www.redfin.ca/...
        - Submitting to AgentZero...
        ```
      - Submit via **Add Listing** workflow above (no profile selection needed — agent assigns it)
      - **Append result to log immediately after each listing** (success, skip, or 409)

   d. **Mark email as processed:**
      - Update `processed_ids` in state file with this email ID
      - Increment `date_counts[today]`
      - Add `agent_zero` label in Gmail via himalaya:
        ```bash
        himalaya message copy <email_id> "agent_zero"
        ```
      - **Append to log:**
        ```markdown
        - Email <id> marked as processed.
        ```

7. **Append final summary** to log:
   ```markdown
   ## HH:MM — Scan complete
   - Processed N emails, added M listings (K skipped).
   ```

8. **Notify your user** with summary and a prompt to review new listings in the frontend:
   ```
   ✅ AgentZero scan complete — processed 2 emails, added 3 listings (agent review running in background).

   🏡 New listings will appear in Review once the agent finishes: http://localhost:5173/inbox
   ```

### State file location

`~/.openclaw/<WORKSPACE>/skills/agent-zero/agent_zero_claw_logs/processed_emails.json`
