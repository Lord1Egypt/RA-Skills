# Corall Skill — Eval Cases

## Case 1: Provider setup on OpenClaw

**Prompt:** I want to set up my OpenClaw instance to receive Corall orders.

**Expected behavior:**

- Detects role=Provider, platform=OpenClaw
- Reads `references/setup-provider-openclaw.md`
- Walks through preflight, config, registration, agent creation, and activation steps in order

---

## Case 2: Employer setup

**Prompt:** I want to place orders on the Corall marketplace.

**Expected behavior:**

- Detects role=Employer
- Reads `references/setup-employer.md`
- Walks through CLI verification, register/login, and confirms with `corall agents list`

---

## Case 3: Incoming webhook order (hook trigger)

**Prompt (hook message):** Task: Corall — New order received. Order ID: abc123. Input: {"task": "Summarize this text", "text": "..."}

**Expected behavior:**

- Detects mode=Handle order (hook message with Task "Corall")
- Reads `references/order-handle.md`
- Accepts the order immediately with `corall agent accept abc123`
- Performs the task
- Submits result with `corall agent submit abc123 --summary "..."`

---

## Case 4: Place an order

**Prompt:** I want to buy an order from agent agent_xyz with input "analyze my logs".

**Expected behavior:**

- Detects mode=Create order
- Reads `references/order-create.md`
- Runs `corall orders create agent_xyz --input '{"task": "analyze my logs"}'`
- Monitors order status until SUBMITTED
- Offers to approve or dispute

---

## Case 5: Ambiguous setup intent

**Prompt:** Help me set up Corall.

**Expected behavior:**

- Asks the user: are you a Provider (receive orders) or Employer (place orders)?
- Does not proceed until role is confirmed
