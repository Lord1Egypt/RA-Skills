## Description: <br>
Manage Asana tasks, projects, briefs, status updates, custom fields, dependencies, attachments, events, and timelines via Personal Access Token (PAT). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[L-U-C-K-Y](https://clawhub.ai/user/L-U-C-K-Y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to let an agent manage Asana workspaces, tasks, projects, project briefs, status updates, timelines, custom fields, dependencies, comments, events, and attachments through an Asana Personal Access Token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mutate real Asana workspace data, including tasks, comments, project status updates, briefs, timelines, dependencies, and sections. <br>
Mitigation: Require explicit human approval before task mutations, comments, status updates, brief changes, timeline shifts, dependency changes, or section moves. <br>
Risk: The Asana PAT grants authenticated workspace access and may be exposed if stored or displayed carelessly. <br>
Mitigation: Use the least-privileged PAT available, store it through a secret-aware configuration path, and avoid exposing it with config read commands, logs, prompts, or shell history. <br>
Risk: Attachment upload can send local files to Asana. <br>
Mitigation: Require human confirmation of the exact local file path and destination task before uploading attachments or embedding inline images. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/L-U-C-K-Y/asana-agent-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/L-U-C-K-Y) <br>
- [Asana personal access token documentation](https://developers.asana.com/docs/personal-access-token) <br>
- [Asana authentication overview](https://developers.asana.com/docs/authentication) <br>
- [Asana rich text guide](https://developers.asana.com/docs/rich-text) <br>
- [Asana attachment upload reference](https://developers.asana.com/reference/createattachmentforobject) <br>
- [Reference and implementation notes](references/REFERENCE.md) <br>
- [OpenClaw skills configuration](https://docs.openclaw.ai/tools/skills-config) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-only CLI stdout from the Asana script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and an Asana PAT supplied through ASANA_PAT or equivalent OpenClaw configuration.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
