# Automation state

Before measuring or recommending action, classify the position as directly held, approved to an operator, deposited in a gauge, held by a vault, or temporarily processed by a utility. Record both onchain owner and beneficial owner.

## Read active controls

Inspect every current auto-exit, auto-range, auto-compound, vault, gauge, and keeper configuration. Record triggers, range offsets, swap limits, oracle guards, operator reward caps, pause state, disable path, and upgrade authority.

Do not infer active state from an approval alone. Do not infer inactive state from a dashboard switch. Use contract configuration and receipts.

## Position continuity

A range move can replace the NFT ID. Follow the emitted transition and verify ownership of the replacement. Preserve one accounting lineage across old and new IDs without counting the withdrawal and remint as new profit.

Include claimable and loose token balances held for the beneficial owner by an automation contract. Separate them from operator or protocol fees.

## Action gate

Before recommending a manual collect, increase, move, unstake, or exit:

- check whether automation may execute first
- check whether custody permits the action
- check whether configuration must be disabled or migrated
- include the disable, withdrawal, and approval-cleanup costs

Return `blocked` when automation state, beneficial ownership, or the safe disable path cannot be verified.

Measure auto-compounding net of gas, operator reward, swap cost, taxes, and idle residue. More frequent compounding is not automatically better.
