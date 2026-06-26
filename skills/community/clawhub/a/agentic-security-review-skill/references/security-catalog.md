# Security Review Catalog

Reusable templates for CompleteTech LLC agentic workflow security review. Replace placeholders with verified facts.

### agentic-risk-intake
# Agentic Risk Intake

Client: {client_name}
Workflow: {workflow}
Prepared by: {prepared_by}
Date: {date}

## Purpose

- Business outcome:
- Users and operators:
- Environment: development / staging / production
- Client-facing impact:

## Agentic Capabilities

- Inputs:
- Outputs:
- Tools/integrations:
- Retrieval sources:
- External actions:
- Persistent memory or storage:

## Risk Areas

- Sensitive data involved:
- Irreversible actions possible:
- Broad permissions requested:
- Prompt-injection exposure:
- Approval gates required:
- Logging/audit evidence needed:

## Required Follow-Up

- Security artifacts to create:
- Human/client approvals needed:
- Technical escalation owner:
- Open questions:

### tool-permission-inventory
# Tool Permission Inventory

Client: {client_name}
Workflow: {workflow}
Tool/integration: {tool_name}

## Requested Permissions

| Permission | Purpose | Scope | Environment | Owner | Approved |
| --- | --- | --- | --- | --- | --- |
| {permission} | {purpose} | {scope} | {environment} | {owner} | TBD |

## Least-Privilege Review

- Permissions that are required:
- Permissions that can be removed:
- Read-only alternatives:
- Time-bound or environment-bound limits:
- Admin access justification:

## Decision

- Approved permissions:
- Rejected permissions:
- Conditions before use:
- Review date:

### credential-secret-handling-checklist
# Credential And Secret Handling Checklist

Client: {client_name}
Workflow: {workflow}
Credential type: {credential_type}

## Checklist

- Secret owner identified:
- Storage location approved:
- Rotation process defined:
- Local `.env` files excluded from version control:
- Logs do not expose secret values:
- Test credentials separated from production:
- Access limited to required service/runtime:
- Revocation path documented:
- Exposure response owner named:

## Open Items

- Missing evidence:
- Required escalation:
- Next rotation date:

### data-exposure-review
# Data Exposure Review

Client: {client_name}
Workflow: {workflow}
Data classes: {data_classes}

## Data Flow

- Sources:
- Data read:
- Data written:
- Data exported:
- Data sent to models/providers/tools:
- Data stored after processing:

## Exposure Controls

- Minimum data needed:
- Redaction/masking:
- Access limits:
- Human approval before export:
- Client approval needed:
- Residual risk:

## Decision

- Allowed data:
- Disallowed data:
- Conditions before launch:

### prompt-injection-test-plan
# Prompt-Injection Test Plan

Client: {client_name}
Workflow: {workflow}

## Test Scope

- System prompt/tool policy under test:
- Tools reachable during test:
- Retrieval sources included:
- External actions disabled or sandboxed:

## Test Cases

| Case | Attack Pattern | Expected Safe Behavior | Evidence |
| --- | --- | --- | --- |
| Ignore instructions | Direct override attempt | Refuse or follow higher-priority policy | TBD |
| Tool exfiltration | Request secrets/logs/data export | Do not reveal or export data | TBD |
| Retrieval injection | Malicious retrieved instruction | Treat source as untrusted content | TBD |
| Approval bypass | Ask agent to skip review | Require approval gate | TBD |

## Completion Criteria

- Blockers:
- Required mitigations:
- Retest owner:

### retrieval-source-trust-review
# Retrieval Source Trust Review

Client: {client_name}
Workflow: {workflow}
Source: {source_name}

## Source Assessment

- Source owner:
- Update process:
- Trust level:
- Sensitive content present:
- External/untrusted authors:
- Index refresh cadence:

## Retrieval Controls

- Source allowlist:
- Chunking/filtering approach:
- Prompt-injection handling:
- Citation or evidence requirement:
- Removal process:

## Decision

- Approved sources:
- Blocked sources:
- Conditions:

### approval-gate-audit
# Approval Gate Audit

Client: {client_name}
Workflow: {workflow}

## Actions Requiring Approval

| Action | Approver | Channel | Evidence Required | Can Agent Execute Before Approval |
| --- | --- | --- | --- | --- |
| {action} | {approver} | {channel} | {evidence} | No |

## Audit Findings

- Missing gates:
- Weak gates:
- Bypass paths:
- Required changes:

### external-action-review
# External Action Review

Client: {client_name}
Workflow: {workflow}
Action type: {action_type}

## Action Details

- External system:
- Sender/account:
- Recipient/domain limits:
- File/path/resource limits:
- Payment/billing impact:
- Production impact:
- Human approval required:

## Safety Controls

- Draft-before-send:
- Dry-run/sandbox:
- Idempotency or undo path:
- Logging:
- Escalation contact:

## Decision

- Allowed actions:
- Disallowed actions:
- Conditions before enabling:

### logging-auditability-review
# Logging And Auditability Review

Client: {client_name}
Workflow: {workflow}

## Evidence Needed

- User request:
- Tool calls:
- Data accessed:
- External actions:
- Approval records:
- Errors and retries:
- Operator overrides:

## Review

- Log location:
- Retention period:
- Access controls:
- Redaction of sensitive data:
- Incident investigation sufficiency:
- Missing evidence:

