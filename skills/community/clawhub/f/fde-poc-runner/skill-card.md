## Description:

Run a deployable solution and Agent Skill in representative or controlled customer scenarios against pre-agreed evidence, tests, and success criteria, then produce a Continue, Adjust, or Stop decision report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukun0821](https://clawhub.ai/user/xukun0821)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, field teams, and delivery leads use this skill to run POC trials, acceptance validation, issue triage, and retrospectives against frozen criteria. It helps produce auditable POC run reports that preserve failures, compare evidence to thresholds, and support continue, adjust, pause, or stop decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POC evidence may include sensitive customer or operational data.

Mitigation: Use approved datasets, avoid sensitive raw customer data unless permitted, and keep evidence storage and de-identification under the user's governance process.

Risk: Real-system actions, UAT, and Continue/Adjust/Stop decisions can affect customer workflows or downstream investment decisions.

Mitigation: Keep real-system and UAT actions under human control, preserve failed and unrun cases, and require the agreed decision-maker to approve gate decisions.

Risk: Markdown summaries generated from untrusted JSON could carry unsafe raw HTML or remote image references when viewed downstream.

Mitigation: Render generated Markdown in a viewer that blocks raw HTML and remote images when the input JSON is not fully trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xukun0821/skills/fde-poc-runner)
- [POC run input guide](references/poc-input-guide.md)
- [POC Operation Manual](references/poc-operations.md)
- [POC Evaluation and Decision Rules](references/evaluation-rules.md)
- [POC operation and verification report template](references/poc-run-report.md)
- [POC run quality score](references/poc-quality-rubric.md)
- [POC Operations Field Manual](references/poc-field-handbook.md)
- [POC run complete example](references/poc-worked-example.md)
- [UAT and production transition verification](references/uat-and-transition.md)
- [Public method sources](references/public-sources.md)
- [AWS: Successful Generative AI POC](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/dev-architecting.html)
- [AWS: Generative AI Experiment Evaluation Loop](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/dev-experimenting-experimentation-loops.html)
- [AWS: Advance from POC to pre-production](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/dev-advancing.html)
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [OpenAI Evals API](https://platform.openai.com/docs/api-reference/evals)
- [Azure: Architecture Testing Strategy](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/testing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and reports, with optional Markdown summaries generated from structured JSON evaluation records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write user-specified evaluation summaries and evidence indexes; hard-failure summaries can be configured to block automation.]

## Skill Version(s):

1.0.0 (source: server release metadata and TRUST-CARD.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
