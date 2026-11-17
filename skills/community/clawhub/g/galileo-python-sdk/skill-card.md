## Description:

Complete reference for the Galileo AI platform Python SDK for evaluating, observing, and protecting GenAI applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyanesh-m](https://clawhub.ai/user/gyanesh-m)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a reference for adding Galileo SDK evaluation, observability, tracing, framework integrations, and runtime guardrails to Python GenAI applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes Galileo tracing and observability workflows that can send evaluation, prompt, response, and trace data to Galileo services.

Mitigation: Use it only where sending this data to Galileo is acceptable under privacy, retention, and customer-data requirements.

Risk: The examples rely on API keys and package installation choices that can affect production environments.

Mitigation: Keep API keys in environment variables or secret storage, avoid logging secrets or regulated data, and pin package versions in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gyanesh-m/skills/galileo-python-sdk)
- [Galileo Documentation](https://docs.galileo.ai)
- [Galileo Python SDK Repository](https://github.com/rungalileo/galileo-python)
- [Galileo SDK Examples](https://github.com/rungalileo/sdk-examples)
- [Galileo PyPI Package](https://pypi.org/project/galileo/)
- [Framework Integrations](references/INTEGRATIONS.md)
- [Advanced Evaluation Patterns](references/EVALUATION.md)
- [Guardrail Metrics Reference](references/METRICS.md)
- [Promptquality 1.x Reference](references/PROMPTQUALITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SDK version selection guidance, environment variable setup, tracing patterns, evaluation examples, and guardrail metric references.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata; artifact frontmatter metadata.version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
