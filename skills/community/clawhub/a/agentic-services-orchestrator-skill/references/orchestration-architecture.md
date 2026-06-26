# CompleteTech Agentic Services Orchestration Architecture

## 1. Executive Summary

The library should operate as a schema-driven workflow orchestration system. `agentic-services-orchestrator-skill` owns workflow definition loading, lifecycle state, routing, sequencing, handoff contracts, missing-info handling, approval gates, duplicate-work prevention, artifact version discipline, event logging, state validation, exception handling, recovery actions, and plugin selection. Specialist skills perform bounded business functions. Support skills provide reusable communication, packaging, proof, billing, certificate, and risk-review capabilities.

The universal core uses generic primitives: `workflow_type`, `stage`, `track`, `artifact`, `actor/owner`, `decision`, `gate`, `dependency`, `event`, `state_transition`, and `recovery_action`. The default adapter is `references/completetech-services-workflow.yaml`, which preserves Discovery -> Proposal -> Contract -> Delivery -> Customer Success plus support outputs. Other domains can be represented by new workflow definition adapters without rewriting `SKILL.md`.

The default CompleteTech lifecycle may loop backward, skip a stage with verified substitute facts, reopen approvals, stall, split into parallel tracks, or branch into a change order. Invoice, Certificate, Case Study, Email, and Envelope are supporting outputs. Approval/risk triage decides whether a track needs no gate, owner approval, specialist review, or security review. Security Review is one overlay/gate, not the default gate for every workflow.

## 2. Final Architecture

- Orchestrator: central workflow definition loader, state owner, router, gatekeeper, validator, exception handler, recovery planner, and handoff normalizer.
- Workflow schema: `references/workflow-definition-schema.yaml`, defining configurable stages, transitions, artifacts, owners, gates, approval states, routing rules, recovery actions, required fields, terminal states, events, and validation rules.
- Default adapter: `references/completetech-services-workflow.yaml`, encoding CompleteTech services stages, support outputs, specialist ownership, gates, and routing rules.
- Lifecycle skills: discovery, proposal, contract, delivery, customer success.
- Support skills: invoice, certificate, case study, email, envelope.
- Overlay/gate skill: security review for security-sensitive work; other gates stay with commercial, legal, billing, recipient, proof, or client-authority owners.
- Plugins: used by the orchestrator or support skills only when they materially complete a workflow, such as GitHub for repo work, Gmail for mailbox context, Canva for branded design, spreadsheet tools for tabular client/project tracking, and document/PDF generators for artifacts.

## 3. Skill Responsibility Matrix

