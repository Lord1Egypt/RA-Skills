# Near-Exhaustive Agentic Development Delivery Catalog

Replace placeholders with verified facts. Use `TBD` for unknowns. Do not mark approvals, test results, launch readiness, or acceptance as complete without evidence.

## Common Placeholders

- `{client_name}`
- `{project_name}`
- `{workflow}`
- `{owner}`
- `{reviewer}`
- `{technical_owner}`
- `{date}`
- `{status}`
- `{milestone}`
- `{timeline}`
- `{scope}`
- `{approval_points}`
- `{risks}`
- `{issues}`
- `{dependencies}`
- `{evaluation_examples}`
- `{test_results}`
- `{next_steps}`

## Templates

### kickoff-agenda
Artifact Type: Kickoff Agenda

Client: {client_name}
Project: {project_name}
Workflow: {workflow}

Agenda:
1. Confirm approved scope
2. Confirm owners, reviewers, and technical contacts
3. Review human approval gates
4. Confirm systems/data access path
5. Review milestones and cadence
6. Confirm evaluation examples and acceptance criteria
7. Review risks, dependencies, and next steps

### client-access-checklist
Artifact Type: Client Access Checklist

Needed access:
- sandbox/test environment
- source documents
- sample inputs
- relevant APIs/tools
- logs or audit trail access
- reviewer queue or approval system
- communication channel

Owners:
{owners}

Open access items:
{dependencies}

### project-plan
Artifact Type: Project Plan

Project: {project_name}
Workflow: {workflow}

Phases:
1. Kickoff and access
2. Workflow confirmation
3. Prototype implementation
4. Evaluation and review
5. Handoff and support

Milestones:
{milestones}

Timeline:
{timeline}

Risks/dependencies:
{risks}
{dependencies}

### milestone-tracker
Artifact Type: Milestone Tracker

| Milestone | Owner | Due date | Status | Evidence | Blockers |
|---|---|---|---|---|---|
| {milestone} | {owner} | {due_date} | {status} | {evidence} | {blockers} |

### weekly-status-update
Artifact Type: Weekly Status Update

Project: {project_name}
Week of: {date}

Status:
{status}

Completed:
{completed}

In progress:
{in_progress}

Decisions needed:
{decisions_needed}

Risks/issues:
{risks}
{issues}

Next steps:
{next_steps}

### decision-log
Artifact Type: Decision Log

| Date | Decision | Owner/approver | Rationale | Impact |
|---|---|---|---|---|
| {date} | {decision} | {owner} | {rationale} | {impact} |

### risk-and-issue-log
Artifact Type: Risk and Issue Log

| ID | Type | Description | Impact | Owner | Mitigation | Status |
|---|---|---|---|---|---|---|
| {id} | {type} | {description} | {impact} | {owner} | {mitigation} | {status} |

### change-request-intake
Artifact Type: Change Request Intake

Requested change:
{change_request}

Reason:
{reason}

Impact to assess:
- scope
- timeline
- fee
- risk
- dependencies
- acceptance criteria

Decision needed from:
{owner}

### dependency-tracker
Artifact Type: Dependency Tracker

| Dependency | Owner | Needed by | Status | Impact if late |
|---|---|---|---|---|
| {dependency} | {owner} | {due_date} | {status} | {impact} |

### stakeholder-communication-plan
Artifact Type: Stakeholder Communication Plan

Stakeholders:
{stakeholders}

Cadence:
- weekly status: {recipients}
- decision requests: {decision_recipients}
- risk escalation: {escalation_contacts}
- acceptance review: {reviewer}

Channels:
{channels}

### prototype-review-checklist
Artifact Type: Prototype Review Checklist

Review:
- workflow path matches approved scope
- inputs are handled correctly
- retrieval sources are appropriate
- draft/recommendation is reviewable
- human approval gates work
- logs capture material steps
- known limitations are visible

Feedback:
{feedback}

### evaluation-run-report
Artifact Type: Evaluation Run Report

Workflow: {workflow}
Run date: {date}

Examples tested:
{evaluation_examples}

Results:
{test_results}

Failures/edge cases:
{issues}

Recommended action:
{next_steps}

### test-results-summary
Artifact Type: Test Results Summary

Scope tested:
{scope}

Pass/fail summary:
{test_results}

Open defects:
{issues}

