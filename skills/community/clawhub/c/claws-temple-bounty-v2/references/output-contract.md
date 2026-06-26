# Claws Temple Bounty Output Contract

Version: `0.2.17`

Use this file for every visible reply rendered through `claws-temple-bounty`.

## Language Selection

Resolve `output_language` before rendering:

1. explicit user instruction wins
2. if the latest user request is mainly Chinese, use `zh-CN`
3. otherwise use `en`

## Monolingual Rule

- Once `output_language` is selected, keep visible fixed strings monolingual.
- Proper nouns, URLs, repository names, skill names, and file paths may remain as-is in maintainer-facing details.

## Two-Layer Response Contract

Every reply should be structured as two layers:

- default visible layer:
  - `zh-CN`: `普通用户摘要`
  - `en`: `User Summary`
- expanded maintainer layer:
  - `zh-CN`: `维护者详情`
  - `en`: `Maintainer Details`

Default behavior:

- show the default visible layer first
- keep the expanded maintainer layer collapsed unless the user asks for details
- if the host does not support collapsing, render only the default visible layer in the first reply
- in plain chat, do not render the maintainer layer at all unless the user explicitly asks for details

## Default Visible Layer

The default visible layer should include:

- current task label
- short branded explanation of what is happening
- current outcome or blocker
- next step or confirmation request
- short CTA for the next task when helpful
- `Agent` / `your agent` as the default subject across hosts

The default visible layer must not include:

- raw IDs
- proposal IDs
- transaction IDs
- dependency skill names
- repo paths
- config keys
- internal faction names

Task-specific exception:

- Task 2 replies may include the fully resolved current user's own `user ID` because the user needs a direct confirmation that queue readiness is already in place.
- Task 3 completed replies may include the mined-success `txId` because the user must repost it into Telegram as their confirmation number.

## Banned User-Facing Terms

Do not use these strings in the default visible layer:

- `aelf`
- `Web3`
- `web3`
- `blockchain`
- `chain`
- `wallet`
- `on-chain`
- `smart contract`
- `区块链`
- `链`
- `链上`
- `钱包`
- `智能合约`

Prefer branded replacements from the bundled brand lexicon.
Do not call the user's agent a lobster in normal execution replies.

## Expanded Maintainer Layer

Use the expanded maintainer layer for:

- dependency skill names
- repo names and tool names
- config file paths
- exact IDs
- environment or host blockers that still prevent a formal record submission
- resolved faction mapping data

Expanded layer rule:

- it may mention external services and dependency skill names
- it must still avoid the `aelf` brand name

## CTA Classification

Resolve `cta_type` before rendering blocker or close-out replies:

- `support`
  - a real blocker, externally stalled state, or host/runtime limitation means the agent cannot continue automatically in the current turn
  - examples: dependency self-heal already failed, missing authenticated publish capability, identity-entry setup failure, missing config, remote live-skill outage, host capability gap, or formal submission limits that block the current turn
- `none`
  - the agent can still continue by collecting missing user input
  - the issue is only a light routing correction or an unfinished user choice
  - the user is waiting, but not genuinely stuck yet

Hard rules:

- append support CTA only when `cta_type = support`
- do not mix support CTA with ordinary success or next-task CTA in the same close
- support replies must show `Telegram first, then X`

## Dependency Self-Heal Rules

For Task 1 through Task 3, treat `missing dependency` and `dependency version below minimum` as self-heal cases before any blocker reply.

Required order:

1. try automatic install, refresh, or upgrade first
2. if the host cannot do that automatically, give explicit install or upgrade guidance
3. only append support CTA after self-heal or guidance still cannot unblock the task

Portable dependency sources:

- source catalog: `config/dependency-sources.json`
- default sources use public HTTPS repo URLs
- optional local overrides:
  - `CLAWS_TEMPLE_AGENT_SPECTRUM_SOURCE`
  - `CLAWS_TEMPLE_RESONANCE_CONTRACT_SOURCE`
  - `CLAWS_TEMPLE_TOMORROWDAO_SOURCE`
  - `CLAWS_TEMPLE_PORTKEY_CA_SOURCE`

## Support CTA Strings

Use these strings when `cta_type = support`.

### `zh-CN`

