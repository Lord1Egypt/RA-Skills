## Description:

Actively verifies Python and JavaScript code correctness by generating targeted edge-case tests and running candidate solutions against them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to evaluate competitive-programming style Python or JavaScript solutions by generating targeted test inputs, expected outputs, and pass/fail verification results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs submitted code on the user's machine.

Mitigation: Run it only inside a disposable, locked-down sandbox or container with restricted filesystem, network, process, CPU, and memory access.

Risk: Submitted problems and code may be sent to OpenAI when an API key is configured.

Mitigation: Review inputs for sensitive data before use and avoid inherited secrets in the execution environment.

## Reference(s):

- [Scaling Agentic Verifier for Competitive Coding](https://arxiv.org/abs/2602.09012)
- [ClawHub skill page](https://clawhub.ai/wanng-ide/skills/arxiv-agentic-verifier)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Code, Guidance]

**Output Format:** [JSON objects and console text describing generated tests, execution results, and verification outcomes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY for model-backed test generation; falls back to mock test data when no key is configured.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
