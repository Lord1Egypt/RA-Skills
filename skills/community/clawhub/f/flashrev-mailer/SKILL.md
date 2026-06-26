---
name: flashrev-mailer
description: Use this skill when an AI agent needs to plan, build, commit, monitor, or follow up on FlashRev-powered email outreach via the flashrev-mailer npm CLI (v2.0+). Triggers on requests involving cold email, outreach campaigns, multi-step follow-up sequences, AI auto-reply, prospect reply triage, or mailbox-pool drip sending. The CLI delegates send timing and reply tracking to the FlashRev backend sequence engine; live sends require explicit per-batch user approval; AI auto-reply prompts must be shown verbatim and approved before enabling. Agents should invoke with FLASHREV_MAILER_AI_MODE=1 (or --ai-mode) so all list/view outputs and errors are JSON-structured.
---

# FlashRev AI Mailer (v2.0.1)

Use the `flashrev-mailer` CLI to build personalized email sequences with
FlashRev mailbox pools, multi-step follow-up, event tracking (open/click/reply),
and optional LLM auto-reply. v2 delegates send timing and reply tracking to
the FlashRev backend; the CLI orchestrates building, commit, and inspection.

## Security posture

This skill creates and runs outbound email campaigns. The following
constraints apply to every workflow and are non-negotiable:

- **API key** lives only in the operator's shell environment
  (`FLASHREV_API_KEY` or the name set via `flashrev.apiKeyEnv`). It is never
  written to `.flashrev/config.json`, campaign exports, send logs, or chat
  output.
- **Live sending requires explicit human approval per batch.** The agent must
  run `--dry-run --yes` first, show rendered drafts and the destination
  mailbox to the user, and only proceed with `--live --yes` after the user
  approves drafts, schedule, and recipient set. The agent never auto-escalates
  batch size, never auto-resumes after pause without confirmation.
- **`ai-auto-reply enable` is high-risk.** Once enabled, the LLM will reply to
  prospects on the user's behalf using the saved prompt. The agent must:
  1. Show the full prompt verbatim to the user before calling `enable`
  2. Never write or modify the prompt without the user's explicit text
  3. Default to `disable` if there is any ambiguity
- **`pause` / `resume`** change production state. Confirm with the user before
  running either.
- **`reply --mail-id <ID>`** sends a real email to a prospect. Show the user
  the prospect's identity (from `inbox`) + the proposed reply body before
  sending.
- **`reschedule`** changes when emails go out. Confirm new window with user.
- **`send --live --send-now`** bypasses the working-time-window (sends step 1
  immediately, may include weekends or off-hours). Confirm with user before
  using.
- **`delete`** is irreversible. Even with `--yes`, list what will be deleted
  (local path + sequenceId + contact/step counts) in chat and get explicit
  confirmation from the user. Already-sent emails are not recalled.
- **Recipient gating**: only `emailSyntaxValid=true` contacts are committed.
  `send --live` triggers backend deliverability check automatically (dispatch-svc
  EmailVerifyService); undeliverable contacts are flagged errorContacts and skipped.
  `validate` is optional and only useful as a pre-commit preview for cold lists.
- **Failure mode is stop-and-ask**, not retry-with-different-input. If a
  prerequisite or confirmation is missing, halt the workflow and surface the
  gap to the user.

## Agent invocation convention

Agents calling this CLI should set **either**:

- Environment variable: `FLASHREV_MAILER_AI_MODE=1` (recommended; once per shell)
- Per-call flag: `--ai-mode` on every invocation

When enabled, the CLI **forces JSON output** on `list / outbox / inbox /
status / mailboxes / ai-auto-reply show / export` AND **wraps errors in JSON**
to stderr:

```json
{ "error": { "code": "...", "message": "...", "remediation": "..." } }
```

Without ai-mode, output is human-formatted tables — fine for users at a
terminal, fragile for agents to parse.

## Prerequisites

These must be set up by the **human operator**. The agent's role is to
**verify** each one and **guide the user** to fix anything missing — never
attempt to install software, generate API keys, or modify the shell
environment unattended.

