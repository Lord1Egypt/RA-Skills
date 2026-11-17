# Complete example of problem discovery

## Original dictation

"We have a lot of customer service tickets. If we want to build an agent to automatically reply, it would be best if we can also automatically close the tickets."

## Content that should not be accepted immediately

- "Auto-reply" is the solution;
- "Automatic shutdown" involves high-risk write operations;
- "There are many ticket" has no defined metric;
- It is unknown which ticket type, which user, and what business impact is most important.

## Supplementary evidence

- A total of 12,480 ticket in the past 8 weeks, of which 31% were bill explanations;
- Median first response for billing is 6.4 hours, SLA is 4 hours;
- 42% of responses require querying the knowledge base, and 37% require reading customer levels;
- 18% due to rework using old policy templates;
- 4 customer service followers showed that the actual process spanned three systems: ticket, CRM and knowledge base;
- The customer service executive is willing to provide 500 de-identified tickets and 5 trial people, but does not allow automatic routing or closing.

## Problem statement

After the bill explanation ticket is queued, frontline support agents needs to combine the customer level and the latest policy to generate an auditable response; currently, information needs to be found across three systems, and old policy references lead to rework, making the first response exceed the SLA. The evidence comes from ticket logs, follow-up and support supervisor confirmation.

## Hypothesis to be verified

- H-001: Automatically retrieve and generate basis-based drafts to reduce query time;
- H-002: Customer service is willing to review the draft instead of writing it from scratch;
- H-003: Read-only CRM and knowledge base are sufficient to cover POC;
- H-004: Time savings are not offset by the cost of additional reviews.

## non-target

- Not sent automatically;
- Do not automatically close or modify the status of ticket;
- Does not handle refunds, complaint escalations and legal disputes;
- Does not demonstrate full ticket or production scale performance.

## Suggestions

Entering the POC contract, the scope is limited to bill interpretation draft assistance; data permissions, quality thresholds, manual confirmation and stop conditions must be frozen.
