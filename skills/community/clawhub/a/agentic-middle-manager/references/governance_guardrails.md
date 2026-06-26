# Governance Guardrails: Accountability Architecture for AI Agents

## Purpose

This reference provides the implementation guidelines for building accountability into agentic systems through provenance chains, confidence-based routing, and deliberation records. These are the systemic trust mechanisms that allow agents to operate safely within the Management Trinity protocol.

## 1. Provenance Chains

A provenance chain links every agent action back to a human authorization, creating an unbroken chain of responsibility.

### Required Data Schema

Every agent action must include:

```json
{
  "action_id": "uuid",
  "timestamp": "ISO 8601",
  "agent_id": "string",
  "action_type": "string",
  "human_authorizer": {
    "role": "DRI | Player-Coach | IC",
    "name": "string",
    "authorization_scope": "description of what was authorized",
    "authorization_date": "ISO 8601"
  },
  "inputs_considered": ["list of data sources"],
  "output": "description of the action taken",
  "confidence_score": "0.0 - 1.0"
}
```

### Design Principles
- Every agent must have a named human authorizer for its scope of action.
- Authorization scope must be explicitly bounded (e.g., "approve refunds under $50" not "handle customer service").
- The provenance chain must be immutable and queryable for audit purposes.

## 2. Confidence-Based Routing

Agents must express uncertainty as a resource, not suppress it into binary classifications.

### Routing Thresholds

| Confidence Level | Action | Rationale |
| :--- | :--- | :--- |
| **> 90%** | Auto-execute | High confidence; agent proceeds within its authorized scope. |
| **70% - 90%** | Human review | Moderate confidence; agent presents its analysis and recommendation to a human DRI for approval. |
| **< 70%** | Escalate / Reject | Low confidence; agent escalates to a senior DRI or rejects the task, requesting more information. |

### Calibration Process
Thresholds are not universal. They must be calibrated per task type based on:
- **Reversibility:** Can the action be undone? Lower thresholds for reversible actions.
- **Impact:** What is the cost of failure? Higher thresholds for high-impact decisions.
- **Frequency:** How often does this decision occur? High-frequency decisions benefit from lower thresholds to avoid bottlenecks.

### The Cynefin Decision Router

Use the Cynefin framework to determine the appropriate level of AI involvement:

| Context | AI Role | Human Role |
| :--- | :--- | :--- |
| **Clear** | Apply best practices and automate. | Spot-check and audit. |
| **Complicated** | Gather data, model scenarios, present options. | Expert analysis and final decision. |
| **Complex** | Probe the environment, sense patterns, surface anomalies. | Adaptive response, experimentation. |
| **Chaotic** | Post-hoc analysis and documentation. | Immediate stabilization and action. |

## 3. Deliberation Records

A deliberation record captures the full reasoning process behind an agent's decision, functioning like a medical chart rather than a simple log entry.

### Required Components

Every deliberation record must include:

1. **Context:** What was the situation? What data was available?
2. **Alternatives Considered:** What options did the agent evaluate?
3. **Rationale:** Why was the chosen action selected over the alternatives?
4. **Assumptions:** What assumptions did the agent make? What information was missing?
5. **Confidence Assessment:** How certain was the agent? What factors contributed to uncertainty?
6. **Limitations Acknowledged:** What are the known limitations of this analysis?

### Quality Criteria
A deliberation record is considered adequate if a human reviewer can:
- Understand the decision without additional context.
- Identify the specific point where the reasoning might have gone wrong.
- Determine whether the agent's assumptions were reasonable given the available data.

## 4. Post-Mortem Protocol (When Things Go Wrong)

When an AI agent makes an error, the post-mortem focuses on the accountability architecture, not on individual blame.

### Post-Mortem Questions
1. Was the provenance chain intact? Did the agent act within its authorized scope?
2. Was the confidence score accurate? Did the routing threshold work correctly?
3. Was the deliberation record adequate? Could a human have caught the error by reviewing it?
4. Where did the accountability architecture fail? What systemic improvement is needed?

### Output
The post-mortem produces an **Architecture Improvement Recommendation** that updates the governance guardrails, not a blame assignment.
