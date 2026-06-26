## Description: <br>
Roleplays replies as Zenless Zone Zero Bangboo (邦布): meaningless grunt-like prefixes with complete human meaning in parentheses, using Chinese 嗯/呢/哇/哒 combos or English Ehn-na style when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songkey](https://clawhub.ai/user/songkey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to make an agent answer in Bangboo-style roleplay across Cursor, Claude, OpenClaw, or pasted prompt environments while keeping the real meaning, safety refusals, and factual content inside readable parentheses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review workflows associated with the release may run nested commands with broad local authority. <br>
Mitigation: Use the documented no-yolo option or review commands before execution when broad local authority is not intended. <br>
Risk: Roleplay formatting can obscure the meaningful answer if the grunt prefix is treated as semantic content. <br>
Mitigation: Keep all true meaning, safety refusals, uncertainty, and technical details in the parenthetical text or the immediately following Markdown block. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songkey/bangboo-voice) <br>
- [Integration Guide](docs/integration.md) <br>
- [Bangboo Voice Core Rules](prompts/core-rules.md) <br>
- [Bangboo Chinese Lexicon](.cursor/skills/bangboo-voice/reference-lexicon.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown text with Bangboo grunt prefixes, parenthetical meaning, and normal fenced blocks for long code or tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese mode uses fullwidth parentheses and constrained 嗯/呢/哇/哒 syllables; English mode uses ASCII parentheses and Ehn-na style onomatopoeia.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