- **Node.js ≥ 20** is on `PATH`.
- **CLI is installed globally**: `npm install -g flashrev-ai-mailer`. Verify
  with `flashrev-mailer --help`. Confirm version 2.x:
  `flashrev-mailer --help 2>&1 | head -1` should not look like the v1 single-shot CLI.
- **FlashRev API key** generated at
  https://info.flashlabs.ai/settings/privateApps and exported as
  `export FLASHREV_API_KEY="..."`. Persist in `~/.zshrc` or `~/.bashrc` per
  user preference. Never persist inside any config file.
- **Base URL initialized** once per workspace:
  `flashrev-mailer init --base-url "https://open-ai-api.flashlabs.ai"` (or
  the test/staging URL provided by your FlashRev team).
- **Outbound network access** to the FlashRev API host.
- **Workspace is writable** — campaign state and inbox cache live under the
  current working directory at `.flashrev/`.

Always run `flashrev-mailer doctor --check-api` before the first command.
This verifies endpoints AND triggers backend lazy-init of a default schedule
("Default Business Hours") for new accounts. If a check fails, **stop the
workflow, tell the user the exact missing prerequisite, and wait** — do not
proceed to `import` / `send` until the user reports it resolved.

## Required confirmations

Each item below is a business decision the agent must explicitly align with
the user before proceeding — do not assume defaults:

- Contact source approved (CSV, TSV, public CSV URL, Google Sheets export,
  Clay export).
- The email column and personalization variables are understood. Personalization
  uses `{{ FirstName }}` / `{{ LastName }}` / `{{ Company }}` / `{{ Title }}`
  syntax (displayProperty names from the FlashRev contact property whitelist).
- Campaign goal, offer, tone, sender identity, call-to-action approved.
- For multi-step follow-up: each step's content, `--delay-days`, and whether
  it's a reply (same thread, no subject) or a new thread are confirmed.
- Sending schedule (timezone + window + weekdays + holidays-skip policy)
  approved.
- **AI auto-reply prompt** (if used) approved verbatim. Show the full prompt
  text to the user before `ai-auto-reply enable`. The prompt is ≤ 2000 chars.
- User has reviewed drafts (`--dry-run`) and explicitly approved committing
  (`--live`).

## Workflow A — Single-step campaign (v1 style, still works)

```bash
flashrev-mailer doctor --check-api
flashrev-mailer mailboxes                                     # pick an addressId
flashrev-mailer import --campaign CAMPAIGN_ID --source contacts.csv
flashrev-mailer validate --campaign CAMPAIGN_ID --limit 200   # optional (backend auto-checks on send --live)
flashrev-mailer draft  --campaign CAMPAIGN_ID \
    --subject "Quick idea for {{ Company }}" \
    --body    "Hi {{ FirstName }}, ..."
flashrev-mailer send   --campaign CAMPAIGN_ID --dry-run --yes --mailbox ADDR_ID  # SHOW USER
# After user approves drafts:
flashrev-mailer send   --campaign CAMPAIGN_ID --live --yes --mailbox ADDR_ID
flashrev-mailer status --campaign CAMPAIGN_ID
```

The agent shows the user the dry-run table and waits for explicit "yes,
send" before `--live`.

## Workflow B — Multi-step follow-up

```bash
flashrev-mailer import --campaign CAMPAIGN_ID --source contacts.csv

# Step 1 (new thread)
flashrev-mailer draft --campaign CAMPAIGN_ID \
    --subject "Hi {{ FirstName }}" --body "..."

# Step 2 (3-day follow-up, same thread, no subject — backend uses "Re: ...")
flashrev-mailer draft --campaign CAMPAIGN_ID --step 2 --delay-days 3 \
    --reply-to 1 --body "Just following up..."

# Optionally step 3 etc — use --step N --delay-days N --reply-to <prev>
flashrev-mailer send  --campaign CAMPAIGN_ID --dry-run --yes --mailbox ADDR_ID
# User approves drafts + delay structure:
flashrev-mailer send  --campaign CAMPAIGN_ID --live --yes --mailbox ADDR_ID
flashrev-mailer status --campaign CAMPAIGN_ID
```

