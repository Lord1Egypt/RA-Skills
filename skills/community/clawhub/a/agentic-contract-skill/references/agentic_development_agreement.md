# {{ agreement.title }}

**Contract ID:** {{ agreement.contract_id }}  
**Agreement Date:** {{ agreement.agreement_date }}  
**Effective Date:** {{ agreement.effective_date }}  
**Project:** {{ agreement.project_name }}

> Demonstration notice: this template is intentionally generic and is provided only to demonstrate programmatic contract generation. It is not legal advice and should be replaced or reviewed before real use.

## 1. Parties

This {{ agreement.title }} (the **"Agreement"**) is entered into by and between **{{ provider.legal_name }}**, a {{ provider.entity_type }} formed in {{ provider.state_of_formation }} with offices at {{ provider.full_address }} (**"Provider"**), and **{{ client.legal_name }}**, a {{ client.entity_type }} formed in {{ client.state_of_formation }} with offices at {{ client.full_address }} (**"Client"**). Provider and Client may be referred to individually as a **"Party"** and together as the **"Parties"**.

| Party | Notice Details |
|---|---|
| Provider | {{ provider.legal_name }}; {{ provider.full_address }}; {{ provider.email }}; {{ provider.phone }} |
| Client | {{ client.legal_name }}; {{ client.full_address }}; {{ client.email }}; {{ client.phone }} |

## 2. Engagement Summary

Provider will perform agentic development services for Client under this Agreement and any written statement of work, order form, or change order signed or otherwise approved by both Parties. The initial project summary is: **{{ agreement.services_summary }}**

| Item | Current Configuration |
|---|---|
| Project name | {{ agreement.project_name }} |
| System description | {{ agentic_development.system_description }} |
| Autonomy level | {{ agentic_development.autonomy_level }} |
| Human review | {{ agentic_development.human_in_loop }} |
| Model or stack | {{ agentic_development.model_or_stack }} |
| Deployment environment | {{ agentic_development.deployment_environment }} |

## 3. Scope of Services and Deliverables

Provider will use commercially reasonable efforts to deliver the services and deliverables described in the applicable statement of work. Unless a signed statement of work says otherwise, the project includes:

- Discovery and requirements clarification for the agentic workflow.
- Architecture, prompt, tool-routing, and workflow design for the agreed use case.
- Prototype implementation in the agreed development environment.
- Evaluation artifacts, including test cases and acceptance demonstrations.
- Handoff documentation suitable for technical administrators and business stakeholders.
- Basic post-handoff support for {{ agreement.support_period_days }} days after acceptance.

Out-of-scope services include production operations, legal compliance certification, regulated-use validation, data labeling at scale, model training, cloud hosting charges, managed security operations, procurement, and any use listed in Section 8 as excluded unless added by written change order.

## 4. Timeline, Review, and Acceptance

The target delivery schedule is: {{ agreement.delivery_schedule }} The Parties may adjust dates by mutual written agreement when delays are caused by dependency changes, delayed feedback, unavailable Client systems, new requirements, or change orders.

Client will review each material deliverable within {{ agreement.acceptance_period_days }} calendar days after delivery. A deliverable is accepted when Client approves it in writing, uses it in a non-test context, or does not provide a written rejection with specific deficiencies during the review period. Provider will use reasonable efforts to correct nonconformities that materially deviate from the accepted scope.

## 5. Fees, Invoicing, and Taxes

| Term | Value |
|---|---|
| Fee type | {{ agreement.fee_type }} |
| Fee amount | {{ agreement.fee_amount }} |
| Deposit | {{ agreement.deposit }} |
| Payment terms | {{ agreement.payment_terms }} |
| Included revisions | {{ agreement.revision_rounds }} |

Fees do not include taxes, third-party software, API usage, hosting, data storage, travel, or other pass-through expenses unless expressly stated. Client is responsible for sales, use, value-added, withholding, or similar taxes, excluding taxes on Provider's net income.

## 6. Client Responsibilities

Client will provide timely access to required subject-matter experts, systems, test data, documentation, credentials, APIs, third-party accounts, and decision makers. Client is responsible for the accuracy, legality, completeness, and permissions associated with Client-provided materials and instructions. Client will not provide regulated, sensitive, or restricted data unless the applicable statement of work expressly authorizes it and describes the safeguards required for that data.

## 7. Change Control

Either Party may request changes to scope, timelines, fees, deliverables, assumptions, data sources, deployment targets, security requirements, or support obligations. Provider is not required to perform changed or additional work unless the Parties approve a written change order describing the change and any related adjustments.

## 8. Agentic System Governance

The Parties acknowledge that agentic workflows can combine prompts, tools, APIs, memory, retrieval, evaluators, automations, and human approvals. The following controls apply unless replaced by a signed statement of work:

