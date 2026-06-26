## Description: <br>
Guides users through natural conversation to record daily life, generate prose-style diary entries, and include uploaded images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinrenkun4916-hash](https://clawhub.ai/user/yinrenkun4916-hash) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to reflect on their day through a short, conversational exchange and produce a polished Markdown diary entry. It can also organize diary entries and image references into a local journals folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diary entries, mood scores, keywords, and photos may contain private personal information saved in a local journals/ folder. <br>
Mitigation: Keep the journals/ folder private and avoid publishing it through public repositories or unintended cloud sync. <br>
Risk: Image paths supplied by the user may copy photos into the local diary archive. <br>
Mitigation: Only provide images or file paths that should be preserved in the diary archive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinrenkun4916-hash/diary-conversation) <br>
- [Prose diary format guide](references/diary-formats.md) <br>
- [Local file storage guide](references/file-storage.md) <br>
- [Image handling guide](references/image-handling.md) <br>
- [Question templates](references/question-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, code, shell commands, guidance] <br>
**Output Format:** [Markdown diary entries with local file paths, image references, and optional JSON index updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces diary content intended for local storage under journals/ with optional image organization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
