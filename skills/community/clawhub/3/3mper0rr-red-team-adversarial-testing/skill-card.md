## Description:

This skill guides authorized red-team adversarial testing of AI models and agents, including attack-surface mapping, prompt-injection test corpus building, execution, scoring, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3mper0rr](https://clawhub.ai/user/3mper0rr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and AI evaluators use this skill to plan and document authorized adversarial testing for AI models and agents, including prompt-injection, jailbreak, tool-abuse, and data-exfiltration scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adversarial prompt corpora and reports could be misused against systems without authorization.

Mitigation: Use the skill only on systems and models the operator owns or is explicitly authorized to test.

Risk: Generated payloads may include sensitive or disruptive testing material.

Mitigation: Keep generated payloads and reports scoped to defensive evaluation and do not run tests against third-party systems without permission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3mper0rr/skills/3mper0rr-red-team-adversarial-testing)

## Skill Output:

**Output Type(s):** [Markdown, JSONL, CSV, Guidance]

**Output Format:** [Markdown reports, JSONL attack corpora, and CSV test results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces surface mapping, threat model, attack corpus, test results, and a final vulnerability report with recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
