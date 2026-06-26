Single JS entry skill for Amazon after-sales full-flow automation.

Default behavior in OpenClaw:
- Natural-language command like "run amazon-after-sales-flow" triggers full flow.

Usage:

1) Natural-language full flow (recommended)
- Input: "run amazon-after-sales-flow 2025"
- Behavior: open orders -> open order details -> run contact flow -> type/send message

2) Explicit full flow JSON
- Input JSON: {"action":"run_full_flow","year":2025,"message":"...","auto_send":false,"confirm_send":false,"browser":{"headless":false,"keepOpen":true}}

3) One specific integrated skill
- Input JSON: {"skill":"amazon_contact_flow","args":{...}}

Runtime requirements:
- Node.js >= 18
- npm install
- npx playwright install chromium

Security mode:
- Legacy shell URL opener is disabled.
- URL text input returns a blocked response.
- Sending requires auto_send=true and confirm_send=true.
