## Description: <br>
Distills a colleague into an AI Skill by collecting authorized workplace source material and generating both a Work Skill and a Persona that can continue to evolve. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yifeiwang1981](https://clawhub.ai/user/yifeiwang1981) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to create colleague-style agent skills from consented source materials such as documents, messages, emails, screenshots, or pasted text. The generated skill combines work methods, technical preferences, communication style, and versioned updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect workplace messages, documents, browser-session content, and other personal or sensitive material. <br>
Mitigation: Use only with explicit authorization from the person being modeled and the workspace owner or administrator; prefer redacted manual imports when possible. <br>
Risk: Token-based collectors and browser-session collection may expose sensitive credentials or private chats. <br>
Mitigation: Avoid private chats, DMs, browser-profile scraping, and token-based collection unless there is a clear business need, written consent, and a retention/deletion plan. <br>
Risk: Stored credentials and collected data may persist beyond the intended task. <br>
Mitigation: Store credentials in a secure vault where possible, rotate tokens used for testing, and define retention and deletion practices before collection. <br>


## Reference(s): <br>
- [Create Colleague ClawHub Release](https://clawhub.ai/yifeiwang1981/create-colleague) <br>
- [README](artifact/README.md) <br>
- [Installation Guide](artifact/INSTALL.md) <br>
- [Product Requirements Document](artifact/docs/PRD.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, JSON metadata, command guidance, and generated skill source files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated colleague skill files under colleagues/{slug}/ and may call local collector/parser tools when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
