# Agentic Development Services Agreement

**Contract ID:** ADSA-2026-0142  
**Agreement Date:** 2026-05-18  
**Effective Date:** 2026-05-25  
**Project:** Customer Support Email Triage Agent (Pilot)

> Demonstration notice: this template is intentionally generic and is provided only to demonstrate programmatic contract generation. It is not legal advice and should be replaced or reviewed before real use.

## 1. Parties

This Agentic Development Services Agreement (the **"Agreement"**) is entered into by and between **CompleteTech LLC**, a Limited Liability Company formed in Wyoming with offices at 30 N Gould St, Ste R, Sheridan, WY 82801, USA (**"Provider"**), and **Northwind Trading Co.**, a Corporation formed in Washington with offices at 240 Harbor Point Blvd, Suite 700, Seattle, WA 98121, USA (**"Client"**). Provider and Client may be referred to individually as a **"Party"** and together as the **"Parties"**.

| Party | Notice Details |
|---|---|
| Provider | CompleteTech LLC; 30 N Gould St, Ste R, Sheridan, WY 82801, USA; Timothy.Gregg@complete.tech; 1-844-TECH-WIN |
| Client | Northwind Trading Co.; 240 Harbor Point Blvd, Suite 700, Seattle, WA 98121, USA; legal@northwindtrading.example; +1 (206) 555-0142 |

## 2. Engagement Summary

Provider will perform agentic development services for Client under this Agreement and any written statement of work, order form, or change order signed or otherwise approved by both Parties. The initial project summary is: **Design, build, evaluate, and document a bounded agentic email-triage workflow that classifies inbound customer support email, drafts suggested replies, and routes each case to the correct queue, with human approval required before any customer-facing send.**

| Item | Current Configuration |
|---|---|
| Project name | Customer Support Email Triage Agent (Pilot) |
| System description | Multi-step support-email triage agent: intake classification, reply drafting with retrieval over approved help-center content, queue routing, logging, and a mandatory human approval gate before any outbound customer reply. |
| Autonomy level | Bounded autonomy: the agent classifies, drafts, and routes, but a support agent must approve or edit every customer-facing reply before it is sent. |
| Human review | Required before any customer-facing send, queue escalation to a human specialist, refund or credit suggestion, and any change to production routing rules. |
| Model or stack | Configurable hosted LLM API plus a retrieval index over Northwind's approved help-center articles; specific model identifiers fixed in the statement of work. |
| Deployment environment | Northwind-controlled sandbox mailbox and staging helpdesk until acceptance; production rollout only by written change order. |

## 3. Scope of Services and Deliverables

Provider will use commercially reasonable efforts to deliver the services and deliverables described in the applicable statement of work. Unless a signed statement of work says otherwise, the project includes:

- Discovery and requirements clarification for the agentic workflow.
- Architecture, prompt, tool-routing, and workflow design for the agreed use case.
- Prototype implementation in the agreed development environment.
- Evaluation artifacts, including test cases and acceptance demonstrations.
- Handoff documentation suitable for technical administrators and business stakeholders.
- Basic post-handoff support for 30 days after acceptance.

Out-of-scope services include production operations, legal compliance certification, regulated-use validation, data labeling at scale, model training, cloud hosting charges, managed security operations, procurement, and any use listed in Section 8 as excluded unless added by written change order.

## 4. Timeline, Review, and Acceptance

The target delivery schedule is: Discovery: 1 week; Prototype: 3 weeks; Evaluation: 2 weeks; Documentation and handoff: 1 week; buffer: 1 week. The Parties may adjust dates by mutual written agreement when delays are caused by dependency changes, delayed feedback, unavailable Client systems, new requirements, or change orders.

Client will review each material deliverable within 10 calendar days after delivery. A deliverable is accepted when Client approves it in writing, uses it in a non-test context, or does not provide a written rejection with specific deficiencies during the review period. Provider will use reasonable efforts to correct nonconformities that materially deviate from the accepted scope.

## 5. Fees, Invoicing, and Taxes

| Term | Value |
|---|---|
| Fee type | Fixed fee |
| Fee amount | USD 28,000 |
| Deposit | USD 8,400 due at signing |
| Payment terms | Net fifteen (15) days from invoice date; undisputed late amounts may accrue service charges stated in an accepted statement of work. |
| Included revisions | Two (2) included review rounds per major deliverable. |

Fees do not include taxes, third-party software, API usage, hosting, data storage, travel, or other pass-through expenses unless expressly stated. Client is responsible for sales, use, value-added, withholding, or similar taxes, excluding taxes on Provider's net income.

## 6. Client Responsibilities

Client will provide timely access to required subject-matter experts, systems, test data, documentation, credentials, APIs, third-party accounts, and decision makers. Client is responsible for the accuracy, legality, completeness, and permissions associated with Client-provided materials and instructions. Client will not provide regulated, sensitive, or restricted data unless the applicable statement of work expressly authorizes it and describes the safeguards required for that data.

## 7. Change Control

Either Party may request changes to scope, timelines, fees, deliverables, assumptions, data sources, deployment targets, security requirements, or support obligations. Provider is not required to perform changed or additional work unless the Parties approve a written change order describing the change and any related adjustments.

## 8. Agentic System Governance

The Parties acknowledge that agentic workflows can combine prompts, tools, APIs, memory, retrieval, evaluators, automations, and human approvals. The following controls apply unless replaced by a signed statement of work:

