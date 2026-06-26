# Near-Exhaustive Agentic Development Discovery Catalog

Replace placeholders with verified facts. Use `TBD` for unknowns.

## Common Placeholders

- `{client_name}`
- `{workflow}`
- `{stakeholders}`
- `{systems}`
- `{data_sources}`
- `{tools}`
- `{inputs}`
- `{outputs}`
- `{approval_points}`
- `{risks}`
- `{exclusions}`
- `{success_criteria}`
- `{evaluation_examples}`
- `{dependencies}`
- `{owner}`
- `{next_step}`

## Templates

### client-intake-questionnaire
Artifact Type: Client Intake Questionnaire

Client: {client_name}
Workflow under consideration: {workflow}

Questions:
1. What repeated workflow should we examine first?
2. What starts the workflow?
3. Who owns the workflow?
4. Which systems, documents, inboxes, tickets, or tools are involved?
5. What decisions are made by people today?
6. What actions require approval?
7. What data is sensitive or restricted?
8. What would make a pilot useful?
9. What timeline or business trigger matters?
10. Who must approve the next step?

### workflow-discovery-script
Artifact Type: Workflow Discovery Script

Opening:
The goal is to understand {workflow} well enough to decide whether a bounded agentic pilot is worth proposing.

Sections:
1. Current trigger and inputs: {inputs}
2. Current steps and handoffs
3. Systems and source-of-truth documents: {systems}
4. Human decisions and approvals: {approval_points}
5. Common edge cases
6. Risks and excluded uses: {risks}
7. Evaluation examples and success criteria
8. Next step: {next_step}

### stakeholder-interview-guide
Artifact Type: Stakeholder Interview Guide

Stakeholders:
{stakeholders}

Operator questions:
- What work repeats most often?
- Where do delays or rework happen?
- What context is hard to find?

Reviewer questions:
- What must you approve?
- What makes a draft acceptable?
- What requires escalation?

Technical owner questions:
- Which systems and APIs are available?
- What permissions are needed?
- What logging and retention rules apply?

Decision maker questions:
- What business outcome matters?
- What risks would block approval?
- What evidence would justify a pilot?

### current-state-workflow-map
Artifact Type: Current-State Workflow Map

Workflow: {workflow}

Current trigger:
{inputs}

Current steps:
1. {step_1}
2. {step_2}
3. {step_3}

Systems/tools:
{systems}

Decision points:
{decision_points}

Pain points:
{pain_points}

Known exceptions:
{exceptions}

### future-state-agentic-workflow-map
Artifact Type: Future-State Agentic Workflow Map

Workflow: {workflow}

Proposed reviewed-agent path:
1. Intake received
2. Agent classifies or extracts key facts
3. Agent retrieves context from approved sources
4. Agent drafts or recommends next action
5. Human reviews and approves where required
6. Approved action is taken
7. Result and rationale are logged

Agent responsibilities:
{agent_responsibilities}

Human approval points:
{approval_points}

Logs/monitoring:
{logging_needs}

### systems-and-data-access-checklist
Artifact Type: Systems and Data Access Checklist

Systems:
{systems}

Data sources:
{data_sources}

Check:
- system owner identified
- access path known
- sandbox/test environment available
- sample inputs available
- source-of-truth rules known
- data sensitivity understood
- retention expectations known
- export restrictions known

Open access issues:
{dependencies}

### tool-api-readiness-checklist
Artifact Type: Tool/API Readiness Checklist

Tools/APIs:
{tools}

Check:
- API documentation available
- authentication method known
- permission scope understood
- rate limits known
- test credentials available
- write actions can be disabled or reviewed
- audit logs available
- rollback or correction path known

Readiness notes:
{notes}

### human-approval-gate-checklist
Artifact Type: Human Approval Gate Checklist

Workflow: {workflow}

Require human approval before:
- external communication
- production change
- purchase or financial action
- data export
- account, permission, or security change
- material business decision
- regulated or sensitive action

Specific approval points:
{approval_points}

Reviewer roles:
{reviewer_roles}

### risk-and-excluded-use-checklist
Artifact Type: Risk and Excluded-Use Checklist

Risks to assess:
- sensitive data
- incorrect or incomplete output
- unauthorized tool use
- missing approval
- poor source retrieval
- production impact
- legal/regulatory constraints

Excluded uses:
{exclusions}

Mitigations:
{mitigations}

### success-criteria-worksheet
Artifact Type: Success Criteria Worksheet

Workflow: {workflow}

A successful pilot should prove:
- the workflow can be mapped clearly
- approved sources can be retrieved
- drafts/recommendations are reviewable
- approval gates are practical
- logs capture material steps
- users can operate the workflow after handoff