**Rules the agent must enforce when building follow-up:**
- `--reply-to N` requires step N to already exist; if not, draft step N first.
- `--reply-to N` rejects `--subject` (backend auto-sets `Re: <step N subject>`).
- Confirm with user: "step 2 will be sent N days after step 1 unless the
  prospect replies first — is that what you want?"

## Workflow C — AI auto-reply

LLM-driven replies trigger when prospects respond, using the prompt the user
provides. **Independent** from `prospectRepliesEnabled` (which stops the
sequence on reply). The two can be combined.

```bash
# At commit time (all params on the send command):
flashrev-mailer send --campaign CAMPAIGN_ID --live --yes --mailbox ADDR_ID \
    --ai-auto-reply --ai-auto-reply-prompt "You are a friendly SDR..."

# Or after commit (REQUIRES TWO-STEP FLOW — see below):
# Step 1: probe — show the prompt to the user (CLI prints to stderr, then errors out)
flashrev-mailer ai-auto-reply enable  --campaign CAMPAIGN_ID --prompt "..."
# → CLI prints the full prompt to stderr + a warning + errors out

# Step 2: confirm — user has reviewed and approved; agent adds --yes
flashrev-mailer ai-auto-reply enable  --campaign CAMPAIGN_ID --prompt "..." --yes

flashrev-mailer ai-auto-reply show    --campaign CAMPAIGN_ID
flashrev-mailer ai-auto-reply disable --campaign CAMPAIGN_ID --yes  # prompt preserved; --yes required
flashrev-mailer ai-auto-reply enable  --campaign CAMPAIGN_ID --yes   # reuses prompt; --yes still required
```

**Mandatory two-step flow for `enable`** (CLI-enforced, not just a guideline):

1. **Probe step**: agent runs `enable ... --prompt "..."` **without `--yes`**.
   CLI will print the full prompt + warning to stderr and error out.
2. **Show stderr output to the user verbatim**, get explicit "yes I approve this prompt".
3. **Confirm step**: agent re-runs `enable ... --prompt "..." --yes`.

**Hard agent rules:**
- Never invoke `ai-auto-reply enable ... --yes` in a single call without first
  showing the user the probe-step output. The CLI's two-step flow exists so this
  cannot happen silently.
- Never paraphrase or auto-generate prompts. The user supplies the exact text.
- If the user asks "make a prompt for me", help them draft it conversationally,
  but only call `enable` after they confirm the final text.
- `disable` also requires `--yes` (changes production sequence behavior).

## Workflow D — Triage replies, reply directly

After `send --live`, replies will arrive over hours/days. The agent helps the
user triage:

```bash
flashrev-mailer inbox --campaign CAMPAIGN_ID                  # see all replies
flashrev-mailer inbox --campaign CAMPAIGN_ID --sentiment positive  # only positives
flashrev-mailer inbox --campaign CAMPAIGN_ID --intent Interested

# To reply to a specific message:
flashrev-mailer reply --mail-id <MAIL_ID> --body "Thanks {{...}}"
# (MAIL_ID is the first column of `inbox` output)

# Mark as read without replying:
flashrev-mailer inbox --mark-read <MAIL_ID>

# View full event timeline for a sent message:
flashrev-mailer outbox --view <MAIL_ID>
```

**`reply` rules:**
- Show the user the inbox row first (from / snippet / sentiment / intent).
- Show the user the proposed reply body and wait for "yes".
- `reply` sends to the prospect's email (preserves thread).

## Workflow E — Operational control

```bash
flashrev-mailer pause   --campaign CAMPAIGN_ID    # stop future steps
flashrev-mailer resume  --campaign CAMPAIGN_ID    # resume

flashrev-mailer list                              # all local campaigns
flashrev-mailer list --remote                     # also pull backend sources=ai_mailer

flashrev-mailer steps list   --campaign CAMPAIGN_ID           # view current step list
flashrev-mailer steps remove --campaign CAMPAIGN_ID --step N  # delete step N (effective at next send --live)

flashrev-mailer reschedule --campaign CAMPAIGN_ID \
    --send-start 09:00 --send-end 18:00 --weekdays mon-fri \
    --timezone "America/New_York"   # or numeric id: --timezone 22

# Add contacts to existing campaign (default append; --overwrite to clear entire campaign)
flashrev-mailer import --campaign CAMPAIGN_ID --source new-contacts.csv
flashrev-mailer send   --campaign CAMPAIGN_ID --live --yes

# Delete a campaign (irreversible, --yes required)
flashrev-mailer delete --campaign CAMPAIGN_ID --yes                  # default: local + backend
flashrev-mailer delete --campaign CAMPAIGN_ID --keep-local --yes     # backend only
flashrev-mailer delete --campaign CAMPAIGN_ID --keep-remote --yes    # local only
```

