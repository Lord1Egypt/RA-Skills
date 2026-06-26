## Description: <br>
Builds and updates OpenClaw agents by designing personas, operating rules, autonomy settings, and complete workspace files with safety checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced OpenClaw users use this skill to design new agents or refine existing ones, including persona, operating rules, autonomy model, safety boundaries, memory posture, heartbeat plan, skill roster, and workspace files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent workspace files can enable unsafe autonomy, memory, heartbeat, external tool, or outbound-action behavior if adopted without review. <br>
Mitigation: Review generated AGENTS.md, SOUL.md, MEMORY.md, and HEARTBEAT.md before use, and require deliberate approval before enabling memory, heartbeats, external tools, or autonomous actions. <br>
Risk: Generated workspace content could expose secrets or credentials if a user includes them in prompts or files. <br>
Mitigation: Do not place secrets, OAuth tokens, API keys, credentials, or private session transcripts in the generated workspace. <br>


## Reference(s): <br>
- [OpenClaw agent workspace](references/openclaw-workspace.md) <br>
- [OpenClaw agent file templates](references/templates.md) <br>
- [Agent Architecture Patterns](references/architecture.md) <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-agent-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown file contents, checklists, and concise scenario prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw workspace files such as IDENTITY.md, SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md, and acceptance-test prompts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