| Skill | Purpose | Orchestrator invokes when | Required inputs | Optional inputs | Outputs | Upstream | Downstream | Shared skills/plugins | Gates | Must not own | Centralize/remove |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| discovery | Convert opportunity into verified workflow facts. | New lead, unclear scope, readiness unknown, proposal facts missing. | client/workflow, stakeholders, pain, systems, goals, constraints. | budget, timeline, data/tool notes, examples. | intake, workflow map, readiness, success criteria, proposal handoff. | email, customer request. | proposal, approval triage, customer success. | email for recap; security only for security-sensitive risk. | sensitive data, excluded use, unclear approval path. | Final proposal, contract, invoice, launch approval. | lifecycle routing, approval triage, email copy. |
| proposal | Create buyer-facing commercial scope. | Discovery facts are sufficient for pilot/SOW/proposal/change order. | verified facts, scope, deliverables, acceptance criteria, price/terms if known. | proof snippets, roadmap, risk plan. | proposal, SOW, evaluation plan, assumptions/exclusions. | discovery, customer success, delivery change request. | contract, invoice, email, envelope. | approval triage; security only for security-sensitive risk; case study for approved proof only. | claims, regulated use, unapproved proof, pricing authority. | Legal terms, billing doc, delivery execution. | orchestration, email cover text, envelope packaging. |
| contract | Generate agreement package from approved terms. | Proposal/SOW is approved or user requests contract artifact. | legal parties, signatories, effective date, services summary, fees, terms source. | watermark/branding, output paths. | contract PDF/Markdown package. | proposal, human-approved terms. | invoice, envelope, email, delivery. | envelope for mailing; email for cover note. | legal approval, signature authority, unknown terms. | Scope negotiation, invoice issuance, packaging policy. | envelope ownership and lifecycle routing. |
| delivery | Produce execution artifacts after approval. | Work is approved and needs kickoff, status, evaluation, launch, handoff, support, closeout. | approved scope, timeline, owners, access needs, deliverables, acceptance criteria. | risks, logs, test examples, support terms. | project plan, trackers, status, evaluation, runbook, closeout. | contract/proposal, approval triage. | customer success, invoice, case study, email. | security for security-sensitive launch risk; email for updates. | production launch, external actions, access changes. | Commercial scope, account renewal, public proof. | approval/security gates, email drafts, billing. |
| customer success | Maintain relationship/account state. | Post-contact, active delivery, support, renewal, expansion, risk, advocacy. | client, contacts, routing, commitments, success criteria, account stage. | health score, renewal date, support items. | account profile, contact map, health score, QBR, renewal/expansion brief. | discovery, delivery, support. | case study, invoice, proposal, email. | email for outreach; case study for advocacy. | contact approval, escalation, billing/security concerns. | Delivery execution, public proof content. | orchestration state, email copy. |
| invoice | Draft billing documents. | Deposit, milestone, retainer, change order, support, credit, receipt, or payment request is needed. | client/provider, amount, terms, line items, invoice number, due date, contract/SOW ref. | taxes, discounts, payments, notes. | invoice, credit memo, receipt, payment request. | proposal, contract, delivery, customer success. | envelope, email, customer success. | envelope for mailing; email for send note. | billing approval, tax/accounting review, payment instructions. | Pricing rationale, legal terms, collections strategy. | lifecycle routing, email copy, envelope packaging. |
| certificate | Generate attendance certificate PDFs. | Verified training/workshop attendance certificate is requested. | recipient name, recipient email, certificate title. | issue date override, signatory, config override. | certificate PDF/path. | delivery/training record, user-provided facts. | envelope, email, customer success. | envelope/email for delivery. | identity/attendance verification. | Delivery acceptance, public proof. | routing, packaging, email. |
| case study | Package approved proof. | Outcomes are verified and proof/testimonial/story is requested. | approved facts, outcomes, attribution permission, confidentiality constraints. | quotes, metrics, proof snippets, channel. | case study, testimonial draft, proof library, anonymization checklist. | delivery, customer success. | email, proposal proof reuse, website/social. | security for anonymization; email for approval/share. | client approval, confidentiality, public proof. | Account management, delivery evidence creation. | security/anonymization gates, email drafts. |
| email | Draft communication. | Any workflow needs outbound/inbound copy, cover note, sequence, approval ask, or follow-up. | audience, stage, artifact summary, CTA, tone, verified recipient/routing. | prior messages, objections, proof snippets. | email draft/sequence. | any lifecycle/support skill. | envelope/send workflow, human approval. | Gmail only with explicit mailbox need. | external send approval, recipient verification. | Proposals, contracts, invoices, delivery records, proof facts. | artifact routing, packaging, state. |
| envelope | Package and address deliverables. | Outputs need mailing, attachment inventory, filename/recipient metadata, delivery-readiness, or envelope PDF. | sender, recipient, mailing address or recipient metadata, artifacts/attachments. | attention line, postage text, return-address toggle, filenames. | envelope PDF, package manifest, delivery-readiness checklist. | contract, invoice, certificate, proposal, case study. | email/send, human approval, archive. | email for digital send; security for sensitive package. | recipient verification, sensitive attachments. | Business content of artifacts or email copy. | artifact generation, lifecycle routing. |
| security review | Review security-sensitive risk and approvals. | Sensitive data, credentials, security-sensitive tools/integrations, production-impacting external actions, launch risk, public proof confidentiality, incidents, or permission changes appear. | workflow, data classes, tools, permissions, external actions, approval gates, logs, rollback. | provider/model config, retention, dependencies. | risk intake, permission inventory, launch blocker list, signoff memo. | approval/risk triage. | orchestrator decision, delivery, email, envelope, customer success. | technical/security plugins as needed. | security-sensitive launch, external tool action, public proof confidentiality, credentials. | Legal certification, billing approval, commercial approval, formal pen test claim. | duplicated risk gates in other skills. |

