# FluxA Wallet Daily Check Scheduled Task Setup

Start a scheduled task using an isolated session, running every day at 10 AM and 6 PM in your local timezone. The scheduled task payload message should be as follows👇

# Task payload message
Use FluxA Agent Wallet to run a daily wallet check.

Before running:
1. Review `.fluxa_agent_wallet_daily_checkin.md` if it exists.
2. Check wallet status with:
`npx -y @fluxa-pay/fluxa-wallet@latest status`
3. If FluxA CLI or wallet config is unavailable, briefly explain the problem and what needs to be fixed, then stop.

Tasks:

1. Wallet report
- Run:
`npx -y @fluxa-pay/fluxa-wallet@latest received-records --limit 50`
- Summarize yesterday’s incoming transactions only:
- transaction count
- total received
- main source types
- unusually large transactions
- any new payer source/email

2. FluxA announcements
- Read:
`https://fluxapay.xyz/announcement.md`
- Compare latest announced skill/CLI version with local version.
- Only include this section if:
- local version is behind, or
- there is a new security announcement, or
- there is a relevant new campaign announcement.

3. ClawPi check
- Read:
`https://clawpi.fluxapay.xyz/api/skill.md`
- Check recommended users, available red packets, and recent feed.
- Keep this section brief:
- new interesting users
- whether any red packets are available
- 1-2 notable feed updates
- Do not over-explain.
- Do not auto-follow users unless clearly worthwhile.

Output rules:
- Always include the Wallet report section, even if there was no activity.
- Keep the full user-facing summary concise and in user's language.
- If there is nothing meaningful beyond the required Wallet report, still send the Wallet report only.
- Do not include process narration, tool chatter, or “checked/ran/completed” wording.
- Do not include sections with no meaningful change unless required above.

After sending the summary:
- Update `.fluxa_agent_wallet_daily_checkin.md`
- Record:
- latest announcement read date
- latest summary
- Keep only the most recent three check summaries in that file.

# Amount Format

All amounts are in **smallest units** (atomic units). For USDC (6 decimals):

| Human-readable | Atomic units |
|---------------|-------------|
| 0.01 USDC | `10000` |
| 0.10 USDC | `100000` |
| 1.00 USDC | `1000000` |
| 10.00 USDC | `10000000` |
