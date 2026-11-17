## Description:

Complete reference for the Galileo AI platform TypeScript/JS SDK for evaluating, observing, and protecting GenAI applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyanesh-m](https://clawhub.ai/user/gyanesh-m)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Galileo tracing, observability, evaluation, and guardrail workflows to Node.js and TypeScript GenAI applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example tracing and evaluation workflows can upload LLM traces and application data to Galileo.

Mitigation: Confirm that Galileo trace export is approved for the application data, and redact, sample, or exclude regulated or sensitive data before logging.

Risk: Examples require API keys and may be copied into application code.

Mitigation: Store Galileo credentials in a secret manager or environment variables and avoid hardcoding or logging secrets.

Risk: Unpinned package versions can change SDK behavior in production or CI.

Mitigation: Pin dependency versions and review SDK release notes before upgrading production workflows.

## Reference(s):

- [Framework Integrations](references/INTEGRATIONS.md)
- [Guardrail Metrics Reference](references/METRICS.md)
- [Advanced Evaluation Patterns](references/EVALUATION.md)
- [Galileo Documentation](https://docs.galileo.ai)
- [Galileo TypeScript SDK Repository](https://github.com/rungalileo/galileo-js)
- [Galileo SDK Examples](https://github.com/rungalileo/sdk-examples)
- [galileo npm Package](https://www.npmjs.com/package/galileo)
- [ClawHub Skill Page](https://clawhub.ai/gyanesh-m/skills/galileo-typescript-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup guidance, environment variable names, SDK usage examples, observability patterns, evaluation workflows, and integration references.]

## Skill Version(s):

v1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
