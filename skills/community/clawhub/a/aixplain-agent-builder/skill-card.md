## Description: <br>
Design and deploy aiXplain agents with conservative defaults, read-only discovery first, and explicit approval gates for higher-risk actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nurhamdan1987](https://clawhub.ai/user/nurhamdan1987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, inspect, build, deploy, and debug aiXplain agents while keeping discovery read-only by default and requiring approval for higher-risk actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an aiXplain API key and may involve OAuth integrations or other sensitive credentials. <br>
Mitigation: Use existing environment configuration such as AIXPLAIN_API_KEY, avoid requesting secrets in chat, and review approval prompts before creating authenticated integrations. <br>
Risk: Agent creation, deployed-agent changes, file uploads, write-capable tools, runtime code tools, and custom script-backed tools can change remote state or widen access. <br>
Mitigation: Start in read-only planning mode, search existing marketplace assets first, and proceed only after the user explicitly approves the specific higher-risk step. <br>
Risk: Verbose debugging traces may expose prompts, tool inputs, tool outputs, or sensitive integration data. <br>
Mitigation: Use detailed trace verbosity sparingly and only when needed for debugging or verification. <br>


## Reference(s): <br>
- [Safety Gates](references/safety-gates.md) <br>
- [Read-Only Patterns](references/read-only-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown with Python SDK code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include approval prompts, aiXplain Studio links, and debugging trace guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
