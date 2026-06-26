## Description: <br>
Reviews Elixir code for security vulnerabilities including code injection, atom exhaustion, and secret handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to review Elixir source code that handles user input, external data, or sensitive configuration. It helps structure findings around code injection, unsafe term deserialization, atom exhaustion, secrets, ETS exposure, and process-data exposure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt an agent to inspect source files for secrets and security-sensitive patterns. <br>
Mitigation: Run reviews only in repositories the agent is authorized to inspect, and avoid adding live credentials to prompts or test fixtures. <br>
Risk: Security findings can be misleading if reported from partial context or without a concrete external-data path. <br>
Mitigation: Apply the skill's hard gates before reporting: verify current file locations, read the surrounding code, and name a concrete ingress for user or untrusted input claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/elixir-security-review) <br>
- [Atom Exhaustion](references/atom-exhaustion.md) <br>
- [Code Injection](references/code-injection.md) <br>
- [Secrets and configuration](references/secrets.md) <br>
- [Process Exposure](references/process-exposure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown security review findings with file and line references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to follow the skill's hard gates and include current file locations before reporting.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