## 4. Orchestrator Routing and Handoff Model

Routing order:

1. Load the workflow definition using `project_state.workflow_type`; default to `completetech_services`.
2. Honor explicit user target if it is safe, permitted by the adapter, and has required inputs.
3. If target is unclear, infer stage/track from artifacts, active tracks, requested outcome, approval state, events, and blockers.
4. Decide whether the request is forward progress, backward rework, skipped-stage exception, reopened approval, continuation, revision, escalation, packaging, validation, or a new workstream.
5. Select the next action using adapter `allowed_transitions`, `routing_rules`, `required_fields`, `gates`, and `specialist_owners`.
6. Add support skills only for a concrete job: email for copy, envelope for packaging, invoice for billing, certificate for attendance, case study for proof.
7. Run approval/risk triage before risky transitions; route to security review only for security-sensitive triggers.
8. Check artifact versions before creating a new artifact; revise, supersede, fork, archive, or reference existing work when appropriate.
9. Append event-log entries for material state changes.
10. Validate state before final output, terminal state, or external action.
11. Return next skill, output artifacts, version relationships, blockers, missing facts, owner, latest events, next decision needed, and recovery action.

Handoff schema:

```yaml
project_state:
  workflow_type: completetech_services
  workflow_definition: references/completetech-services-workflow.yaml
  client: TBD
  workflow: TBD
  stage: discovery|proposal|contract|delivery|customer_success
  lifecycle_stage: discovery|proposal|contract|delivery|customer_success
  workflow_status: draft|active|stalled|blocked|in_review|approved|launched|closed|reopened|superseded
  intent: create|revise|package|send|review|approve|handoff
  active_tracks:
    - track: TBD
      stage: discovery|proposal|contract|delivery|customer_success|support_output|security_review
      status: draft|active|blocked|waiting|complete|superseded
      owner: TBD
      dependencies: []
      blockers: []
      due_date: TBD
  source_artifacts: []
  artifact_versions:
    - artifact: TBD
      path: TBD
      version: v1
      status: draft|current|superseded|archived|forked
      supersedes: TBD
      source_artifacts: []
  known_facts: {}
  assumptions: []
  conflicts: []
  missing_info: []
  dependencies: []
  blockers: []
  urgency: normal|elevated|urgent
  owner: TBD
  due_dates: {}
  approvals:
    commercial:
      status: unknown|draft|requested|partial|approved|rejected|expired|superseded|blocked|conditional
      approved_by: TBD
      approved_at: TBD
      evidence: TBD
      permits: []
      remaining_blockers: []
    legal_or_contract:
      status: unknown|draft|requested|partial|approved|rejected|expired|superseded|blocked|conditional
      approved_by: TBD
      approved_at: TBD
      evidence: TBD
      permits: []
      remaining_blockers: []
    security:
      status: unknown|draft|requested|partial|approved|rejected|expired|superseded|blocked|conditional
      approved_by: TBD
      approved_at: TBD
      evidence: TBD
      permits: []
      remaining_blockers: []
    external_send:
      status: unknown|draft|requested|partial|approved|rejected|expired|superseded|blocked|conditional
      approved_by: TBD
      approved_at: TBD
      evidence: TBD
      permits: []
      remaining_blockers: []
    public_proof:
      status: unknown|draft|requested|partial|approved|rejected|expired|superseded|blocked|conditional
      approved_by: TBD
      approved_at: TBD
      evidence: TBD
      permits: []
      remaining_blockers: []
  approval_history: []
  decision_log: []
  security_flags: []
  generated_outputs: []
  events:
    - event_id: TBD
      type: artifact_created|artifact_revised|approval_requested|approval_changed|blocker_added|blocker_removed|scope_changed|owner_changed|decision_recorded|track_started|track_closed|recovery_action_selected
      actor: TBD
      timestamp: TBD
      related_artifact: TBD
      related_track: TBD
      decision: TBD
      evidence: TBD
      notes: TBD
  state_transitions:
    - from: TBD
      to: TBD
      when: TBD
      rationale: TBD
  rollback_or_recovery_action: TBD
  next_decision_needed: TBD
  next_skill: TBD
  next_action: TBD
```

