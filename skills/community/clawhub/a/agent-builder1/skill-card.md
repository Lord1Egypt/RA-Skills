## Description: <br>
Build high-performing OpenClaw agents end-to-end. Use when you want to design a new agent (persona + operating rules) and generate the required OpenClaw workspace files (SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md + memory/YYYY-MM-DD.md). Also use to iterate on an existing agent's behavior, guardrails, autonomy model, heartbeat plan, and skill roster. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design new OpenClaw agent workspaces, generate the core workspace files, and revise existing agents' behavior, guardrails, autonomy model, heartbeat plan, and skill roster. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent files could permit excessive autonomy, destructive actions, or outbound messages if reviewed carelessly. <br>
Mitigation: Review generated workspace files before use and confirm ask-before-destructive and ask-before-outbound-message rules. <br>
Risk: Optional memory files could capture secrets, private chat logs, or other sensitive user information. <br>
Mitigation: Avoid storing secrets or private chat logs in MEMORY.md or dated memory notes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/marjoriebroad/agent-builder1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with generated workspace file content, targeted diffs, checklists, and scenario prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce proposed contents for IDENTITY.md, SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md, dated memory notes, and TOOLS.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
