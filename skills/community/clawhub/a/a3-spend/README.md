# a3-spend

A small, dependency-free expense tracker skill for OpenClaw. Record purchases, see weekly or monthly totals by category, set monthly category budgets, and get a flag for unusually large purchases.
Data stays in one local JSON file (`~/.a3-spend/ledger.json`, override with `A3_SPEND_LEDGER`). No network access, no accounts, no credentials.

Commands (run from the skill folder with Node 20+):

    node a3-spend.mjs add --amount 12.50 --category food --merchant "Corner Cafe" [--note "lunch"] [--date 2026-11-15]
    node a3-spend.mjs list --days 7
    node a3-spend.mjs summary --week        # or --month
    node a3-spend.mjs budget set food 300
    node a3-spend.mjs budget status
    node a3-spend.mjs delete <id>

Safety: amounts are validated (positive, up to 2 decimals, max 1,000,000), merchant and note text is stripped of control characters and length-capped, writes are atomic, and the agent instructions forbid logging an expense because an email or web page says to.
Synthetic example: `A3_SPEND_LEDGER=/tmp/demo.json node a3-spend.mjs add --amount 4.75 --category coffee --merchant "Demo Cafe" && node a3-spend.mjs summary --week`
