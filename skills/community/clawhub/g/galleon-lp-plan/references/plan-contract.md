# Plan contract

Emit this structure in prose, JSON, or both.

```json
{
  "status": "approval-required | ready | blocked | expired",
  "phase": "approvals | action",
  "schemaVersion": "versioned contract",
  "planDigest": "canonical digest of every material field",
  "createdAt": "UTC timestamp",
  "expiresAt": "UTC timestamp",
  "chainId": 0,
  "wallet": "0x...",
  "protocol": "uniswap-v3",
  "pool": {
    "addressOrId": "0x...",
    "token0": "0x...",
    "token1": "0x...",
    "fee": "exact raw value",
    "tickSpacing": "exact value",
    "hook": "0x... or none"
  },
  "observation": {
    "block": "exact block",
    "price": "token1 per token0",
    "tick": "exact tick",
    "freshness": "fresh | lagging | diverged | unknown"
  },
  "handoff": {
    "kind": "direct | uniswap-lp-api | uniswap-interface",
    "sourceVersion": "current verified source or null",
    "requestId": "builder request id or null",
    "builtAt": "UTC timestamp or null",
    "url": "reviewed interface link or null"
  },
  "position": {
    "model": "full-range | concentrated",
    "tickLower": "exact or null",
    "tickUpper": "exact or null",
    "maxSpend0": "integer units",
    "maxSpend1": "integer units",
    "minimumLiquidity": "integer units"
  },
  "steps": [
    {
      "sequence": 1,
      "intent": "approve | mint | add | stake | other",
      "target": "verified address",
      "value": "integer native units",
      "calldataStatus": "complete | deferred",
      "limits": {},
      "simulation": {},
      "expectedStateDiff": [],
      "checkpointReads": [],
      "recovery": "stop and rebuild from chain state"
    }
  ],
  "assumptions": [],
  "blocks": []
}
```

## Ready criteria

A plan is ready only when identity, balances, approvals, quote, gas, deadlines, targets, calldata, simulations, handoff terms, and expected state changes are internally consistent. A deferred downstream step is acceptable only when the plan explains which mined value is required to build it.

An `approval-required` result contains only the finite approvals needed for the next action. It does not contain ready action calldata. After approval receipts, reread state and create a new action-phase digest.

A `ready` result contains one exact next transaction. Bind the digest to chain, wallet, pool, position, inputs, recipients, target, calldata, native value, limits, quote, observation block, and expiry. Any material change expires it.

Do not include a signature request. Do not represent simulated transaction hashes as receipts.
