---
name: bcp-plan
version: 1.0.0
description: "Comprehensive business continuity planning including emergency plans, critical alternatives, drill scripts, and recovery procedures. Covers risk assessment, continuity strategies, crisis management, and organizational resilience for operational preparedness."
author: "openclaw"
tags:
 - bcp-plan
invocable: true
---

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| business_functions | text | Yes | Critical business functions |
| risk_scenarios | text | Yes | Potential disruption scenarios |
| recovery_objectives | text | Yes | RTO and RPO targets |
| current_capabilities | text | Yes | Existing continuity measures |
| dependencies | text | Yes | Internal and external dependencies |
| regulatory_requirements | text | No | Compliance obligations |

## Output

| Name | Type | Description |
|------|------|-------------|
| bcp_document | text | Complete business continuity plan |
| risk_assessment | text | Prioritized risk analysis |
| continuity_strategies | text | Recovery strategies by function |
| emergency_procedures | text | Crisis response procedures |
| recovery_procedures | text | Step-by-step recovery plans |
| drill_scenarios | text | Testing exercise scripts |
| communication_plan | text | Crisis communication framework |

## Example

### Input
```json
{
  "business_functions": "Customer service, order processing, manufacturing, shipping",
  "risk_scenarios": "IT outage, natural disaster, supplier failure, pandemic",
  "recovery_objectives": "Critical systems: 4 hours, Full operations: 48 hours",
  "current_capabilities": "Cloud backup, secondary site, cross-trained staff",
  "dependencies": "Cloud provider, key suppliers, logistics partners"
}
```

### Output
```json
{
  "bcp_document": "Comprehensive plan with activation criteria, procedures, contacts, resources",
  "risk_assessment": "High: IT outage, Medium: Supplier failure, Low: Natural disaster (geographic spread)",
  "continuity_strategies": "Hot standby for critical systems, backup suppliers, remote work capability",
  "emergency_procedures": "Incident assessment, team activation, stakeholder notification, media response",
  "recovery_procedures": "Phase 1: Critical systems, Phase 2: Core operations, Phase 3: Full restoration",
  "drill_scenarios": "Quarterly tabletop exercises, annual full simulation, surprise drills",
  "communication_plan": "Internal cascade, customer notification, media holding statement, regulatory reporting"
}
```