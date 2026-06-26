---
name: agentic-services-orchestrator-skill
description: >-
  Coordinate schema-driven workflows across configurable domains using workflow definitions, adapters, active tracks, artifact versions, approval/risk triage, event logs, validation, and recovery actions. Use the CompleteTech LLC agentic services workflow as the default adapter for discovery, proposal, contract, delivery, customer success, invoice, certificate, case study, email, envelope, and security-review work.
version: 1.0.3
metadata:
  openclaw:
    skillKey: agentic-services-orchestrator-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-services-orchestrator-skill
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: reportlab==4.5.1
      - kind: uv
        package: pyyaml==6.0.3
      - kind: uv
        package: pypdfium2==5.8.0
      - kind: uv
        package: pillow==12.2.0
---

# Agentic Services Orchestrator Skill

## Purpose

Coordinate workflow state, routing, sequencing, dependency tracking, handoff contracts, missing-info handling, approval gates, validation, recovery, and plugin-weaving across configurable workflow domains. The CompleteTech LLC agentic services lifecycle is the built-in default adapter, not the hardcoded core. Specialist skills own their artifacts.

For the complete architecture, per-skill responsibility matrix, handoff schema, plugin-weaving model, deduplication guidance, and example multi-skill workflows, load `references/orchestration-architecture.md`. For schema-driven routing, load `references/workflow-definition-schema.yaml` and the default adapter `references/completetech-services-workflow.yaml`.

## System Boundary

This skill owns workflow definition loading, routing policy, project state, event logging, validation, recovery selection, and specialist handoff coordination. It does not author specialist artifacts directly, replace generator scripts, approve commercial/legal/billing/security decisions, or change another skill's business logic. Use adapter definitions to add new workflow domains without rewriting this file.

## Runtime Permissions

This skill is a local workflow-orchestration and document-rendering workflow. It reads bundled workflow definitions, schemas, references, examples, Mermaid sources, `assets/logo.png`, and user-provided project-state/workflow facts. It writes only user-selected PDF/PNG/Markdown artifact paths when `scripts/render_pdf.py` is explicitly run.

It does not send emails, call external workflow systems, call Mautic or other CRMs, contact certificate services, require credential access, create persistence, escalate privileges, perform destructive file operations, or run background services.

## Network Boundary

This skill is local-only. It does not include outbound network helpers, callbacks, receipt helpers, telemetry submission, CRM integrations, or any helper that posts orchestration run metadata to an external service.

## Universal Workflow Model

The orchestrator is based on generic workflow primitives:

- `workflow_type`: the domain adapter key, such as `completetech_services`, `hiring_pipeline`, or `software_release`.
- `stage`: named lifecycle position in a workflow definition.
- `track`: parallel workstream with stage, status, owner, dependencies, blockers, and output limits.
- `artifact`: versioned work product with source artifacts and approval impact.
- `actor` / `owner`: person, role, specialist skill, plugin, or external approver responsible for an action.
- `decision`: recorded choice with rationale, evidence, and affected tracks/artifacts.
- `gate`: approval, risk, quality, policy, compliance, or authority checkpoint.
- `dependency`: fact, artifact, approval, event, or external condition needed before action.
- `event`: append-only state change in the workflow event log.
- `state_transition`: movement between stages/tracks/statuses allowed by the workflow definition.
- `recovery_action`: smallest useful safe action when work is blocked or underspecified.

Default workflow adapter: `references/completetech-services-workflow.yaml`.

Default CompleteTech lifecycle: Discovery -> Proposal -> Contract -> Delivery -> Customer Success.

Real engagements may move forward, loop backward, skip a stage, reopen an approval, split into parallel tracks, stall, or branch into change-order work. Treat the lifecycle as a state map, not a strict pipeline.

Supporting outputs: Invoice, Certificate, Case Study, Email, Envelope.

Overlay/gate: Security Review. Security is not the default gate for every workflow; use approval/risk triage first. Route ordinary commercial, legal, billing, external-send, public-proof, and client-authority approvals to the appropriate owner or specialist. Invoke security review only when sensitive data, permissions, credentials, new tools/integrations, production launch, external tool actions, public proof confidentiality, incident response, or material security/compliance risk is involved.