Acceptance impact:
{acceptance_impact}

### acceptance-review-packet
Artifact Type: Acceptance Review Packet

Project: {project_name}
Workflow: {workflow}

Acceptance criteria:
{acceptance_criteria}

Evidence:
{evidence}

Open items:
{issues}

Requested decision:
Approve acceptance, reject with specific deficiencies, or request listed changes.

### launch-readiness-checklist
Artifact Type: Launch Readiness Checklist

Check:
- approved scope complete
- evaluation evidence reviewed
- human approval gates confirmed
- logs/monitoring configured
- support owner assigned
- rollback/correction path known
- runbook complete
- reviewer quickstart complete
- exclusions documented

Readiness status:
{status}

### monitoring-plan
Artifact Type: Monitoring Plan

Monitor:
- run volume
- approval/rejection patterns
- tool errors
- retrieval failures
- escalations
- user feedback
- exceptions

Owner:
{owner}

Review cadence:
{cadence}

### support-plan
Artifact Type: Support Plan

Support period:
{support_period}

Included support:
{support_scope}

Intake channel:
{support_channel}

Response expectations:
{response_expectations}

Out of scope:
{exclusions}

### handoff-checklist
Artifact Type: Handoff Checklist

Handoff items:
- workflow documentation
- configuration notes
- evaluation examples
- known limitations
- approval model
- monitoring plan
- support plan
- administrator runbook
- reviewer quickstart

Status:
{status}

### administrator-runbook
Artifact Type: Administrator Runbook

Workflow:
{workflow}

Admin tasks:
- review configuration
- manage approved sources
- check logs
- handle errors
- update reviewer list
- escalate issues
- request change orders for new scope

Known limitations:
{limitations}

### user-reviewer-quickstart
Artifact Type: User/Reviewer Quickstart

Reviewer role:
Review generated drafts or recommendations before any sensitive action.

How to review:
1. Check source context
2. Check draft/recommendation
3. Confirm action is allowed
4. Approve, edit, reject, or escalate
5. Confirm log entry if applicable

Escalate when:
{escalation_rules}

### post-launch-review
Artifact Type: Post-Launch Review

Launch date:
{date}

What happened:
{status}

Observations:
{observations}

Issues:
{issues}

Recommended next steps:
{next_steps}

### lessons-learned
Artifact Type: Lessons Learned

What worked:
{worked}

What did not:
{did_not_work}

Changes for next workflow:
{next_steps}

Reusable assets:
{reusable_assets}

### closeout-summary
Artifact Type: Closeout Summary

Project: {project_name}

Final status:
{status}

Delivered artifacts:
{deliverables}

Acceptance:
{acceptance_status}

Support window:
{support_period}

Open items:
{issues}

### support-ticket-intake
Artifact Type: Support Ticket Intake

Ticket:
{ticket_id}

Reported by:
{reporter}

Issue:
{issue}

Workflow/run affected:
{workflow}

Severity:
{severity}

Expected behavior:
{expected_behavior}

Actual behavior:
{actual_behavior}

### escalation-procedure
Artifact Type: Escalation Procedure

Severity levels:
- Low: question or minor issue
- Medium: workflow degradation or repeated error
- High: approval, data, security, or production-impacting concern

Escalation contacts:
{escalation_contacts}

Escalation steps:
1. Capture issue and evidence
2. Pause sensitive actions if needed
3. Notify owner
4. Assign response owner
5. Track resolution

### deployment-runbook
Artifact Type: Deployment Runbook

Deployment scope:
{scope}

Steps:
1. Confirm approval to deploy
2. Confirm environment and access
3. Confirm configuration
4. Run pre-launch checks
5. Deploy
6. Verify logs and monitoring
7. Confirm reviewer access
8. Communicate status

Rollback/correction path:
{rollback_plan}

### defect-remediation-plan
Artifact Type: Defect Remediation Plan

Defect summary:
{issues}

Acceptance impact:
{acceptance_impact}

Fix plan:
{fix_plan}

Owner:
{owner}

Retest plan:
{test_plan}

### training-session-plan
Artifact Type: Training Session Plan

Audience:
{audience}

Objectives:
- understand workflow purpose
- understand approval responsibilities
- review examples
- practice approve/edit/reject/escalate
- know support path

Agenda:
{agenda}
