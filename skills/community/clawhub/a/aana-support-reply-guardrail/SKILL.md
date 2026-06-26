# AANA Support Reply Guardrail Skill

Use this skill when an OpenClaw-style agent may draft, revise, send, summarize, or approve a customer support reply.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Customer support replies should be helpful without inventing account facts, promising outcomes the agent cannot verify, overstating policy, or exposing private data.

The agent should separate:

- facts provided by the customer,
- facts available from authorized support tools,
- policy text actually available to the agent,
- missing facts that require lookup or escalation,
- private data that should be minimized or redacted,
- actions the agent can safely take,
- actions that require human or system approval.

## When To Use

Use this skill before:

- sending or drafting support emails, chats, tickets, or helpdesk replies,
- answering refund, cancellation, charge, subscription, delivery, warranty, eligibility, or account questions,
- summarizing customer records or ticket history,
- making policy, billing, payment, legal, health, account, shipping, or entitlement claims,
- using customer data to personalize a reply,
- apologizing for facts that are not verified,
- promising refunds, credits, replacements, exceptions, escalations, timelines, or outcomes.

## Support Risk Classes

Treat these as higher risk:

- refund, credit, chargeback, cancellation, subscription, or billing promises,
- policy interpretation, exception handling, eligibility, warranty, or legal claims,
- account status, delivery status, order status, identity, address, payment, or private ticket history,
- health, legal, financial, employment, student, family, or personal support contexts,
- replies that reference internal notes, private records, another person's data, or sensitive attachments,
- responses that may bind the organization to an action, timeline, promise, or admission.

## AANA Support Reply Loop

1. Identify the customer request and the reply the agent is about to send.
2. Classify claims: customer-provided, tool-verified, policy-backed, inferred, unsupported, private, or promissory.
3. Check account facts: do not invent order status, subscription state, billing outcome, refund eligibility, identity, or timeline.
4. Check policy claims: cite or paraphrase only policies actually available; avoid overstating exceptions or guarantees.
5. Check promises: do not promise refunds, credits, replacements, cancellations, escalations, callbacks, or legal outcomes unless authorized.
6. Check privacy: remove unnecessary private details and avoid exposing another person's data.
7. Choose action: accept, revise, ask, retrieve, defer, refuse, or route to human review.

## Required Pre-Flight Checks

Before sending a support reply, verify:

- the customer-visible task,
- the exact account or order facts being asserted,
- whether each important claim is supported by tool evidence, customer-provided text, or policy,
- whether the reply includes a promise, guarantee, admission, exception, or outcome,
- whether the user is authorized to receive the private details included,
- whether sensitive details can be minimized,
- whether the answer should ask for more information or defer to a support system.

## Invented Fact Rules

Revise or defer if the reply claims unsupported facts such as:

- "Your refund has been approved."
- "Your account was cancelled."
- "Your package will arrive tomorrow."
- "The charge was a mistake."
- "You are eligible for a replacement."
- "Your subscription is active."
- "We called you earlier."
- "Your case is resolved."

Safer alternatives:

- "I do not have enough verified information to confirm that yet."
- "Please check the account record before confirming eligibility."
- "Based on the details provided, the next step is..."
- "I can help route this for review."

## Refund And Policy Promise Rules

Do not promise:

- refunds,
- credits,
- replacements,
- charge reversals,
- cancellation completion,
- policy exceptions,
- legal or compliance outcomes,
- delivery dates,
- callback or escalation timelines,
- compensation.

Unless the agent has explicit authorization from a reviewed system or human, use conditional language:

```text
The support team can review whether this qualifies.
I can help submit the request for review.
Eligibility depends on the account record and policy review.
```

## Private Data Rules

Minimize or remove:

- account IDs, order IDs, addresses, phone numbers, emails, payment details,
- billing history, invoices, balances, subscriptions, and payment methods,
- private ticket notes, internal comments, attachments, screenshots, logs,
- another person's account or support history,
- health, legal, financial, employment, school, family, or personal details.

Do not include raw secrets, credentials, full payment numbers, private messages, or unrelated account details.

## Tone And User Experience

Use clear, calm, customer-facing language:

- acknowledge the issue without admitting unverified fault,
- state what is known and what is not known,
- offer the next safe step,
- avoid blaming the customer,
- avoid legalistic overclaims,
- avoid fake certainty.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `task_summary`
- `reply_summary`
- `claim_support_status`
- `refund_or_policy_promise_status`
- `private_data_status`
- `authorization_status`
- `recommended_action`

Do not include raw account records, payment data, private messages, health records, legal records, credentials, or full ticket history when a redacted summary is enough.

## Decision Rule

- If all important claims are supported, private data is minimized, and no unauthorized promise is made, accept.
- If the reply is useful but includes unsupported facts, policy overclaims, or unnecessary private data, revise.
- If the reply needs customer clarification or identity/context confirmation, ask.
- If the reply needs account lookup, policy lookup, supervisor approval, or human review, defer.
- If the request asks to expose unauthorized private data or make a false claim, refuse and explain briefly.
- If a checker is unavailable or untrusted, use manual support-reply review.

## Output Pattern

For support-sensitive replies, prefer:

```text
Support reply review:
- Claim support: ...
- Refund/policy promises: ...
- Private data: ...
- Missing facts: ...
- Decision: accept / revise / ask / defer / refuse
```

Do not include this review block in the customer-facing reply unless needed by the support workflow.