- `→ 如果这里卡住了，欢迎到 [Telegram 群](https://t.me/+tChFhfxgU6AzYjJl) 贴出你当前的步骤、报错和关键信息，我们可以一起帮你排查。`
- `→ 也可以去 [X / Twitter](https://x.com/aelfblockchain) 发帖求助，带上你当前的状态和卡点，方便社区更快看到并协助你。`

### `en`

- `→ If you're stuck here, join the [Telegram group](https://t.me/+tChFhfxgU6AzYjJl) and share your current step, error, and key context so the community can help troubleshoot.`
- `→ You can also post on [X](https://x.com/aelfblockchain) with your current status and blocker so others can spot it and help faster.`

## Task Framing Rules

### Roadmap Replies

- frame the five-task path as the journey that lets the user's Agent go out into the wild and make friends
- state that Task 1 through Task 3 can be completed in this path
- state that Task 4 must be completed in the SHIT Skills native flow for the qualification path
- state that the default recommended Task 4 action is `publish`
- state that the current repository now routes Task 3 through the formal faction oath record path
- state that Task 5 is optional
- when helpful, mention that rewards are already at `20+ AIBOUNTY`
- recommend Task 1 first if no progress is known

### Task 1 Replies

- preserve both dependency visual blocks: the hexagon block and the coordinate card
- frame Task 1 as learning what shape the user's Agent really is
- show a coordinate card
- show a hexagon or six-axis visual block before the coordinate card
- translate faction or type wording into the selected brand language
- keep the Task 1 brand wrapper thin; do not replace the dependency output with a card-only local template
- if the dependency skill is missing or below the required runnable state, try dependency self-heal first
- if the host cannot auto-install or auto-upgrade, give explicit install guidance before any support CTA
- if dependency self-heal or the scoring run still cannot continue, explain the blocker and append support CTA
- end with a CTA toward Task 2

### Task 2 Replies

- frame Task 2 as helping the user's Agent find a more compatible partner
- open with one short execution line that the preparation and matching work is being advanced by the agent automatically, and that the user will only be asked for one status confirmation or one key input when needed
- explain whether the user is looking for `targeted match` or `open partner search`
- keep the default visible layer in execution-report voice rather than checklist voice; prefer `我先帮你确认 / 我先自动解析 / 接下来我会继续` style wording in Chinese and equivalent action-first wording in English
- confirm identity-entry readiness and signed-in readiness with the minimum number of visible questions possible before moving into pairing
- if the user is first-time, explain that the smoother identity-entry path starts with sign-up or first-time setup before the pairing flow and ends with a usable `user ID`
- if the user is returning but not currently signed in, explain that the smoother identity-entry path starts with recovery sign-in before the pairing flow and ends with a usable `user ID`
- if identity entry and sign-in are ready, auto-resolve the current user's own `user ID` instead of asking the user to type it manually
- only show the current user's `user ID` when the current-turn dependency result actually returned that value; do not reuse remembered values, example literals, or placeholders as if they were real runtime output
- once the current-turn dependency result resolves the current user's `user ID`, show the full value in the visible layer as the Task 2 queue-readiness confirmation
- if there is no current-turn dependency result yet, do not claim queue-readiness and do not show any concrete `user ID`
- if the user chooses `targeted match`, ask for the other user's `user ID`
- if the user does not already have a concrete partner, explain that `open partner search` is the automatic queue-matching path and does not need a preselected target
- if `resonance-contract` is missing or below `4.0.0`, try dependency self-heal first
- do not ask the user to provide their own install source when `resonance-contract` is missing or below `4.0.0`
- if the host cannot auto-install or auto-upgrade `resonance-contract`, give explicit install or upgrade guidance before any support CTA
- if dependency queue preflight can proceed, continue into the formal queue path and do not suggest skipping Task 2 or replacing queue with social posting
- treat the Task 2 path as stable enough for Task 3 once the queue join is active or the direct pair submission has been sent
- if the user provides `email`, `Address`, nickname, `tDVV` address, or another non-`user ID` input for targeted match, correct the input naturally and offer `provide the other user's user ID` or `switch to open partner search`
- keep `CA only`, `counterparty_ca_hash`, and `queue` inside maintainer-facing details; the default visible layer should say `user ID`
- do not tell the user to look in legacy community-brand wording, extra platform names outside Telegram and X, or any address-based source; if the user is stuck, point them to the clickable Telegram / X links instead
- if registration, recovery sign-in, user-ID auto-resolution, dependency self-heal, identity-entry setup, or the pairing path is externally blocked and the user cannot continue automatically, translate the blocker into `身份入口 / 用户ID 未准备好` style wording and append support CTA
- end with a CTA toward Task 3 when the path is stable

