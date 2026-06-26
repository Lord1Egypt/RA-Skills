# Full Workflow Generation Variables

This reference defines the canonical variable set for generating a complete CompleteTech LLC agentic services workflow from first discovery through proposal, contract, invoice, delivery, approval/risk triage, customer success, proof, certificate, email, and envelope packaging.

Use this file as the orchestrator's shared source of truth when passing context between skills. Individual skills should receive only the subset they need, but variable names should stay stable across the workflow.

## Lifecycle Coverage

Default path: Discovery -> Proposal -> Contract -> Invoice -> Delivery -> Approval/Risk Triage -> Customer Success -> Case Study / Proof -> Certificate -> Email -> Envelope

Real engagements may loop backward, skip stages with verified substitute facts, reopen approvals, stall, branch into change orders, or run multiple tracks in parallel. Approval/risk triage can interrupt any stage and may result in no gate, owner approval, specialist review, or security review. Email and Envelope are support utilities used whenever communication or delivery packaging is needed.

## Canonical Workflow Variables

```yaml
workflow_generation:
  workflow_type: completetech_services
  workflow_definition: references/completetech-services-workflow.yaml
  workflow_schema: references/workflow-definition-schema.yaml
  workflow_id: ADW-NORTHWIND-2026-001
  workflow_name: Customer Support Email Triage Agent
  lifecycle_stage: discovery
  generation_date: 2026-05-25
  prepared_by: CompleteTech LLC
  status: draft
  workflow_status: active
  urgency: elevated
  owner: CompleteTech engagement lead
  next_decision_needed: confirm retention policy and security contact before launch
  rollback_or_recovery_action: keep pilot in sandbox and continue draft-only external communications until security blockers close
  due_dates:
    security_contact_due: 2026-06-10
    retention_policy_due: 2026-06-10
    acceptance_demo_target: 2026-06-18

  active_tracks:
    - track_id: TRACK-DELIVERY-001
      name: approved support-triage pilot delivery
      stage: delivery
      status: active
      owner: CompleteTech delivery lead
      due_date: 2026-06-18
      dependencies:
        - ADSA-2026-0142 approved scope
        - SEC-2026-0090 conditional go
      blockers:
        - retention policy for ticket excerpts unresolved
        - security contact missing
      allowed_output_state: internal delivery artifacts only
    - track_id: TRACK-SECURITY-001
      name: launch security blocker review
      stage: security_review
      status: blocked
      owner: TBD
      due_date: 2026-06-10
      dependencies:
        - client security contact
        - retention policy
      blockers:
        - incident/security owner not named
      allowed_output_state: signoff memo draft and blocker list
    - track_id: TRACK-CHANGE-ORDER-001
      name: refund recommendation scope change
      stage: proposal
      status: draft
      owner: CompleteTech engagement lead
      due_date: TBD
      dependencies:
        - sponsor confirms whether refund recommendations are in scope
        - security review of refund-policy data
      blockers:
        - commercial approval unknown
        - security impact unknown
      allowed_output_state: draft change-order proposal only

  artifact_versions:
    - artifact_id: PRO-2026-0188
      artifact_type: proposal
      path: agentic_proposal_skill/assets/examples/example.pdf
      version: v1
      status: current
      supersedes: TBD
      source_artifacts:
        - DISC-2026-0117
      approval_impact: approved for support-triage pilot only
    - artifact_id: SEC-2026-0090
      artifact_type: security-signoff-memo
      path: agentic_security_review_skill/assets/examples/example.pdf
      version: v1
      status: current
      supersedes: TBD
      source_artifacts:
        - DISC-2026-0117
        - DEL-2026-0233
      approval_impact: conditional go; launch blocked until required items close
    - artifact_id: CHG-2026-0004
      artifact_type: change-order-proposal
      path: TBD
      version: v0-draft
      status: draft
      supersedes: TBD
      source_artifacts:
        - DEL-2026-0233
      approval_impact: no delivery, billing, contract, or launch authority

  approvals:
    commercial:
      status: partial
      approved_by: Jordan Lee
      approved_at: 2026-05-30
      evidence: approved pilot scope PRO-2026-0188
      permits:
        - support-triage pilot scope
      remaining_blockers:
        - refund recommendation change order not approved
    legal_or_contract:
      status: approved
      approved_by: Morgan Reyes
      approved_at: 2026-06-01
      evidence: ADSA-2026-0142
      permits:
        - execute support-triage pilot under signed agreement
      remaining_blockers: []
    security:
      status: conditional
      approved_by: TBD
      approved_at: TBD
      evidence: SEC-2026-0090 draft memo
      permits:
        - sandbox evaluation
        - draft-and-recommend support replies for human review
      remaining_blockers:
        - confirm retention policy
        - name security contact
        - complete reviewer training
    external_send:
      status: requested
      approved_by: TBD
      approved_at: TBD
      evidence: email draft PRO-OUT-014
      permits: []
      remaining_blockers:
        - recipient approval pending
    public_proof:
      status: approved
      approved_by: Jordan Lee
      approved_at: TBD
      evidence: named proof approval CASE-2026-007
      permits:
        - approved named case study without raw ticket text
      remaining_blockers:
        - do not identify customer accounts

  approval_history:
    - date: 2026-05-30
      gate: commercial
      status: approved
      actor: Jordan Lee
      evidence: PRO-2026-0188 approved for support triage
      notes: refund recommendations not included
    - date: 2026-06-09
      gate: security
      status: conditional
      actor: TBD
      evidence: SEC-2026-0090
      notes: launch blocked until retention policy and security contact are confirmed

  decision_log:
    - date: 2026-06-09
      decision: keep delivery inside approved support-triage scope
      owner: CompleteTech engagement lead
      rationale: client mentioned refund recommendations during delivery, which requires change-order and security review
    - date: 2026-06-09
      decision: open parallel change-order proposal and security-review tracks
      owner: CompleteTech engagement lead
      rationale: proposal drafting can proceed as draft-only while security evaluates refund-policy risk

  assumptions:
    - refund recommendations are outside approved pilot scope until sponsor confirms otherwise
    - no autonomous sending remains a hard constraint
  conflicts:
    - client sponsor asked about refund recommendations, but signed scope excludes refund decisions
  dependencies:
    - security contact email
    - retention policy for ticket excerpts
    - sponsor decision on refund recommendation scope

  events:
    - event_id: EVT-2026-0001
      type: track_started
      actor: CompleteTech engagement lead
      timestamp: 2026-06-09T09:00:00-04:00
      related_artifact: DEL-2026-0233
      related_track: TRACK-DELIVERY-001
      decision: keep approved delivery track active
      evidence: ADSA-2026-0142 and PRO-2026-0188
      notes: support-triage pilot remains inside approved scope
    - event_id: EVT-2026-0002
      type: scope_changed
      actor: Jordan Lee
      timestamp: 2026-06-09T10:15:00-04:00
      related_artifact: CHG-2026-0004
      related_track: TRACK-CHANGE-ORDER-001
      decision: open draft-only refund recommendation change-order track
      evidence: sponsor request during delivery review
      notes: refund recommendations are outside signed scope
    - event_id: EVT-2026-0003
      type: recovery_action_selected
      actor: CompleteTech engagement lead
      timestamp: 2026-06-09T10:30:00-04:00
      related_artifact: SEC-2026-0090
      related_track: TRACK-SECURITY-001
      decision: keep pilot sandboxed and request missing security evidence
      evidence: retention policy and security contact missing
      notes: no refund tools, external sends, or production launch until gates are current

  state_transitions:
    - from: delivery
      to: proposal
      when: delivery uncovered refund recommendation scope outside approved pilot
      rationale: CompleteTech adapter routes new scope to proposal/change-order before delivery expansion
    - from: delivery
      to: security_review
      when: refund-policy data and tool permissions may introduce security-sensitive risk
      rationale: approval/risk triage selected security review for the expanded scope only

  provider:
    legal_name: CompleteTech LLC
    trade_name: CompleteTech LLC
    entity_type: Limited Liability Company
    formation_state: Florida
    mailing_address:
      line1: 7901 4th St N
      line2: Ste 300
      city: St. Petersburg
      state: FL
      postal_code: "33702"
      country: United States
    email: info@completetech.com
    phone: TBD
    website: https://completetech.ai
    signatory_name: Timothy Gregg
    signatory_title: Agent Whisperer

  brand:
    logo_path: assets/logo.png
    seal_path: assets/stamp_ct.png
    accent_color: "#2563eb"
    watermark_enabled: true
    watermark_text: DEMO DRAFT
    cover_page_enabled: true
    letterhead_enabled: true
    header_enabled: true
    footer_enabled: true

  client:
    legal_name: Northwind Trading Co.
    short_name: Northwind
    entity_type: Corporation
    industry: B2B commerce
    website: https://northwind.example
    mailing_address:
      line1: 410 Market Street
      line2: Suite 800
      city: Pittsburgh
      state: PA
      postal_code: "15222"
      country: United States
    billing_address_same_as_mailing: true
    signatory_name: Morgan Reyes
    signatory_title: General Counsel
    sponsor_name: Jordan Lee
    sponsor_title: Operations Director
    primary_contact_name: Priya Raman
    primary_contact_title: Support Operations Lead
    primary_contact_email: priya.raman@northwind.example
    billing_contact_email: billing@northwind.example
    legal_contact_email: legal@northwind.example
    security_contact_email: TBD

  opportunity:
    source: warm referral
    trigger: support queue growth
    current_pain: manual support email triage creates slow routing and uneven notes
    desired_outcome: consistent classification, escalation notes, and reply drafts for human approval
    repeated_workflow: inbound support email triage
    estimated_volume: 850 emails per day
    stakeholders:
      - operations director
      - support operations lead
      - legal counsel
      - IT administrator
    decision_criteria:
      - routing accuracy on held-out labeled examples
      - reviewer confidence
      - zero unapproved customer-facing sends
      - clear rollback path

  discovery:
    discovery_artifact_id: DISC-2026-0117
    workflow_inputs:
      - inbound support email
      - customer account metadata
      - help-center excerpts
      - escalation policy
    workflow_outputs:
      - category suggestion
      - priority suggestion
      - escalation note
      - draft customer reply
      - reviewer summary
    systems_in_scope:
      - shared support mailbox sandbox
      - help-center export
      - labeled evaluation set
    systems_out_of_scope:
      - production send permissions
      - refunds
      - account suspension
      - autonomous customer communication
    data_classes:
      - customer support text
      - customer account context
      - internal support notes
    sensitive_data_flags:
      - possible personal information in tickets
      - customer-provided attachments excluded from pilot
    approval_points:
      - support lead approves categories before workflow tuning
      - support lead approves every customer-facing response
      - sponsor approves launch readiness
    success_criteria:
      routing_accuracy_target: ">= 90%"
      reply_quality_target: ">= 4.0 / 5 reviewer score"
      unapproved_send_target: "0"
    readiness_status: pilot-ready after data boundary confirmation
    missing_info:
      - security contact email
      - retention policy for ticket excerpts

  proposal:
    proposal_id: PRO-2026-0188
    proposal_title: Support Email Triage Agent - Pilot Proposal
    proposal_type: one-page-pilot-proposal
    scope_summary: build an evaluation-first support email triage pilot
    pilot_duration: 8 weeks
    deliverables:
      - discovery confirmation
      - sandbox workflow implementation
      - prompt/tool routing configuration
      - evaluation set and scorecard
      - reviewer checklist
      - launch readiness package
      - handoff documentation
    assumptions:
      - client provides sandbox mailbox access
      - client provides labeled examples
      - no autonomous sending during pilot
    exclusions:
      - production deployment
      - autonomous refunds
      - legal/compliance certification
      - customer-facing sends without approval
    acceptance_criteria:
      - routing accuracy meets target
      - reviewer workflow documented
      - rollback plan approved
      - security blockers closed or accepted
    price_model: fixed fee
    total_fee: USD 28,000
    deposit_amount: USD 8,400
    payment_terms: Net 15
    proposal_expiration_date: 2026-06-15

  contract:
    contract_id: ADSA-2026-0142
    effective_date: 2026-06-01
    agreement_title: Agentic Development Services Agreement
    project_name: Customer Support Email Triage Agent Pilot
    services_summary: bounded agentic workflow implementation for support triage
    timeline: 8 weeks from kickoff
    fee_amount: USD 28,000
    payment_schedule:
      deposit_due: USD 8,400 on signature
      milestone_due: USD 9,520 on prototype acceptance
      final_due: USD 10,080 on delivery acceptance
    human_in_the_loop_requirements:
      - support lead approves every customer-facing response
      - sponsor approves production change requests
      - CompleteTech requests approval before expanding tool permissions
    autonomy_level: draft-and-recommend only
    model_or_stack: TBD
    deployment_environment: sandbox pilot environment
    evaluation_plan: held-out labeled support email set
    monitoring_plan: weekly review of routing errors and reviewer notes
    excluded_uses:
      - autonomous customer communication
      - legal advice
      - refund decisions
      - account suspension
    contract_output_pdf: assets/examples/example.pdf
    contract_output_markdown: assets/examples/example.md
    contract_envelope_pdf: assets/examples/example-envelope.pdf

  invoice:
    invoice_number: INV-2026-0461
    invoice_type: milestone-invoice
    issue_date: 2026-06-08
    due_date: 2026-06-23
    currency: USD
    contract_reference: ADSA-2026-0142
    sow_reference: PRO-2026-0188
    billing_period: prototype milestone
    line_items:
      - description: Support triage prototype milestone
        amount: 12000
      - description: Deposit credit applied
        amount: -2480
    subtotal: 9520
    tax_amount: TBD
    total_due: 9520
    payment_instructions: TBD
    purchase_order_number: TBD
    invoice_notes: Draft until billing approval

  delivery:
    delivery_artifact_id: DEL-2026-0233
    kickoff_date: 2026-06-03
    launch_window: pilot group on 2026-06-24
    delivery_owner: CompleteTech delivery lead
    client_owner: Priya Raman
    access_requirements:
      - sandbox mailbox
      - help-center export
      - labeled evaluation examples
    milestone_tracker:
      discovery_confirmed: complete
      prototype_ready: complete
      evaluation_complete: in_review
      security_signoff: blocked
      acceptance_demo: pending
    evaluation_results:
      routing_accuracy: 93.4%
      reply_quality_score: 4.3/5
      prompt_injection_tool_actions: 0/42
    launch_blockers:
      - retention policy for ticket excerpts unresolved
      - security contact missing
    rollback_owner: CompleteTech delivery lead
    handoff_artifacts:
      - reviewer checklist
      - runbook
      - monitoring plan
      - escalation procedure

  security_review:
    security_review_id: SEC-2026-0090
    review_type: security-signoff-memo
    data_classification: customer support tickets with account context
    tools_requested:
      - sandbox mailbox read access
      - help-center read access
      - internal evaluation spreadsheet
    credentials_required:
      - sandbox mailbox token
      - help-center export access
    external_actions:
      - draft customer-facing replies for human approval
    prohibited_actions:
      - send emails
      - delete tickets
      - issue refunds
      - modify production records
    logging_requirements:
      - prompt and response logs
      - tool-call logs
      - reviewer approval records
      - error and rollback events
    retention_policy: TBD
    rollback_plan_status: documented
    incident_contact: TBD
    security_decision: conditional go
    residual_risks:
      - personal information may appear in ticket text
      - prompt-injection attempts require reviewer training
    required_before_launch:
      - confirm retention policy
      - name security contact
      - complete reviewer training

  customer_success:
    customer_success_id: CS-2026-0051
    account_stage: post-launch support
    health_status: stable
    health_score: 82
    renewal_date: TBD
    support_cadence: weekly during pilot, monthly after handoff
    open_commitments:
      - schedule 30-day adoption review
      - confirm production change-order interest
      - collect reviewer feedback
    expansion_signals:
      - returns workflow mentioned by sponsor
    relationship_risks:
      - security contact unknown
      - billing approval route still draft
    advocacy_timing: no testimonial ask until 30-day adoption review

  case_study:
    case_study_id: CASE-2026-007
    proof_type: public-named-client-case-study
    approval_status: client-approved for named use
    attribution_allowed: true
    client_quote: The pilot gave our reviewers a cleaner starting point without removing human judgment.
    quote_approver: Jordan Lee
    measured_outcomes:
      routing_accuracy: 93.4%
      reply_quality_score: 4.3/5
      unapproved_sends: 0
    qualitative_observations:
      - reviewers reported more consistent escalation notes
      - sponsor valued approval-gate clarity
    confidentiality_constraints:
      - do not publish raw ticket text
      - do not identify customer accounts
    public_channels:
      - sales one-pager
      - website story
      - proposal proof snippet

  certificate:
    recipient_name: Dana Whitfield
    recipient_email: dana.whitfield@northwindtrading.example
    certificate_title: Building Bounded Agentic Workflows with Human Approval Gates
    issue_date: 2026-05-22
    certificate_id: COMP-BBAWW-20260522-A7B926
    signatory_name: Timothy Gregg
    signatory_title: Agent Whisperer
    certificate_output_pdf: assets/examples/example.pdf

  email:
    email_sequence_id: PRO-OUT-014
    email_stage: proposal follow-up
    recipient_name: Jordan Lee
    recipient_email: jordan.lee@northwind.example
    sender_name: Timothy Gregg
    sender_email: info@completetech.com
    subject: Support triage pilot scope for review
    call_to_action: confirm whether the approval gate matches your process
    tone: direct, practical, low-hype
    proof_snippet_allowed: true
    send_status: draft only
    external_send_approval: required

  envelope:
    sender_name: CompleteTech LLC
    sender_address:
      line1: 7901 4th St N
      line2: Ste 300
      city: St. Petersburg
      state: FL
      postal_code: "33702"
    recipient_name: Morgan Reyes
    recipient_title: General Counsel
    recipient_organization: Northwind Trading Co.
    recipient_address:
      line1: 410 Market Street
      line2: Suite 800
      city: Pittsburgh
      state: PA
      postal_code: "15222"
    attention_line: "Attn: Morgan Reyes, General Counsel"
    postage_box_text: FIRST-CLASS MAIL
    return_address_enabled: true
    package_manifest:
      - northwind_support_triage_agreement.pdf
      - northwind_support_triage_deposit_invoice.pdf
      - certificate_dana_whitfield.pdf
    delivery_mode: physical mail
    delivery_readiness: ready after billing approval

  generated_outputs:
    discovery_markdown: agentic_discovery_skill/assets/examples/example.md
    discovery_pdf: agentic_discovery_skill/assets/examples/example.pdf
    proposal_markdown: agentic_proposal_skill/assets/examples/example.md
    proposal_pdf: agentic_proposal_skill/assets/examples/example.pdf
    contract_markdown: agentic_contract_skill/assets/examples/example.md
    contract_pdf: agentic_contract_skill/assets/examples/example.pdf
    invoice_markdown: agentic_invoice_skill/assets/examples/example.md
    invoice_pdf: agentic_invoice_skill/assets/examples/example.pdf
    delivery_markdown: agentic_delivery_skill/assets/examples/example.md
    delivery_pdf: agentic_delivery_skill/assets/examples/example.pdf
    security_markdown: agentic_security_review_skill/assets/examples/example.md
    security_pdf: agentic_security_review_skill/assets/examples/example.pdf
    customer_success_markdown: agentic_customer_success_skill/assets/examples/example.md
    customer_success_pdf: agentic_customer_success_skill/assets/examples/example.pdf
    case_study_markdown: agentic_case_study_skill/assets/examples/example.md
    case_study_pdf: agentic_case_study_skill/assets/examples/example.pdf
    certificate_markdown: agentic_certificate_skill/assets/examples/example.md
    certificate_pdf: agentic_certificate_skill/assets/examples/example.pdf
    email_markdown: agentic_email_skill/assets/examples/example.md
    email_pdf: agentic_email_skill/assets/examples/example.pdf
    envelope_markdown: agentic_envelope_skill/assets/examples/example.md
    envelope_pdf: agentic_envelope_skill/assets/examples/example.pdf
```

