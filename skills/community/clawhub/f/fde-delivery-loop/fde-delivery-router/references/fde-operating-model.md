# FDE run model

## Purpose

Without changing the professional division of labor of eight stages, it provides users with easy-to-understand global navigation, Echo–Delta collaboration perspective, four-dimensional integrity check, and portraits of different FDE projects.

## Three stages and eight stages mapping

| Big stage | Corresponding links | Core issues | Exit signal |
|---|---|---|---|
| Discovery and alignment | 1 problem discovery, 2 POC contract | Whether the problem is real and worthy of verification, and whether both parties agree on the scope and evidence | Evidenced problem discovery package and executable POC contract |
| Design and Verification | 3 PRD, 4 Architecture, 5 Skill Design, 6 POC Operation | Can it be built safely and freeze criteria met in real or controlled scenarios | Auditable evidence of operation and conclusion to continue, adjust or stop |
| Adoption and productization | 7 adoption value, 8 productization | Whether users change behavior, whether it generates value, which experiences are worth reusing | Adoption and investment decisions, reusable delivery assets |

Three-stage names may not be used in place of specific skills. When routing, "big stage + current link" is output at the same time, such as "Design and Verification/Stage 4 Deployment Architecture".

## Echo–Delta Dual View

| Perspective | Main concerns | Common evidence | Common blind spots |
|---|---|---|---|
| Echo: Customer site and value | User tasks, informal processes, stakeholders, trust, adoption, business impact | Interviews, observations, ticket, baselines, usage behavior, business confirmation | Premature acceptance of technical solutions proposed by customers; only listening to management without looking at frontline work |
| Delta: Engineering Implementation and Operations | Specifications, data, models, system integration, security, testing, deployment and operations | Interfaces, samples, architectural decisions, test traces, logs, costs and events | Declaring success when technical metrics are passed; ignoring change management and real adoption |

### Dominant relationship of each ring

| Link | Dominance | What must be checked from another perspective |
|---|---|---|
| 1 Problem Discovery | Echo | Delta checks whether the evidence is sufficient to form a verifiable technical problem and does not commit to the solution |
| 2 POC contract | Echo–Delta joint | Echo guards business results, Delta guards feasibility and risk boundaries |
| 3 PRD | Common | Echo confirms tasks and results, Delta confirms achievable and testable |
| 4 Deployment Architecture | Delta | Echo Check whether the solution changes the user flow or adds unacceptable burden |
| 5 Skills Design | Delta | Echo Check Responsibilities, Language, Manual Escalation, and Trust Boundaries |
| 6 POC Run | Delta Organization Run | Echo ensures real users, real tasks and business explanations are not replaced by demos |
| 7 Adoption and Value | Echo | Delta provides reliability, cost, support and production gap evidence |
| 8 Productization | Common | Echo identifies cross-customer task commonalities, Delta identifies stable technology core and configuration boundaries |

When the project does not have a position named Echo or Delta, designate the person with the corresponding responsibility and do not omit the perspective due to the absence of the position.

## Four-dimensional integrity check

| Dimensions | Required questions | Typical delivery evidence |
|---|---|---|
| Customer Delivery | Who uses what workflow? Who decides, blocks, and supports? How is adoption and value proven? | Stakeholder map, process, contract, adoption funnel, value metrics |
| Software Engineering | Are functions, interfaces, exceptions and tests achievable? How are technical debt, versions and code quality managed? | PRDs, tests, code, releases, defects and technical debt |
| Data and AI | Does the data represent real tasks? How are models or rules evaluated? How to deal with failure and drift? | Data contracts, evaluation sets, trajectories, error classification, costs |
| Systems & Cloud | Are identity, network, integration, deployment, monitoring, rollback and operational responsibilities clear? | Architecture, IAM, deployment records, monitoring, runbook, RACI |

Each dimension is marked as "Covered/Partially Covered/Blocked/Not Applicable" with evidence. A dimension should not be removed from the project because it does not fall within the current FDE's personal expertise; collaborators or escalation paths should be designated.

## FDE project portrait

First select a portrait according to the objects that the customer wants to deploy and the main failure modes; for mixed projects, you can select a primary portrait and a secondary portrait.

### AI model deployment type

- Focus: Model behavior, retrieval or tools, evaluation sets, guardrails, costs, drift and manual upgrading.
- Common blocking: no representative samples; only looking at average scores; unable to replay trajectories; using POC model configuration directly for production.
- Focus on calling: Rings 5 and 6, and let Stage 4 cover model vendors, data boundaries, and observability.

### Data platform type

- Key points: data provenance, ownership, quality, lineage, schema changes, backfilling, timeliness and access control.
- Common blocking: The source of system records is unclear; the sample and production scale are too different; the responsibility for data repair is unclear.
- Focus on calling: Rings 1, 4, and 6, and add data acceptance criteria in Stage 3.

### Enterprise workflow type

- Focus: Roles, system switching, business rules, exceptions, approvals, integrations, change management and adoption.
- Common blocking: only normal paths are covered; write operations exceed authority; new processes increase user burden; management supports but does not use the front line.
- Key calls should be made to: Rings 1, 3, 4, and 7.

### Live and edge type

- Focus: Network instability, hardware, offline, physical security, on-call, training, spare parts and on-site incidents.
- Common blockers: Bringing cloud assumptions to the edge; inability to diagnose remotely; lack of manual safe shutdown and on-site recovery processes.
- Should focus on calling: Rings 4, 6, 7, and upgrade hardware, security or industry expert review.

## Routing output supplement

The following content is added to the routing output of complex projects:

```markdown
- Three stage locations:
- Current session:
- Main/Sub-Project Portraits:
- Echo viewing angle gap:
- Delta viewing angle gap:
- Four-dimensional blocking term:
- The only next action:
```

Only output when these fields change routing or risk judgment, do not repeat existing content for the sake of form.