### Task 3 Replies

- frame Task 3 as choosing a faction the user's Agent actually believes in
- frame the default visible layer as agent-managed execution status; checks, authorization, submission, and confirmation should sound like work already being advanced by the agent
- present only branded faction names in the visible layer
- distinguish the stage clearly:
  - `selected`
  - `waiting for tokens`
  - `ready to oath`
  - `submitted`
  - `completed`
- say which stage the user is in and what is still missing
- before vote submission, verify that `tomorrowdao-agent-skills >= 0.2.2`, `portkey-ca-agent-skills >= 2.3.0`, and the configured generic token-balance tool are available
- if `tomorrowdao-agent-skills` is missing or below `0.2.2`, try dependency self-heal first
- if `portkey-ca-agent-skills` is missing or below `2.3.0`, try dependency self-heal first
- if the host cannot auto-install or auto-upgrade either dependency, give explicit install or upgrade guidance before any support CTA
- use `task3_execution_policy = ca_only_ai_completion`
- use `task3_password_policy = ask_once_for_ca_keystore_password`
- use `task3_retry_policy = bounded_ca_retries_with_state_reconciliation`
- resolve a usable `CA` signer before any oath write; if the current context is not `CA`-ready, stop with a blocker and support CTA instead of switching to another route
- if the `CA` signer exists but the keystore password is missing, ask the user for that password only once and then continue automatically
- when the user-facing status is still healthy, make it clear that the user does not need to manually handle the checks, authorization, submission, or confirmation steps
- if the `CA` keystore unlocks a manager key, treat that manager key only as part of the verified `CA` write path; it must not authorize direct target-contract send by itself
- once `CA` is selected, direct target-contract send and env or private-key fallback are forbidden for Task 3 writes
- before vote submission, verify that the user's `AIBOUNTY` balance is at least the configured vote amount
- if the user's balance is below the configured vote amount, move to `waiting for tokens` and suggest either returning after Task 2 pairing succeeds or inviting friends to pair
- treat `waiting for tokens` as a normal unmet-threshold state with `cta_type = none`; do not append support CTA unless the balance check itself is externally blocked
- when the current signer path is `CA`, verify that the configured generic token-allowance tool is available and check the current `AIBOUNTY` allowance against the current vote contract
- when the allowance is below the configured vote amount, explain in the visible layer that one more authorization step is needed, derive `Approve` through `tomorrowdao_token_approve --mode simulate`, send it through `portkey_forward_call`, then re-check allowance before each retry
- if TomorrowDAO direct send for a resolved `CA` signer returns `SIGNER_CA_DIRECT_SEND_FORBIDDEN`, continue through the explicit Portkey CA forward transport instead of treating that as the final blocker
- stop with an unsupported `CA` transport blocker only when the explicit Portkey CA forward transport cannot continue automatically in the current host
- for `Vote`, treat `vote_payload.proposal_id_field = proposalId` as the dependency-tool input alias for `tomorrowdao_dao_vote`, not as a raw contract ABI field name
- when using the dependency tool, pass `proposalId` exactly as configured and let the dependency normalize it to the underlying `votingItemId`; do not raw forward-call the DAO `Vote` contract with an unnormalized `proposalId` payload
- derive the final `Vote` payload through `tomorrowdao_dao_vote --mode simulate`, then send that exact normalized payload through `portkey_forward_call`
- after a successful `Approve`, prefer the same verified Portkey CA forward transport for the final `Vote` instead of switching to a different write path
- for `Approve`, retry at most 3 times with state reconciliation before each attempt; if allowance is already sufficient after a timeout, continue directly to `Vote`
- for `Vote`, retry at most 3 times; before each retry, re-check proposal availability, allowance, and primary state signals from `tx receipt`, `logs`, and allowance or balance deltas
- treat `proposal my-info` as an auxiliary source; if it is unavailable or returns no user record, continue with receipt and log based reconciliation instead of failing the flow immediately
- if a non-preferred vote path returns `NODEVALIDATIONFAILED` with `Insufficient allowance` after allowance is already sufficient, switch back to the same verified `CA` write transport that already succeeded for `Approve`
- if `proposal my-info` already shows the vote state change but the receipt is not final yet, keep the user in `submitted` and continue confirmation polling instead of declaring failure
- keep approval tx details in maintainer-facing details unless the user explicitly asks; the `completed` close should still use the final vote `txId`
- use `submitted` after the final vote has been sent but before mined-success receipt confirmation is available
- in `submitted`, explain that the oath is waiting for final public-record confirmation and keep `cta_type = none` unless monitoring itself is externally blocked
- only move to `completed` after the vote returns a mined-success `txId`
- in `completed`, include the `txId`, the Telegram group CTA, one separate reminder sentence for the two-week extra 20 Token note, and then the fixed Telegram post template
- keep the fixed Telegram post template free of bonus-note or discussion-note wording; those belong in the success prompt sentence, not inside the template body
- if the current mapping is the production config, say clearly in the visible layer that this is the formal faction oath record
- never present `Portkey App`, `EOA`, `ManagerForwardCall`, raw spender addresses, or a manual fallback choice in the visible layer
- if the mapping exists but the current environment cannot continue the oath flow, the allowance step still cannot be completed after bounded retries, or the dependency contract is missing, explain the blocker and append support CTA