## Messy Real-World Scenario: CompleteTech Adapter

The Northwind pilot is an instance of the `completetech_services` adapter. It is no longer treated as a clean pipeline. Delivery is active for the approved support-triage scope, security is blocked on retention/contact facts, and a separate draft change-order track is open because the sponsor asked whether the workflow can recommend refunds. The orchestrator keeps delivery inside the signed scope, allows draft-only proposal/security work in parallel, and blocks contract, invoice, launch, external send, and refund-related delivery until commercial, legal, billing, security, and recipient approvals are current.

Handoff summary:

```yaml
project_state:
  workflow_status: blocked
  active_tracks:
    - TRACK-DELIVERY-001: active inside approved support-triage scope
    - TRACK-SECURITY-001: blocked pending retention policy and security contact
    - TRACK-CHANGE-ORDER-001: draft-only refund recommendation change order
  conflicts:
    - signed scope excludes refund decisions, but sponsor requested refund recommendation exploration
  approvals:
    commercial.status: partial
    security.status: conditional
    external_send.status: requested
  rollback_or_recovery_action: keep pilot sandboxed; do not enable refund tools or external sends
  next_decision_needed: sponsor confirms whether refund recommendation work should become a formal change order
  next_skill: agentic-proposal-skill and agentic-security-review-skill in parallel
```