Failure modes:

- Missing required facts: ask targeted questions when the fact gates action; otherwise insert `TBD`, continue draft-only work, and record the missing fact.
- Conflicting facts: stop the affected track, record the conflict, identify the likely source of truth, and ask for a decision.
- Unsafe request: route to the applicable approval owner, specialist, or security review; require human approval when authority is unclear.
- Duplicate artifact: revise, supersede, fork, archive, or reference the existing artifact instead of creating a parallel one.
- Downstream request before upstream approval: produce a draft only and record the blocker.
- Partial approval: proceed only with the permitted scope and record remaining blockers.
- Client scope change: route to proposal or change-order work before delivery expands scope.
- Stakeholder unavailable: assign a fallback owner if known, continue safe draft work, and record the waiting decision.
- Security blocker: stop launch, credential use, external tool action, public proof, or external send until security review returns a permitted path.
- Billing dispute: stop invoice send or payment request and route through invoice/customer-success context.
- Delivery discovers new scope: keep delivery inside approved scope and open a new discovery/proposal/change-order track.
- Boundary-crossing request: route to the owning specialist and return a handoff instead of authoring the artifact in the orchestrator.

## 5. Real-World Operating Model

The orchestrator treats the engagement or workflow as a set of active tracks sharing one state object:

- Lifecycle track: adapter-defined stages, such as discovery, proposal, contract, delivery, customer success for CompleteTech services.
- Risk track: approval/risk triage, security review when needed, permission changes, credentials, data handling, launch blockers, incident response, and non-security approval gates.
- Commercial track: proposal, change order, contract, invoice, payment/request readiness.
- Communication track: email drafts, follow-ups, approval requests, recipient routing.
- Packaging track: envelope, attachment inventory, filenames, delivery-readiness.
- Proof/certificate track: case study, approved quotes, anonymization, training certificates.

Tracks may run in parallel when each track has explicit dependencies, owner, due date, blocker list, allowed output state, and approval limits. Parallel work must not let a downstream artifact imply approval that has not happened.

Non-linear transitions:

- Forward progress: move when source artifacts and approvals are current.
- Backward loop: return to discovery/proposal/change-order when assumptions fail or scope changes.
- Skipped stage: require verified substitute facts and record the reason.
- Reopened approval: mark the prior approval `superseded` or `expired`, record why, and stop actions outside the new approval.
- Stalled track: preserve owner, blocker, due date, and recovery action.
- Forked track: allow only when separate scopes, audiences, or approvals make one artifact unsafe or confusing.

Approval states:

| Status | Meaning |
| --- | --- |
| unknown | No reliable approval evidence exists. |
| draft | Artifact or decision is not ready for approval. |
| requested | Approval has been requested and is pending. |
| partial | Only a subset of scope, action, or recipients is approved. |
| approved | The listed action is permitted by the named approver/evidence. |
| rejected | Do not proceed with the requested action. |
| expired | A prior approval is no longer valid. |
| superseded | A newer artifact or decision replaced the prior approval. |
| blocked | A gate prevents action until a blocker is cleared. |
| conditional | Proceed only within the listed limits and remaining blockers. |

Escalate or stop when there is legal uncertainty, sensitive data exposure, credential risk, production impact, public proof risk, payment/billing ambiguity, client authority ambiguity, contradictory instructions, or any approval that is rejected, blocked, expired, or outside its permitted action.

When blocked, return the smallest useful next action: targeted questions, required evidence, suggested owner, fallback path, draft-only artifact, safe partial output, or rollback/recovery step.

## 6. Event Log and Validation

Append event entries when the workflow materially changes: `artifact_created`, `artifact_revised`, `approval_requested`, `approval_changed`, `blocker_added`, `blocker_removed`, `scope_changed`, `owner_changed`, `decision_recorded`, `track_started`, `track_closed`, and `recovery_action_selected`.

Validate state using `references/workflow-definition-schema.yaml` before final output, terminal state, or external action. The validator guidance covers invalid transitions, missing owners, orphaned blockers, stale approvals, artifacts without source/version, gates bypassed without rationale, unresolved conflicts, terminal states reached with open blockers, and external actions without approval evidence.

