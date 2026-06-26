# Task 2 Resonance Partner Flow

Use this flow for Task 2 or any partner-finding request.

## Dependency

- required dependency skill: `resonance-contract`

## Goal

Guide the user toward a branded resonance partner flow, including first-time registration, returning-user recovery sign-in, auto-resolving the current user's own user ID, and the choice between targeted match and open partner search, without re-implementing pairing logic. This is the step where the user's Agent goes looking for a more compatible partner, and the visible layer should feel like an execution update rather than a user checklist.

## Steps

1. Open with one short execution line that the preparation and matching work will be advanced by the agent automatically, and that the user will only be asked for the minimum required status confirmation or key input.
2. Identify whether the user already has a specific partner target.
3. Before any targeted-match or queue action, ask one short readiness question that covers both whether this is the first time here and whether the user is already signed in this time.
4. If the user is returning but not currently signed in, route them into recovery sign-in first.
5. If the user is first-time, or the identity entry is not fully ready, route them into identity-entry setup first.
6. If the user is first-time, explain that the smoother entry path starts with registration or first-time setup and ends with a usable `user ID`.
7. If the user is returning but not currently signed in, explain that the smoother entry path starts with recovery sign-in and ends with a usable `user ID`.
8. If `resonance-contract` is missing or below `4.0.0`, first try the bundled self-heal helper `../../scripts/self-heal-local-dependency.sh resonance-contract`.
9. If that helper cannot run in the current host, use the portable source catalog in `../../config/dependency-sources.json` and return explicit install or upgrade guidance with the repo URL and env override name.
10. Do not ask the user to provide an install source for `resonance-contract`.
11. If the current host still cannot auto-install or auto-upgrade the dependency, return explicit install or upgrade guidance before any support CTA.
12. Once identity entry and sign-in are ready, auto-resolve the current user's own `user ID` from the dependency context instead of asking the user to type it manually.
13. Only show the current user's `user ID` when the current-turn dependency result actually returned that value; never reuse remembered values, example literals, or placeholders as if they were real runtime output.
14. If that current-turn user-ID resolution succeeds, show the full resolved current-user `user ID` in the visible layer so the queue path can be confirmed.
15. If that user-ID resolution fails, or there is no current-turn dependency result yet, keep the user in the identity-entry or recovery branch, do not ask the user to paste their own `user ID`, and do not claim queue-readiness.
16. If the user has a specific partner target, route into `targeted match`.
17. In `targeted match`, ask for the other user's `user ID`.
18. If the user does not have a specific target, route into `open partner search`.
19. Explain plainly that `open partner search` is the automatic queue-matching path and does not require a preselected target.
20. Invoke `resonance-contract` only after identity-entry readiness, sign-in readiness, the auto-resolved current-user `user ID`, and the participation mode are clear.
21. If dependency queue preflight can proceed, continue into queue send and do not suggest skipping Task 2, replacing queue with Telegram or X posting, or claiming there is no usable direct tool.
22. Treat the Task 2 path as stable enough for the Task 3 handoff when either the direct pair submission has been sent or the queue join is active. Do not promise that a real partner has already been found unless the dependency flow actually returned that result.
23. If the user provides `email`, `Address`, nickname, `tDVV` address, or other non-`user ID` input for targeted match, correct the input in plain language and offer two next steps: provide the other user's `user ID`, or switch to `open partner search`.
24. If registration, recovery sign-in, dependency self-heal, identity-entry setup, or the pairing path is genuinely blocked and the agent cannot continue automatically, return a blocker summary and append support CTA.
25. Rewrite the visible output into the Claws Temple partner language.
26. End with a CTA toward Task 3 once the partner path is stable.

## Required Visible Output

- task label
- one short execution line that the agent is already advancing the preparation and matching work
- identity-entry readiness prompt
- sign-in or recovery prompt
- first-time registration or first-time setup wording
- returning-user recovery sign-in wording
- wording that asks in direct user language whether this is the first time here or a returning-but-not-signed-in visit
- visible confirmation that the current user's `user ID` was auto-resolved
- `targeted match` vs `open partner search`
- wording that `open partner search` is the automatic queue-matching path
- plain-language explanation of what happens next
- brand wording such as `共振伙伴` or `resonance partner`
- first-time user wording such as `先开通身份入口`
- wording such as `如果你是老用户但这次还没登录，我会先带你完成恢复登录`
- wording that the smoother entry path ends with a `用户ID / user ID`
- wording such as `我会先自动解析你当前的用户ID，不需要你自己手动填写`
- wording such as `这一步里的准备和匹配动作由我来自动推进；我只会在必要时向你确认一个状态或补一个关键信息。`
- wording such as `我先帮你确认一个最小前置：你这次是第一次来、老用户但这次还没登录，还是已经可以直接继续`
- wording such as `已解析到你的用户ID`
- wording that this confirmation is allowed only after the current-turn dependency result really returned the value
- targeted-match wording such as `请提供对方的用户ID`
- wording such as `如果你没有具体对象，就直接走开放寻配，这条路就是系统自动排队匹配`
- wording such as `如果依赖版本过低，我会先帮你升级，不会先让你提供安装源`
- wording such as `只要开放寻配已经正式入队，或指定匹配请求已经发出，我就会把 Task 2 视为路径已稳定，可以继续 Task 3`
- wording that Task 2 can hand off to Task 3 once the pairing path is stable, without falsely claiming a partner is already found
- wording that queue should continue once onboarding is ready, instead of skipping Task 2 or replacing it with social fallback
- blocker summary plus support CTA when the user is genuinely stuck
- next-step CTA toward faction belonging

## Maintainer Notes

- dependency-specific account routing, local-context preparation, and read-before-write logic stay inside the dependency skill
- the dependency write path is `CA only`, but the default visible layer should not say `CA`, `AA`, or `EOA`
- the dependency contract is now aligned with `resonance-contract 4.0.0`; there is no user-side `EOA` route to preserve in this skill
- user-facing `identity entry` maps to dependency local account-context readiness; first-time setup may create that context, while returning-user recovery sign-in may restore it
- the current user's own `用户ID / user ID` should be auto-resolved from dependency context once onboarding is ready; the user should not be asked to type it manually for queue participation
- never treat example formatting, remembered values, or placeholder literals as proof that the current user's `user ID` has been resolved
- the visible layer may show the current user's `用户ID / user ID` only when the current-turn dependency result actually returned it
- user-facing `用户ID / user ID` maps to dependency `ca_hash`
- user-facing `targeted match` maps to dependency direct pair with `counterparty_ca_hash`
- user-facing `open partner search` maps to dependency `queue`
- if dependency queue preflight can proceed, do not replace the flow with Telegram or X outreach and do not suggest skipping Task 2
- dependency install or upgrade guidance should come from `../../config/dependency-sources.json`, not from a machine-specific path
- do not mention legacy community-brand wording, legacy platform names outside Telegram and X, legacy runtime-address wording, or address-based matching in the visible layer
- do not accept `email`, `Address`, or nickname as a direct-match identifier
- keep raw method names and execution details out of the visible layer
- keep the default visible layer in execution-report voice; do not dump the full branch tree before the minimum user decision is actually needed
