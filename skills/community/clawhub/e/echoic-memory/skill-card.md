## Description: <br>
Echoic Memory helps an agent create local memorial AI skills from chat history, photos, videos, voice memos, social media, and written memories to preserve a person's personality, expression style, and shared memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quqicolour](https://clawhub.ai/user/quqicolour) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to collect memories and source materials about a departed or absent loved one, analyze them, and generate a local conversational memorial skill with memory and persona files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive personal data such as chats, photos, voice or video metadata, relationship details, and generated persona files. <br>
Mitigation: Use copied or redacted inputs, store outputs only in a trusted local workspace, and get permission before using data about living people. <br>
Risk: The workflow references third-party chat export and decryption tools for WeChat and similar data sources. <br>
Mitigation: Use those tools only after reviewing their legal, account, and privacy implications; avoid importing data that you are not authorized to process. <br>
Risk: The skill includes delete and rollback behaviors that can overwrite or remove generated memorial skill files. <br>
Mitigation: Back up important outputs before delete, farewell, rollback, or update commands. <br>
Risk: Video metadata parsing includes eval-based frame-rate handling. <br>
Mitigation: Do not analyze untrusted video files until the frame-rate parsing is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quqicolour/echoic-memory) <br>
- [Publisher profile](https://clawhub.ai/user/quqicolour) <br>
- [README](artifact/README.md) <br>
- [Architecture](artifact/docs/ARCHITECTURE.md) <br>
- [Cross-platform guide](artifact/docs/CROSS_PLATFORM.md) <br>
- [Product requirements](artifact/docs/PRD.md) <br>
- [WeChatMsg export tool](https://github.com/LC044/WeChatMsg) <br>
- [PyWxDump export tool](https://github.com/xaoyaoo/PyWxDump) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory, persona, metadata, and generated SKILL.md files under an echoes directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