Specific criteria:
{success_criteria}

### evaluation-example-worksheet
Artifact Type: Evaluation Example Worksheet

Workflow: {workflow}

Representative examples:
{evaluation_examples}

For each example capture:
- input
- expected classification
- relevant source context
- expected draft/recommendation
- required approval
- expected log entry
- failure modes

### pilot-readiness-scorecard
Artifact Type: Pilot Readiness Scorecard

Score each 1-5:
- repeated workflow clarity
- business value
- system/data access
- source-of-truth clarity
- approval gate clarity
- evaluation example availability
- risk manageability
- stakeholder ownership

Recommendation:
{next_step}

Notes:
{notes}

### discovery-recap-memo
Artifact Type: Discovery Recap Memo

Client: {client_name}
Workflow: {workflow}

What we learned:
{current_state}

Pain points:
{pain_points}

Systems/data:
{systems}

Approval/risk notes:
{approval_points}
{risks}

Recommended next step:
{next_step}

### requirements-brief-for-proposal-sow-handoff
Artifact Type: Requirements Brief for Proposal/SOW Handoff

Client: {client_name}
Workflow: {workflow}
Owner: {owner}

Recommended scope:
{recommended_scope}

Deliverables to propose:
{deliverables}

Success criteria:
{success_criteria}

Assumptions:
{assumptions}

Exclusions:
{exclusions}

Dependencies:
{dependencies}

### assumptions-and-unknowns-log
Artifact Type: Assumptions and Unknowns Log

Known facts:
{known_facts}

Assumptions:
{assumptions}

Unknowns:
{unknowns}

Owner for answers:
{owner}

Deadline:
{deadline}

### stakeholder-responsibility-matrix
Artifact Type: Stakeholder Responsibility Matrix

| Area | Client owner | CompleteTech LLC role | Notes |
|---|---|---|---|
| Workflow ownership | {workflow_owner} | Discovery/scoping | {notes} |
| Systems access | {technical_owner} | Access requirements | {notes} |
| Review/approval | {review_owner} | Approval model design | {notes} |
| Business decision | {decision_maker} | Proposal recommendation | {notes} |

### implementation-dependency-checklist
Artifact Type: Implementation Dependency Checklist

Dependencies:
- signed scope or written approval
- project owner
- reviewer list
- sample inputs
- system access
- source documents
- API/tool credentials
- approval rules
- evaluation examples
- logging/retention requirements

Open dependencies:
{dependencies}

### data-sensitivity-and-retention-worksheet
Artifact Type: Data Sensitivity and Retention Worksheet

Data involved:
{data_sources}

Sensitivity categories:
- public
- internal
- confidential
- regulated or restricted
- credentials/secrets

Retention expectations:
{retention}

Handling requirements:
{handling_requirements}

### workflow-prioritization-matrix
Artifact Type: Workflow Prioritization Matrix

Score each candidate 1-5:
- repeatability
- business value
- pain/urgency
- data readiness
- tool readiness
- approval clarity
- risk manageability
- pilot size

Candidate workflows:
{candidate_workflows}

Recommended first workflow:
{workflow}

### quick-qualification-checklist
Artifact Type: Quick Qualification Checklist

Qualify if:
- workflow repeats often
- inputs are identifiable
- source context exists
- outputs are reviewable
- approval points are clear or discoverable
- risk is manageable
- owner exists
- buyer has a reason to act

Disqualify or defer if:
- workflow is one-off
- final decision is regulated or safety-critical without separate review
- no owner exists
- no sample inputs are available
- scope is too broad for a pilot

Recommendation:
{next_step}

### logging-and-monitoring-needs-worksheet
Artifact Type: Logging and Monitoring Needs Worksheet

Workflow: {workflow}

Log:
- inputs received
- retrieval sources used
- draft/recommendation
- tool calls proposed or made
- reviewer approval/rejection
- final action
- errors and escalations

Monitoring needs:
{monitoring_needs}

### support-and-handoff-discovery-worksheet
Artifact Type: Support and Handoff Discovery Worksheet

Post-delivery expectations:
- who operates the workflow?
- who reviews outputs?
- who handles exceptions?
- who updates source documents?
- who monitors logs?
- what support window is expected?

Support/handoff notes:
{support_expectations}

### pilot-to-production-readiness-checklist
Artifact Type: Pilot-to-Production Readiness Checklist

Check:
- pilot accepted
- evaluation examples passed
- approval gates confirmed
- production permissions reviewed
- monitoring/logging ready
- support owner assigned
- rollback/correction path known
- documentation complete
- training complete
- excluded uses documented

Production readiness recommendation:
{next_step}