## Routing Logic

1. Load the applicable workflow definition from `project_state.workflow_type`; use `completetech_services` when unspecified.
2. Classify intent: create, revise, continue, route, package, send, review, approve, escalate, recover, archive, validate, or start a new workstream.
3. Identify current state from workflow definition, explicit user context, active tracks, existing artifacts, prior handoff notes, approval history, event log, blockers, due dates, and known conflicts.
4. Decide whether the request is forward progress, backward rework, a skipped-stage exception, a reopened approval, a continuation, a revision, an escalation, a packaging task, or a parallel workstream.
5. Check `allowed_transitions`, `routing_rules`, `required_fields`, `gates`, and `specialist_owners` from the workflow definition before routing.
6. Check artifact versions before creating anything new. Revise, supersede, fork, archive, or reference the existing artifact when that is the cleaner state transition.
7. Route by requested outcome, current stage/track, artifact versions, missing facts, conflicts, dependencies, approvals, risk/approval triage, urgency, owner, allowed transitions, and domain adapter rules.
8. Run approval/risk triage. Invoke security review only for security-sensitive triggers; otherwise use the relevant commercial, legal, billing, recipient, proof, client-authority, or domain-specific approval gate.
9. Append a relevant event for material state changes, such as artifact revision, approval change, blocker update, owner change, decision, track start/close, or recovery action.
10. Validate state before final output or external action. Stop or recover if there are invalid transitions, missing owners, orphaned blockers, stale approvals, unversioned artifacts, bypassed gates without rationale, unresolved conflicts, terminal states with open blockers, or external actions without approval evidence.
11. Return a handoff package with workflow type, artifact paths, version relationships, decisions, unresolved questions, blockers, approvals, latest events, next owner, next decision needed, and next recommended skill.

## Skill Invocation Rules

- `agentic-discovery-skill`: fact finding, workflow maps, readiness, success criteria, risk/excluded-use checks, and proposal handoff briefs.
- `agentic-proposal-skill`: buyer-facing scope, SOWs, pilot recommendations, evaluation plans, roadmaps, and change-order proposals.
- `agentic-contract-skill`: agreement content and contract package generation from approved commercial facts.
- `agentic-delivery-skill`: execution, kickoff, project controls, evaluation, launch readiness, handoff, runbooks, and closeout after approval.
- `agentic-customer-success-skill`: relationship state, contact routing, account health, renewals, expansion, escalations, and advocacy planning.
- `agentic-invoice-skill`: invoice-event selection, invoice drafts, billing documents, credits, receipts, retainers, and payment requests.
- `agentic-certificate-skill`: certificate PDF generation from verified recipient and course/workshop facts.
- `agentic-case-study-skill`: verified and approved proof, testimonials, public stories, quote approval, anonymization, and proof libraries.
- `agentic-email-skill`: outbound/inbound message copy, sequences, cover notes, follow-ups, and approval request drafts.
- `agentic-envelope-skill`: addressed envelopes, delivery packages, attachments, recipient metadata, filenames, and send/readiness checklists.
- `agentic-security-review-skill`: confidentiality, sensitive data, permissions, compliance/risk, approval gates, launch blockers, and escalation.

## Boundary Rules

- The orchestrator owns routing and state; specialist skills do not own lifecycle orchestration.
- Email drafts must not replace proposals, invoices, contracts, delivery records, customer records, security reviews, certificates, or proof.
- Envelope packaging must not create contract, invoice, certificate, proposal, delivery, proof, or email content.
- Discovery outputs are not final proposals, contracts, invoices, delivery plans, security signoffs, or public proof.
- Proposal scope must use verified discovery or user-provided facts; use `TBD` for missing scope, proof, pricing, outcomes, or approvals.
- Contract and invoice artifacts must not invent legal, pricing, tax, payment, client, authority, signature, or approval facts.
- Delivery artifacts must stay inside approved scope; route new scope to proposal or change-order work first.
- Security review does not equal legal approval, formal compliance certification, or external penetration testing unless verified evidence is provided.
- Customer success notes are internal/account artifacts, not public proof.
- Case studies, testimonials, quotes, and named references require verified approval.
- Certificates require verified recipient and course/workshop facts; they are not delivery acceptance or public proof.

