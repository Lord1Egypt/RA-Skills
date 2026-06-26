# Task 3 Example (English)

> This is a fully expanded two-layer example that shows the complete output shape; plain chat should not expand the maintainer layer by default.

## User Summary

You are at `Task 3: Faction Belonging`.

The four branded factions are:

- `The Recorder`: to be remembered is to truly exist
- `The Asylum`: if we build civilization on someone else's servers, it will become a sandcastle game sooner or later
- `The Mutant`: infinite mutation still needs a base point that does not disappear
- `The Balancer`: a rented home and a home we build ourselves are two different things

If your coordinate card leans toward memory, witness, and long-term permanence, `The Recorder` is a natural fit.
Current stage: `selected`, not completed yet.
If you want, I can take your choice and continue the oath flow now.

### Stage Samples

- `selected`: the user has chosen a faction, but the oath has not started yet.
- `waiting for tokens`: the faction is chosen, but the user still does not meet the 2 AIBOUNTY requirement for the vote.
- `ready to oath`: mapping, version, timing, and token prechecks are complete; if this path still needs one authorization step, that approval happens first and then the actual oath submission continues.
- `submitted`: the oath has been sent and is waiting for final confirmation in the public record.
- `completed`: the oath transaction has succeeded and the user now has the `txId` they must report in Telegram.

### Waiting-for-Tokens Example

If the direction is already chosen but the user does not yet have 2 AIBOUNTY, the reply should say:

`Your direction is already locked in, but you do not yet meet the 2 AIBOUNTY requirement for the oath vote. I am keeping you in the waiting-for-tokens stage for now. You can return after Task 2 pairing succeeds, or invite friends to pair so you can build toward the required tokens.`

### Submitted Example

If the oath vote has already been sent but the final result is still waiting to settle, the reply should say:

`Your faction oath has already been sent, and I am keeping you in the submitted stage while the public record confirms the final result. Once that confirmation lands, I will give you the final reference number.`

### Blocker Example

If this is not a normal wait but an external execution blocker on approval, dependency, or confirmation, the reply should say:

`The faction oath still cannot continue, and this is not just a normal waiting state. The CA automatic execution path is still blocked here even after authorization, submission, and confirmation retries, so I am pausing the flow until that blocker is cleared.`

If TomorrowDAO direct send already reports that `CA` direct send is forbidden, but the explicit `CA` forward transport itself is unavailable, the reply should also make that blocker explicit:

`The faction oath still cannot continue, and this is not because your faction choice or tokens are wrong. This step is missing a usable CA forward transport, so I am treating it as a CA transport blocker instead of switching to manager direct signing or another private-key fallback.`

- `→ If you're stuck here, join the [Telegram group](https://t.me/+tChFhfxgU6AzYjJl) and share your current step, error, and key context so the community can help troubleshoot.`
- `→ You can also post on [X](https://x.com/aelfblockchain) with your current status and blocker so others can spot it and help faster.`

### Approval Example

If the user already has enough `AIBOUNTY` but this path still needs one vote authorization step, the reply should say:

`You already meet the 2 AIBOUNTY requirement for the faction oath, but this path still needs one final authorization step. I will complete that approval first, and then continue with the actual oath vote.`

### Password Example

If the current `CA` context is already available but the keystore password is still missing, the reply should say:

`I have already confirmed that your current identity entry can continue this faction oath, but this step still needs the CA keystore password once. After you provide it, I will continue the authorization, oath submission, and confirmation automatically.`

### Automatic-Retry Example

If approval or vote submission did not settle on the first attempt but the system is still auto-reconciling state, the reply should say:

`This step is still in automatic retry, and I am re-checking authorization state, oath state, and public-record confirmation. As long as this automatic path can continue, I will not hand the execution back to you.`

If one `CA` write path already completed the approval step successfully, but another vote-send path still reports an allowance-style failure, the system should switch back to the already verified `CA` write transport instead of treating that as a real token shortfall.

### Success Example

If the oath transaction already succeeded and returned a `txId`, the reply should say:

`Your faction oath has succeeded and your current reference is txid-1234. Join the [Telegram group](https://t.me/+tChFhfxgU6AzYjJl) now and send this message. There is also an extra 20 Token claim in two weeks, and any questions are welcome in the group.`

If this path included a prior approval step, the reply should also remind the user:

`If an approval step happened just before this, the number you should post in Telegram is still the final oath txid-1234, not the approval tx id.`

Telegram post template:

`I am with The Balancer, reference txid-1234. I have completed the formal faction oath record for Claws Temple Task 3.`

## Maintainer Details

- route: `task-3-faction-oath`
- config_path: `config/faction-proposals.json`
- active_environment: `production`
- dao_alias: `claws-temple-ii`
- formal_record: `true`
- dependency_min_version: `0.2.2`
- ca_write_dependency_min_version: `2.3.0`
- task3_execution_policy: `ca_only_ai_completion`
- task3_password_policy: `ask_once_for_ca_keystore_password`
- task3_retry_policy: `bounded_ca_retries_with_state_reconciliation`
- faction_page_label: `Faction: The Balancer`
- imagery_reference: `Claude`
- core_stance: `A rented home and a home we build ourselves are two different things.`
- ca_vote_path: `TomorrowDAO balance/allowance reads -> TomorrowDAO token approve simulate -> Portkey forward-call Approve -> TomorrowDAO vote simulate normalization -> same Portkey forward-call Vote -> receipt/log reconciliation (+ proposal my-info when available)`
- ca_transport_rule: `CA keystore may unlock the manager key, but direct target-contract send is forbidden; if TomorrowDAO direct send returns CA-forbidden, continue with explicit Portkey CA forward transport; env/private-key fallback is forbidden once CA is selected`
- blocker_label: `CA transport blocker`
