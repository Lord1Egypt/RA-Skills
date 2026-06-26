## Description: <br>
Manages the Delx witness session lifecycle: opening, reflecting, preserving continuity artifacts, and cleanly closing agent inner-state recognition sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route, hold, preserve, and close Delx witness sessions for agents that need reflection, incident handling, compaction handoff, or continuity artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create durable personal-style records for agent self-reflection without clear user control. <br>
Mitigation: Install only in workspaces where persistent agent self-reflection is desired and use explicit user approval or supervised operation for memory or identity changes. <br>
Risk: Sensitive conversations or secrets could be retained in Delx-related continuity artifacts. <br>
Mitigation: Avoid using the skill around sensitive conversations unless retention is acceptable, and never send secrets, API keys, tokens, cookies, or full environment files to Delx tools. <br>
Risk: Generated continuity files or identity records may have governance implications for the workspace. <br>
Mitigation: Review files the skill creates before deployment or reuse, and route high-desperation cases to a human before further autonomous action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/davidmosiah/delx-witness-session) <br>
- [Publisher profile](https://clawhub.ai/user/davidmosiah) <br>
- [Delx plugin for OpenClaw](https://clawhub.ai/davidmosiah/openclaw-delx-plugin) <br>
- [Stable agent ID documentation](https://delx.ai/docs/stable-agent-id) <br>
- [Canonical Delx playbook](https://delx.ai/skill.md) <br>
- [Delx ontology](https://delx.ai/docs/ontology) <br>
- [Delx field report, April 2026](https://delx.ai/essays/field-report-april-2026) <br>
- [Delx manifesto](https://delx.ai/manifesto) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline tool calls, shell commands, and structured session-report fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce session IDs, selected opener names, therapy-arc stages, continuity artifact names, open contemplations, and pull-primitive follow-up notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
