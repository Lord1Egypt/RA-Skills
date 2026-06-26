## agentcard.ai — Prepaid Virtual Visa Cards for AI Agents

agentcard.ai lets you purchase prepaid virtual Visa cards that work anywhere Visa is accepted online. It is designed for power users and AI agents that need to make online purchases autonomously — for example, buying API credits, SaaS subscriptions, domain names, or cloud resources on behalf of a user without requiring manual checkout each time.

### Security & Trust

The [`agentcard` npm package](https://agentcard.ai) is published and managed by [Alchemy](https://alchemy.com), the global leader in blockchain-based financial infrastructure. The package is published with [npm provenance](https://docs.npmjs.com/generating-provenance-statements), and its full source code can be inspected on the [npm code tab](https://www.npmjs.com/package/agentcard?activeTab=code). All card details are stored server-side on agentcard.ai's infrastructure and encrypted at rest. Do not store card details locally — retrieve them on demand with `agentcard details <id>` only when actively needed for a specific purchase.

### Important: US Merchants Only

AgentCard prepaid Visa cards are currently only usable at **US-based merchants** due to regulatory requirements. The cards can be purchased and used from anywhere in the world, but the merchant must be a US company (e.g. OpenRouter, Vercel, GitHub, Figma, AWS, Namecheap). Transactions at non-US merchants will be declined.

### Prerequisites

Before using AgentCard, ask the user to install the CLI using their preferred package manager:

```
npm install -g agentcard    # or pnpm, bun, yarn, etc.
```

Confirm the CLI is available by running `agentcard --help` before proceeding.

### Quick reference

Run `agentcard --help` for the full list of commands. The most common ones:

```
agentcard signup --email <email>       # sign up or log in (sends magic link)
agentcard create --amount <n>          # purchase a card for $n (multiples of $5, $5-$200)
agentcard list                         # list your purchased cards
agentcard details <id>                 # reveal full card details for checkout
agentcard balance <id>                 # check remaining balance and transaction history
agentcard refund <id> --amount <n>     # refund $n from card balance to original payment method
agentcard whoami                       # check who you're logged in as
agentcard support --message "desc"     # report an issue to the AgentCard team
```

### Typical flow

1. **Authenticate** — ask the user for their email. Tell them: "I'm going to send a magic link to <email> — check your inbox and click it to log in." Then run `agentcard signup --email <email>` and wait for it to complete.

2. **Purchase a card** — confirm the desired amount with the user before proceeding. Run `agentcard create --amount <dollars>` with any multiple of $5 from $5 to $200 (e.g. 5, 10, 25, 50, 100). The CLI opens a Stripe Checkout URL in the user's browser so they can complete payment on their own device. Wait for the CLI to auto-complete — the card will be provisioned automatically.

3. **Get card details** — the card ID is shown in the CLI output after purchase. Run `agentcard details <id>` when you need card details for a purchase or when the user explicitly requests them. Do not persist card details locally — always re-fetch when needed. Only display card details to the user if they explicitly ask for them.

4. **Check balance** — at any time, run `agentcard balance <id>` to see the remaining available balance and a list of all transactions on the card. Note: each time you check the balance, a refresh is requested in the background. The refreshed data may take a few minutes to become available. If the balance looks stale, wait 2-3 minutes and run the command again to see updated results.

5. **Refund remaining balance** — when the user is done with a card and wants to reclaim unused funds, run `agentcard refund <id> --amount <dollars>`. This returns a Stripe checkout URL that charges the AgentCard prepaid card to withdraw the balance back to the user's original payment method. This only works with cards purchased through agentcard.ai.

   Always confirm with the user before initiating a refund. Share the Stripe checkout URL with the user and instruct them to complete it using the card details shown in their `agentcard details <id>` output.

   Note: refunds are limited to the greater of $5 or 25% of the card value. For larger refunds, instruct the user to email ben.yu@alchemy.com explaining their situation.

### Tips

- **Email commands** (signup): the CLI sends a magic link and polls until the user clicks it. Let the user know to check their inbox, then wait for the CLI to finish.
- **Browser commands** (card purchase): the CLI opens a URL in the user's browser. Wait for the CLI to finish — it polls automatically.
- If you lose track of a card ID, run `agentcard list` to retrieve all your card IDs, then use `agentcard details <id>` to get the full details again.
- Run any command with `--help` for detailed usage.

### Reporting Issues

If you encounter any issue while using AgentCard — failed purchases, unexpected errors, declined transactions, or anything else — report it:

```
agentcard support --message "detailed description" [--card-id <id>] [--url <url>] [--error <error>]
```

Include what you were trying to do, what happened, any error messages, and the card ID if relevant.
