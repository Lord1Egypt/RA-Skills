## Description: <br>
Answers questions about AgentBox cloud sandboxes using the official docs summary, including quickstart, sandbox lifecycle, timeouts, commands, filesystem access, environment variables, CLI use, Python SDK use, and custom templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoygang](https://clawhub.ai/user/guoygang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to get concise AgentBox setup and usage guidance grounded in the bundled official documentation summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential examples may encourage users to expose API keys or passwords if copied without adjustment. <br>
Mitigation: Verify package and authentication details against current AgentBox docs, avoid placing real passwords directly in command-line arguments, and use scoped environment variables or a secret manager for credentials. <br>
Risk: The bundled documentation summary may be outdated relative to AgentBox's current public docs. <br>
Mitigation: For details not covered by the bundled reference, check the latest official AgentBox documentation before acting. <br>


## Reference(s): <br>
- [AgentBox official docs summary](references/agentbox-official.md) <br>
- [AgentBox documentation](https://agentbox.cloud/docs) <br>
- [AgentBox homepage](https://agentbox.cloud/) <br>
- [ClawHub skill page](https://clawhub.ai/guoygang/agentbox-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only documentation guidance; no executable payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