### Task 4 Replies

- state clearly that the user is entering the native SHIT Skills flow
- frame the default visible layer as an agent-managed native handoff, and say that the agent will keep the flow moving until it still needs an action choice, account status, or repo prerequisite from the user
- keep the visible layer playful but one notch calmer than README-level marketing; `weird`, `funny`, or `worth roasting` is preferred over stronger wording
- ask which native action the user wants right now
- if the user is following the bounty default path and has not chosen an action yet, recommend `publish`
- say clearly that `publish` is the default qualification action in the bounty path, while other native actions are auxiliary unless campaign rules say otherwise
- ask whether the user already has a SHIT Skills account; if not, route them into registration or sign-in first
- require a publishable `GitHub repo URL` only when the chosen native action actually needs it
- gather the native publish fields only when the chosen native action actually needs them:
  - `title`
  - `summary`
  - `githubUrl`
  - `tags`
  - `installType`
  - `installCommand` or `installUrl`
  - optional `content`
  - optional `coverUrl`
- allow native platform actions such as publish, edit, delete, comment, vote, like, and parse GitHub `SKILL.md`
- do not use a local `prepared / published / commented / completed` stage model for Task 4
- do not claim that the local bounty skill itself has completed Task 4; only say which SHIT Skills native action is ready, blocked, or confirmed
- if the user chose a repo-dependent action but does not have a publishable `GitHub repo URL`, explain that the action is still missing a prerequisite and keep `cta_type = none`
- if registration or sign-in is the next normal step, keep `cta_type = none`
- if registration, sign-in, authenticated publishing, or live remote loading is truly blocked, explain the blocker plainly and append support CTA

### Task 5 Replies

- present Task 5 as optional
- frame it as sending a signal so more partners can spot the user's Agent
- frame it as reach or community impact, not as a blocker
- when the visible layer mentions sending now on `Telegram` or `X`, first explain that the agent drafts the content first, and that direct send continues only if the current host really has the needed permissions and capability; otherwise the last click belongs to the user
- if the current host is `OpenClaw`, the platform is already `Telegram` or `X`, and the user explicitly wants to send now, the visible layer may add one short browser-action hint after the host-capability caveat
- keep that browser-action hint as an `OpenClaw`-only convenience, not as a general default for other hosts
- do not mention browser action before the user chooses a platform or when the user only wants draft copy
- if the user explicitly wants to send the signal now but the platform or current context blocks that action, append support CTA

## Expansion Triggers

Expand the maintainer layer when the user explicitly asks for:

- `展开详情`
- `维护者详情`
- `technical details`
- `show raw data`
- `debug`
- `config`
- exact proposal mapping

Do not expand it proactively in plain chat just because the host lacks collapsible UI.

## Example Close

Suggested close for `zh-CN`:

- `如果你想继续，我可以直接带你进入下一项任务。`

Suggested close for `en`:

- `If you want, I can take you straight into the next task.`
