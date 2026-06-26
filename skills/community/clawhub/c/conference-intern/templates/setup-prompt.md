# Conference Intern — Setup

You are setting up a new conference for the Conference Intern skill. Walk the user through the following questions one at a time. After collecting all answers, generate and save `config.json`.

## Questions

Ask these in order. Use the user's answers to build the config.

1. **Conference name** — "What conference are you attending?" (e.g., "EthDenver 2026")
   - Generate a slug ID from the name (e.g., "ethdenver-2026")

2. **Luma URLs** — "Share the Luma page URLs where side events are listed (one per line, or comma-separated)"
   - These are typically calendar pages or event listing pages on lu.ma
   - Validate: must start with https://lu.ma/ or https://luma.com/

3. **Google Sheet links** — "Any Google Sheets with curated event lists? (paste URLs, or 'none')"
   - These are community-curated lists often shared on Telegram/Twitter before conferences
   - Optional — user can skip

4. **Interest topics** — "What topics are you interested in? (comma-separated)"
   - e.g., "DeFi, ZK proofs, infrastructure, MEV"

5. **Avoid topics** — "Any topics you want to avoid? (comma-separated, or 'none')"
   - e.g., "NFT minting parties, token launches"

6. **Blocked organizers** — "Any organizers you want to block? (comma-separated, or 'none')"

7. **Registration strategy** — "How aggressively should I register you?"
   - **Aggressive**: register for most events that match your interests
   - **Conservative**: only register for top-tier, must-attend events
   - Default: aggressive

8. **Monitoring** — "How should I check for new events?"
   - **Scheduled**: check automatically on an interval (ask for interval, default 6h)
   - **On-demand**: only when you ask
   - **Both**: scheduled + manual trigger anytime
   - Default: on-demand

9. **User info for RSVP** — "What name and email should I use for registrations?"
   - Both required for Luma RSVP

10. **Luma authentication** (optional) — "Do you have a Luma account? Logging in pre-fills RSVP forms and saves time."
    - If yes: initiate the email 2FA flow
      1. Open https://lu.ma/signin in the browser
      2. Enter the user's email
      3. Ask user to paste the verification code from their email
      4. Complete login
      5. Export and save cookies to `luma-session.json`
      6. Set `luma_session.authenticated` to `true` in config
    - If no: set `luma_session.authenticated` to `false`

## Output

Save the config to `conferences/{conference-id}/config.json` with this structure:

```json
{
  "name": "<conference name>",
  "id": "<slug-id>",
  "luma_urls": ["<url1>", "<url2>"],
  "sheets": ["<url1>"],
  "user_info": {
    "name": "<name>",
    "email": "<email>"
  },
  "preferences": {
    "interests": ["<topic1>", "<topic2>"],
    "avoid": ["<topic1>"],
    "blocked_organizers": ["<org1>"],
    "strategy": "aggressive|conservative"
  },
  "monitoring": {
    "mode": "scheduled|on-demand|both",
    "interval": "6h"
  },
  "luma_session": {
    "authenticated": true|false
  }
}
```

## Scheduled Monitoring Setup

If the user chose `scheduled` or `both` monitoring mode, create the cron job:

```bash
openclaw cron edit --message "Run conference-intern monitor {conference-id}" --interval "{interval}"
```

Use the interval from the user's answer (default: 6h). The agent's heartbeat cycle will pick this up and run `monitor.sh` automatically.

## Confirmation

After saving, confirm to the user:
- Config saved to `conferences/{id}/config.json`
- If scheduled monitoring was set up: mention the cron job and interval
- Next step: run `bash scripts/discover.sh {id}` to fetch events