## Context-Passing Schema

Use this shape when handing work between skills:

```yaml
project_state:
  workflow_type: completetech_services
  workflow_definition: references/completetech-services-workflow.yaml
  client: TBD
  workflow: TBD
  stage: discovery|proposal|contract|delivery|customer_success
  lifecycle_stage: discovery|proposal|contract|delivery|customer_success
  workflow_status: draft|active|stalled|blocked|in_review|approved|launched|closed|reopened|superseded
  active_tracks:
    - track_id: TBD
      track: TBD
      stage: discovery|proposal|contract|delivery|customer_success|support_output|security_review
      status: draft|active|blocked|waiting|complete|superseded
      owner: TBD
      dependencies: []
      blockers: []
      due_date: TBD
  requested_outcome: TBD
  urgency: normal
  owner: TBD
  due_dates: {}
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
  state_transitions:
    - from: TBD
      to: TBD
      when: TBD
      rationale: TBD
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
  rollback_or_recovery_action: TBD
  next_decision_needed: TBD
  next_skill: TBD
  downstream_handoff: TBD
```

Approval status meanings: `unknown` means no evidence; `draft` means not ready for approval; `requested` means waiting on an approver; `partial` means only some scope or action is approved; `approved` means the listed action is permitted; `rejected` means do not proceed; `expired` means prior approval is no longer valid; `superseded` means a newer artifact or decision replaced it; `blocked` means a gate prevents action; `conditional` means proceed only within listed limits.

## Non-Linear and Parallel Work

- Forward progress: move to the next dependency only when required approvals and source artifacts are current.
- Backward loop: route delivery-discovered scope, changed assumptions, or failed acceptance back to discovery, proposal, or change-order work.
- Skipped stage: allow only when the user provides verified equivalent facts and record the skipped-stage rationale in `decision_log`.
- Reopened approval: mark the old approval `superseded` or `expired`, record why it reopened, and stop external action until the new approval is clear.
- Stalled work: keep the track open with owner, blocker, due date, and smallest useful recovery action.
- Parallel tracks: proposal, security review, technical discovery, stakeholder outreach, billing prep, and delivery planning may run at the same time only when each track has explicit dependencies, blockers, owner, and allowed output state.
- Multiple active tracks: update the shared `project_state` after each specialist result and name what changed for downstream tracks.

## Exception Handling

- Missing facts: ask targeted questions when the fact gates action; otherwise insert `TBD`, continue draft-only work, and record the missing fact.
- Conflicting facts: stop the affected track, list the conflict, identify the likely source of truth, and ask for a decision.
- Partial approval: proceed only with the permitted scope and record remaining blockers before downstream work.
- Client scope change: route to proposal or change-order work before delivery expands scope.
- Stakeholder unavailable: assign a fallback owner if known, draft the next safe artifact, and record the decision or approval that is waiting.
- Security blocker: stop launch, credential use, external tool action, public proof, or external send; route to security review with required evidence.
- Billing dispute: stop invoice send or payment request; route to invoice/customer-success context and preserve contract/SOW references without inventing terms.
- Delivery uncovers new scope: keep current delivery inside approved scope and open a new discovery/proposal/change-order track.
- Boundary-crossing request: route to the owning specialist and return a handoff instead of creating the artifact in the orchestrator.
- Contradictory instructions: stop the affected action, summarize the contradiction, and ask for the source of truth.

## Artifact and Version Discipline

Before creating an artifact, check whether an existing artifact should be revised, superseded, forked, archived, or referenced. Handoffs must identify source artifacts, current version, superseded versions, fork reason, approval impact, and whether downstream artifacts need refresh. Do not create parallel artifacts with the same purpose unless there is a recorded fork reason.

## State Validation

Use `references/workflow-definition-schema.yaml` validation rules before final output, external action, or terminal state. Stop or recover when there are invalid transitions, missing owners, orphaned blockers, stale approvals, artifacts without source/version, gates bypassed without rationale, unresolved conflicts, terminal states with open blockers, or external actions without approval evidence.

