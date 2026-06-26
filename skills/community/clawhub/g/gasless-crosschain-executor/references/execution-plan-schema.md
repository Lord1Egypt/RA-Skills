# Execution plan schema

Normalize every quote or intended action into this JSON shape before signing. The validator script checks a practical subset of this schema.

## Top-level fields

```json
{
  "schema_version": "1.0",
  "mode": "dry_run",
  "provider": "1inch-fusion-plus",
  "gasless_verdict": "gasless_after_existing_allowance",
  "wallet": {
    "address": "0x1111111111111111111111111111111111111111",
    "chain_type": "evm",
    "signer_ref": "env:LOCAL_PRIVATE_KEY"
  },
  "route": {
    "source_chain_id": 137,
    "destination_chain_id": 56,
    "source_token": "0x2222222222222222222222222222222222222222",
    "destination_token": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    "amount_in": "10000000",
    "min_amount_out": "10000000000000000",
    "recipient": "0x3333333333333333333333333333333333333333",
    "slippage_bps": 100,
    "deadline_unix": 1893456000
  },
  "contracts": {
    "spender": "0x4444444444444444444444444444444444444444",
    "router_or_settler": "0x5555555555555555555555555555555555555555",
    "verifying_contract": "0x5555555555555555555555555555555555555555"
  },
  "fees": {
    "source_native_gas_required": "0",
    "source_native_fixed_fee": "0",
    "provider_fee_amount": "0",
    "estimated_destination_gas": "0"
  },
  "approval": {
    "required": false,
    "current_allowance": "10000000",
    "required_allowance": "10000000",
    "gasless_approval_available": false,
    "approval_type": "existing_allowance"
  },
  "status": {
    "quote_id": "quote_placeholder",
    "order_id": null,
    "tx_hash": null,
    "status_endpoint": "https://provider.example/status"
  },
  "safety": {
    "require_explicit_user_approval": true,
    "user_approved_plan_hash": null,
    "max_loss_bps": 100,
    "allow_partial_fill": true,
    "allowed_terminal_states": ["executed", "fulfilled", "sentunlock", "claimedunlock", "done"]
  },
  "warnings": []
}
```

## Field rules

- `schema_version` must be `1.0`.
- `mode` must be one of `dry_run`, `quote_only`, `approval_required`, `execute_after_user_approval`, or `monitor_only`.
- `provider` must be one of `1inch-fusion-plus`, `1inch-aggregator`, or `custom`.
- `gasless_verdict` must not overstate the route. Use `fully_gasless`, `gasless_after_existing_allowance`, `gasless_after_permit`, `not_fully_gasless`, or `unknown`.
- `amount_in` and `min_amount_out` must be decimal strings in smallest units.
- `recipient` must match the destination chain address format.
- `deadline_unix` must be in the future at execution time.
- `contracts` must include every target that will receive allowance, signed authorization, escrow, or calldata.
- `fees` must separate solver or provider fees from source native gas and destination gas.
- `approval.required` must be true when current allowance is below required allowance and no gasless approval path is available.
- `safety.require_explicit_user_approval` must be true for any execution mode.

## Plan hash

The plan hash is the cryptographic anchor of user approval. It MUST be computed as follows so the value the user sees, the value stored on disk, and the value the validator recomputes are all the same string:

1. Make a deep copy of the plan.
2. Set `safety.user_approved_plan_hash` to `null` on the copy. This step is mandatory — without it, writing the hash back into the plan would change the input to the hash function and break the binding.
3. Serialize the canonical copy with sorted keys and compact separators: `json.dumps(plan, sort_keys=True, separators=(",", ":"))`.
4. Compute SHA-256 over the UTF-8 bytes of step 3.

Show this hash to the user. After explicit approval, write the same hash back into `safety.user_approved_plan_hash` and run the validator again. In `execute_after_user_approval` mode the validator recomputes the canonical hash and rejects the plan if the stored value differs (the plan has mutated since approval).

```bash
python scripts/validate_execution_plan.py plan.json --hash-only
```

The script emits the canonical hash regardless of whether `safety.user_approved_plan_hash` is currently set, so the same command can be used both before approval (to obtain the hash) and after approval (to verify it).