- **Human-in-the-loop controls:** {{ agentic_development.human_in_loop }}
- **Evaluation plan:** {{ agentic_development.evaluation_plan }}
- **Monitoring plan:** {{ agentic_development.monitoring_plan }}
- **Excluded uses:** {{ agentic_development.excluded_uses }}
- **AI-specific notice:** {{ risk.ai_specific_notice }}

Client is responsible for operational decisions, production authorization, end-user notices, model/provider account configuration, and ongoing monitoring after handoff unless Provider separately agrees to provide managed services.

## 9. Confidentiality, Data Handling, and Security

Each Party may receive non-public business, technical, financial, product, security, workflow, customer, or operational information from the other Party. Confidential information includes {{ confidentiality_data.client_data }} and {{ confidentiality_data.provider_data }}. The receiving Party will use confidential information only to perform or administer the Agreement and will protect it using reasonable safeguards appropriate to the nature of the information and demonstration context.

{{ confidentiality_data.privacy_terms }} Client materials retained for project administration will be handled according to this retention baseline: {{ confidentiality_data.retention_period_days }} days after final delivery or termination, subject to this exception: {{ confidentiality_data.backup_policy }}

## 10. Intellectual Property

{{ ip.pre_existing_ip }} {{ ip.work_product_owner }} {{ ip.license_back }} {{ ip.open_source_policy }}

Provider may use general skills, ideas, know-how, workflows, methods, templates, and reusable non-client-specific components learned or developed during the project, provided Provider does not disclose Client confidential information.

## 11. Third-Party Services and Open-Source Components

Agentic development frequently depends on third-party models, APIs, cloud providers, software libraries, connectors, repositories, or open-source components. Unless expressly stated otherwise, third-party services are not controlled by Provider. Client is responsible for approving third-party accounts, usage limits, terms, credentials, and costs associated with Client-controlled services.

## 12. Warranties and Disclaimers

Provider warrants for {{ agreement.warranty_days }} days after acceptance that final deliverables will materially conform to the accepted scope when used as documented in the agreed environment. This warranty does not apply to modifications not made by Provider, Client systems, third-party services, excluded uses, new data, new regulations, production usage not included in scope, or failure to follow documentation.

Except for the limited warranty above and any warranties that cannot be excluded by law, the deliverables and services are provided **as is** for demonstration and development purposes. No output from an agentic system should be treated as professional advice or an autonomous final decision without appropriate human review.

## 13. Limitation of Liability

To the fullest extent permitted by applicable law and except for claims that cannot legally be limited, each Party's aggregate liability arising out of or related to this Agreement will not exceed {{ risk.liability_cap }}. Neither Party will be liable for indirect, incidental, special, consequential, exemplary, punitive damages, lost profits, lost revenue, lost data, business interruption, or replacement services, even if advised of the possibility of those damages.

## 14. Indemnification

{{ risk.indemnity_summary }} Client will be responsible for claims arising from Client-provided materials, Client instructions, Client systems, Client-approved third-party services, or Client's use of deliverables outside the agreed scope. Provider will be responsible for claims that final deliverables, as provided by Provider and used within scope, infringe third-party intellectual property rights, excluding third-party components, open-source materials, Client materials, and Client-directed designs.

## 15. Term, Suspension, and Termination

The Agreement begins on the Effective Date and continues for the following term: {{ agreement.term }} Either Party may terminate for material breach if the breach is not cured within ten (10) business days after written notice. Provider may suspend work for overdue undisputed invoices, unsafe or unlawful instructions, unavailable dependencies, or Client failure to provide required access.

Upon termination, Client will pay for accepted work, work performed through termination, approved expenses, and non-cancelable commitments. Sections relating to payment, confidentiality, data return or deletion, intellectual property, limitations of liability, indemnities, dispute resolution, and general terms survive termination.

## 16. Governing Law and Dispute Resolution

This Agreement is governed by the laws of {{ agreement.governing_law }}, without regard to conflict-of-law rules. The venue for permitted court proceedings is {{ agreement.venue }}. Before filing a formal claim, the Parties will try in good faith to resolve disputes through executive escalation or another mutually acceptable informal process.

## 17. Notices

Formal notices must be sent by personal delivery, reputable courier, certified mail, or email with confirmation of receipt to the notice addresses listed in Section 1, or to updated addresses provided by written notice.

## 18. General Terms

This Agreement and any incorporated statement of work form the entire agreement for the project and supersede prior discussions about the same subject. A waiver must be in writing and does not waive future rights. Neither Party may assign the Agreement without the other Party's consent except to an affiliate or successor in connection with merger, reorganization, or sale of substantially all assets. If any provision is unenforceable, the remaining provisions remain effective. Counterparts and electronic signatures are acceptable for demonstration purposes unless replaced by jurisdiction-specific requirements.

## 19. Signatures

By signing below, the Parties indicate that they are authorized to enter into this Agreement.

[SIGNATURE_BLOCK]
