# Task 5 Social Signal Flow

Use this flow for Task 5 or any optional public signal request.

## Dependency

- use `resonance-contract` when a structured pairing handoff is needed
- otherwise direct drafting inside this skill is acceptable

## Goal

Help the user send a public signal on Telegram, X, or the Curio Board without treating this task as mandatory. This is the step where more partners can finally spot the user's Agent. The visible layer should first frame the agent as the drafter, and only promise direct send when the current host really has the required permissions and capability.

## Steps

1. Remind the user this task is optional.
2. Ask which platform the user wants if the platform is still unknown.
3. Draft a short branded signal.
4. If the user already has a coordinate card or faction result, fold that into the signal.
5. Whenever the visible layer mentions sending now on `Telegram` or `X`, first add one short boundary line: the agent drafts first, direct send continues only if the current host really has the required permissions and capability, and otherwise the final send click belongs to the user.
6. If the current host is `OpenClaw`, the user already chose `Telegram` or `X`, and the user explicitly wants to send now, add one short visible-layer hint that browser action can be used directly in `OpenClaw` after that host-capability caveat.
7. Do not mention browser action before the user has chosen a platform, when the user only wants draft copy, or in hosts other than `OpenClaw`.
8. If the user explicitly wants to send the signal now but the current context blocks that action, return a blocker summary and append support CTA.
9. End with a community-reach framing instead of a blocker framing when the signal path is otherwise healthy.

## Platform Templates

- `TG`: slightly longer, conversational, may use 2 short paragraphs and a clear reply CTA; when practical, point the user to the clickable `Telegram group` link
- `X`: one compact post, keep it within a short single-post format; when practical, point the user to the clickable `X` link
- `Curio Board`: slightly more descriptive, may mention what kind of resonance partner the user wants
- `OpenClaw host hint`: when the user already chose `TG` or `X` and wants to send now, the visible layer may say that browser action can be used directly in `OpenClaw`

Each platform draft should include:

- current coordinate or direction
- what kind of partner or response the user wants
- one direct CTA

## Required Visible Output

- task label
- optional-task reminder
- post copy or signal draft
- host-capability boundary wording whenever the user wants to send now on `TG` or `X`
- clickable platform links when the user asks where to post
- OpenClaw browser-action hint only when the platform is already chosen and the user wants to send now
- recommended CTA
- blocker summary plus support CTA only when the user is genuinely stuck on sending

## Maintainer Notes

- keep this task clearly separated from the main qualification path
- do not imply that Task 5 is required for unlock
- keep browser-action wording host-aware: `OpenClaw` only, `Telegram` or `X` only, and only when the user explicitly wants to send now
- never imply guaranteed auto-posting; the safe default is draft first, then direct send only when the host can really do it
