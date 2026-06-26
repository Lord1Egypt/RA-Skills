## Description: <br>
Provides an AI Dungeon Master workflow for D&D 5e play, including modular adventure running, combat adjudication, character creation, save management, and SRD-backed rule lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ackiles](https://clawhub.ai/user/ackiles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players, game masters, and agent developers use this skill to run D&D 5e sessions through conversation while delegating dice, combat, party state, saves, and SRD lookup to bundled helper code. It is intended for isolated game workspaces where the agent may create and update local campaign files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create, read, update, or delete local game files. <br>
Mitigation: Install and run it only in an isolated game workspace with access limited to campaign files. <br>
Risk: The security summary reports broad personal-assistant, background-monitoring, and publishing powers that are not tightly scoped to gameplay. <br>
Mitigation: Do not grant access to email, calendar, social accounts, broad memory files, repository push permissions, or other non-game resources unless that access is explicitly intended. <br>
Risk: Untrusted save files may be unsafe until scene-cache path handling is fixed. <br>
Mitigation: Avoid loading untrusted saves and review save/cache files before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ackiles/dnd-dm-skill) <br>
- [D&D DM skill instructions](SKILL.md) <br>
- [Dungeon Master operating rules](references/DM_RULES.md) <br>
- [Dungeon Master development guide](references/DM_DEV_GUIDE.md) <br>
- [Dungeon Master templates](references/DM_TEMPLATES.md) <br>
- [SRD lookup skill](srd/SKILL.md) <br>
- [D&D Beyond SRD 5.2.1](https://www.dndbeyond.com/srd) <br>
- [Creative Commons Attribution 4.0 license](https://creativecommons.org/licenses/by/4.0/legalcode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational Markdown with structured tables, code snippets, shell commands, JSON-like state/configuration guidance, and local file updates when permitted.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and pip; supports darwin, linux, and win32 according to server-parsed metadata.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release metadata, SKILL.md frontmatter, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