- **Human-in-the-loop controls:** Required before any customer-facing send, queue escalation to a human specialist, refund or credit suggestion, and any change to production routing rules.
- **Evaluation plan:** Labeled triage test set, reply-quality rubric, prompt-injection checks on inbound email, routing-accuracy regression suite, and an acceptance demonstration on held-out cases.
- **Monitoring plan:** Run logs, misclassification register, approval-override tracking, and recommended post-launch accuracy and escalation dashboards.
- **Excluded uses:** No regulated medical, legal, financial, employment, housing, insurance, credit, biometric, surveillance, safety-critical, or autonomous production decisioning use unless separately reviewed and documented.
- **AI-specific notice:** Agentic systems can produce unexpected, incomplete, or incorrect outputs. Client is responsible for human review and operational decisions based on system outputs.

Client is responsible for operational decisions, production authorization, end-user notices, model/provider account configuration, and ongoing monitoring after handoff unless Provider separately agrees to provide managed services.

## 9. Confidentiality, Data Handling, and Security

Each Party may receive non-public business, technical, financial, product, security, workflow, customer, or operational information from the other Party. Confidential information includes Client-provided documentation, prompts, datasets, credentials, workflow requirements, and business information. and Provider methods, templates, reusable code, know-how, development tools, and pre-existing materials.. The receiving Party will use confidential information only to perform or administer the Agreement and will protect it using reasonable safeguards appropriate to the nature of the information and demonstration context.

Parties will use reasonable safeguards appropriate to the demonstration context and will not intentionally disclose confidential information except as needed to perform or enforce the Agreement. Client materials retained for project administration will be handled according to this retention baseline: 30 days after final delivery or termination, subject to this exception: Delete or return Client-provided non-public materials after the retention period unless retention is required for legal, billing, or security purposes.

## 10. Intellectual Property

Each party retains ownership of materials, tools, code, libraries, models, documentation, inventions, templates, or know-how owned or developed outside the project. Upon full payment, Client owns the project-specific deliverables expressly identified as final work product, excluding Provider pre-existing IP and third-party components. Provider grants Client a non-exclusive, perpetual license to use embedded Provider pre-existing IP solely as necessary to use the final deliverables. Open-source and third-party components remain subject to their applicable licenses and provider terms.

Provider may use general skills, ideas, know-how, workflows, methods, templates, and reusable non-client-specific components learned or developed during the project, provided Provider does not disclose Client confidential information.

## 11. Third-Party Services and Open-Source Components

Agentic development frequently depends on third-party models, APIs, cloud providers, software libraries, connectors, repositories, or open-source components. Unless expressly stated otherwise, third-party services are not controlled by Provider. Client is responsible for approving third-party accounts, usage limits, terms, credentials, and costs associated with Client-controlled services.

## 12. Warranties and Disclaimers

Provider warrants for 30 days after acceptance that final deliverables will materially conform to the accepted scope when used as documented in the agreed environment. This warranty does not apply to modifications not made by Provider, Client systems, third-party services, excluded uses, new data, new regulations, production usage not included in scope, or failure to follow documentation.

Except for the limited warranty above and any warranties that cannot be excluded by law, the deliverables and services are provided **as is** for demonstration and development purposes. No output from an agentic system should be treated as professional advice or an autonomous final decision without appropriate human review.

## 13. Limitation of Liability

To the fullest extent permitted by applicable law and except for claims that cannot legally be limited, each Party's aggregate liability arising out of or related to this Agreement will not exceed Fees paid or payable under the applicable statement of work during the three (3) months before the event giving rise to the claim.. Neither Party will be liable for indirect, incidental, special, consequential, exemplary, punitive damages, lost profits, lost revenue, lost data, business interruption, or replacement services, even if advised of the possibility of those damages.

## 14. Indemnification

Each party is responsible for claims arising from its own gross negligence, willful misconduct, or violation of law, subject to the Agreement's limitations. Client will be responsible for claims arising from Client-provided materials, Client instructions, Client systems, Client-approved third-party services, or Client's use of deliverables outside the agreed scope. Provider will be responsible for claims that final deliverables, as provided by Provider and used within scope, infringe third-party intellectual property rights, excluding third-party components, open-source materials, Client materials, and Client-directed designs.

## 15. Term, Suspension, and Termination

The Agreement begins on the Effective Date and continues for the following term: Initial pilot term of eight (8) weeks, followed by month-to-month support only if ordered in writing. Either Party may terminate for material breach if the breach is not cured within ten (10) business days after written notice. Provider may suspend work for overdue undisputed invoices, unsafe or unlawful instructions, unavailable dependencies, or Client failure to provide required access.

Upon termination, Client will pay for accepted work, work performed through termination, approved expenses, and non-cancelable commitments. Sections relating to payment, confidentiality, data return or deletion, intellectual property, limitations of liability, indemnities, dispute resolution, and general terms survive termination.

## 16. Governing Law and Dispute Resolution

This Agreement is governed by the laws of New York, without regard to conflict-of-law rules. The venue for permitted court proceedings is New York County, New York. Before filing a formal claim, the Parties will try in good faith to resolve disputes through executive escalation or another mutually acceptable informal process.

## 17. Notices

Formal notices must be sent by personal delivery, reputable courier, certified mail, or email with confirmation of receipt to the notice addresses listed in Section 1, or to updated addresses provided by written notice.

## 18. General Terms

This Agreement and any incorporated statement of work form the entire agreement for the project and supersede prior discussions about the same subject. A waiver must be in writing and does not waive future rights. Neither Party may assign the Agreement without the other Party's consent except to an affiliate or successor in connection with merger, reorganization, or sale of substantially all assets. If any provision is unenforceable, the remaining provisions remain effective. Counterparts and electronic signatures are acceptable for demonstration purposes unless replaced by jurisdiction-specific requirements.

## 19. Signatures

By signing below, the Parties indicate that they are authorized to enter into this Agreement.

[SIGNATURE_BLOCK]