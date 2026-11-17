# Reusable asset model

| Assets | Applicable Questions | Required Components |
|---|---|---|
| Discovery Scripts | Repetition of scenarios requiring interviews, observations, and screening | Inputs, Question Banks, Rules of Evidence, Access Control |
| POC Contract Template | Success Criteria and Customer Investment Often Out of Focus | Roles, Scope, Metrics, Stops and Changes |
| PRD/Test Templates | Duplication of Specifications and Acceptance Structures | Fields, Numbers, Tracking, Quality Gates |
| Deployment blueprint | Duplicate system, data, and permission combinations | Boundary diagram, configuration points, security, observation, rollback |
| Connectors/Tools | Repeated implementation of the same system integration | Interfaces, authentication, permissions, errors, testing |
| Agent skills | Stable tasks require model judgment and tool use | SKILL, reference, guardrails, evaluation, adaptation |
| Evaluation set/scorer | Repeated verification of similar quality | Data, gold standard, scale, version, pollution control |
| Product capability candidates | Problem and value stable across customers | Users, market evidence, needs, costs, governance |

## Selection principle

- When the repetitive question is "how to deliver", give priority to scripts or templates;
- When the repeated question is "How to connect the system", the connector or deployment blueprint will be given priority;
- Prioritize skills and assessment sets when what is repeated is "how the model completes the task";
- Only enter the product roadmap when what is repeated is "stable capabilities that customers need";
- When a large number of customer-specific judgments are still required, retain service-based delivery and do not force productization.

## Minimum content of asset package

Targeting and triggering, applicable/not applicable, inputs, standard steps, configuration variables, outputs, quality gates, risks, assessments, examples, versions, owners and evidence of provenance.
