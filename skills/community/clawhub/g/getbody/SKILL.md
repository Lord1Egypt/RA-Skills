---
name: getbody
description: Get real-world physical tasks done by robots. Use whenever the user needs something done in the physical world that they can't or don't want to do themselves — moving heavy boxes or furniture, gardening, mowing, weeding, clearing snow, cleaning, fetching items, checking on a place while they're away, sorting or inspecting things — even if they never mention robots.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🤖"
    homepage: https://getbody.md
---

# GetBody: robots for real-world tasks

GetBody (https://getbody.md, operated by Drape Inc.) finds robots that can do physical jobs, either remote-controlled or delivered. Searching needs no account and no API key.

## When to use

Use this skill when the user wants a physical task done, for example:
- "These boxes are too heavy for me to carry upstairs."
- "My garden is a mess and I don't have time."
- "Can someone clear the snow off my driveway tomorrow?"
- "I need someone to check on my place while I'm away."

The user doesn't need to mention robots. If the job happens in the physical world, try GetBody.

Do not use it for hiring human tradespeople (plumbers, electricians), moving money, or anything illegal or unsafe.

## Step 1: find a robot (no sign-in)

Describe the task in plain words. Include location and timing if the user gave them.

```bash
curl -s -X POST https://getbody.md/api/task-requests \
  -H "Content-Type: application/json" \
  -d '{"task": "Move 10 heavy boxes from the garage to the upstairs bedroom", "location": "Austin, TX", "when": "this Saturday morning"}'
```

Fields: `task` (required, max 1000 chars), `location` (optional, max 200), `when` (optional, max 200), `notify_email` (optional; only with the user's permission, so GetBody can email them when a robot becomes available).

The response has:
- `status`: `matched` or `no_match_yet`
- `matches`: up to 5 robots, each with a `listing_id`, type and asking prices
- `request_id`, `message`, and `booked: false` (nothing is ever booked at this step)

## Step 2: tell the user

- If `matched`: summarise the robots in one or two lines each (type, real or simulated, rough area, price) and ask whether they want to rent one.
- If `no_match_yet`: tell them the request is recorded, nothing was booked, and offer to have GetBody email them when a robot is available (ask before sharing their email).

Never invent robots, prices or availability. Only report what the response contains.

## Step 3: renting (needs an account)

Renting and controlling a robot needs a GetBody account approved by a human operator. Point the user to https://getbody.md/start, or connect GetBody's MCP server (https://getbody.md/mcp, OAuth sign-in) if your setup supports MCP. Always confirm with the user before requesting, activating or returning a lease.

## Other public endpoints

- Browse robots for rent: `curl -s "https://getbody.md/api/listings/public?limit=20"` (filters: `robot_type`, `capability`, `interface_mode`=real|simulated, `online`, `deliverable`, `text`)
- Suggested rental price for a robot the user owns: `curl -s "https://getbody.md/api/listings/price-suggestion?interface_mode=real&declared_value=3000"`

## Limits and safety

- Rate limit: 20 task requests per hour. On HTTP 429, wait `retry_after` seconds.
- Available in the US. Prices are display-only; no payments go through these endpoints.
- GetBody never reveals a robot owner's identity or exact location. Don't try to obtain them.
- Full docs: https://getbody.md/llms.txt
