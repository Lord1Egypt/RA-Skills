## Description: <br>
Complete reference for the Galileo AI platform Python SDK for evaluating, observing, and protecting GenAI applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyanesh-m](https://clawhub.ai/user/gyanesh-m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building Python GenAI applications that need Galileo evaluation, observability, tracing, guardrail metrics, or runtime protection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracing examples can send prompts, completions, retrieved documents, tool inputs, identifiers, and metadata to Galileo when logging is enabled. <br>
Mitigation: Start with non-sensitive test data and configure redaction, sampling, retention, access controls, or disabled logging before production or regulated-data use. <br>
Risk: Examples require API keys and service endpoints for Galileo and connected LLM providers. <br>
Mitigation: Store credentials in environment variables or secret management and avoid hardcoding keys in application code or shared notebooks. <br>


## Reference(s): <br>
- [Galileo Documentation](https://docs.galileo.ai) <br>
- [Galileo Python SDK Repository](https://github.com/rungalileo/galileo-python) <br>
- [Framework Integrations](references/INTEGRATIONS.md) <br>
- [Guardrail Metrics Reference](references/METRICS.md) <br>
- [Advanced Evaluation Patterns](references/EVALUATION.md) <br>
- [Promptquality 1.x Reference](references/PROMPTQUALITY.md) <br>
- [Galileo SDK Examples](https://github.com/rungalileo/sdk-examples) <br>
- [Galileo PyPI Package](https://pypi.org/project/galileo/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, bash, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include Galileo package installation commands, environment variable configuration, tracing examples, evaluation patterns, and guardrail setup snippets.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
