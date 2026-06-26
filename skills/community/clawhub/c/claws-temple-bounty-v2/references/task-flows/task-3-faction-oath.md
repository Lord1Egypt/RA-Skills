# Task 3 Faction Oath Flow

Use this flow for Task 3 or any faction belonging request.

## Dependency

- required dependency skill: `tomorrowdao-agent-skills`
- required dependency skill: `portkey-ca-agent-skills`

## Required Config

Always read `../../config/faction-proposals.json` before rendering the faction list or executing an oath flow.

## Goal

Present four branded factions, map the selected faction to the current formal config, keep the whole oath flow inside a `CA-only + AI-only` execution path, verify the user can fund the vote with 2 AIBOUNTY, derive exact `Approve` and normalized `Vote` payloads through TomorrowDAO simulate, execute real writes through Portkey CA forward transport, and close the flow only after a mined-success vote tx plus Telegram follow-up. The visible layer should sound like agent-managed execution status, not like a manual user runbook.

## Steps

1. Read the faction config file.
2. Present the four branded factions with one-line positioning.
3. If the user has not chosen, help them pick one in brand language.
4. Map the branded choice to the config entry.
5. Run a formal preflight:
   - confirm the selected faction entry exists
   - confirm the dependency invocation contract exists in the config file
   - confirm the TomorrowDAO dependency minimum version exists and is `0.2.2` or above
   - confirm the Portkey CA write dependency minimum version exists and is `2.3.0` or above
   - confirm the required proposal id is present
   - confirm the proposal end time is still in the future
6. Resolve the current signer or address before any token check or vote attempt.
7. Accept only a usable `CA` signer for Task 3 writes. If the current context is not `CA`-ready, stop with a branded blocker instead of switching to another signer route.
8. If the `CA` signer exists but the keystore password is missing, ask the user for the `CA keystore` password only once and then continue automatically.
9. If the current `CA` context unlocks a manager key, treat that key as part of the verified `CA` write path only; do not reinterpret it as permission for direct target-contract send.
10. If `tomorrowdao-agent-skills` is missing or below the configured minimum version, first try the bundled self-heal helper `../../scripts/self-heal-local-dependency.sh tomorrowdao-agent-skills`.
11. If `portkey-ca-agent-skills` is missing or below the configured CA write minimum version, first try the bundled self-heal helper `../../scripts/self-heal-local-dependency.sh portkey-ca-agent-skills`.
12. If that helper cannot run in the current host, use the portable source catalog in `../../config/dependency-sources.json` and return explicit install or upgrade guidance with the repo URL and env override name.
13. If the current host still cannot auto-install or auto-upgrade either dependency, return explicit install or upgrade guidance before any support CTA.
14. Check that the installed TomorrowDAO and Portkey dependency versions both satisfy the config minimums.
15. Check that the configured generic token-balance tool, generic token-allowance tool, TomorrowDAO token-approve tool, and Portkey CA forward-call tool are available.
16. Query the configured vote token balance with the configured token symbol.
17. If the balance is below the configured vote amount, stop before vote submission and move the user to `waiting for tokens`.
18. In `waiting for tokens`, tell the user to return after Task 2 pairing succeeds or invite friends to pair so they can build toward the required 2 AIBOUNTY.
19. Treat `waiting for tokens` as a normal unmet-threshold state, not as a support CTA state, unless the token-balance check itself is externally blocked.
20. Query the current allowance for the vote token against the current vote contract before sending the vote.
21. If the allowance is below the configured vote amount, first call `tomorrowdao_token_approve --mode simulate` and use its exact `contractAddress`, `methodName`, and `args` as the approval payload source.
22. Send the actual `Approve` through `portkey_forward_call`, and once one Portkey CA forward transport has already succeeded for `Approve`, keep that same verified CA forward transport as the preferred path for the final `Vote`.
23. Retry `Approve` at most 3 times using bounded backoff `3s -> 8s -> 15s`. After each attempt or timeout, re-check allowance before deciding whether another approval attempt is still necessary.
24. If allowance is already sufficient after an `Approve` timeout or uncertain receipt, continue into `Vote` instead of repeating authorization blindly.
25. Do not blindly mix a successful Portkey CA forward approval transport with a different direct vote transport. If another path is attempted and returns `NODEVALIDATIONFAILED` with `Insufficient allowance` while allowance is already sufficient, treat that as a transport mismatch and switch back to the same verified CA forward transport used by `Approve`.
26. Keep the visible layer natural during the allowance step. Tell the user that one more authorization step is being completed before the oath can be sent, but keep raw contract path and approval tx details in the maintainer layer unless the user asks.
27. Invoke `tomorrowdao_dao_vote --mode simulate` after the mapping, dependency checks, token-balance precheck, and any required approval step all pass; use the exact dependency-tool vote payload contract from the config file and do not reinterpret `proposalId` there as a raw contract ABI field name.
28. Use the normalized `tomorrowdao_dao_vote --mode simulate` result as the only source for the final `Vote` contract address and final `votingItemId` payload, then send that exact payload through `portkey_forward_call`.
29. For `Vote`, prefer receipt, event logs, and allowance or balance deltas as the primary reconciliation signals.
30. Treat `proposal my-info` as an auxiliary source only. If it is unavailable or returns no user record, continue the flow with receipt and log based reconciliation instead of failing immediately.
31. If TomorrowDAO direct send returns `SIGNER_CA_DIRECT_SEND_FORBIDDEN`, treat that as expected CA-routing evidence and continue through the explicit Portkey CA forward transport instead of stopping.
32. If `Vote` returns a timeout, validation failure, or another uncertain send result, re-check proposal availability, allowance, primary reconciliation signals, and then `proposal my-info` when available before retrying.
33. Retry `Vote` at most 3 times using bounded backoff `3s -> 8s -> 15s`.
34. If the receipt or logs already show that the vote state changed but the final confirmation is not settled yet, move the user to `submitted` and continue polling for final confirmation.
35. If `proposal my-info` also shows that the vote state changed but the final receipt is not confirmed yet, keep the user in `submitted` and continue polling instead of declaring failure.
36. Once the final vote is sent but before a mined-success receipt is available, move the user to `submitted`.
37. In `submitted`, tell the user that the oath has been sent and is waiting for final confirmation in the public record. Do not move to `completed` yet, and do not append support CTA unless receipt monitoring itself is externally blocked.
38. Treat the oath as successful only when the final vote returns a mined-success `txId` from `TxReceipt`.
39. In the success close, show the final vote `txId`, tell the user to join the configured Telegram group, give the separate bonus or discussion reminder from the config, and then render the fixed Telegram post template with `{faction_name}` and `{txId}` filled in.
40. If the config is marked as production, present the result as the formal faction oath record and do not mention testing, rehearsal, or a later record replacement.

