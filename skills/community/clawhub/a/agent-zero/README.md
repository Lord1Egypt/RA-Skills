# AgentZero 🏠

> **Your personal AI real estate agent.**

Searching for a home is exciting. Scrolling through hundreds of listings every day is not.

Built to run with **[OpenClaw](https://openclaw.ai)**, AgentZero watches the market for you. Tell it what you're looking for, and it quietly surfaces only the homes worth your attention — no phone calls, no pressure, no awkward "I'll pass on this one" conversations.

## What It Does

- 📋 **Set your search profile** — location, price range, must-haves, described in plain language
- 🤖 **Let the agent do the watching** — AgentZero checks listings automatically on a schedule
- 📬 **Inbox new matches** — only the properties that fit, surfaced when they appear
- ✅ **Triage at your pace** — one-click Interested / Pass, no follow-up required
- 📸 **Full listing details** — photos, price history, notes, all in one place

No sign-ups. No subscriptions. Runs locally on your machine.

## Screenshots

Home screen shows you the properties that you are watching.

![Home](./screenshots/home.png)

Daily agent curated listings in the inbox:

![Agent Suggestions](./screenshots/agent_suggestions.png)

Details for listings you're interested in:

![Listing Detail](./screenshots/listing_detail.png)

---

## Getting Started

1. Install [OpenClaw](https://openclaw.ai) — your local AI orchestrator
2. Ask your AI to **install AgentZero** and **set up a daily cron job**
3. On your favourite listing site (Redfin, Realtor.ca, or REW.ca), **set up a search and subscribe to new listing email alerts** — AgentZero will pick these up automatically
4. Open `http://localhost:5173` — your AI agent curates new listings daily for you to review

## Supported Sites

- ✅ Redfin
- ✅ REW.ca
- ✅ Realtor.ca
- 🚧 Zillow *(coming soon)*

---

## How It Works

### Listing lifecycle

Every listing moves through a fixed set of states:

```
           POST /api/listings/agent-suggest         
           AgentZero OpenClaw skill as daily cron job to find new listings
                   │
                   ▼
             [ AgentPending ]
                   │
                   │ POST /:id/agent-review
                   │ Agent review
                   │
                   ├──────────────────► AgentSkip  
                   │                    Terminal — no profile match
                   │
                   │ Move to inbox for users
                   │
                   ▼
  ┌──────────[ HumanReview ]
  │                │
  │                │
  ▼                ▼
[ Pass ]◄─────[ Interested ]─────►[ Candidate ]
                   ▲
                   │
          POST /api/listings
          Manually added by user
```

| Status | Set by | Meaning |
|---|---|---|
| `AgentPending` | Claw | Just added via email scan; agent review is running in the background |
| `AgentSkip` | Agent (Claude) | No search profile matched this listing |
| `HumanReview` | Agent (Claude) | Matched a profile; ready for you to review in the Inbox |
| `Interested` | You | You're tracking this listing |
| `Buyable` | You | Strong candidate |
| `Pass` | You | Dismissed |

### Agent triage

When a listing is added via the email scan, the backend immediately spawns a background task that:

1. Fetches all your search profiles from the database
2. Builds a compact prompt from the parsed property fields (price, beds, baths, sqft, location, schools, taxes, features)
3. Calls **Claude Haiku** (`claude-haiku-4-5`) to pick the best matching profile, or skip if none fit
4. Calls `POST /api/listings/:id/agent-review` with the decision

