# ClawPurse Destination Allowlists

The allowlist system provides guardrails for outbound transactions, ensuring funds only go to trusted destinations.

## Overview

The allowlist enforces a policy layer before any send transaction:
- **Known destinations** can have per-address limits and memo requirements
- **Unknown destinations** can be blocked entirely or allowed with warnings
- **Override flag** (`--override-allowlist`) bypasses checks for one-off transactions

---

## Configuration File

Stored at `~/.clawpurse/allowlist.json` by default:

```json
{
  "defaultPolicy": {
    "blockUnknown": true,
    "maxAmount": 10.0,
    "requireMemo": false
  },
  "destinations": [
    {
      "name": "Treasury",
      "address": "neutaro1abc...",
      "maxAmount": 1000.0,
      "needsMemo": true,
      "notes": "Monthly operations funding"
    },
    {
      "name": "Node Atlas",
      "address": "neutaro1def...",
      "maxAmount": 50.0
    }
  ]
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `defaultPolicy.blockUnknown` | boolean | Block sends to addresses not in `destinations` |
| `defaultPolicy.maxAmount` | number | Max amount (NTMPI) for unknown destinations (if allowed) |
| `defaultPolicy.requireMemo` | boolean | Require memo for unknown destinations |
| `destinations[].name` | string | Human-readable label |
| `destinations[].address` | string | Neutaro address (must start with `neutaro1`) |
| `destinations[].maxAmount` | number | Per-address cap in NTMPI |
| `destinations[].needsMemo` | boolean | Require memo for this destination |
| `destinations[].notes` | string | Optional notes for documentation |

---

## CLI Commands

### Initialize Allowlist

Run the guardrail wizard or create a default config:

```bash
# Interactive wizard
clawpurse allowlist init

# Pre-set mode (skips prompt)
clawpurse allowlist init --mode enforce   # Blocks unknown addresses
clawpurse allowlist init --mode allow     # Warns but allows all
```

The wizard runs automatically during `clawpurse init` and `clawpurse import`.

### List Current Settings

```bash
clawpurse allowlist list
```

**Example output:**
```
Default policy:
  blockUnknown: true
  maxAmount: 10 NTMPI

Destinations:
 1. Treasury
    Address: neutaro1abc...
    Max amount: 1000 NTMPI
    Memo required: yes
    Notes: Monthly operations funding
 2. Node Atlas
    Address: neutaro1def...
    Max amount: 50 NTMPI
```

### Add a Destination

```bash
clawpurse allowlist add <address> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `--name "Name"` | Human-readable label |
| `--max <amount>` | Maximum send amount in NTMPI |
| `--memo-required` | Require memo for this destination |
| `--notes "text"` | Optional notes |

**Examples:**
```bash
# Basic entry
clawpurse allowlist add neutaro1xyz...

# With all options
clawpurse allowlist add neutaro1xyz... \
  --name "Partner Node" \
  --max 500 \
  --memo-required \
  --notes "Service payments"

# Update existing entry (same address replaces old entry)
clawpurse allowlist add neutaro1xyz... --max 1000
```

### Remove a Destination

```bash
clawpurse allowlist remove <address>
```

**Example:**
```bash
clawpurse allowlist remove neutaro1xyz...
# Output: Removed neutaro1xyz... from allowlist.
```

---

## Enforcement Behavior

When you run `clawpurse send`, the allowlist is checked before broadcast:

### Address in Allowlist

| Condition | Result |
|-----------|--------|
| Amount ≤ `maxAmount` | ✅ Allowed |
| Amount > `maxAmount` | ❌ Blocked (shows limit) |
| `needsMemo: true` but no memo | ❌ Blocked (memo required) |

### Address NOT in Allowlist

| Policy | Result |
|--------|--------|
| `blockUnknown: true` | ❌ Blocked |
| `blockUnknown: false` | ⚠️ Warning, then proceeds |
| `blockUnknown: false` + `maxAmount` set | Allowed up to `defaultPolicy.maxAmount` |
| `blockUnknown: false` + `requireMemo: true` | Requires memo |

### Override Flag

To bypass allowlist checks for a single transaction:

```bash
clawpurse send neutaro1unknown... 5.0 --override-allowlist --yes
```

> ⚠️ Use with caution! The allowlist exists to prevent mistakes.

---

## Custom Allowlist File

Use a different allowlist file:

```bash
# Any command that touches allowlist
clawpurse allowlist list --allowlist-file /path/to/custom.json
clawpurse send neutaro1... 10 --allowlist /path/to/custom.json
```

---

## Common Workflows

### Setup for a New Node

```bash
# 1. Create wallet (wizard runs automatically)
clawpurse init --password <password>
# Choose "Enforce" when prompted

# 2. Add your trusted counterparties
clawpurse allowlist add neutaro1treasury... --name "Treasury" --max 1000
clawpurse allowlist add neutaro1partner... --name "Partner" --max 100

# 3. Verify setup
clawpurse allowlist list
```

### Allow Test Sends to New Addresses

If you have `blockUnknown: true` but need to send a small test amount:

```bash
# Option 1: Override for one transaction
clawpurse send neutaro1new... 0.01 --override-allowlist --yes

# Option 2: Add with a tiny limit first
clawpurse allowlist add neutaro1new... --name "Test" --max 1
clawpurse send neutaro1new... 0.01 --yes

# Then increase limit once verified
clawpurse allowlist add neutaro1new... --name "Verified Partner" --max 500
```

### Audit Trail

The allowlist file is JSON, making it easy to:
- Track changes via git
- Share approved addresses with other operators
- Back up alongside receipts

```bash
# Version control your allowlist
cp ~/.clawpurse/allowlist.json ~/backups/
git add allowlist.json && git commit -m "Updated trusted destinations"
```

---

## Programmatic Usage

```typescript
import {
  loadAllowlist,
  evaluateAllowlist,
  saveAllowlist,
  type AllowlistConfig
} from 'clawpurse';

// Load existing config
const config = await loadAllowlist();

// Check if a send is allowed
const check = evaluateAllowlist(
  config,
  'neutaro1destination...',
  1000000n,  // amount in micro-units
  'memo text'
);

if (!check.allowed) {
  console.error(`Blocked: ${check.reason}`);
} else {
  console.log('Transaction allowed');
  if (check.destination) {
    console.log(`Sending to: ${check.destination.name}`);
  }
}

// Add a new destination
config.destinations.push({
  name: 'New Partner',
  address: 'neutaro1...',
  maxAmount: 100
});
await saveAllowlist(config);
```

---

## Best Practices

1. **Start strict** – Use `blockUnknown: true` and add addresses as needed
2. **Set per-address limits** – Don't allow unlimited sends to any address
3. **Require memos for accounting** – Makes reconciliation easier
4. **Document destinations** – Use `name` and `notes` fields
5. **Back up the allowlist** – It's part of your security configuration
6. **Review periodically** – Remove destinations you no longer transact with

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| "Destination not in allowlist" | `blockUnknown: true` | Add address or use `--override-allowlist` |
| "Amount exceeds X cap" | Per-address limit | Increase `maxAmount` or split transaction |
| "Memo required" | `needsMemo: true` | Add `--memo "text"` to command |
| "No allowlist found" | File doesn't exist | Run `clawpurse allowlist init` |