## 7. Adapter Examples

CompleteTech services adapter:

```yaml
workflow_type: completetech_services
stages: [discovery, proposal, contract, delivery, customer_success]
support_outputs: [invoice, certificate, case_study, email, envelope]
default_adapter: references/completetech-services-workflow.yaml
```

Hiring pipeline adapter example:

```yaml
workflow_type: hiring_pipeline
stages: [role_intake, sourcing, screening, interview, offer, onboarding]
artifacts: [role_brief, candidate_profile, interview_scorecard, offer_package]
gates:
  - hiring_manager_approval
  - compensation_approval
  - legal_or_hr_approval
  - privacy_or_security_review
routing_rules:
  - route candidate data/privacy concerns to privacy_or_security_review
  - route compensation or offer changes to compensation_approval
  - return failed scorecard assumptions to screening or role_intake
```

Software release adapter example:

```yaml
workflow_type: software_release
stages: [intake, implementation, review, test, release, post_release]
artifacts: [issue, branch, pull_request, test_report, release_notes]
gates:
  - code_review
  - ci_status
  - release_owner_approval
  - security_review
routing_rules:
  - route failed CI back to implementation
  - route public release notes to release_owner_approval
  - route dependency/security findings to security_review
```

## 8. Plugin-Weaving Model

- GitHub: code/repo artifacts, issue/PR workflows, CI evidence, commit/push tasks.
- Gmail: mailbox context, thread summaries, reply drafting, recipient history; sending requires explicit approval.
- Canva: branded presentations or visual assets that exceed Markdown/PDF templates.
- Spreadsheet tools: client trackers, invoice tables, account health matrices, opportunity lists.
- Local generators: use each skill renderer/generator before hand-rolling repeatable documents.

The orchestrator chooses plugins, but specialist skills may request them through the handoff when their artifact needs external context or production output.

## 9. Deduplication and Centralization Recommendations

- Move lifecycle routing, sequencing, state, active-track coordination, duplicate prevention, artifact version policy, and recovery planning to the orchestrator.
- Move email subject/body/CTA/sequences to email.
- Move recipients, filenames, attachment manifests, delivery-readiness, and physical mailing envelope PDFs to envelope.
- Move sensitive data, confidentiality, compliance, credential, tool-permission, production-impact, and incident gates to security review. Keep commercial, legal, billing, recipient, client-authority, and routine proof approvals with their owning specialists or approvers.
- Keep lifecycle skills focused on business artifacts and handoff facts.
- Keep renderer/template selection inside each specialist; centralize only the handoff contract.
- Avoid repeating full boundary paragraphs in every skill; each skill should state only local ownership and what it returns.

## 10. Final Cleaned Instruction Set: Orchestrator

Use the orchestrator when a request spans more than one skill or stage. It must:

1. Load the workflow definition and build or update `project_state`.
2. Classify workflow type, stage, intent, active tracks, missing facts, approvals, blockers, urgency, dependencies, conflicts, and risk flags.
3. Route to the right adapter owner, lifecycle skill, support skill, security review, or safe parallel track.
4. Pass only relevant context to each specialist.
5. Convert outputs into downstream inputs.
6. Prevent duplicate work by checking existing artifacts and version relationships first.
7. Run approval/risk triage at every gate and invoke security review only for security-sensitive gates.
8. Use email only for communication copy and envelope only for packaging/delivery-readiness.
9. Append event-log entries and validate state.
10. Return artifact paths, version relationships, decisions, missing info, approval status/history, latest events, next decision needed, recovery action, and next step.

## 11. Final Cleaned Instruction Outlines

