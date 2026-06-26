## Description: <br>
Formats Discord-ready messages and templates using Discord Markdown syntax, including emphasis, spoilers, code blocks, mentions, timestamps, and metadata summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BillChirico](https://clawhub.ai/user/BillChirico) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Community managers, Discord moderators, developers, and bot authors use this skill to compose copy-paste-ready Discord messages, bot responses, embed descriptions, forum posts, and webhook payloads with preserved Markdown syntax and message metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Discord messages may include @everyone, @here, or role mentions that notify a broad audience. <br>
Mitigation: Review mention counts and remove or replace broad notifications before posting. <br>
Risk: Masked links, public-channel content, or over-limit messages may cause unintended disclosure or posting failures. <br>
Mitigation: Inspect links and content destination, and split or shorten messages when the metadata summary approaches Discord limits. <br>


## Reference(s): <br>
- [Discord Markdown Formatting](SKILL.md) <br>
- [Syntax Highlighting Languages](references/syntax-highlighting.md) <br>
- [Discord Formatting Templates](references/templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/BillChirico/discord-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown fenced code blocks with a metadata summary table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Discord-ready messages are presented in copyable fenced code blocks; summaries report character count, sections, mentions, URLs, and code block languages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
