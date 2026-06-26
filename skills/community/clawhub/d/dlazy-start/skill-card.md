## Description: <br>
Quickstart for AI orchestrators driving @dlazy/cli, covering install, authentication, capability discovery, cloud and local tool invocation, async task polling, and common recovery steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to install, authenticate, discover, and invoke @dlazy/cli cloud and local media tools. It helps agents poll asynchronous generation tasks, inspect tool schemas and cost shapes, and recover from common CLI failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication secrets and ~/.dlazy/config.json can expose dLazy account access. <br>
Mitigation: Prefer device-code login, avoid pasting API keys into commands, and treat the local dLazy config file as sensitive. <br>
Risk: Cloud-backed or paid tool calls can send private content to external services or consume credits. <br>
Mitigation: Review tool schemas and cost estimates before invocation, and avoid sending private content unless that is acceptable for the environment. <br>
Risk: Browser-cookie based downloads can expose session material. <br>
Mitigation: Use browser cookies only when required and acceptable, and avoid that option in shared or untrusted environments. <br>


## Reference(s): <br>
- [Dlazy Start on ClawHub](https://clawhub.ai/dlazyai/dlazy-start) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [@dlazy/cli source](https://github.com/dlazyai/cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes discovering current tool schemas, reviewing cost estimates, and handling dLazy credentials carefully.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