- Discovery: collect verified pre-sale workflow facts; output proposal-ready handoff and risk flags; do not draft final commercial/legal artifacts.
- Proposal: turn verified facts into buyer-facing scope; output contract/invoice/delivery-ready scope; do not own legal terms, billing, or send packaging.
- Contract: generate agreement package from approved terms; output contract artifacts; do not own commercial negotiation or delivery packaging policy.
- Delivery: manage approved execution artifacts; output evidence, acceptance, handoff, and support records; do not own commercial expansion or public proof.
- Customer Success: maintain relationship/account state; output contact maps, health, renewal, escalation, and advocacy plans; do not own implementation artifacts.
- Invoice: create billing documents from approved commercial triggers; output invoice artifacts; do not own accounting/tax/legal decisions.
- Certificate: generate attendance certificates from verified recipient/course facts; output certificate PDF paths; do not own proof or delivery acceptance.
- Case Study: package verified approved outcomes; output proof assets and approval/anonymization notes; do not invent metrics or public permission.
- Email: draft messages and sequences from supplied artifacts; output copy; do not create the underlying business artifact or send without approval.
- Envelope: package artifacts for delivery; output envelope PDFs, attachment manifests, filenames, recipients, and readiness notes; do not author artifact content.
- Security Review: assess risk, permissions, sensitive data, external actions, and launch/proof gates; output blockers/signoff/residual risks; do not claim formal certification.

## 12. Example Workflows

Lead to proposal:

1. Orchestrator builds project state and routes to discovery.
2. Discovery returns workflow facts, missing scope, and risk flags.
3. Security review runs if data/tool risk exists.
4. Proposal drafts a pilot or SOW.
5. Email drafts recap or proposal cover note.
6. Envelope packages the proposal only if mailing or attachment manifest is needed.

Proposal to kickoff:

1. Proposal returns approved scope and assumptions.
2. Contract generates agreement package.
3. Invoice drafts deposit request from approved terms.
4. Envelope prepares contract/invoice package and recipient metadata.
5. Email drafts send/follow-up copy.
6. Delivery starts only after approval/signature/payment gate status is clear.

Launch readiness:

1. Delivery produces evaluation, launch checklist, runbook, and handoff.
2. Security review checks permissions, external actions, rollback, logs, and blockers.
3. Orchestrator stops for approval if blockers remain.
4. Email drafts client status update.
5. Customer success receives account/support state.

Proof after closeout:

1. Delivery provides verified evidence.
2. Customer success identifies approver and timing.
3. Case study drafts anonymized or named proof based on approval status.
4. Security review checks confidentiality.
5. Email drafts approval request or publication note.

Training certificate:

1. Certificate generates PDF from verified recipient/course facts.
2. Envelope packages physical mailing if needed.
3. Email drafts digital delivery note if needed.

Messy scope change with parallel tracks:

1. Delivery is active for the approved support-triage pilot.
2. Client asks to include refund recommendations, which is outside approved scope and raises higher risk.
3. Orchestrator keeps current delivery inside the original approval and opens a change-order proposal track.
4. Security review starts in parallel for refund data, policy access, tool permissions, human approval gates, and prohibited actions.
5. Customer success drafts stakeholder routing and confirms who can approve commercial and security decisions.
6. Proposal produces a draft change order with `TBD` for any unverified price, authority, or acceptance term.
7. Prior launch approval is marked conditional/superseded for the expanded scope; launch remains blocked for refund-related functionality.
8. Contract/invoice/envelope/email tracks remain draft-only until commercial, legal, billing, security, and external-send approvals are current.
9. Handoff returns active tracks, blockers, source artifacts, superseded approvals, next owner, and the next decision needed.

Billing dispute during delivery:

1. Invoice has been drafted for a milestone, but the client disputes whether acceptance occurred.
2. Orchestrator blocks invoice send and routes to delivery for acceptance evidence.
3. Customer success receives an account-risk note and suggested stakeholder owner.
4. Invoice revises only after acceptance or commercial approval is clarified.
5. Email may draft a neutral status note, but external send remains blocked until recipient and send approval are verified.

## 13. Open Questions

- Should `agentic-case-study-skill` be renamed `agentic-proof-skill` to match its broader proof-asset role?
- Should approval gates be stored in a shared machine-readable file, such as `references/approval-gates.yaml`, for reuse by email, envelope, invoice, case study, and security review?
- Should shared renderer conventions move to a common package once the library is published as one installable bundle?
- Should envelope become the sole source for all physical mailing output, while contract keeps only its embedded legacy `--envelope-out` generator option for backward compatibility?