## Required Visible Output

- task label
- the four branded faction names
- one-line faction thesis per faction
- one short execution line that checks, authorization, submission, and confirmation are being advanced automatically by the agent
- current stage or selection prompt
- token-precheck outcome when relevant
- allowance or authorization outcome when relevant
- password request wording when the `CA` keystore password is missing
- automatic retry wording when authorization or vote confirmation is still being reconciled
- submitted-state waiting explanation when relevant
- blocker summary plus support CTA when the oath cannot continue automatically
- `txId` plus Telegram follow-up prompt and template after success
- next step after the oath

## Faction Display Mapping

Load the branded faction names from `../../config/faction-proposals.json`.
Use the matching brand lexicon only for task labels, helper wording, and close-out phrasing.

## Maintainer Notes

- only the config file may carry exact proposal IDs and end times
- use the exact dependency invocation contract from `config/faction-proposals.json` instead of repeating invocation parameters in this file
- use the config file for the TomorrowDAO dependency minimum version, the Portkey CA write minimum version, token symbol, vote amount, generic token-balance tool, generic token-allowance tool, TomorrowDAO token-approve tool, Telegram success template, and separate Telegram bonus note
- `task3_execution_policy = ca_only_ai_completion`
- `task3_password_policy = ask_once_for_ca_keystore_password`
- `task3_retry_policy = bounded_ca_retries_with_state_reconciliation`
- `CA` keystore unlock may expose the manager key, but that manager key alone still must not authorize direct target-contract send
- `proposalId` in the config vote payload is the dependency-tool input alias for the configured vote tool, not a promise about the raw contract ABI field name
- if an implementation ever has to bypass the dependency tool, it must reproduce the dependency normalization from `proposalId` to the underlying `votingItemId` before any raw contract packing or forwarding
- once `CA` is selected, env or private-key fallback must not continue the write path if they would become direct target-contract send
- if TomorrowDAO direct send for a resolved `CA` signer returns `SIGNER_CA_DIRECT_SEND_FORBIDDEN`, continue with the explicit Portkey CA forward transport instead of stopping
- stop with an unsupported `CA` transport blocker only if the explicit Portkey CA forward transport is unavailable or cannot continue automatically
- do not present `Portkey App`, `EOA`, `ManagerForwardCall`, or manual route choices in the visible layer
- when the current signer path is `CA`, the fastest unblock is inside this skill: read allowance, derive `Approve` and `Vote` payloads through TomorrowDAO simulate, then send both writes through the same verified `CA` write transport, implemented here as the same verified Portkey CA forward transport
- if a different vote path returns `NODEVALIDATIONFAILED` with `Insufficient allowance` after allowance is already sufficient, treat that as a transport mismatch instead of a real allowance failure
- use `proposal my-info` as an auxiliary reconciliation helper, not as the only source of truth for vote-state confirmation
- the spender for the allowance check and approval must be the current vote contract address from the dependency runtime, not a new hardcoded visible-layer constant
- if `environment = production` and `is_test_only = false`, the visible layer should treat the selected mapping as the final formal record for Task 3
- do not repeat raw IDs in any other reference file
