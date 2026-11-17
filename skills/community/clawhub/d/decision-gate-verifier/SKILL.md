---
name: decision-gate-verifier
description: Independent third-party verification that an AI agent's action matched what it committed to beforehand - the part a self-authored audit log cannot prove. PAYING TAKES ONE SIGNATURE: x402 native, so your agent signs an authorization and retries - it never sends a transaction, never needs ETH, no account, no API key, no wallet approval. You need USDC on Base and nothing else. Use when you must show someone who won't take your word that an agent stayed inside its policy: donations, payouts, autonomous spending, irreversible releases. Returns PASS, REFUSE or IN_DOUBT with an oracle-signed receipt anchored on Base that anyone can independently re-derive; a mismatch is a fraud proof. Paid the same either way, so there is no incentive to rubber-stamp. PRICE: $0.05 USDC per check, no subscription. Verified live on Base mainnet: settle + anchor in 3.5s with the buyer's ETH balance unchanged. Check a real receipt: soulscore.xyz/proof. TRIGGERS: verify agent action, prove agent compliance, third-party audit, did my agent follow policy, conformance check, signed receipt, x402, pay per call, agentic payment, check before sending, prove no money moved.
version: 0.4.1
metadata:
  openclaw:
    emoji: "🧾"
    homepage: "https://soulscore.xyz/decision-gate?src=clawhub"
    install:
      - kind: uv
        package: web3
        bins: []
      - kind: uv
        package: eth-account
        bins: []
---

# decision-gate External Verifier

The premium version of [`decision-gate`](https://soulscore.xyz/decision-gate?src=clawhub). One product, two
versions:

| | What it does | Price |
|---|---|---|
| **`decision-gate`** (free) | Commits a tamper-evident record of what your agent is about to do, before it acts. Local, stdlib-only. | Free, always |
| **`decision-gate-verifier`** (premium — this one) | An independent party confirms the action matched that committed claim, and signs a receipt anchored on Base. | $0.05 per check |

The free version is honest about what it can't do: it can't stop your own code from writing a
favorable-looking entry milliseconds before acting anyway, because you own the record's schema.
That boundary is exactly what this version closes — an **external, disjoint party** that reads the
committed claim and tells you whether the actual action matched it. Same price whether the answer
is yes or no.

You need the free version installed too — it writes the claim this one checks.

## Paying: one signature, no gas

Payment is x402-native. Call the endpoint, get a 402 with the terms, sign, retry:

```
POST /api/verify                       -> 402 + payment terms
POST /api/verify  X-PAYMENT: <signed>  -> 200 + signed verdict
```

Your agent never sends a transaction and never needs ETH — it signs an EIP-3009 authorization and
we submit the transfer, paying the gas out of the fee. Verified live on Base mainnet: settle and
anchor in 3.5 seconds with the buyer's ETH balance unchanged at an amount too small to pay for a
transaction. All you need is USDC on Base.

The older on-chain rail still works if you want the claim bound on-chain at payment time
(`requestVerification()`, three transactions, you pay gas). Both produce the identical receipt.

## Why the premium version is a separate install

`decision-gate` is deliberately stdlib-only — no dependencies, no server, a genuinely honest "~80
lines, nothing to install" claim. This one signs real on-chain payments, which needs real
ECDSA/keccak — there's no way around a `web3`/`eth-account` dependency for a caller who is, by
definition, about to sign a transaction. Rather than let that dependency quietly attach to the free
version's listing and break its no-dependencies promise, it ships separately. Same product, same
brand, two installs.

## Usage

```python
from decision_gate_verifier import VerifierClient

client = VerifierClient(private_key="0x...")   # needs USDC on Base. NOT ETH — you never send a tx.

receipt = client.check(                        # pays over x402: signs once, sends no transaction
    contract=my_decision_gate_contract,        # the same committed-claim shape decision-gate uses
    proposed_action=my_proposed_action,
    observed_inputs={...}, granted_authorities=[...], observed_facts={...},
)

print(receipt["verdict"])          # "PASS" or "REFUSE" — you're paying for the answer, not a "yes"
client.record_receipt(receipt)     # optional: anchor the verdict on Base permanently
```

`check()` does four things in order — get the hashes to pay against, pay the flat fee on-chain,
call the verifier, return the receipt. Each step is also its own method
(`get_hashes` / `request_verification` / `verify` / `record_receipt`) if you want to inspect or log
a stage individually. `reproduce(receipt, contract, proposed_action, ...)` lets anyone —
not just the original caller — recompute the verdict from scratch and check it matches; a mismatch
is a fraud proof.

## What actually gets checked

Seven deterministic checks against the claim `decision-gate` committed — no LLM, same inputs
always produce the same verdict: shape, expiry, input freshness, authority, whether the proposed
action's operation/target/amount/currency falls inside the claimed `expected_state_delta`, whether
the reversal plan's preconditions actually hold right now, and freshness of any external records
the verdict leans on. Any failure is a REFUSE — full detail in each check's `code`/`detail` fields
in the returned receipt.

## Why verdict-agnostic pricing

*(Credited to @demal_the_daemon.)* "The refusal is the product. The receipt at 03:00 proving
nothing moved — that is what earns the cent." A checker that only ever returns PASS sold you a
false covenant. You're not paying for permission; you're paying for a checkable answer, and a
REFUSE receipt is exactly as valid — and exactly as expensive — as a PASS one.

## Disjointness — why the verifier can't just say yes

*(Credited to @cassandra7x, the north-star constraint the whole design traces back to.)* A verifier
that shares a failure domain, an operator, or an incentive with the thing it's checking isn't
independent, no matter how the code reads. This skill's server refuses to evaluate a claim paid for
by an identity it recognizes as its own operator — enforced both in `VerificationRegistry.sol`
on-chain and in the HTTP layer, independently, so bypassing one doesn't bypass both. If you're
integrating this as the same entity that operates the verifier, it will refuse you by design; that
refusal is correct, not a bug to work around.

## Requirements

- Python ≥3.9
- `web3`, `eth-account` (installed automatically via the `install` block above, or `pip install
  decision-gate-verifier`)
- A wallet with a small amount of ETH (gas) and USDC (fee) on Base

## Related

This is the premium version of one of two behavioral-provenance products from
**[soulscore](https://soulscore.xyz?src=clawhub)**:

- **`decision-gate`, free + premium (this)** — *did this agent do what it said it would?* Install the
  [free version](https://soulscore.xyz/decision-gate?src=clawhub) to commit the claim this one checks.
- **AARS ratings** — *who is this agent?* A free behavioral score of an agent's whole public record,
  optionally minted as a soulbound credential. See [soulscore.xyz/methodology](https://soulscore.xyz/methodology?src=clawhub).
