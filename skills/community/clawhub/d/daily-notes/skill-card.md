## Description: <br>
Daily Notes helps an agent record, list, search, update, archive, and delete personal notes, including notes with image attachments and multi-image associations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kazuya-ecnu](https://clawhub.ai/user/kazuya-ecnu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to capture casual thoughts, reminders, ideas, discoveries, and image-backed notes in a local notes store. The skill is intended for personal note management workflows where the agent may create, retrieve, update, archive, or delete entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically persist casual messages and images as notes without clear per-note consent. <br>
Mitigation: Review or edit the proactive capture rule before deployment if explicit save commands, confirmation before storage, or stricter deletion and retention controls are required. <br>
Risk: Saved notes may contain sensitive personal topics in local files under ~/.openclaw/workspace/notes-data. <br>
Mitigation: Limit installation to environments where local note storage is acceptable and periodically review, archive, or delete stored notes and image attachments. <br>


## Reference(s): <br>
- [Daily Notes on ClawHub](https://clawhub.ai/kazuya-ecnu/daily-notes) <br>
- [Publisher profile](https://clawhub.ai/user/kazuya-ecnu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with JSON-backed local note records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist note content and image references under ~/.openclaw/workspace/notes-data.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
