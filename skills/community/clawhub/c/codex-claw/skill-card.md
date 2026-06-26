## Description: <br>
Install and verify Codex Claw for Codex Desktop AGENTS.md, Agent MD, SOUL.md, soul file, session memory, personality, and OpenClaw workspace context loading through the @openclaw/codex-claw plugin with post-compaction reinjection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[100yenadmin](https://clawhub.ai/user/100yenadmin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and verify Codex Claw so Codex Desktop can load selected AGENTS.md and SOUL.md workspace context. They also use it to review those files before enabling them broadly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on AGENTS.md or SOUL.md context can expose secrets, private memories, local-only paths, or unsafe instructions to future Codex sessions. <br>
Mitigation: Review and scope those files before enabling Codex Claw; remove secrets, private data, and instructions that conflict with native Codex behavior. <br>
Risk: Plugin installation and marketplace configuration changes affect local Codex Desktop behavior. <br>
Mitigation: Install only verified package artifacts, check bridge status and logs, and enable plugin hooks only where the user intends to load this context. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and TOML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, configuration, verification, and review guidance; does not produce runtime artifacts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
