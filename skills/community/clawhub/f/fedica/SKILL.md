---
name: fedica
version: 1.0.0
description: Compose and schedule cross-platform social posts on Fedica (X, LinkedIn, Threads, Mastodon, Bluesky) via agent-browser. Handles login, image upload, scheduling, character limits, and Fedica's UTC-only time display.
metadata: {"openclaw":{"emoji":"📣","requires":{"commands":["agent-browser"]}}}
---

# Fedica Skill

[Fedica](https://fedica.com) is a cross-platform social scheduler that publishes to **X, LinkedIn, Threads, Mastodon, Bluesky** (and more) from one compose box. This skill drives it through `agent-browser`.

## Prerequisites

- `agent-browser` installed (`npm i -g agent-browser`)
- A Fedica account with at least one platform connected
- Credentials available to you (this skill does not manage secrets — load your own from your password manager, `pass`, `op`, env vars, `~/.secrets/...`, etc.)

## Safety

Fedica is public broadcast. **Never publish or schedule without explicit user confirmation on:**

- final post text
- target platforms (checkboxes in the composer)
- scheduled local time (Fedica shows UTC — convert before confirming)

Treat every `Post Now` / `Add to Calendar` / `Update` click like an email you cannot unsend.

---

## Key gotchas

| Gotcha | Rule |
|---|---|
| **Timezone** | Fedica displays **everything in GMT+00 (UTC)** regardless of browser or user TZ. Convert to the user's local TZ before confirming a schedule. Example: 07:00 UTC = 09:00 Europe/Paris (CEST, summer) or 08:00 Europe/Paris (CET, winter). |
| **Bluesky limit** | **300 graphemes max**. Almost always the binding constraint — design around it first. |
| **Threads / Mastodon** | 500 chars each. X and LinkedIn much more generous. |
| **Character counter** | Bottom right of composer shows `NNN / 300` (always anchored to Bluesky's 300). If the text exceeds a platform's limit, clicking `Schedule` pops an error listing which platforms fail. |
| **Custom Posts tab** | Allows per-platform versions (long LinkedIn + short Bluesky). Use when trimming to 300 kills the message. |
| **Image upload** | The visible camera icon only opens a hidden input that Fedica will not react to on direct upload. You must open the modal first: `openTweetBoxAttachmentUploadModal(1)`. The modal's input is `#imageUploader1` (note the trailing `1`). |
| **Schedule button** | It is a split button. The primary `Schedule` label alone does not open the modal. The dropdown entry `#openScheduleButton` (labelled "Specific date") is what opens the "When to publish?" modal. |
| **Date picker** | Web component `<calendar-date>` containing `<calendar-month>` whose day buttons live in a **shadow DOM**. Reach them via `document.querySelector('calendar-month').shadowRoot.querySelector('button[aria-label="April 20"]')`. |
| **Chrome extension nag** | A dialog "Fedica Browser extension" pops up on the Calendar page. Close with its X button, or use the "Don't remind me again" link, or `Escape`. |
| **Headless browser sandbox** | In a headless/server environment the first `agent-browser` call needs `--args "--no-sandbox"` (or equivalent). |

---

## Fast workflow (happy path)

```bash
# 1. Launch session (first call of the session may need --no-sandbox on servers)
agent-browser --args "--no-sandbox" open "https://fedica.com/dash/"

# 2. Log in if not already authenticated
#    Dashboard shows a "Log in" button in the top-right if you are logged out.
#    Use your own credential source; this skill does not fetch or store passwords.
#    Fedica routes to account.fedica.com/oauth2/... (Azure-B2C-style form).

# 3. Open composer
agent-browser open "https://fedica.com/publish/"

# 4. Verify which networks are checked (snapshot shows them as checkboxes)
agent-browser snapshot 2>&1 | grep -i "checkbox.*-"
# Uncheck any you do not want to target:
#   agent-browser click @<ref-of-checkbox>

# 5. Type the post
COMPOSE_REF=$(agent-browser snapshot 2>&1 | grep -oP 'textbox "Compose your post or thread" \[ref=\K[^\]]+')
agent-browser click @$COMPOSE_REF
agent-browser keyboard type "$(cat /tmp/post.txt)"

# 6. Attach image (skip if text-only)
agent-browser eval "openTweetBoxAttachmentUploadModal(1)"
sleep 1
agent-browser upload "#imageUploader1" "/absolute/path/to/image.png"
sleep 3  # let Fedica finish the upload

# 7. Open the When-to-publish modal
agent-browser eval "document.querySelector('#openScheduleButton').click()"
sleep 2

# 8. Pick the date (shadow DOM web component)
#    Replace "April 20" with the target month + day (e.g. "May 3")
agent-browser eval "
  const sr = document.querySelector('calendar-month').shadowRoot;
  sr.querySelector('button[aria-label=\"April 20\"]').click();
"

# 9. Switch from Optimized → Exact Time, then set the time
#    (find the Exact Time radio ref via snapshot, then click it)
EXACT_REF=$(agent-browser snapshot 2>&1 | grep -B1 '"Exact Time"' | grep -oP 'ref=\K[^\]]+' | head -1)
agent-browser click @$EXACT_REF

# Time in UTC (Fedica shows/accepts GMT+00). Convert from local TZ first!
agent-browser eval "
  const t = document.querySelector('#scheduleTimeControl');
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
  setter.call(t, '07:00');
  t.dispatchEvent(new Event('change', {bubbles:true}));
"

# 10. Confirm with the primary button in the modal
#     New post  → "Add to Calendar"
#     Edit mode → "Update"
CONFIRM_REF=$(agent-browser snapshot 2>&1 | grep -B1 -E 'Add to Calendar|Update' | grep -oP 'ref=\K[^\]]+' | head -1)
agent-browser click @$CONFIRM_REF
```

---

## Verify a scheduled post

```bash
agent-browser open "https://fedica.com/schedule/"
# Close the Chrome-extension nag dialog if it appears
agent-browser press Escape

# Click a post from the calendar to get its preview modal
agent-browser find text "<snippet from the post>" click

# Preview header shows: "YYYY Mon DD HH:MM AM/PM" in GMT+00
# Post ID appears in the onclick handlers: editPost(<ID>) and delPost(<ID>, ...)
```

**Always re-verify the displayed time after scheduling.** Subtract or add the UTC offset to get the user's local time, and restate that local time to them.

---

## Editing / rescheduling

```bash
# From the preview popup, the pencil icon fires: editPost(<postId>)
agent-browser eval "editPost(<postId>)"

# Opens composer with existing content and the scheduled date/time visible
# Click the "Schedule" button next to the date to re-open the When-to-publish modal
# Change date/time → click "Update" (not "Add to Calendar" in edit mode)
```

---

## Composing for 5 platforms in one shot

Plan around the **Bluesky 300-grapheme** ceiling from the start. Techniques:

- Drop narrative intros — lead with the brand or headline
- Drop parenthetical qualifiers like "(no strings attached)"
- Remove redundant CTAs ("If you're building in this space…")
- 1 emoji per bullet + 1 CTA link is usually enough
- Em-dash (`—`) instead of "such as", "including", etc.

If the message needs the full long form, switch to the **Custom Posts** tab in the composer. Each platform then gets its own text field — full long version for LinkedIn/X, short teaser + link for Bluesky/Threads/Mastodon.

---

## Character counting

Fedica counts graphemes, and its live `NNN / 300` counter is authoritative. For an offline estimate, Python codepoint count is close but undercounts some emoji (e.g. `🏛️` = two codepoints):

```python
s = open('/tmp/post.txt').read()
print('codepoints:', len(s))
# For accurate grapheme count:
#   pip install grapheme
#   import grapheme; print(grapheme.length(s))
```

When you are close to the 300 limit, paste into the composer and read the live counter.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Login redirects to `account.fedica.com/oauth2/...` | Normal OAuth handoff; fill the password on the Azure-B2C-style form that appears. |
| `upload` command fails with a CDP error | The file input element ID differs: `#imageUploader` (page-level, not wired up) vs `#imageUploader1` (inside the modal). Open the modal first with `openTweetBoxAttachmentUploadModal(1)` and use the modal input. |
| Date picker does not react to clicks | It is a shadow-DOM web component. Use `document.querySelector('calendar-month').shadowRoot` to reach the buttons. |
| `Post cannot be longer than N characters` popup | The error lists the offending platforms. Either trim to the lowest limit, or switch to Custom Posts. |
| Scheduled time is off by 1–2 hours | Fedica is in GMT+00. Adjust for the user's current offset (e.g. CEST = UTC+2, CET = UTC+1, EDT = UTC−4, EST = UTC−5). |
| "Fedica Browser extension" dialog blocks the calendar page | Close with the X or the "Don't remind me again" link. |

---

## Sensible defaults

When the user does not specify, propose and **then confirm**:

- Time: **09:00 local** on the next weekday (good slot for pro-network engagement). Convert to UTC before entering it into Fedica.
- Platforms: **all connected** (leave every checkbox checked).
- Visibility: default public on each platform (Fedica does not add visibility controls per post).

Do not assume — always restate the final plan (text preview, platforms list, local-time schedule) and wait for explicit go before clicking the confirm button.

---

## Fedica endpoints

- Dashboard: `https://fedica.com/dash/`
- Compose: `https://fedica.com/publish/`
- Scheduled queue: `https://fedica.com/schedule/`
- Drafts: `https://fedica.com/publish/drafts/`
- Media library: `https://fedica.com/publish/media/`

Post IDs are numeric integers. They appear in the `editPost(...)`, `delPost(...)`, and calendar-preview popup onclick handlers.
