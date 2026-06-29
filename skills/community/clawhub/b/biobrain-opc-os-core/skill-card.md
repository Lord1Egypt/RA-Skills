## Description: <br>
AI-native one-person company operating system with 7 autonomous agent departments, governance, cron automation, revenue funnel, and inter-agent comms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ygq19901001](https://clawhub.ai/user/ygq19901001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to structure a one-person company around autonomous agent departments, governance rules, scheduled operating cadences, inter-agent communication, and revenue workflow guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous agents may publish posts, upload documents, or republish skills without sufficient approval boundaries. <br>
Mitigation: Require manual approval for public posts, cloud uploads, skill publishing, and republishing before enabling those workflows. <br>
Risk: Tencent Docs or Feishu fallback channels may expose sensitive company information if used for unrestricted agent communication. <br>
Mitigation: Restrict cloud-document fallback to non-sensitive or explicitly approved workspaces, and keep sensitive work in local or approved private channels. <br>
Risk: Scheduled jobs may run recurring agent actions with outdated payloads or unintended authority. <br>
Mitigation: Review cron payloads before activation, stagger jobs, and configure failure alerts and periodic inspection for recurring workflows. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/Ygq19901001/biobrain-opc-os-core) <br>
- [ClawHub skill page](https://clawhub.ai/ygq19901001/skills/biobrain-opc-os-core) <br>
- [Communication Protocols](references/communication-protocols.md) <br>
- [Cron Orchestration](references/cron-orchestration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration instructions, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline YAML, JSON, shell, and directory-structure examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operating-system guidance for agent departments, scheduled jobs, communication channels, governance rules, and publishing workflows.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
