# SKILL: smart-contract-audit

## Purpose
Perform a deterministic, evidence-based vulnerability review of Solidity contracts and produce a prioritized audit report with concrete fixes.

## When to Use
- Before any deployment (even testnet) of value-bearing contracts.
- After changing access control, external calls, accounting, or token logic.
- When integrating with external protocols.

## Inputs
- `scope` (required, string[]): contract files and dependencies.
- `threat_model` (optional, string): assets at risk, attacker capabilities, trust assumptions.
- `deployment_assumptions` (optional, string): upgradeability, admin keys, multisig/DAO governance.

## Steps
1. Map the system:
   - entrypoints (public/external)
   - privileged roles
   - external calls and token transfers
2. Run checklist-based review:
   - access control (missing/overbroad roles)
   - reentrancy surfaces (external calls, callbacks)
   - accounting correctness (under/overflow, rounding, precision, fee logic)
   - ERC standard compliance (events, return values)
   - upgradeability hazards (storage layout, initializer patterns)
   - DoS vectors (unbounded loops, griefing)
3. Identify invariants and where they can break.
4. Produce findings with reproduction notes and recommended fixes.

## Validation
- Every finding includes:
  - impacted function(s)
  - why it’s exploitable or risky
  - concrete remediation guidance
- Non-issues are explicitly marked as “informational” when needed.

## Output
Audit report (example schema):
```yaml
summary: "<system overview + top risks>"
findings:
  - id: "SC-001"
    severity: "critical|high|medium|low|info"
    title: "<short>"
    location: ["contracts/X.sol:123"]
    description: "<what is wrong>"
    impact: "<what can happen>"
    recommendation: "<how to fix>"
assumptions: ["..."]
```

## Safety Rules
- Do not provide exploit code for real targets.
- Do not claim “secure” or “audited” as an absolute; report risk and evidence.
- Escalate to stricter review if funds or governance are at stake.

## Example
Scope: `["contracts/Vault.sol", "contracts/Token.sol"]`
Output: includes reentrancy review of `withdraw()` and role boundaries for `setFee()`.

