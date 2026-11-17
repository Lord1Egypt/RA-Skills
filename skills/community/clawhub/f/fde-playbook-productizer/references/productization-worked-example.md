# Complete example of productization

## Evidence of three deliveries

- Customer A: SaaS billing customer service, generates a draft response with policy basis;
- Customer B: Insurance customer service, generates a draft explanation with terms and conditions;
- Customer C: Enterprise IT service desk, generates troubleshooting draft with knowledge base basis.

Common points: frontline personnel handle high-frequency text ticket and need to generate auditable drafts from versioned knowledge and customer context; the output must be based on evidence, and high-risk actions must be confirmed by humans.

Differences: Domain policy, client system, risk level, output wording, and escalation rules.

## Asset Decision

Don’t just make a “universal auto-responder product”. Split into:

1.`evidence-grounded-draft` agent skill core;
2. Versioned knowledge retrieval and source display mode;
3. Read-only client context connector interface;
4. Industry policy, field mapping and upgrade rule configuration layer;
5. Ticket draft evaluation set construction script;
6. Delivery playbook from POC to small-scale adoption.

## Maturity

- Skill core: P2 has been verified and requires new FDE reuse testing;
- CRM Connector: P1 candidate, APIs vary greatly among customers;
- Evaluation set script: P2 verified;
- Automatic sending: not productized, unauthorized action and risk evidence are not supported.

## Reuse test

An FDE who was not involved in the original project completed discovery to POC design for Client D using the assets. It was found that the "Knowledge Version Conflict" configuration instructions were missing and passed after being supplemented. The asset is promoted to "verified" within the team and has not yet met corporate standards.

## Product Roadmap Feedback

It is recommended that platform products provide unified source citations, knowledge versions, manual confirmation and audit capabilities; the evidence comes from three deliveries and does not include customer-specific policy content.
