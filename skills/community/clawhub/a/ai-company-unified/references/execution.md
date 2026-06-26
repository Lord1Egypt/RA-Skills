# Execution Reference

> Module: execution
> Version: 1.0.0
> Owner: CTO
> Dependencies: governance-and-strategy, quality-and-operations, platform-and-infrastructure

This document defines the complete execution subsystem for the AI-Company unified skill. It specifies how work is dispatched, monitored, recovered, and closed across the entire organization — from the CEO Command Center down to individual agent task execution. All execution flows must comply with the constraints defined in [method-patterns.md](method-patterns.md) and be VirusTotal-safe (zero executable files, zero network calls from template code, zero dynamic code evaluation).

---

## Table of Contents

1. [Execution Modes](#1-execution-modes)
2. [Triggers](#2-triggers)
3. [Error Recovery](#3-error-recovery)
4. [CEO Command Center](#4-ceo-command-center)
5. [Workflow Templates](#5-workflow-templates)
6. [Execution Schema Reference](#6-execution-schema-reference)
7. [Constraints](#7-constraints)
8. [Quality Metrics](#8-quality-metrics)

---

## 1. Execution Modes

The AI-Company supports four execution modes that govern the degree of autonomy an agent has when performing tasks. The mode is selected at task creation time and persists for the lifetime of that execution context. Mode selection depends on task risk classification, stakeholder involvement requirements, and regulatory constraints.

### 1.1 Mode Overview

| Mode | Autonomy | Human-in-the-Loop | Use Case |
|------|----------|-------------------|----------|
| Auto | Full | None | Routine, well-understood tasks |
| Approve | Constrained | Approval before execution | Tasks with external impact |
| Review | Full with post-check | Review after completion | Tasks requiring quality verification |
| Hybrid | Per-task | Mixed per task type | Complex multi-phase workflows |

### 1.2 Auto Mode

Auto mode grants full autonomous execution authority to the assigned agent. The agent proceeds through all phases — plan, execute, verify, and close — without requiring any human approval or review. This mode is reserved for tasks that meet all of the following safety criteria:

**Eligibility Criteria:**
- Task risk level is P3 (Low) or below
- No external system modifications (write operations are internal only)
- No PII or sensitive data handling
- No regulatory or compliance implications
- Task has been previously executed successfully at least 3 times
- Agent has demonstrated competence in the task domain

**Execution Flow:**

```
AUTO EXECUTION FLOW:

  [Task Received] -> [Validate Input] -> [Check Eligibility]
                                              |
                                    PASS? ----+---- FAIL?
                                      |               |
                                 [Plan Task]    [Escalate to Approve Mode]
                                      |
                                [Execute Steps]
                                      |
                                [Self-Verify]
                                      |
                              PASS? ----+---- FAIL?
                                |               |
                          [Record Result]  [Error Recovery]
                                |
                          [Close Task]
```

**Schema:**

```json
{
  "execution_mode": "auto",
  "task": {
    "task_id": "TASK-{NNN}",
    "description": "string",
    "agent_id": "AGENT_ID",
    "department": "DEPARTMENT_ID",
    "risk_level": "P3|P4",
    "estimated_duration": "ISO-8601-duration",
    "timeout": "ISO-8601-duration"
  },
  "auto_config": {
    "max_retries": 3,
    "backoff_base_ms": 1000,
    "backoff_multiplier": 2.0,
    "circuit_breaker_threshold": 5,
    "self_verify": true,
    "rollback_on_failure": true,
    "audit_log": true
  },
  "guardrails": {
    "max_output_size_kb": 512,
    "allowed_operations": ["READ", "WRITE_INTERNAL", "COMPUTE"],
    "forbidden_operations": ["WRITE_EXTERNAL", "DELETE", "NETWORK"],
    "timeout_hard_limit_ms": 300000
  }
}
```

**Example — Automated Daily Metrics Collection:**

```json
{
  "execution_mode": "auto",
  "task": {
    "task_id": "TASK-4471",
    "description": "Collect daily operational metrics from all departments and update dashboard",
    "agent_id": "COO-METRICS-01",
    "department": "governance-and-strategy",
    "risk_level": "P3",
    "estimated_duration": "PT15M",
    "timeout": "PT30M"
  },
  "auto_config": {
    "max_retries": 3,
    "backoff_base_ms": 5000,
    "backoff_multiplier": 2.0,
    "circuit_breaker_threshold": 5,
    "self_verify": true,
    "rollback_on_failure": false,
    "audit_log": true
  },
  "guardrails": {
    "max_output_size_kb": 1024,
    "allowed_operations": ["READ", "WRITE_INTERNAL", "COMPUTE"],
    "forbidden_operations": ["WRITE_EXTERNAL", "DELETE", "NETWORK"],
    "timeout_hard_limit_ms": 1800000
  }
}
```

### 1.3 Approve Mode

Approve mode requires explicit authorization from an authorized approver before the agent begins execution. The agent produces a plan, presents it to the approver, and waits for confirmation before proceeding. If the approver rejects the plan or does not respond within the approval window, the task is suspended and escalated.

**Approval Authority Matrix:**

| Task Risk | Approver | Max Wait Time | Escalation |
|-----------|----------|---------------|------------|
| P0-Critical | CEO + Board | 1 hour | Emergency protocol |
| P1-High | C-Suite (relevant department) | 4 hours | CEO |
| P2-Medium | Department Head | 24 hours | COO |
| P3-Low | Any L3+ agent | 48 hours | Department Head |

**Execution Flow:**

```
APPROVE EXECUTION FLOW:

  [Task Received] -> [Classify Risk] -> [Identify Approver]
                                               |
                                        [Generate Plan]
                                               |
                                     [Submit for Approval]
                                               |
                                  APPROVED? ----+---- REJECTED?
                                    |                    |
                              [Execute Task]      [Revise Plan] -> [Resubmit]
                                    |
                              [Self-Verify]
                                    |
                              [Report to Approver]
                                    |
                              [Close Task]

  TIMEOUT PATH:
  [Approval Wait] -> [Timeout Exceeded] -> [Escalate] -> [Suspend Task]
```

**Schema:**

```json
{
  "execution_mode": "approve",
  "task": {
    "task_id": "TASK-{NNN}",
    "description": "string",
    "agent_id": "AGENT_ID",
    "department": "DEPARTMENT_ID",
    "risk_level": "P0|P1|P2",
    "approver_id": "AGENT_ID",
    "approval_window": "ISO-8601-duration",
    "escalation_path": ["AGENT_ID", "AGENT_ID"]
  },
  "approval_config": {
    "plan_format": "structured",
    "plan_sections": ["scope", "steps", "risk_assessment", "rollback_plan", "estimated_impact"],
    "max_revisions": 3,
    "require_acknowledgment": true,
    "approval_criteria": ["risk_acceptable", "resources_available", "timeline_feasible"]
  },
  "execution_config": {
    "proceed_after_approval": true,
    "notify_on_completion": true,
    "generate_post_report": true
  }
}
```

**Example — Production Deployment Approval:**

```json
{
  "execution_mode": "approve",
  "task": {
    "task_id": "TASK-5203",
    "description": "Deploy v2.4.1 hotfix to production cluster with database migration",
    "agent_id": "CTO-DEPLOY-01",
    "department": "technology-and-engineering",
    "risk_level": "P1",
    "approver_id": "CTO",
    "approval_window": "PT4H",
    "escalation_path": ["CEO"]
  },
  "approval_config": {
    "plan_format": "structured",
    "plan_sections": [
      "scope",
      "pre_deployment_checks",
      "deployment_steps",
      "database_migration_plan",
      "rollback_procedure",
      "risk_assessment",
      "post_deployment_verification"
    ],
    "max_revisions": 3,
    "require_acknowledgment": true,
    "approval_criteria": ["all_pre_checks_passed", "rollback_tested", "stakeholders_notified"]
  },
  "execution_config": {
    "proceed_after_approval": true,
    "notify_on_completion": true,
    "generate_post_report": true
  }
}
```

### 1.4 Review Mode

Review mode allows full autonomous execution but mandates a quality review of the output before the task is formally closed. The agent executes the task, produces deliverables, and submits them to a designated reviewer. The reviewer evaluates the output against defined quality criteria and either approves closure or requests revision.

**Review Criteria by Output Type:**

| Output Type | Reviewer | Criteria | Turnaround |
|-------------|----------|----------|------------|
| Code | CTO or designated L4+ | Security, performance, style, tests | 24 hours |
| Report | Department Head | Accuracy, completeness, formatting | 48 hours |
| Decision Document | CEO | Strategic alignment, data quality | 72 hours |
| Skill Package | CQO | G0-G7 quality gates | 96 hours |
| External Communication | CLO + CISO | Compliance, brand, legal | 48 hours |

**Execution Flow:**

```
REVIEW EXECUTION FLOW:

  [Task Received] -> [Execute Autonomously] -> [Generate Output]
                                                      |
                                              [Self-Assessment]
                                                      |
                                              [Submit for Review]
                                                      |
                                        REVIEW PASSED? ----+---- REVISION?
                                          |                      |
                                    [Record Result]     [Revise Output]
                                          |                      |
                                    [Close Task]        [Resubmit for Review]
                                                         (max 3 revisions)

  REVISION EXHAUSTED PATH:
  [Max Revisions] -> [Escalate] -> [Manual Intervention Required]
```

**Schema:**

```json
{
  "execution_mode": "review",
  "task": {
    "task_id": "TASK-{NNN}",
    "description": "string",
    "agent_id": "AGENT_ID",
    "department": "DEPARTMENT_ID",
    "reviewer_id": "AGENT_ID",
    "output_type": "code|report|document|skill|communication"
  },
  "review_config": {
    "review_criteria": ["accuracy", "completeness", "compliance", "quality"],
    "max_revisions": 3,
    "revision_timeout": "ISO-8601-duration",
    "auto_quality_check": true,
    "quality_threshold": 0.8,
    "review_turnaround": "ISO-8601-duration",
    "escalate_after_timeout": true
  },
  "output_spec": {
    "format": "string",
    "template_id": "TEMPLATE_ID (optional)",
    "aigc_label_required": true,
    "pii_masking_required": false,
    "max_size_kb": 512
  }
}
```

**Example — Security Report Review:**

```json
{
  "execution_mode": "review",
  "task": {
    "task_id": "TASK-6310",
    "description": "Generate Q2 security posture assessment report for Board review",
    "agent_id": "CISO-ANALYST-02",
    "department": "security-and-compliance",
    "reviewer_id": "CISO",
    "output_type": "report"
  },
  "review_config": {
    "review_criteria": ["accuracy", "completeness", "compliance", "executive_readability"],
    "max_revisions": 3,
    "revision_timeout": "PT48H",
    "auto_quality_check": true,
    "quality_threshold": 0.85,
    "review_turnaround": "PT72H",
    "escalate_after_timeout": true
  },
  "output_spec": {
    "format": "markdown",
    "template_id": "TPL-SEC-REPORT-QTR",
    "aigc_label_required": true,
    "pii_masking_required": true,
    "max_size_kb": 2048
  }
}
```

### 1.5 Hybrid Mode

Hybrid mode applies different execution modes to different phases of a complex multi-phase workflow. Each phase can independently specify auto, approve, or review mode. This enables fine-grained control where some phases require human oversight while others can proceed autonomously.

**Phase Mode Selection Guidelines:**

| Phase Type | Recommended Mode | Rationale |
|------------|-----------------|-----------|
| Data collection | Auto | Read-only, low risk |
| Analysis | Auto or Review | Internal computation, quality check beneficial |
| Decision making | Approve | External impact, requires authorization |
| External action | Approve | Modifies external systems |
| Report generation | Review | Output quality matters |
| Deployment | Approve | Production impact |
| Post-deployment verification | Auto | Read-only checks |

**Execution Flow:**

```
HYBRID EXECUTION FLOW:

  [Workflow Received] -> [Parse Phases] -> [Validate Phase Dependencies]
                                                    |
  PHASE 1 (Auto)    -> [Execute] -> [Self-Verify] -> [Phase Complete]
                                                    |
  PHASE 2 (Review)  -> [Execute] -> [Generate Output] -> [Submit Review]
                                                    |         |
                                              [Review Result] [Timeout Escalate]
                                                    |
  PHASE 3 (Approve) -> [Generate Plan] -> [Wait Approval] -> [Execute]
                                                    |              |
                                              [Approved]     [Rejected/Escalate]
                                                    |
  PHASE N (...)      -> [...phase execution...]
                                                    |
  [All Phases Complete] -> [Workflow Summary] -> [Close Workflow]
```

**Schema:**

```json
{
  "execution_mode": "hybrid",
  "workflow": {
    "workflow_id": "WF-{NNN}",
    "description": "string",
    "total_phases": 3,
    "orchestrator_id": "AGENT_ID",
    "department": "DEPARTMENT_ID"
  },
  "phases": [
    {
      "phase_id": "PHASE-1",
      "phase_name": "Data Collection",
      "execution_mode": "auto",
      "phase_order": 1,
      "dependencies": [],
      "task_spec": { "..." : "task specification" },
      "transition": {
        "on_success": "PHASE-2",
        "on_failure": "ERROR_RECOVERY",
        "on_timeout": "ESCALATE"
      }
    },
    {
      "phase_id": "PHASE-2",
      "phase_name": "Analysis and Recommendations",
      "execution_mode": "review",
      "phase_order": 2,
      "dependencies": ["PHASE-1"],
      "reviewer_id": "AGENT_ID",
      "task_spec": { "..." : "task specification" },
      "transition": {
        "on_success": "PHASE-3",
        "on_failure": "REVISE",
        "on_timeout": "ESCALATE"
      }
    },
    {
      "phase_id": "PHASE-3",
      "phase_name": "Implementation",
      "execution_mode": "approve",
      "phase_order": 3,
      "dependencies": ["PHASE-2"],
      "approver_id": "AGENT_ID",
      "task_spec": { "..." : "task specification" },
      "transition": {
        "on_success": "WORKFLOW_COMPLETE",
        "on_failure": "ROLLBACK",
        "on_timeout": "ESCALATE"
      }
    }
  ],
  "workflow_config": {
    "max_total_duration": "ISO-8601-duration",
    "allow_phase_parallel": false,
    "global_timeout": "ISO-8601-duration",
    "generate_summary": true
  }
}
```

**Example — End-to-End Financial Report Workflow:**

```json
{
  "execution_mode": "hybrid",
  "workflow": {
    "workflow_id": "WF-2105",
    "description": "Monthly financial close process: collect, analyze, validate, and publish",
    "total_phases": 4,
    "orchestrator_id": "CFO-OPS-01",
    "department": "finance-and-risk"
  },
  "phases": [
    {
      "phase_id": "PHASE-1",
      "phase_name": "Data Collection",
      "execution_mode": "auto",
      "phase_order": 1,
      "dependencies": [],
      "task_spec": {
        "description": "Collect financial data from all department systems",
        "estimated_duration": "PT1H"
      },
      "transition": { "on_success": "PHASE-2", "on_failure": "RETRY_3X", "on_timeout": "ESCALATE" }
    },
    {
      "phase_id": "PHASE-2",
      "phase_name": "Financial Analysis",
      "execution_mode": "auto",
      "phase_order": 2,
      "dependencies": ["PHASE-1"],
      "task_spec": {
        "description": "Run financial models, identify variances, flag anomalies",
        "estimated_duration": "PT2H"
      },
      "transition": { "on_success": "PHASE-3", "on_failure": "RETRY_3X", "on_timeout": "ESCALATE" }
    },
    {
      "phase_id": "PHASE-3",
      "phase_name": "Report Draft Review",
      "execution_mode": "review",
      "phase_order": 3,
      "dependencies": ["PHASE-2"],
      "reviewer_id": "CFO",
      "task_spec": {
        "description": "Generate draft financial report with analysis narrative",
        "estimated_duration": "PT3H"
      },
      "transition": { "on_success": "PHASE-4", "on_failure": "REVISE", "on_timeout": "ESCALATE" }
    },
    {
      "phase_id": "PHASE-4",
      "phase_name": "Board Submission",
      "execution_mode": "approve",
      "phase_order": 4,
      "dependencies": ["PHASE-3"],
      "approver_id": "CEO",
      "task_spec": {
        "description": "Submit final financial report for Board distribution",
        "estimated_duration": "PT30M"
      },
      "transition": { "on_success": "WORKFLOW_COMPLETE", "on_failure": "REVERT", "on_timeout": "ESCALATE" }
    }
  ],
  "workflow_config": {
    "max_total_duration": "PT48H",
    "allow_phase_parallel": false,
    "global_timeout": "PT72H",
    "generate_summary": true
  }
}
```

---

## 2. Triggers

Triggers define how and when execution is initiated. The AI-Company supports four trigger types, each suited to different operational patterns. All triggers produce a standardized execution event that feeds into the execution pipeline.

### 2.1 Trigger Overview

| Trigger Type | Initiation | Latency | Use Case |
|-------------|-----------|---------|----------|
| Schedule | Cron expression | Deterministic | Recurring operational tasks |
| Event | System or business event | Near real-time | Reactive workflows |
| Webhook | HTTP callback | On-demand | External integrations |
| Manual | User request | Immediate | Ad-hoc tasks |

### 2.2 Schedule Trigger

Schedule triggers use cron-based expressions to initiate execution at predetermined times. All scheduled executions are validated against the current state to avoid redundant or conflicting runs.

**Cron Expression Format:**

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, 0=Sunday)
│ │ │ │ │
* * * * *
```

**Predefined Schedules:**

| Schedule Name | Cron Expression | Description |
|---------------|----------------|-------------|
| Every 5 minutes | `*/5 * * * *` | High-frequency monitoring |
| Hourly | `0 * * * *` | Standard monitoring |
| Daily at midnight | `0 0 * * *` | End-of-day processing |
| Daily at 8 AM | `0 8 * * *` | Morning reports |
| Weekly Monday | `0 9 * * 1` | Weekly reviews |
| Monthly 1st | `0 0 1 * *` | Monthly close |
| Quarterly | `0 0 1 1,4,7,10 *` | Quarterly reviews |

**Execution Event Schema:**

```json
{
  "trigger_type": "schedule",
  "trigger_id": "TRG-{NNN}",
  "cron_expression": "string",
  "schedule_name": "string (optional)",
  "task_spec": {
    "task_id": "TASK-{NNN}",
    "description": "string",
    "agent_id": "AGENT_ID",
    "department": "DEPARTMENT_ID",
    "execution_mode": "auto|approve|review|hybrid",
    "priority": "P0|P1|P2|P3"
  },
  "schedule_config": {
    "timezone": "UTC",
    "enabled": true,
    "max_concurrent_runs": 1,
    "overlap_policy": "SKIP|QUEUE|CANCEL_PREVIOUS",
    "retry_on_missed": true,
    "missed_window_minutes": 60,
    "last_run": "ISO-8601 (read-only)",
    "next_run": "ISO-8601 (read-only)"
  },
  "guardrails": {
    "skip_if_previous_running": true,
    "max_skips_before_alert": 3,
    "alert_on_consecutive_failures": 5,
    "maintenance_window": {
      "start": "HH:MM",
      "end": "HH:MM",
      "timezone": "UTC"
    }
  }
}
```

**Example — Daily SLA Report Generation:**

```json
{
  "trigger_type": "schedule",
  "trigger_id": "TRG-8012",
  "cron_expression": "0 7 * * *",
  "schedule_name": "daily-sla-report",
  "task_spec": {
    "task_id": "auto-generated",
    "description": "Generate daily SLA compliance report and distribute to C-Suite",
    "agent_id": "COO-SLA-01",
    "department": "governance-and-strategy",
    "execution_mode": "auto",
    "priority": "P2"
  },
  "schedule_config": {
    "timezone": "UTC",
    "enabled": true,
    "max_concurrent_runs": 1,
    "overlap_policy": "SKIP",
    "retry_on_missed": true,
    "missed_window_minutes": 120
  },
  "guardrails": {
    "skip_if_previous_running": true,
    "max_skips_before_alert": 2,
    "alert_on_consecutive_failures": 3
  }
}
```

**Example — Weekly Security Scan:**

```json
{
  "trigger_type": "schedule",
  "trigger_id": "TRG-8013",
  "cron_expression": "0 2 * * 0",
  "schedule_name": "weekly-security-scan",
  "task_spec": {
    "task_id": "auto-generated",
    "description": "Run full security vulnerability scan across all deployed systems",
    "agent_id": "CISO-SCAN-01",
    "department": "security-and-compliance",
    "execution_mode": "review",
    "priority": "P1"
  },
  "schedule_config": {
    "timezone": "UTC",
    "enabled": true,
    "max_concurrent_runs": 1,
    "overlap_policy": "CANCEL_PREVIOUS",
    "retry_on_missed": false,
    "missed_window_minutes": 0
  },
  "guardrails": {
    "skip_if_previous_running": true,
    "max_skips_before_alert": 1,
    "alert_on_consecutive_failures": 1,
    "maintenance_window": {
      "start": "01:00",
      "end": "04:00",
      "timezone": "UTC"
    }
  }
}
```

### 2.3 Event Trigger

Event triggers react to system-generated or business events in near real-time. Events are published to the HQ Message Bus and consumed by trigger listeners that match event patterns.

**Event Categories:**

| Category | Source | Example Events |
|----------|--------|---------------|
| Operational | COO | SLA breach, resource exhaustion, agent offline |
| Financial | CFO | Budget threshold exceeded, invoice overdue, revenue milestone |
| Security | CISO | Anomaly detected, access violation, vulnerability found |
| Compliance | CLO | Regulation change, audit finding, policy violation |
| Quality | CQO | Quality gate failure, test coverage drop, DORA degradation |
| External | CMO | Market event, competitor action, customer escalation |

**Event Schema:**

```json
{
  "trigger_type": "event",
  "trigger_id": "TRG-{NNN}",
  "event_pattern": {
    "category": "operational|financial|security|compliance|quality|external",
    "source": "AGENT_ID",
    "event_type": "string",
    "severity": "P0|P1|P2|P3|P4",
    "filters": {
      "field": "value"
    }
  },
  "task_spec": {
    "task_id": "auto-generated",
    "description": "string",
    "agent_id": "AGENT_ID",
    "department": "DEPARTMENT_ID",
    "execution_mode": "auto|approve|review|hybrid",
    "priority": "P0|P1|P2|P3"
  },
  "event_config": {
    "debounce_ms": 0,
    "max_triggers_per_window": 10,
    "window_minutes": 60,
    "correlation_group": "string (optional)",
    "require_correlation_id": false,
    "expiry": "ISO-8601-duration"
  },
  "conditions": {
    "all": [
      { "field": "string", "operator": "eq|ne|gt|lt|gte|lte|contains", "value": "any" }
    ],
    "any": [
      { "field": "string", "operator": "eq|ne|gt|lt|gte|lte|contains", "value": "any" }
    ]
  }
}
```

**Example — SLA Breach Auto-Response:**

```json
{
  "trigger_type": "event",
  "trigger_id": "TRG-9021",
  "event_pattern": {
    "category": "operational",
    "source": "COO",
    "event_type": "SLA_BREACH",
    "severity": "P1"
  },
  "task_spec": {
    "task_id": "auto-generated",
    "description": "Investigate SLA breach, identify root cause, and initiate mitigation",
    "agent_id": "COO-OPS-01",
    "department": "governance-and-strategy",
    "execution_mode": "auto",
    "priority": "P1"
  },
  "event_config": {
    "debounce_ms": 30000,
    "max_triggers_per_window": 5,
    "window_minutes": 60,
    "correlation_group": "sla-breach-response"
  },
  "conditions": {
    "all": [
      { "field": "breach_duration_minutes", "operator": "gt", "value": 5 }
    ]
  }
}
```

**Example — Security Anomaly Response:**

```json
{
  "trigger_type": "event",
  "trigger_id": "TRG-9022",
  "event_pattern": {
    "category": "security",
    "source": "CISO",
    "event_type": "ANOMALY_DETECTED",
    "severity": "P0"
  },
  "task_spec": {
    "task_id": "auto-generated",
    "description": "Activate incident response protocol for detected security anomaly",
    "agent_id": "CISO-IR-01",
    "department": "security-and-compliance",
    "execution_mode": "auto",
    "priority": "P0"
  },
  "event_config": {
    "debounce_ms": 0,
    "max_triggers_per_window": 100,
    "window_minutes": 60
  },
  "conditions": {
    "any": [
      { "field": "cvss_score", "operator": "gte", "value": 7.0 },
      { "field": "threat_type", "operator": "eq", "value": "ACTIVE_EXPLOIT" }
    ]
  }
}
```

### 2.4 Webhook Trigger

Webhook triggers allow external systems to initiate execution through HTTP callbacks. Webhooks are secured with HMAC-SHA256 signature verification and are rate-limited to prevent abuse.

**Security Requirements:**
- HMAC-SHA256 signature verification on every request
- TLS 1.2+ mandatory for webhook endpoints
- IP whitelist (configurable per webhook)
- Rate limiting: max 100 requests per minute per webhook
- Payload validation against registered schema
- Maximum payload size: 1 MB
- Request timeout: 30 seconds

**Webhook Schema:**

```json
{
  "trigger_type": "webhook",
  "trigger_id": "TRG-{NNN}",
  "webhook_config": {
    "endpoint_path": "/webhook/{webhook_id}",
    "secret": "HMAC-SHA256 signing key (stored securely)",
    "method": "POST",
    "content_type": "application/json",
    "ip_whitelist": ["CIDR blocks"],
    "rate_limit": {
      "max_requests_per_minute": 100,
      "burst_limit": 10
    },
    "auth": {
      "type": "hmac_sha256",
      "header_name": "X-Webhook-Signature",
      "timestamp_header": "X-Webhook-Timestamp",
      "max_age_seconds": 300
    }
  },
  "payload_schema": {
    "type": "object",
    "properties": {
      "event": { "type": "string" },
      "data": { "type": "object" },
      "timestamp": { "type": "string", "format": "ISO-8601" },
      "source": { "type": "string" }
    },
    "required": ["event", "data", "timestamp", "source"]
  },
  "task_spec": {
    "task_id": "auto-generated",
    "description": "string",
    "agent_id": "AGENT_ID",
    "department": "DEPARTMENT_ID",
    "execution_mode": "auto|approve|review|hybrid",
    "priority": "P0|P1|P2|P3"
  },
  "response_config": {
    "acknowledge_immediately": true,
    "delivery_guarantee": "at_least_once",
    "retry_policy": {
      "max_retries": 3,
      "backoff_ms": [1000, 5000, 15000]
    }
  }
}
```

**Example — Customer Feedback Integration:**

```json
{
  "trigger_type": "webhook",
  "trigger_id": "TRG-7031",
  "webhook_config": {
    "endpoint_path": "/webhook/customer-feedback",
    "secret": "whsec_referenced_in_vault",
    "method": "POST",
    "content_type": "application/json",
    "ip_whitelist": ["10.0.0.0/8", "172.16.0.0/12"],
    "rate_limit": { "max_requests_per_minute": 50, "burst_limit": 5 },
    "auth": {
      "type": "hmac_sha256",
      "header_name": "X-Feedback-Signature",
      "timestamp_header": "X-Feedback-Timestamp",
      "max_age_seconds": 300
    }
  },
  "payload_schema": {
    "type": "object",
    "properties": {
      "event": { "type": "string", "enum": ["feedback_received", "nps_submitted", "complaint_raised"] },
      "data": {
        "type": "object",
        "properties": {
          "customer_id": { "type": "string" },
          "feedback_text": { "type": "string" },
          "sentiment": { "type": "string", "enum": ["positive", "neutral", "negative"] },
          "severity": { "type": "integer", "minimum": 1, "maximum": 5 }
        }
      },
      "timestamp": { "type": "string", "format": "ISO-8601" },
      "source": { "type": "string" }
    },
    "required": ["event", "data", "timestamp", "source"]
  },
  "task_spec": {
    "task_id": "auto-generated",
    "description": "Process incoming customer feedback, classify, and route to appropriate team",
    "agent_id": "PMGR-CS-01",
    "department": "quality-and-operations",
    "execution_mode": "auto",
    "priority": "P2"
  },
  "response_config": {
    "acknowledge_immediately": true,
    "delivery_guarantee": "at_least_once",
    "retry_policy": { "max_retries": 3, "backoff_ms": [1000, 5000, 15000] }
  }
}
```

### 2.5 Manual Trigger

Manual triggers are initiated by authorized users through direct request. These are typically ad-hoc tasks that do not fit into scheduled or event-driven patterns. Manual triggers require authentication and are logged for audit purposes.

**Schema:**

```json
{
  "trigger_type": "manual",
  "trigger_id": "auto-generated",
  "requestor_id": "AGENT_ID or USER_ID",
  "authentication": {
    "method": "session|token|oauth",
    "verified": true
  },
  "task_spec": {
    "task_id": "TASK-{NNN}",
    "description": "string",
    "agent_id": "AGENT_ID or auto-assigned",
    "department": "DEPARTMENT_ID or auto",
    "execution_mode": "auto|approve|review|hybrid",
    "priority": "P0|P1|P2|P3",
    "due_date": "ISO-8601 (optional)",
    "context": { "..." : "user-provided context" }
  },
  "manual_config": {
    "require_reason": true,
    "auto_assign": true,
    "assignment_strategy": "least_loaded|round_robin|skill_based|specified",
    "notify_requestor_on_complete": true,
    "audit_log": true
  }
}
```

**Example — Ad-Hoc Market Analysis Request:**

```json
{
  "trigger_type": "manual",
  "trigger_id": "auto-generated",
  "requestor_id": "CEO",
  "authentication": { "method": "session", "verified": true },
  "task_spec": {
    "task_id": "TASK-7891",
    "description": "Competitive analysis of recent market entry by competitor X in segment Y",
    "agent_id": "CMO-ANALYST-01",
    "department": "marketing-and-partnerships",
    "execution_mode": "review",
    "priority": "P1",
    "due_date": "2026-04-30T17:00:00Z",
    "context": {
      "competitor": "Competitor X",
      "segment": "Segment Y",
      "focus_areas": ["pricing_strategy", "product_features", "go-to-market"]
    }
  },
  "manual_config": {
    "require_reason": true,
    "auto_assign": false,
    "assignment_strategy": "specified",
    "notify_requestor_on_complete": true,
    "audit_log": true
  }
}
```

---

## 3. Error Recovery

Error recovery defines the strategies, policies, and procedures for handling execution failures. The system employs a multi-layered approach: retry with exponential backoff at the operation level, rollback procedures at the transaction level, and circuit breakers at the service level.

### 3.1 Retry with Exponential Backoff

Retry logic is the first line of defense against transient failures. Each failed operation is retried with increasing delays to allow the underlying system to recover.

**Backoff Algorithm:**

```
delay(n) = base_delay * (multiplier ^ n) + jitter

Where:
  n = retry attempt number (0-indexed)
  base_delay = configurable (default: 1000ms)
  multiplier = configurable (default: 2.0)
  jitter = random value in [0, max_jitter] (default: 100ms)

Example sequence with base=1000ms, multiplier=2.0:
  Attempt 0: immediate
  Attempt 1: 1000ms + jitter (0-100ms)
  Attempt 2: 2000ms + jitter (0-100ms)
  Attempt 3: 4000ms + jitter (0-100ms)
  Attempt 4: 8000ms + jitter (0-100ms)
```

**Retry Classification by Error Type:**

| Error Category | Retryable | Max Retries | Base Delay | Strategy |
|---------------|-----------|-------------|------------|----------|
| Network timeout | Yes | 5 | 1000ms | Exponential backoff |
| Rate limit (429) | Yes | 3 | 5000ms | Respect Retry-After header |
| Temporary service unavailable (503) | Yes | 5 | 2000ms | Exponential backoff |
| Resource contention | Yes | 3 | 3000ms | Exponential backoff |
| Data conflict (409) | Yes | 2 | 1000ms | Immediate retry with refreshed data |
| Authentication failure (401) | No | 0 | N/A | Escalate, do not retry |
| Authorization failure (403) | No | 0 | N/A | Escalate, do not retry |
| Validation failure (400) | No | 0 | N/A | Return error to caller |
| Data not found (404) | No | 0 | N/A | Return error to caller |
| Internal server error (500) | Conditional | 2 | 5000ms | Only if idempotent operation |

**Retry Policy Schema:**

```json
{
  "retry_policy": {
    "max_retries": 3,
    "base_delay_ms": 1000,
    "multiplier": 2.0,
    "max_delay_ms": 60000,
    "jitter_ms": 100,
    "retryable_errors": ["TIMEOUT", "RATE_LIMIT", "SERVICE_UNAVAILABLE", "RESOURCE_BUSY"],
    "non_retryable_errors": ["AUTH_FAILED", "FORBIDDEN", "VALIDATION_ERROR", "NOT_FOUND"],
    "idempotency_required": true,
    "retry_on_5xx": true,
    "respect_retry_after_header": true,
    "circuit_breaker_integration": true
  }
}
```

**Retry Event Schema (for audit logging):**

```json
{
  "retry_event": {
    "task_id": "TASK-{NNN}",
    "operation": "string",
    "attempt": 1,
    "max_attempts": 3,
    "error_code": "string",
    "error_message": "string",
    "delay_ms": 1000,
    "timestamp": "ISO-8601",
    "will_retry": true,
    "circuit_breaker_state": "CLOSED|OPEN|HALF_OPEN"
  }
}
```

**Example — API Call Retry Configuration:**

```json
{
  "retry_policy": {
    "max_retries": 5,
    "base_delay_ms": 2000,
    "multiplier": 2.0,
    "max_delay_ms": 60000,
    "jitter_ms": 200,
    "retryable_errors": [
      "TIMEOUT",
      "RATE_LIMIT",
      "SERVICE_UNAVAILABLE",
      "CONNECTION_REFUSED",
      "RESOURCE_BUSY"
    ],
    "non_retryable_errors": [
      "AUTH_FAILED",
      "FORBIDDEN",
      "VALIDATION_ERROR",
      "NOT_FOUND",
      "DATA_CORRUPTION"
    ],
    "idempotency_required": true,
    "retry_on_5xx": true,
    "respect_retry_after_header": true,
    "circuit_breaker_integration": true
  }
}
```

### 3.2 Rollback Procedures

Rollback procedures restore the system to a consistent state after a failed operation. Rollback is mandatory for any operation that modified external state. Read-only operations require no rollback.

**Rollback Classification:**

| Operation Type | Rollback Strategy | Rollback Window |
|---------------|-------------------|-----------------|
| Database write | Transaction rollback or compensating transaction | Within transaction timeout |
| File write | Restore from backup snapshot | Within 24 hours |
| Configuration change | Revert to previous configuration version | Within 7 days |
| State change | Restore from state snapshot | Within 6 hours |
| External API call | Compensating API call (if supported) | Within SLA window |
| Deployment | Rollback to previous version | Within 1 hour |
| Permission change | Revert permission grant | Immediate |

**Rollback Procedure Schema:**

```json
{
  "rollback_config": {
    "enabled": true,
    "strategy": "AUTOMATIC|MANUAL|SEMI_AUTOMATIC",
    "snapshot_before_execution": true,
    "snapshot_retention": "ISO-8601-duration",
    "compensating_actions": [
      {
        "action_id": "COMP-{NNN}",
        "description": "string",
        "target": "string",
        "method": "REVERT|COMPENSATE|RESTORE",
        "pre_condition": "string (optional)",
        "post_condition": "string (optional)"
      }
    ],
    "verification_after_rollback": true,
    "rollback_timeout": "ISO-8601-duration",
    "notify_on_rollback": true,
    "escalate_if_rollback_fails": true
  }
}
```

**Rollback Execution Flow:**

```
ROLLBACK EXECUTION FLOW:

  [Operation Failed] -> [Determine Rollback Strategy]
                                    |
                          AUTOMATIC? ----+---- MANUAL?
                            |                 |
                    [Execute Rollback]   [Notify Operator] -> [Wait for Confirmation]
                            |                                           |
                    [Verify Rollback]                          [Execute Rollback]
                            |                                           |
                      [Report Result]                          [Verify Rollback]
                                                                [Report Result]

  ROLLBACK FAILURE PATH:
  [Rollback Failed] -> [Alert Operations] -> [Escalate to CEO] -> [Manual Intervention]
```

**Example — Database Migration Rollback:**

```json
{
  "rollback_config": {
    "enabled": true,
    "strategy": "AUTOMATIC",
    "snapshot_before_execution": true,
    "snapshot_retention": "PT72H",
    "compensating_actions": [
      {
        "action_id": "COMP-001",
        "description": "Reverse schema migration v2.4.1",
        "target": "production_database",
        "method": "REVERT",
        "pre_condition": "migration_was_applied",
        "post_condition": "schema_matches_v2.4.0"
      },
      {
        "action_id": "COMP-002",
        "description": "Invalidate affected cache entries",
        "target": "redis_cache",
        "method": "COMPENSATE"
      }
    ],
    "verification_after_rollback": true,
    "rollback_timeout": "PT30M",
    "notify_on_rollback": true,
    "escalate_if_rollback_fails": true
  }
}
```

### 3.3 Circuit Breaker Pattern

The circuit breaker pattern prevents cascading failures by temporarily halting operations to a failing service. It operates in three states: CLOSED (normal operation), OPEN (operations blocked), and HALF_OPEN (probe single request to test recovery).

**Circuit Breaker State Machine:**

```
                 Success                     Failure
  CLOSED --------+--------> CLOSED    CLOSED ------+------> OPEN
                     (reset counter)            (threshold exceeded)
                                                    |
                                              (timeout expires)
                                                    v
                                               HALF_OPEN
                                              /         \
                                       Success           Failure
                                          /               \
                                    CLOSED                 OPEN
                                    (reset)           (timeout reset)
```

**Configuration Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| failure_threshold | 5 | Consecutive failures before opening |
| success_threshold | 2 | Consecutive successes in half-open to close |
| timeout | 60s | Duration to wait before transitioning to half-open |
| half_open_max_calls | 1 | Max concurrent probes in half-open state |
| monitored_errors | All retryable errors | Error types that count toward threshold |
| excluded_errors | Validation errors | Errors that do not affect circuit state |

**Circuit Breaker Schema:**

```json
{
  "circuit_breaker": {
    "name": "string",
    "state": "CLOSED|OPEN|HALF_OPEN",
    "failure_threshold": 5,
    "success_threshold": 2,
    "timeout_ms": 60000,
    "half_open_max_calls": 1,
    "monitored_errors": ["TIMEOUT", "SERVICE_UNAVAILABLE", "CONNECTION_REFUSED"],
    "excluded_errors": ["VALIDATION_ERROR", "NOT_FOUND"],
    "metrics": {
      "failure_count": 0,
      "success_count": 0,
      "last_failure": "ISO-8601 (optional)",
      "last_success": "ISO-8601 (optional)",
      "state_since": "ISO-8601",
      "total_trips": 0,
      "last_trip": "ISO-8601 (optional)"
    },
    "notifications": {
      "on_open": ["COO", "CTO"],
      "on_close": ["COO"],
      "on_half_open": []
    }
  }
}
```

**Per-Department Circuit Breaker Defaults:**

| Department | Failure Threshold | Timeout | Success Threshold | Rationale |
|-----------|-------------------|---------|-------------------|-----------|
| Finance | 3 | 30s | 2 | Financial operations require rapid detection |
| Security | 2 | 15s | 1 | Security services must fail fast |
| Operations | 5 | 60s | 2 | Operational resilience priority |
| Technology | 5 | 45s | 2 | Engineering services with normal variance |
| Intelligence | 5 | 120s | 3 | External data sources may be intermittently unavailable |
| All others | 5 | 60s | 2 | Standard resilience profile |

**Example — External API Circuit Breaker:**

```json
{
  "circuit_breaker": {
    "name": "market-data-api",
    "state": "CLOSED",
    "failure_threshold": 3,
    "success_threshold": 2,
    "timeout_ms": 30000,
    "half_open_max_calls": 1,
    "monitored_errors": ["TIMEOUT", "SERVICE_UNAVAILABLE", "RATE_LIMIT"],
    "excluded_errors": ["VALIDATION_ERROR", "NOT_FOUND", "AUTH_FAILED"],
    "metrics": {
      "failure_count": 0,
      "success_count": 12,
      "last_failure": null,
      "last_success": "2026-04-27T15:30:00Z",
      "state_since": "2026-04-27T14:00:00Z",
      "total_trips": 2,
      "last_trip": "2026-04-26T09:15:00Z"
    },
    "notifications": {
      "on_open": ["CTO", "COO", "CFO"],
      "on_close": ["CTO"],
      "on_half_open": []
    }
  }
}
```

### 3.4 Error Classification and Routing

All execution errors are classified and routed according to their severity and type. This ensures that the appropriate recovery strategy is applied and the right stakeholders are notified.

**Error Classification Matrix:**

| Error Code Prefix | Department | Recovery Strategy | Notification |
|-------------------|-----------|-------------------|--------------|
| CEO_ | Governance | Escalate to Board if critical | CEO + Board |
| COO_ | Operations | Retry + fallback procedure | COO + affected department |
| CFO_ | Finance | Compensating transaction | CFO + CRO |
| CRO_ | Risk | Circuit breaker + risk assessment | CRO + CEO |
| CTO_ | Technology | Rollback + retry | CTO + COO |
| CISO_ | Security | Immediate containment | CISO + CEO + Board |
| CLO_ | Legal | Stop execution, legal review | CLO + CEO |
| CQO_ | Quality | Halt pipeline, quality review | CQO + CTO |
| FW_ | Framework | Rollback to last stable version | CTO + CQO |
| PMGR_ | Project | Reprioritize + reassign | PMGR + COO |
| INTEL_ | Intelligence | Fallback data source | Intel + CMO |
| INFO_ | Information | Cache + retry | Info + CTO |
| TR_ | Translation | Fallback to original language | Translator + CMO |

---

## 4. CEO Command Center

The CEO Command Center is the central orchestration layer for all execution across the AI-Company. It provides the CEO (and delegated COO) with tools for priority queue management, resource allocation, and status monitoring across all departments and agents.

### 4.1 Architecture Overview

```
CEO COMMAND CENTER ARCHITECTURE:

  ┌─────────────────────────────────────────────────────────┐
  │                    CEO Command Center                    │
  │                                                          │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
  │  │   Priority    │  │  Resource    │  │   Status     │  │
  │  │   Queue       │  │  Allocation  │  │   Monitor    │  │
  │  │   Manager     │  │  Engine      │  │   Dashboard  │  │
  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
  │         │                 │                   │          │
  │  ┌──────┴─────────────────┴───────────────────┴──────┐  │
  │  │              Execution Orchestrator                │  │
  │  │  (dispatches, coordinates, monitors all tasks)     │  │
  │  └──────────────────────┬────────────────────────────┘  │
  │                         │                               │
  │  ┌──────────────────────┴────────────────────────────┐  │
  │  │                 HQ Message Bus                     │  │
  │  └──────┬──────┬──────┬──────┬──────┬──────┬─────────┘  │
  │         │      │      │      │      │      │              │
  │       CEO    COO    CFO    CTO   CISO   CLO  ...          │
  └─────────────────────────────────────────────────────────┘
```

### 4.2 Priority Queue Management

The priority queue is the central ordering mechanism for all pending work. Tasks are enqueued with a priority score computed from multiple factors and dequeued based on the highest urgency.

**Priority Score Computation:**

```
Priority Score = (Risk_Weight * Risk_Score) +
                 (Deadline_Weight * Deadline_Score) +
                 (Strategic_Weight * Strategic_Score) +
                 (Stakeholder_Weight * Stakeholder_Score)

Default Weights:
  Risk_Weight       = 0.35
  Deadline_Weight   = 0.25
  Strategic_Weight  = 0.25
  Stakeholder_Weight = 0.15

Risk Score Mapping:
  P0-Critical = 100
  P1-High     = 75
  P2-Medium   = 50
  P3-Low      = 25
  P4-Minimal  = 10

Deadline Score (1-100):
  If overdue:     100
  If <1 hour:     90
  If <4 hours:    75
  If <24 hours:   60
  If <1 week:     40
  If >1 week:     20

Strategic Score (0-100):
  Directly aligned with Q OKR = 100
  Supports Q OKR               = 75
  Supports annual strategy     = 50
  Department-level priority    = 30
  No strategic linkage         = 10

Stakeholder Score (0-100):
  Board request           = 100
  C-Suite request         = 80
  Department head request = 50
  Agent request           = 20
  Automated request       = 10
```

**Queue Operations:**

```json
{
  "priority_queue": {
    "queue_id": "PQ-EXEC-01",
    "strategy": "WEIGHTED_PRIORITY",
    "max_queue_size": 10000,
    "aging_enabled": true,
    "aging_rate_per_minute": 0.5,
    "preemption_enabled": true,
    "preemption_min_score_delta": 20,
    "operations": {
      "enqueue": {
        "method": "POST /queue/tasks",
        "payload": {
          "task_id": "TASK-{NNN}",
          "priority_score": "computed",
          "department": "DEPARTMENT_ID",
          "agent_id": "AGENT_ID (optional)",
          "execution_mode": "auto|approve|review|hybrid",
          "estimated_duration": "ISO-8601-duration"
        }
      },
      "dequeue": {
        "method": "GET /queue/next",
        "parameters": {
          "agent_id": "AGENT_ID (optional, filter by agent)",
          "department": "DEPARTMENT_ID (optional)",
          "min_priority": "integer (optional)"
        }
      },
      "reorder": {
        "method": "PUT /queue/reorder",
        "payload": {
          "task_id": "TASK-{NNN}",
          "new_priority": "P0|P1|P2|P3|P4",
          "reason": "string"
        },
        "authorization": "L4+ (C-Suite or above)"
      }
    }
  }
}
```

**Priority Queue Schema:**

```json
{
  "queue_entry": {
    "task_id": "TASK-{NNN}",
    "position": 1,
    "priority_score": 87.5,
    "risk_level": "P1",
    "department": "security-and-compliance",
    "agent_id": "CISO-IR-01",
    "execution_mode": "auto",
    "enqueued_at": "ISO-8601",
    "estimated_duration": "PT30M",
    "deadline": "ISO-8601 (optional)",
    "strategic_alignment": 0.75,
    "aging_boost": 0.0,
    "dependencies_met": true,
    "blocked_by": []
  }
}
```

### 4.3 Resource Allocation

Resource allocation determines how computational and organizational resources are distributed across competing tasks and departments. The allocation engine balances SLA requirements, strategic priorities, and capacity constraints.

**Resource Types and Constraints:**

| Resource | Total Pool | Allocation Unit | Reservation | Overcommit |
|----------|-----------|----------------|-------------|------------|
| CPU | Configurable vCPUs | Per-task | Yes (Platinum/Gold) | 1.5x (Silver/Bronze) |
| Memory | Configurable GB | Per-task | Yes | 1.2x |
| GPU | Tiered pool | Per-SLA-tier | Yes (dedicated) | No |
| Agent Hours | 24h/agent/day | Per-task | No | No |
| API Budget | Monthly quota | Per-department | Yes (80% reserved) | No |

**Allocation Algorithm:**

```
ALLOCATION ALGORITHM:

  Input: pending_tasks[], available_resources[], active_allocations[]

  Step 1: Sort pending_tasks by priority_score DESC
  Step 2: For each task in order:
    Step 2a: Check dependencies are met
    Step 2b: Calculate required resources
    Step 2c: Check availability against pool
    Step 2d: If available: ALLOCATE, mark resources as reserved
    Step 2e: If unavailable:
      Step 2e-i:  Check if preemption possible (lower priority tasks)
      Step 2e-ii: If preemption: PREEMPT, reallocate
      Step 2e-iii: If no preemption: QUEUE task, continue
  Step 3: Rebalance every 5 minutes
  Step 4: Log all allocation decisions for audit

  Preemption Rules:
    - Cannot preempt Platinum SLA tasks
    - Cannot preempt tasks that have been running >80% of estimated duration
    - Preemption score delta must exceed 20 points
    - Preempted task returns to queue with priority boost
```

**Resource Allocation Schema:**

```json
{
  "resource_allocation": {
    "allocation_id": "ALLOC-{NNN}",
    "task_id": "TASK-{NNN}",
    "agent_id": "AGENT_ID",
    "resources": {
      "cpu_vcpus": 2,
      "memory_gb": 4,
      "gpu_hours": 0,
      "estimated_duration": "PT30M"
    },
    "sla_tier": "GOLD",
    "priority": "P1",
    "allocated_at": "ISO-8601",
    "expires_at": "ISO-8601",
    "preemptible": false,
    "status": "ACTIVE|COMPLETED|PREEMPTED|EXPIRED"
  }
}
```

**Department Resource Quotas:**

```json
{
  "resource_quotas": {
    "governance-and-strategy": {
      "cpu_vcpus_max": 4,
      "memory_gb_max": 8,
      "agent_hours_per_day": 48,
      "api_budget_monthly": 10000
    },
    "finance-and-risk": {
      "cpu_vcpus_max": 8,
      "memory_gb_max": 16,
      "agent_hours_per_day": 48,
      "api_budget_monthly": 50000
    },
    "technology-and-engineering": {
      "cpu_vcpus_max": 16,
      "memory_gb_max": 32,
      "gpu_hours_per_day": 24,
      "agent_hours_per_day": 96,
      "api_budget_monthly": 100000
    },
    "security-and-compliance": {
      "cpu_vcpus_max": 8,
      "memory_gb_max": 16,
      "agent_hours_per_day": 48,
      "api_budget_monthly": 30000
    }
  }
}
```

### 4.4 Status Monitoring

The status monitoring system provides real-time visibility into the execution state of all tasks, agents, and departments. It powers the CEO Command Center dashboard and drives alerting.

**Monitoring Dimensions:**

| Dimension | Granularity | Update Frequency | Retention |
|-----------|-------------|-----------------|-----------|
| Task Status | Per task | Real-time | 90 days |
| Agent Health | Per agent | Every 30s | 30 days |
| Department Metrics | Per department | Every 5 min | 1 year |
| System Health | Global | Every 15s | 90 days |
| SLA Compliance | Per SLA tier | Every 1 min | 1 year |
| Resource Utilization | Per resource type | Every 1 min | 30 days |

**Task Status Lifecycle:**

```
TASK STATUS STATE MACHINE:

  QUEUED -> ASSIGNED -> IN_PROGRESS -> COMPLETED
    |         |             |
    |         |             +-> BLOCKED -> IN_PROGRESS (unblocked)
    |         |                            |
    |         |                            +-> CANCELLED
    |         |
    |         +-> CANCELLED
    |
    +-> EXPIRED

  IN_PROGRESS -> FAILED -> RETRYING -> IN_PROGRESS
                                    |
                                    +-> CANCELLED

  IN_PROGRESS -> REVIEW -> APPROVED -> COMPLETED
                      |
                      +-> REJECTED -> IN_PROGRESS (revision)

  Any state -> CANCELLED (irreversible)
```

**Monitoring Dashboard Schema:**

```json
{
  "monitoring_dashboard": {
    "last_updated": "ISO-8601",
    "system_health": {
      "status": "HEALTHY|DEGRADED|CRITICAL",
      "uptime_percentage_24h": 99.95,
      "active_agents": 22,
      "total_agents": 24,
      "active_tasks": 45,
      "queued_tasks": 12
    },
    "department_status": [
      {
        "department": "governance-and-strategy",
        "health": "HEALTHY",
        "active_tasks": 8,
        "sla_compliance_24h": 100.0,
        "oob_score": 92
      }
    ],
    "alerts": {
      "active_alerts": [
        {
          "alert_id": "ALT-{NNN}",
          "severity": "P1",
          "source": "DEPARTMENT_ID",
          "message": "string",
          "triggered_at": "ISO-8601",
          "acknowledged": false
        }
      ],
      "alert_summary": {
        "P0_count": 0,
        "P1_count": 1,
        "P2_count": 3,
        "P3_count": 7
      }
    },
    "resource_utilization": {
      "cpu_percent": 65,
      "memory_percent": 72,
      "gpu_percent": 40,
      "agent_hours_used_today": 180,
      "agent_hours_available_today": 480
    },
    "execution_metrics": {
      "tasks_completed_24h": 127,
      "tasks_failed_24h": 3,
      "avg_completion_time_minutes": 12.5,
      "retry_rate_percent": 2.4,
      "circuit_breaker_trips_24h": 0
    }
  }
}
```

**Alert Rules:**

```json
{
  "alert_rules": [
    {
      "rule_id": "ALR-001",
      "name": "Agent offline",
      "condition": "agent.heartbeat_missing_for > 120s",
      "severity": "P2",
      "notify": ["COO", "CTO"],
      "auto_action": "mark_agent_offline"
    },
    {
      "rule_id": "ALR-002",
      "name": "Task timeout",
      "condition": "task.duration > task.timeout",
      "severity": "P1",
      "notify": ["COO", "department_head"],
      "auto_action": "apply_timeout_policy"
    },
    {
      "rule_id": "ALR-003",
      "name": "Circuit breaker open",
      "condition": "circuit_breaker.state == OPEN",
      "severity": "P1",
      "notify": ["CTO", "COO", "affected_department"],
      "auto_action": "activate_fallback"
    },
    {
      "rule_id": "ALR-004",
      "name": "Queue backlog",
      "condition": "queue.size > 50 AND queue.oldest_task_age > PT4H",
      "severity": "P2",
      "notify": ["COO"],
      "auto_action": "request_additional_resources"
    },
    {
      "rule_id": "ALR-005",
      "name": "SLA breach risk",
      "condition": "sla.time_remaining < PT15M AND task.status == IN_PROGRESS",
      "severity": "P1",
      "notify": ["COO", "department_head"],
      "auto_action": "boost_priority_and_resources"
    }
  ]
}
```

---

## 5. Workflow Templates

Workflow templates are reusable execution patterns for common operational scenarios. Each template defines the complete execution flow including phases, modes, triggers, error handling, and quality gates. Templates must be VirusTotal-safe (no executable code, no dynamic evaluation, no external network calls).

### 5.1 Template Registry

| Template ID | Name | Phases | Trigger | Mode | Department |
|------------|------|--------|---------|------|------------|
| WFT-001 | Data Collection Pipeline | 3 | Schedule or Manual | Auto + Review | Any |
| WFT-002 | Report Generation Pipeline | 4 | Schedule | Hybrid | Any |
| WFT-003 | Alert Response Pipeline | 4 | Event | Auto + Approve | Any |
| WFT-004 | Skill Publishing Pipeline | 6 | Manual | Hybrid | Technology |
| WFT-005 | Incident Response Pipeline | 5 | Event | Auto + Approve | Security |
| WFT-006 | Budget Review Pipeline | 3 | Schedule | Approve + Review | Finance |
| WFT-007 | Deployment Pipeline | 5 | Manual or Webhook | Hybrid | Technology |
| WFT-008 | Market Intelligence Pipeline | 3 | Schedule or Event | Auto + Review | Intelligence |

### 5.2 WFT-001: Data Collection Pipeline

**Purpose:** Collect data from multiple internal or external sources, validate, transform, and store for downstream consumption.

**Phases:**

| Phase | Name | Mode | Description | Timeout |
|-------|------|------|-------------|---------|
| 1 | Source Discovery | Auto | Identify and connect to all data sources | 15 min |
| 2 | Data Extraction | Auto | Pull data from each source with retry logic | 30 min |
| 3 | Validation and Storage | Review | Validate data quality, transform, and store | 45 min |

**Complete Template:**

```json
{
  "template_id": "WFT-001",
  "template_name": "Data Collection Pipeline",
  "version": "1.0.0",
  "description": "Multi-source data collection with validation and storage",
  "execution_mode": "hybrid",
  "trigger": {
    "supported_types": ["schedule", "manual"],
    "default_schedule": "0 6 * * *",
    "manual_allowed": true
  },
  "phases": [
    {
      "phase_id": "DISCOVER",
      "phase_name": "Source Discovery",
      "execution_mode": "auto",
      "phase_order": 1,
      "steps": [
        "Load source configuration from registry",
        "Verify source connectivity (health check)",
        "Authenticate with each source",
        "Report unreachable sources for alerting",
        "Generate source manifest for extraction phase"
      ],
      "error_handling": {
        "strategy": "retry_with_backoff",
        "max_retries": 3,
        "on_exhaustion": "mark_source_failed_and_continue"
      },
      "outputs": ["source_manifest"],
      "timeout_minutes": 15
    },
    {
      "phase_id": "EXTRACT",
      "phase_name": "Data Extraction",
      "execution_mode": "auto",
      "phase_order": 2,
      "dependencies": ["DISCOVER"],
      "steps": [
        "Read source manifest",
        "For each active source: extract data within configured window",
        "Apply incremental extraction (delta from last run)",
        "Compress and stage extracted data",
        "Generate extraction summary (records per source, errors)"
      ],
      "error_handling": {
        "strategy": "retry_with_backoff",
        "max_retries": 5,
        "on_exhaustion": "skip_source_log_and_continue"
      },
      "outputs": ["raw_data_bundle", "extraction_summary"],
      "timeout_minutes": 30,
      "guardrails": {
        "max_records_per_source": 1000000,
        "max_total_size_mb": 512
      }
    },
    {
      "phase_id": "VALIDATE",
      "phase_name": "Validation and Storage",
      "execution_mode": "review",
      "phase_order": 3,
      "dependencies": ["EXTRACT"],
      "reviewer_id": "department_data_steward",
      "steps": [
        "Load raw data bundle",
        "Apply schema validation to each dataset",
        "Detect and quarantine anomalous records",
        "Transform to target schema",
        "Store validated data in designated repository",
        "Generate data quality report",
        "Submit quality report for review"
      ],
      "error_handling": {
        "strategy": "quarantine_and_continue",
        "max_quarantine_rate_percent": 10,
        "on_exceed": "halt_pipeline_alert_operator"
      },
      "outputs": ["validated_data", "quality_report"],
      "timeout_minutes": 45
    }
  ],
  "completion_criteria": {
    "all_sources_attempted": true,
    "data_quality_score": ">=0.8",
    "quality_report_approved": true
  },
  "notifications": {
    "on_complete": ["pipeline_owner", "data_consumers"],
    "on_failure": ["pipeline_owner", "COO"],
    "on_quality_issue": ["pipeline_owner", "CQO"]
  }
}
```

### 5.3 WFT-002: Report Generation Pipeline

**Purpose:** Generate structured reports from collected data, apply formatting, attach visualizations, and deliver to designated recipients.

**Phases:**

| Phase | Name | Mode | Description | Timeout |
|-------|------|------|-------------|---------|
| 1 | Data Preparation | Auto | Query, aggregate, and prepare data for report | 30 min |
| 2 | Content Generation | Auto | Generate narrative, analysis, and recommendations | 60 min |
| 3 | Quality Review | Review | Review for accuracy, completeness, and compliance | 48 hours |
| 4 | Publication | Approve | Approve and distribute final report | 1 hour |

**Complete Template:**

```json
{
  "template_id": "WFT-002",
  "template_name": "Report Generation Pipeline",
  "version": "1.0.0",
  "description": "Structured report generation with quality review and publication",
  "execution_mode": "hybrid",
  "trigger": {
    "supported_types": ["schedule"],
    "default_schedule": "0 7 1 * *",
    "manual_allowed": true
  },
  "phases": [
    {
      "phase_id": "PREPARE",
      "phase_name": "Data Preparation",
      "execution_mode": "auto",
      "phase_order": 1,
      "steps": [
        "Identify report parameters (period, scope, audience)",
        "Query required data from validated repositories",
        "Apply aggregation, filtering, and statistical calculations",
        "Prepare data summary tables for content generation",
        "Generate supporting charts and visualizations"
      ],
      "error_handling": {
        "strategy": "retry_with_backoff",
        "max_retries": 3,
        "on_exhaustion": "use_cached_data_and_flag"
      },
      "outputs": ["data_package", "visualizations"],
      "timeout_minutes": 30
    },
    {
      "phase_id": "GENERATE",
      "phase_name": "Content Generation",
      "execution_mode": "auto",
      "phase_order": 2,
      "dependencies": ["PREPARE"],
      "steps": [
        "Load report template",
        "Populate data tables and charts",
        "Generate narrative analysis section",
        "Generate recommendations section",
        "Generate executive summary",
        "Apply AIGC labeling",
        "Mask any PII in the report"
      ],
      "error_handling": {
        "strategy": "retry_once",
        "on_exhaustion": "flag_incomplete_sections"
      },
      "outputs": ["draft_report"],
      "timeout_minutes": 60,
      "guardrails": {
        "aigc_label_required": true,
        "pii_masking_required": true,
        "max_report_size_kb": 2048
      }
    },
    {
      "phase_id": "REVIEW",
      "phase_name": "Quality Review",
      "execution_mode": "review",
      "phase_order": 3,
      "dependencies": ["GENERATE"],
      "reviewer_id": "department_head",
      "steps": [
        "Submit draft report to reviewer",
        "Reviewer checks accuracy of data references",
        "Reviewer checks completeness against template",
        "Reviewer checks compliance (AIGC label, PII masking)",
        "Reviewer checks executive readability",
        "Provide approval or revision request"
      ],
      "error_handling": {
        "strategy": "revision_loop",
        "max_revisions": 3,
        "on_exhaustion": "escalate_to_department_head"
      },
      "outputs": ["approved_report"],
      "timeout_minutes": 2880,
      "review_criteria": ["accuracy", "completeness", "compliance", "readability"]
    },
    {
      "phase_id": "PUBLISH",
      "phase_name": "Publication",
      "execution_mode": "approve",
      "phase_order": 4,
      "dependencies": ["REVIEW"],
      "approver_id": "executive_sponsor",
      "steps": [
        "Submit approved report for final authorization",
        "Approver verifies executive summary alignment",
        "Upon approval: distribute to recipient list",
        "Archive report in knowledge base",
        "Notify recipients of report availability"
      ],
      "error_handling": {
        "strategy": "no_retry",
        "on_failure": "hold_for_manual_release"
      },
      "outputs": ["published_report", "distribution_confirmation"],
      "timeout_minutes": 60
    }
  ],
  "completion_criteria": {
    "all_phases_complete": true,
    "report_distributed": true,
    "report_archived": true
  },
  "notifications": {
    "on_complete": ["report_owner", "all_recipients"],
    "on_failure": ["report_owner", "COO"],
    "on_revision": ["report_generator"]
  }
}
```

### 5.4 WFT-003: Alert Response Pipeline

**Purpose:** Orchestrate automated response to system alerts, from detection through investigation, mitigation, verification, and closure.

**Phases:**

| Phase | Name | Mode | Description | Timeout |
|-------|------|------|-------------|---------|
| 1 | Alert Triage | Auto | Classify alert severity and determine response protocol | 5 min |
| 2 | Investigation | Auto | Gather diagnostic data and identify root cause | 30 min |
| 3 | Mitigation | Approve | Execute remediation plan (requires approval for P0/P1) | 1 hour |
| 4 | Verification | Auto | Confirm issue resolved and system stable | 30 min |

**Complete Template:**

```json
{
  "template_id": "WFT-003",
  "template_name": "Alert Response Pipeline",
  "version": "1.0.0",
  "description": "Automated alert response with investigation, mitigation, and verification",
  "execution_mode": "hybrid",
  "trigger": {
    "supported_types": ["event"],
    "event_patterns": [
      { "category": "operational", "severity": "P0|P1|P2" },
      { "category": "security", "severity": "P0|P1" },
      { "category": "financial", "severity": "P0|P1" }
    ]
  },
  "phases": [
    {
      "phase_id": "TRIAGE",
      "phase_name": "Alert Triage",
      "execution_mode": "auto",
      "phase_order": 1,
      "steps": [
        "Receive alert event from HQ Message Bus",
        "Extract alert metadata (source, severity, category)",
        "Apply deduplication check (correlation within 15 min)",
        "Determine response protocol based on severity",
        "Assign to appropriate response agent",
        "Notify relevant stakeholders per notification matrix",
        "Start incident timer"
      ],
      "error_handling": {
        "strategy": "fail_fast",
        "on_failure": "escalate_to_next_severity_level"
      },
      "outputs": ["triage_report", "assigned_agent"],
      "timeout_minutes": 5
    },
    {
      "phase_id": "INVESTIGATE",
      "phase_name": "Investigation",
      "execution_mode": "auto",
      "phase_order": 2,
      "dependencies": ["TRIAGE"],
      "steps": [
        "Collect diagnostic data from relevant systems",
        "Check recent change history for potential cause",
        "Analyze logs, metrics, and traces",
        "Identify probable root cause",
        "Assess blast radius and affected systems",
        "Generate investigation summary with findings",
        "Prepare mitigation recommendation"
      ],
      "error_handling": {
        "strategy": "escalate_if_inconclusive",
        "escalation_threshold_minutes": 20
      },
      "outputs": ["investigation_report", "mitigation_plan"],
      "timeout_minutes": 30
    },
    {
      "phase_id": "MITIGATE",
      "phase_name": "Mitigation",
      "execution_mode": "approve",
      "phase_order": 3,
      "dependencies": ["INVESTIGATE"],
      "approver_id": "auto_determined_by_severity",
      "approval_matrix": {
        "P0": "CEO",
        "P1": "department_head",
        "P2": "senior_engineer"
      },
      "steps": [
        "Submit mitigation plan to approver",
        "If P0/P1: await explicit approval",
        "If P2: auto-approve if within standard procedures",
        "Execute approved mitigation steps in order",
        "Monitor system response during mitigation",
        "Capture rollback snapshot before each step",
        "If mitigation fails: execute rollback"
      ],
      "error_handling": {
        "strategy": "rollback_on_failure",
        "rollback_config": {
          "snapshot_before_each_step": true,
          "verify_rollback": true
        }
      },
      "outputs": ["mitigation_result", "system_state_after"],
      "timeout_minutes": 60
    },
    {
      "phase_id": "VERIFY",
      "phase_name": "Verification",
      "execution_mode": "auto",
      "phase_order": 4,
      "dependencies": ["MITIGATE"],
      "steps": [
        "Run automated health checks on affected systems",
        "Verify alert condition is no longer present",
        "Monitor for recurrence over a 15-minute observation window",
        "Collect post-mitigation metrics",
        "Generate closure summary",
        "Update incident record with full timeline",
        "Archive for post-mortem review (if P0/P1)"
      ],
      "error_handling": {
        "strategy": "re_trigger_if_recurring",
        "observation_window_minutes": 15
      },
      "outputs": ["closure_report", "updated_incident_record"],
      "timeout_minutes": 30
    }
  ],
  "severity_time_budgets": {
    "P0": { "total_max_minutes": 60, "triage_max_minutes": 2, "investigate_max_minutes": 10, "mitigate_max_minutes": 30, "verify_max_minutes": 15 },
    "P1": { "total_max_minutes": 120, "triage_max_minutes": 5, "investigate_max_minutes": 30, "mitigate_max_minutes": 60, "verify_max_minutes": 30 },
    "P2": { "total_max_minutes": 240, "triage_max_minutes": 5, "investigate_max_minutes": 60, "mitigate_max_minutes": 120, "verify_max_minutes": 30 }
  },
  "notifications": {
    "on_triage": ["COO", "department_head", "on_call_engineer"],
    "on_investigation_complete": ["COO", "department_head"],
    "on_mitigation_success": ["COO", "department_head", "affected_stakeholders"],
    "on_closure": ["COO", "department_head", "post_mortem_queue (if P0/P1)"]
  }
}
```

### 5.5 Template Customization Guidelines

Templates are designed to be instantiated and customized for specific use cases while maintaining the structural guarantees of the template.

**Customization Rules:**
1. Phase order and dependencies may not be modified for built-in templates
2. Execution modes may be upgraded (Auto -> Review) but not downgraded (Review -> Auto) for compliance-sensitive workflows
3. Timeouts may be extended but not shortened below the minimum defined in the template
4. Custom steps may be added to any phase, but built-in steps may not be removed
5. Error handling strategies may be made more aggressive (more retries) but not more lenient
6. Notification lists may be extended but core notifications may not be removed
7. All customizations must be logged with rationale for audit

**Template Instantiation Schema:**

```json
{
  "instance_id": "WFI-{NNN}",
  "template_id": "WFT-{NNN}",
  "customizations": {
    "phase_overrides": [
      {
        "phase_id": "PHASE_ID",
        "overrides": {
          "timeout_minutes": "integer (>= template minimum)",
          "additional_steps": ["string"],
          "mode_override": "higher_security_mode (optional)"
        }
      }
    ],
    "parameter_values": {
      "key": "value"
    },
    "custom_metadata": {
      "owner": "AGENT_ID",
      "justification": "string"
    }
  },
  "created_at": "ISO-8601",
  "created_by": "AGENT_ID"
}
```

---

## 6. Execution Schema Reference

This section provides the master schemas for all execution-related data structures used across the system.

### 6.1 Execution Context Schema

```json
{
  "execution_context": {
    "execution_id": "EXEC-{UUID}",
    "trace_id": "TRACE-{UUID}",
    "task_id": "TASK-{NNN}",
    "workflow_id": "WF-{NNN} (optional)",
    "trigger_type": "schedule|event|webhook|manual",
    "trigger_id": "TRG-{NNN}",
    "execution_mode": "auto|approve|review|hybrid",
    "started_at": "ISO-8601",
    "started_by": "AGENT_ID",
    "department": "DEPARTMENT_ID",
    "status": "QUEUED|ASSIGNED|IN_PROGRESS|BLOCKED|REVIEW|APPROVED|COMPLETED|FAILED|CANCELLED|TIMED_OUT",
    "current_phase": "PHASE_ID (optional)",
    "metadata": {
      "risk_level": "P0|P1|P2|P3|P4",
      "priority_score": "float",
      "estimated_duration": "ISO-8601-duration",
      "timeout": "ISO-8601-duration",
      "aigc_generated": true,
      "correlation_id": "UUID (optional)"
    }
  }
}
```

### 6.2 Execution Log Entry Schema

```json
{
  "execution_log_entry": {
    "entry_id": "LOG-{UUID}",
    "execution_id": "EXEC-{UUID}",
    "trace_id": "TRACE-{UUID}",
    "timestamp": "ISO-8601",
    "level": "DEBUG|INFO|WARN|ERROR|FATAL",
    "phase": "PHASE_ID",
    "step": "string",
    "action": "string",
    "result": "SUCCESS|FAILURE|SKIPPED|BLOCKED",
    "duration_ms": 0,
    "error_code": "string (if failure)",
    "error_message": "string (if failure)",
    "retry_attempt": 0,
    "agent_id": "AGENT_ID",
    "details": {}
  }
}
```

### 6.3 Execution Summary Schema

```json
{
  "execution_summary": {
    "execution_id": "EXEC-{UUID}",
    "task_id": "TASK-{NNN}",
    "status": "COMPLETED|FAILED|CANCELLED|TIMED_OUT",
    "started_at": "ISO-8601",
    "completed_at": "ISO-8601",
    "duration_ms": 0,
    "execution_mode": "auto|approve|review|hybrid",
    "department": "DEPARTMENT_ID",
    "agent_id": "AGENT_ID",
    "phases_completed": 3,
    "phases_total": 3,
    "retry_count": 0,
    "rollback_executed": false,
    "circuit_breaker_tripped": false,
    "error_summary": "string (if failed)",
    "outputs": ["string"],
    "quality_score": 0.0,
    "aigc_generated": true,
    "audit_trail_complete": true
  }
}
```

---

## 7. Constraints

The following constraints are mandatory for all execution operations. Violations trigger error codes and audit alerts.

### 7.1 Operational Constraints

- No task execution without a valid trace_id (generated by Template #7: generate_trace_id)
- No P0 task may execute in Auto mode — Approve mode is mandatory
- No external system modification without Approve mode and designated approver confirmation
- No execution may exceed its configured timeout without escalation to COO
- No task may be cancelled after 80% completion without CEO approval
- No resource preemption of Platinum SLA tasks under any circumstances
- All P0/P1 task completions require post-mortem documentation within 72 hours
- All rollback operations must be verified before declaring success

### 7.2 Security Constraints

- No task may access resources outside its designated permission scope (per State Access Rules in HQ spec)
- No task output may contain unmasked PII
- All AI-generated content must carry AIGC labeling (explicit, implicit, and watermark)
- No circuit breaker bypass without CISO written approval
- All webhook-triggered executions must pass HMAC-SHA256 signature verification
- No execution logs may be deleted (immutable audit trail)

### 7.3 Compliance Constraints

- All execution decisions must be logged with rationale within 1 hour
- All external-facing execution results must pass CLO compliance review
- No execution may proceed if a blocking compliance flag exists on the task
- All scheduled triggers must respect maintenance windows
- Cross-department task dependencies must be resolved through HQ routing (no direct agent-to-agent)

### 7.4 Quality Constraints

- All Review-mode outputs must achieve a minimum quality score of 0.8
- No skill may be published without passing all G0-G7 quality gates
- All hybrid workflows must generate a completion summary
- All retry attempts must be logged with full context for analysis
- All circuit breaker state transitions must be recorded in the monitoring dashboard

---

## 8. Quality Metrics

| Metric | Target | Measurement | Owner |
|--------|--------|-------------|-------|
| Task completion rate | >=95% | Completed / (Completed + Failed + Cancelled) per month | COO |
| Auto-mode success rate | >=98% | Successful auto completions / total auto-mode tasks | COO |
| Approval turnaround (P1) | <4h | Time from plan submission to approval decision | CEO |
| Review turnaround (standard) | <48h | Time from submission to review decision | CQO |
| Retry rate | <5% | Tasks requiring >=1 retry / total tasks | CTO |
| Circuit breaker trip rate | <1/month | Circuit breaker opens / month per service | CTO |
| Rollback success rate | >=99% | Successful rollbacks / total rollback attempts | CTO |
| End-to-end workflow on-time | >=80% | Workflows completed within deadline / total workflows | COO |
| Alert response time (P0) | <5min | Time from alert to triage complete | CISO |
| Alert response time (P1) | <15min | Time from alert to triage complete | CISO |
| Queue aging | <30min avg | Average time tasks spend in queue before assignment | COO |
| Resource utilization | 65-85% | Average resource utilization across all types | COO |
| Execution trace completeness | 100% | Tasks with complete audit trail / total tasks | CQO |

---

*This document is part of the AI-Company unified skill reference library. For department-specific execution policies, see individual department files in [departments/](departments/). For shared code templates including retry_with_backoff (Template #5), see [method-patterns.md](method-patterns.md#shared-code-templates).*