`reschedule` creates a private schedule and applies it; existing schedules
referenced by other sequences are not touched.

`steps remove` takes effect on the next `send --live` via sequence/edit's
full-replace semantics — already-sent emails are not recalled; contacts on
the deleted step auto-shift to the next step.

### Scheduling timezone (default behavior)

If `--timezone` is omitted, the CLI resolves in this order:

1. **Your FlashRev profile's `timezoneId`** (auto-fetched from
   `GET /engage/api/v1/user/setting/profile`, cached 24h at
   `.flashrev/profile-cache.json`)
2. **Fallback `id=22 America/New_York`** (when profile is unreachable)

`--timezone` accepts two formats:
- Numeric id (recommended for scripts, e.g. `--timezone 22`) — from the `id`
  field of `GET /engage/api/v1/timezone/list`
- IANA zoneId string (recommended for humans, e.g. `--timezone "Europe/London"`)
  — CLI looks it up in the list and resolves to the corresponding id

Invalid values (not in timezone-list) are rejected at `send --live` with
candidate examples in the error message.

CLI-managed fixed schedules are named by timezone slug
(`cli-anytime-<tz-slug>` / `cli-default-<tz-slug>`); different timezones do
not share the same schedule.

## Commands the agent runs vs. commands requiring confirmation

**Read-only (agent may run freely):**
- `init`, `doctor`, `doctor --check-api`
- `mailboxes`, `validate`
- `import` (local-only), `draft` (local-only)
- `status`, `list`, `list --remote`
- `outbox`, `outbox --view`
- `inbox`, `inbox --view`
- `ai-auto-reply show`
- `export`

**Requires explicit user "yes" per call:**
- `send --dry-run --yes`
- `send --live --yes` ← never auto-escalate
- `send --live --send-now` (extra confirm: "this bypasses the working-time window")
- `pause`, `resume`
- `reply --mail-id <ID>`
- `ai-auto-reply enable` (show prompt verbatim first)
- `ai-auto-reply disable`
- `reschedule`
- `inbox --mark-read`
- `steps remove` (mutates campaign structure)
- `delete --yes` (irreversible; list contents in chat first and re-confirm)

## Notes on backend semantics worth telling the user

- `sources="ai_mailer"` is auto-tagged by the CLI so `list --remote` only shows
  what the CLI created. The user's own web-created sequences are filtered out.
- After `send --live`, the campaign appears in the FlashRev web UI sequence
  list. Editing it there will not break the CLI, but the CLI re-commits go
  through a Full-Replace edit — show user the diff first if they've modified
  the sequence in the web UI.
- `--send-now` makes step 1 fire immediately (skips delay + working-time
  window + holiday calendar). Later steps follow their normal `--delay-days`.
- Prospect replies stop the sequence (default `prospectRepliesEnabled=1`).
  If `ai-auto-reply enable` is on, the LLM will first send an auto-reply,
  *then* the sequence stops further outgoing steps for that contact.

## Failure recovery

- `send --live` failed midway: re-run; the CLI's edit-path detects the
  existing `sequenceId` and merges; no duplicate emails.
- Unknown error from backend (`code: 400, msg: "Unknown error !"`): the
  backend swallowed the real error. Check `.flashrev/campaigns/<id>/campaign.json`
  → `steps[]` for missing fields (see `references/api_contract.md` for the
  full required-field list).
- `list` shows a campaign but `outbox/inbox` returns 0: the sequence was
  paused or deleted server-side. Run `status` to confirm.

For full request/response shapes, paths, and known field traps, see
[references/api_contract.md](references/api_contract.md).
