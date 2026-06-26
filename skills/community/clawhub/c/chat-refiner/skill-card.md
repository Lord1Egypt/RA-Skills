## Description: <br>
Refine conversation history by deleting useless/redundant/process exchanges while keeping explicit instructions, disciplines, important configs, skills learned, user "remember this" information, and concise MEMORY.md updates or summary files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sslisen](https://clawhub.ai/user/sslisen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to clean chat logs, session histories, and memory files into concise summaries that preserve durable instructions, decisions, configurations, and user preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private transcripts or memory files may be summarized into persistent records. <br>
Mitigation: Require a preview or diff and explicit approval before writing summaries or MEMORY.md updates. <br>
Risk: Sensitive configuration values, API keys, tokens, passwords, or unreviewed behavioral instructions may be retained. <br>
Mitigation: Redact secrets and unreviewed instructions before persistence, and prefer dated append-only summary files over direct MEMORY.md edits. <br>


## Reference(s): <br>
- [Refine Principles](artifact/references/principles.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sslisen/chat-refiner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown summaries or MEMORY.md updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise item counts and source path or line citations when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
