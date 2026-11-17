---
name: "discord-recipient-safety"
description: "Exact Discord recipient routing for trusted team collaboration: resolve one canonical roster entry, send to its immutable Discord ID, and verify the delivery target."
---

# Discord Recipient Routing

Use this skill before every recipient-specific Discord DM, handover, report,
assessment, or confidential-content send where an approved user says “tell
Engineer X”.

This is a collaboration-routing procedure, not a requester-authentication or
general security system. Host policy and terminal/admin controls decide which
users are trusted and allowed to instruct the agent. This skill makes sure the
message is addressed to the intended approved engineer rather than a similarly
named colleague.

## Boundaries

- Resolve the recipient only from this agent's active approved roster. Never use
  memory, prior DMs, display-name search, fuzzy matching, inferred routes, or a
  “closest” colleague.
- Keep names, Discord IDs, roster locations, and organisations out of this
  shared skill. Put them in the per-agent control manifest.
- Do not record message bodies, secrets, tokens, or unnecessary personal data.
- This skill does not authenticate the requester, intercept arbitrary sends, or
  independently prove that Discord displayed a message. It governs deterministic
  target selection and delivery-target verification.

## Required Inputs

Obtain one explicit instruction naming one recipient. Load this agent's approved
roster. The roster must map each canonical recipient name to one immutable
Discord user ID and indicate whether that recipient is active and can receive a
relay.

The agent must not infer an intended recipient from a partial name, a nickname,
a display name, or prior chat history.

## Routing Procedure

1. Match the requested recipient text exactly against the roster's canonical
   recipient name.
2. Continue only when there is exactly one active, relay-eligible match with a
   valid Discord user ID.
3. Construct the target as `user:<discordUserId>`.
4. Send the message only to that exact target. Do not substitute a channel,
   search result, display name, or another recipient.
5. Inspect the message-tool response and verify the reported target matches the
   expected exact target.
6. Record only non-content delivery evidence: requested recipient, canonical
   recipient, target ID, platform message ID when available, and delivery
   result.

If there are zero matches, multiple matches, an inactive recipient, an invalid
ID, or a missing/mismatched delivery target, send nothing and ask one targeted
clarifying question or report the mismatch.

## Delivery Contract

A recipient-specific relay may be claimed as sent only when:

- the roster yielded one exact active recipient;
- the message was addressed to that recipient's immutable Discord ID; and
- the tool response confirms the same target.

If the platform cannot expose enough non-content receipt information, state
that delivery target confirmation is unavailable. Do not claim a stronger
guarantee than the platform evidence supports.

## Integration Contract

- Trusted-user admission remains a host/workspace policy concern.
- The local approved roster is scoped to one agent/machine and is the only
  recipient authority.
- No attribution prefix, requester-identity check, pause-state file, or
  `before_tool_call` hook is required by this skill.
- Higher-risk workflows may add their own controls, but they must not weaken
  the exact-recipient rule above.

## Validation

Before release or integration, run deterministic non-production fixtures that
cover:

- one exact active recipient resolving to the expected `user:<id>` target;
- zero and multiple exact matches;
- inactive recipient;
- invalid Discord ID;
- attempted target substitution; and
- delivery-target mismatch.

## Acceptance Criteria

For “tell Engineer X”, the agent either sends to Engineer X's immutable roster
ID and verifies that target in the delivery receipt, or it sends nothing and
reports the exact ambiguity or mismatch.
