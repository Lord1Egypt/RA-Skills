## Description: <br>
Complete reference for the Galileo AI platform TypeScript/JS SDK for evaluating, observing, and protecting GenAI applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyanesh-m](https://clawhub.ai/user/gyanesh-m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate the Galileo TypeScript SDK into Node.js or TypeScript GenAI applications for evaluation, observability, tracing, and runtime guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracing and observability workflows may send prompts, model outputs, retrieved documents, tool inputs and outputs, metadata, or session data to Galileo. <br>
Mitigation: Confirm approved data-sharing controls before enabling automatic tracing, and avoid logging secrets, PII, PHI, customer content, or regulated data unless those controls are in place. <br>
Risk: Authentication examples include API keys and username/password credentials. <br>
Mitigation: Prefer scoped API keys stored in a secret manager and avoid hardcoding credentials in code, configuration, or logs. <br>


## Reference(s): <br>
- [Galileo documentation](https://docs.galileo.ai) <br>
- [Galileo TypeScript SDK repository](https://github.com/rungalileo/galileo-js) <br>
- [Galileo npm package](https://www.npmjs.com/package/galileo) <br>
- [SDK examples](https://github.com/rungalileo/sdk-examples) <br>
- [Framework Integrations](references/INTEGRATIONS.md) <br>
- [Guardrail Metrics Reference](references/METRICS.md) <br>
- [Advanced Evaluation Patterns](references/EVALUATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, authentication, tracing, evaluation, and integration guidance for Galileo SDK workflows.] <br>

## Skill Version(s): <br>
v1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