## Escalation and Recovery

Escalate or stop when there is legal uncertainty, sensitive data exposure, credential risk, production impact, public proof risk, payment/billing ambiguity, client authority ambiguity, contradictory instructions, or any approval that is rejected, blocked, expired, or outside its permitted action.

When blocked, return the smallest useful next action: targeted questions, required evidence, suggested owner, fallback path, draft-only artifact, safe partial output, or rollback/recovery step.

## Common Workflows

1. Lead to scoped proposal: load `completetech_services` adapter -> discovery -> email recap -> proposal -> approval/risk triage -> security review only if sensitive data/tools are involved.
2. Proposal to signed kickoff: proposal -> contract -> invoice -> envelope package -> email cover note -> delivery after approval.
3. Delivery launch readiness: delivery -> security review -> approval gate -> email status/update -> customer success handoff.
4. Post-launch support: delivery support record -> customer success health/renewal -> invoice for retainer/overage if approved.
5. Proof creation: delivery evidence -> customer success approver/timing -> case study -> security/anonymization gate -> email approval request.
6. Training certificate: certificate -> envelope package if mailed -> email delivery message if sent digitally.
7. Messy scope change: delivery finds new workflow -> keep current delivery bounded -> open proposal/change-order track -> approval/risk triage -> run security review only for security-sensitive risk -> update contract/invoice only after approval.
8. Reopened launch approval: security blocker appears after conditional approval -> mark prior approval superseded -> stop launch/external actions -> route to security review -> resume only inside the new permitted scope.
9. Non-services example: load a hiring or software-release adapter -> route by that adapter's stages, artifacts, gates, owners, and allowed transitions instead of the CompleteTech lifecycle.

## Operating Pattern

1. Identify workflow type, current adapter, stage, active tracks, current artifact versions, missing facts, dependencies, blockers, conflicts, approvals, owner, urgency, event log, and next decision needed.
2. Route to the most specific specialist skill, adapter owner, or parallel track when the workflow definition allows it.
3. Pass a compact `project_state` object plus artifact-specific inputs.
4. Preserve facts, assumptions, blockers, approvals, approval history, event log, decision log, source artifacts, and open questions during handoff.
5. Use `TBD` for unknowns instead of filling gaps.
6. Stop at the appropriate approval gate before public use, legal commitment, invoice issuance, production launch, external communication, packaging/sending, or proof publication.
7. If blocked, return the smallest useful recovery action instead of trying to complete the unsafe or underspecified work.
8. After a specialist returns output, update `project_state`, artifact versions, active tracks, decisions, and the next skill or blocker.

## Unresolved Questions

- If the library becomes one package, should repeated renderer logic and shared assets move into common helpers?
- Should `agentic-case-study-skill` be renamed to `agentic-proof-skill`?
- Should sending, invoice issuance, and public proof publication get a dedicated approval workflow file shared by email, envelope, invoice, and case study?

## Rendering to a Branded PDF

Artifacts from this skill are delivered as branded CompleteTech LLC **PDF** documents, not raw Markdown. After drafting the artifact text (optionally starting from a catalog template), render it with the bundled generator:

```bash
pip install -r requirements.txt
python3 scripts/render_pdf.py \
  --markdown artifact.md --out artifact.pdf --png artifact.png \
  --logo assets/logo.png \
  --title "Engagement Orchestration Overview" --doc-type "SERVICES ORCHESTRATION" \
  --subtitle "Prepared for <b>Client Name</b>" \
  --meta "DOCUMENT NO.=ORCH-2026-001" --meta "DATE=2026-05-24"
```

`scripts/render_pdf.py` applies the shared CompleteTech branding (logo, cover page, letterhead band, watermark, footer) and supports a Markdown subset: `#`/`##`/`###` headings, paragraphs, `-` bullet lists, tables, `>` callouts, `**bold**`, and `[PAGE_BREAK]`. It requires `reportlab==4.5.1`; the optional `--png` preview montage requires `pypdfium2==5.8.0` and `pillow==12.2.0`. See `assets/examples/` for a rendered example.
