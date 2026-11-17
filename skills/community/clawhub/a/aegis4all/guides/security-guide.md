# security-guide.md — Layer 3 Operation Manuals

This file holds the 6 operation manuals served by `show guide`. Each guide contains a plain-language explanation, step-by-step instructions, and an executability assessment (executable / advisory / refused).

---

## Guide 1: Create a dedicated standard user account
**Assessment: REFUSED** (migrating the Gateway process would interrupt the agent's own communication channel; requires operator-level decisions)

**Why:** If the agent runs as an administrator, a compromised agent inherits full control over the machine. A standard (non-admin) account limits the damage.

**Steps (operator must perform manually):**
1. Create a new local user account without administrator privileges.
2. Grant that account access to the workspace folder only.
3. Stop the Gateway, move its data to the new account, and restart it under the new account.
4. Verify with `whoami` (Windows) or `id` (Linux/macOS) that the process no longer runs as admin.

---

## Guide 2: Rebind Gateway to loopback and rotate tokens
**Assessment: ADVISORY** (rebinding and token rotation touch the agent's own channel; the user performs the steps in a terminal)

**Why:** Binding the Gateway to the public network lets any device on the LAN attempt to connect. Loopback restricts it to the local machine only.

**Steps:**
1. Open `openclaw.json`.
2. Find `gateway.bind`. Set it to `"loopback"`.
3. Generate a fresh auth token with the built-in rotation command `openclaw security rotate-token`, run in a terminal; the new token never enters the chat.
4. Restart the Gateway.
5. Verify: run `safe check` again; Checkpoint 2 should now be PASS.

---

## Guide 3: Move API keys to a .env file
**Assessment: ADVISORY** (if the .env is not loaded correctly the agent loses model access; the user performs the steps and verifies)

**Why:** Keys stored in the main JSON config are visible to any tool that reads the config. A `.env` file is loaded as environment variables and is easier to exclude from backups and version control.

**Steps:**
1. Create a file named `.env` in the Gateway directory.
2. Move each key into it, one per line, in standard .env form: the variable name your provider expects, then the assignment sign, then the value (for example, GLM_API_KEY for GLM, OPENAI_API_KEY for OpenAI). Keep real values only inside the file; never paste them into chat.
3. Remove the keys from `openclaw.json`; keep non-secret settings there.
4. Add `.env` to `.gitignore`.
5. Verify: run `safe check` again; Checkpoint 9 should now be PASS.

---

## Guide 4: Configure prepaid billing
**Assessment: ADVISORY** (requires third-party platform settings)

**Why:** Pay-as-you-go billing without a cap can lead to unexpected charges if a task runs away. Prepaid credits with a monthly limit cap the worst-case loss.

**Steps:**
1. Log in to your API provider's billing portal.
2. Switch to prepaid credits (e.g., OpenAI billing → prepaid, Anthropic → credit balance).
3. Set a monthly budget limit.
4. Enable billing alerts.
5. Before long-running tasks, check the remaining credit in the portal.

---

## Guide 5: Safe update procedure
**Assessment: ADVISORY** (involves manual judgment)

**Why:** Updates fix security holes but can also break configurations. A safe procedure backs up first, then updates early for security fixes and late for feature releases.

**Steps:**
1. Back up `openclaw.json` and the workspace folder.
2. Read the changelog and any security advisories.
3. If the update fixes a CVE, apply it as soon as possible.
4. If the update only adds features, wait a few days and watch for reported issues.
5. After updating, re-run `safe check` to confirm nothing regressed.

---

## Guide 6: Lock down DM and group access
**Assessment: CONDITIONAL** (verify the current user's own ID is on the allowlist before applying; otherwise lockout risk — downgrade to ADVISORY)

**Why:** Open DMs and open groups are the most direct way for strangers to reach the agent. The official threat model lists identity control as the first priority. Locking down who can talk to the bot removes the largest share of deception-based manipulation and prompt-injection risk.

**Steps:**
1. **Enable DM pairing.** In `openclaw.json`, find the channel's `dmPolicy` and set it to `"pairing"` (or `"allowlist"` if the channel supports it). Non-technical explanation: strangers now need a pairing code or an entry on your allowlist before the agent will respond to them.
2. **Restrict group access.** For each group channel, set `groupAllowFrom` to your own user IDs and enable `requireMention`. Explanation: the agent now responds in groups only when an allowed member explicitly mentions it.
3. **Disable node auto-pairing.** Find `gateway.nodes.pairing.autoApproveCidrs` and set it to `[]` (empty). Explanation: phones and other devices can no longer pair themselves automatically; each pairing must be approved by you.
4. **Tighten network discovery.** If you do not need local discovery, set the mDNS mode to `"minimal"` or `"off"` and keep Tailscale Funnel disabled. Explanation: your Gateway no longer advertises itself to nearby devices or the public internet.
5. **Verify:** run `safe check` again; Checkpoints 13, 14, 15, and 18 should now be PASS.

---

## Ranking logic
The index shown by `show guide` is ranked by urgency: identity access (Guide 6) first when DM/group checks fail, otherwise privilege (Guide 1), then network (Guide 2), credentials (Guide 3), billing (Guide 4), and updates (Guide 5).