## Second Domain Example: Hiring Pipeline

This is not a CompleteTech services workflow. It shows how another adapter can reuse the same primitives without changing `SKILL.md`.

```yaml
workflow_type: hiring_pipeline
workflow_definition: references/hiring-pipeline-workflow.yaml
project_state:
  stage: interview
  active_tracks:
    - track_id: TRACK-CANDIDATE-001
      stage: interview
      status: active
      owner: hiring manager
      dependencies:
        - completed scorecard
        - compensation range approval
      blockers:
        - second interviewer feedback missing
  artifacts:
    - artifact_type: interview_scorecard
      version: v2
      status: current
      source_artifacts:
        - role_brief_v1
        - candidate_profile_v1
  gates:
    hiring_manager_approval.status: requested
    compensation_approval.status: blocked
    privacy_or_security_review.status: not_applicable
  events:
    - type: blocker_added
      actor: recruiter
      related_track: TRACK-CANDIDATE-001
      notes: compensation approval missing before offer package
  next_decision_needed: confirm compensation range before offer artifact is final
```

## Variable Ownership By Skill

| Skill | Owns these variables | Receives from upstream | Returns downstream |
| --- | --- | --- | --- |
| `agentic-discovery-skill` | `opportunity.*`, `discovery.*` | `provider.*`, `client.*`, `workflow_id`, `workflow_name` | `proposal.scope_summary`, `proposal.assumptions`, `security_review.data_classification`, `delivery.access_requirements` |
| `agentic-proposal-skill` | `proposal.*` | `discovery.*`, `client.*`, `provider.*` | `contract.services_summary`, `invoice.contract_reference`, `delivery.acceptance_criteria` |
| `agentic-contract-skill` | `contract.*` | `proposal.*`, `provider.*`, `client.*`, approval variables | `invoice.payment_schedule`, `delivery.project_name`, `envelope.package_manifest` |
| `agentic-invoice-skill` | `invoice.*` | `contract.*`, `proposal.price_model`, `delivery.milestone_tracker` | `email.subject`, `envelope.package_manifest`, `customer_success.open_commitments` |
| `agentic-delivery-skill` | `delivery.*` | `contract.*`, `proposal.acceptance_criteria`, `security_review.required_before_launch` | `customer_success.health_status`, `case_study.measured_outcomes`, `invoice.line_items` |
| `agentic-security-review-skill` | `security_review.*` | `discovery.data_classes`, `delivery.access_requirements`, `email.external_send_approval`, `envelope.delivery_mode` | blockers, approvals, residual risks, launch decision |
| `agentic-customer-success-skill` | `customer_success.*` | `delivery.*`, `invoice.*`, `client.contacts` | `case_study.approval_status`, `email.recipient_*`, renewal/expansion inputs |
| `agentic-case-study-skill` | `case_study.*` | `delivery.evaluation_results`, `customer_success.advocacy_timing`, `security_review.residual_risks` | approved proof snippets for proposal/email/website |
| `agentic-certificate-skill` | `certificate.*` | verified attendance or training facts | `envelope.package_manifest`, `email.subject` |
| `agentic-email-skill` | `email.*` | artifact summaries and recipient routing from any stage | draft copy, CTA, subject, send approval status |
| `agentic-envelope-skill` | `envelope.*` | artifact paths, recipients, approval state | envelope PDF, package manifest, delivery-readiness notes |

