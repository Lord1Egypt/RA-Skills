## Description:

Add causal reasoning to agent actions by modeling interventions, counterfactuals, outcomes, and uncertainty for planning, debugging, backfilling historical data, and reviewing past actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oswalpalash](https://clawhub.ai/user/oswalpalash)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add causal reasoning around high-level actions, including planning interventions, estimating likely outcomes, debugging failures, and reconstructing historical action logs for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a persistent behavioral log from actions and historical communications.

Mitigation: Require explicit user approval for logging scope, storage location, retention period, and deletion process before enabling action logs or backfills.

Risk: Backfill workflows can ingest private email, calendar, and message history.

Mitigation: Limit backfills to the minimum date range and data sources needed, review exported data before processing, and avoid broad history imports unless the user has approved them.

Risk: Example workflows use fixed temporary export paths under /tmp.

Mitigation: Replace fixed paths with secure temporary files or in-memory processing, and remove intermediate exports after use.

Risk: Causal estimates may be uncertain or misleading when data is sparse, confounded, or not representative.

Mitigation: Report uncertainty, require enough observations before acting on estimates, and escalate high-uncertainty or high-impact decisions for human review.

## Reference(s):

- [Do-Calculus Reference](references/do-calculus.md)
- [Treatment Effect Estimation](references/estimation.md)
- [Introduction to Causal Inference](https://www.bradyneal.com/causal-inference-course)
- [Causal Inference on ClawHub](https://clawhub.ai/oswalpalash/skills/causal-inference)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks, JSON examples, YAML examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local JSONL action logs, causal graph files, effect estimates, and configuration under memory/causal/.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
