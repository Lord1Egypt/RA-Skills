## Description: <br>
E2B Sandbox Runtime is a knowledge skill for guiding agents that work with E2B cloud sandboxes for isolated AI-generated code execution through Python and TypeScript SDKs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide E2B sandbox runtime work, including sandbox creation, command execution, file operations, exposed services, templates, and related safety constraints. Because the evidence also shows finance/ZVT automation content, adopters should confirm the intended scope before relying on it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evidence shows mixed E2B sandbox runtime and finance/ZVT automation scope. <br>
Mitigation: Install only after reviewing that both scopes are intended; otherwise request a split or narrowed release before use. <br>
Risk: The skill may install packages, run shell commands, expose ports, preserve state, use network access, and handle credentials. <br>
Mitigation: Review generated commands before execution, restrict network access where possible, use least-privilege and short-lived credentials, and avoid preserving sensitive state. <br>
Risk: Artifact constraints warn that secrets passed through sandbox environment parameters can be exposed through process listing. <br>
Mitigation: Do not place API keys or tokens in sandbox environment parameters; fetch secrets at runtime through a controlled secret path and clear them after use. <br>
Risk: Artifact constraints warn that missed sandbox cleanup can leave TypeScript sandboxes running until timeout. <br>
Mitigation: Wrap sandbox creation in try/finally and always call the appropriate kill or cleanup method on every exit path. <br>
Risk: Server capability tags indicate crypto, purchase, OAuth token, and sensitive credential handling. <br>
Mitigation: Require explicit user confirmation for paid, broker, exchange, or credentialed actions and keep tokens scoped to the minimum required permissions. <br>


## Reference(s): <br>
- [Authoritative seed.yaml](references/seed.yaml) <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/e2b-sandbox-runtime) <br>
- [Doramagic crystal page](https://doramagic.ai/zh/crystal/e2b-sandbox-runtime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference E2B runtime credentials, sandbox lifecycle controls, network settings, and finance workflow constraints.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