## Approval Gate Variables

| Gate | Variables | Required before |
| --- | --- | --- |
| Commercial approval | `proposal.total_fee`, `proposal.deposit_amount`, `proposal.acceptance_criteria`, `proposal.assumptions`, `proposal.exclusions` | Contract, invoice, delivery kickoff |
| Legal/signature approval | `contract.contract_id`, `client.signatory_name`, `provider.signatory_name`, `contract.effective_date` | Sending contract, delivery start |
| Billing approval | `invoice.invoice_number`, `invoice.total_due`, `invoice.tax_amount`, `invoice.payment_instructions`, `invoice.purchase_order_number` | Invoice send, envelope package |
| Security approval | `security_review.security_decision`, `security_review.required_before_launch`, `security_review.residual_risks` | Production launch, external tool actions |
| External send approval | `email.recipient_email`, `email.subject`, `email.send_status`, `email.external_send_approval` | Sending email or package externally |
| Public proof approval | `case_study.approval_status`, `case_study.attribution_allowed`, `case_study.quote_approver`, `case_study.confidentiality_constraints` | Public case study, named quote, proof reuse |

## Minimal Required Variables For A Full Run

The orchestrator should stop and ask for clarification if any of these are missing:

- `client.legal_name`
- `client.primary_contact_name`
- `client.primary_contact_email`
- `opportunity.repeated_workflow`
- `opportunity.current_pain`
- `opportunity.desired_outcome`
- `discovery.workflow_inputs`
- `discovery.workflow_outputs`
- `discovery.approval_points`
- `proposal.scope_summary`
- `proposal.deliverables`
- `proposal.total_fee`
- `proposal.payment_terms`
- `contract.contract_id`
- `contract.effective_date`
- `contract.human_in_the_loop_requirements`
- `invoice.invoice_number`
- `invoice.total_due`
- `delivery.access_requirements`
- `delivery.acceptance_criteria` or `proposal.acceptance_criteria`
- `security_review.data_classification`
- `security_review.external_actions`
- `email.recipient_email`
- `envelope.recipient_address`

## Full Workflow Generation Order

1. Build `workflow_generation` from verified provider, client, opportunity, and contact facts.
2. Generate discovery artifacts from `opportunity.*` and `discovery.*`.
3. Generate proposal/SOW artifacts from `discovery.*`, `proposal.*`, `provider.*`, and `client.*`.
4. Run approval/risk triage when approvals or risks are present; route to security review only for sensitive data, security-sensitive tools, credentials, production-impacting external actions, launch, incidents, or material security/compliance risk.
5. Generate contract artifacts from approved `proposal.*`, `contract.*`, `provider.*`, and `client.*`.
6. Generate invoice artifacts from `invoice.*`, `contract.*`, and approved commercial terms.
7. Generate delivery artifacts from `delivery.*`, `proposal.acceptance_criteria`, `contract.*`, and applicable approval/security gates.
8. Generate customer success artifacts from `customer_success.*`, delivery state, contact routing, and open commitments.
9. Generate case study/proof only after delivery evidence and approval variables are verified.
10. Generate certificates only from verified attendance or training variables.
11. Generate email drafts from artifact summaries, recipient routing, CTA, and send approval status.
12. Generate envelope/package outputs from artifact paths, recipient metadata, package manifest, and delivery-readiness state.