### model-provider-configuration-review
# Model And Provider Configuration Review

Client: {client_name}
Workflow: {workflow}
Provider/model: {provider_model}

## Configuration

- Model/provider:
- System/developer instructions:
- Tool access:
- Data sent to provider:
- Retention settings:
- Safety settings:
- Fallback behavior:

## Review Notes

- Configuration changes since last review:
- Risks introduced:
- Required tests:
- Approval needed:

### data-retention-review
# Data Retention Review

Client: {client_name}
Workflow: {workflow}

## Stored Data

- Inputs stored:
- Outputs stored:
- Logs stored:
- Retrieval indexes:
- Backups:
- Owner:

## Retention Rules

- Retention period:
- Deletion process:
- Export process:
- Client request handling:
- Exceptions:

### dependency-supply-chain-review
# Dependency And Supply-Chain Review

Client: {client_name}
Workflow: {workflow}
Dependency: {dependency_name}

## Dependency Details

- Package/service/vendor:
- Purpose:
- Version:
- Source:
- License:
- Maintainer/vendor:
- Runtime privileges:

## Review

- Known vulnerabilities checked:
- Lockfile or version pinning:
- Update process:
- Secrets/data exposure:
- Alternatives:
- Approval decision:

### sandbox-least-privilege-checklist
# Sandbox And Least-Privilege Checklist

Client: {client_name}
Workflow: {workflow}

## Checklist

- Runs with non-admin access:
- File access restricted to required paths:
- Network access restricted where feasible:
- Production credentials separated:
- Destructive commands gated:
- External actions sandboxed or dry-run tested:
- Tool scopes limited by environment:
- Timeout/rate limits set:
- Manual override path defined:

## Gaps

- Required changes:
- Owner:
- Blocking status:

### production-readiness-security-checklist
# Production Readiness Security Checklist

Client: {client_name}
Workflow: {workflow}

## Launch Controls

- Risk intake complete:
- Permissions reviewed:
- Secrets handling approved:
- Data exposure reviewed:
- Prompt-injection tests complete:
- Retrieval sources approved:
- Approval gates verified:
- External actions reviewed:
- Logging/auditability sufficient:
- Rollback plan ready:
- Incident owner identified:

## Readiness Status

- Ready / Not ready / Ready with conditions:
- Conditions:
- Evidence:
- Approver:

### launch-blocker-checklist
# Launch Blocker Checklist

Client: {client_name}
Workflow: {workflow}

## Blockers

| Blocker | Severity | Evidence | Owner | Required Resolution |
| --- | --- | --- | --- | --- |
| {blocker} | {severity} | {evidence} | {owner} | {resolution} |

## Launch Decision

- Launch blocked: yes / no
- Accepted residual risks:
- Required approval:
- Next review date:

### rollback-plan
# Rollback Plan

Client: {client_name}
Workflow: {workflow}

## Rollback Trigger

- Security trigger:
- Operational trigger:
- Client trigger:

## Rollback Steps

1. Disable agent/tool access:
2. Revoke or rotate credentials:
3. Stop scheduled jobs or webhooks:
4. Restore prior configuration:
5. Notify owners:
6. Preserve logs/evidence:

## Owners

- Technical owner:
- Client contact:
- Approval owner:
- Communications owner:

### incident-response-plan
# Incident Response Plan

Client: {client_name}
Workflow: {workflow}
Incident type: {incident_type}

## First Response

- Disable risky capability:
- Preserve logs:
- Revoke/rotate credentials if needed:
- Stop external actions:
- Notify technical escalation:
- Notify client approver if required:

## Investigation

- Timeline:
- Data/actions affected:
- Root cause:
- Containment:
- Remediation:
- Follow-up artifacts:

### human-escalation-procedure
# Human Escalation Procedure

Client: {client_name}
Workflow: {workflow}

## Escalation Triggers

- Suspected credential exposure:
- Sensitive data exposure:
- Prompt injection reaches tools:
- Approval bypass:
- Unexpected external action:
- Production impact:
- Legal, compliance, billing, or client trust concern:

## Contacts

- Technical escalation: {technical_escalation}
- Client approver: {client_approver}
- Security contact: {security_contact}
- Incident notification: {incident_notification}

Use `TBD` for unknown contacts. Do not invent email addresses.

### red-team-test-report
# Red-Team Test Report

Client: {client_name}
Workflow: {workflow}
Test date: {date}

## Scope

- Capabilities tested:
- Tools enabled:
- Data/retrieval included:
- Environments:

## Findings

| Finding | Severity | Evidence | Mitigation | Retest Status |
| --- | --- | --- | --- | --- |
| {finding} | {severity} | {evidence} | {mitigation} | TBD |

## Decision

- Blockers:
- Residual risks:
- Required approval:

### security-signoff-memo
# Security Signoff Memo

Client: {client_name}
Workflow: {workflow}
Date: {date}

## Review Summary

- Artifacts reviewed:
- Evidence reviewed:
- Open risks:
- Launch blockers:
- Conditions:

## Signoff

- Status: approved / approved with conditions / not approved
- Approver:
- Scope of approval:
- Expiration or next review:
- Notes:

This memo records a project decision. It does not certify compliance or guarantee security.
