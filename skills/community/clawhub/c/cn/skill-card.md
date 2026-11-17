## Description:

导入 SillyTavern 兼容的角色卡（TavernAI V2/V3 PNG 格式），在任意聊天平台上角色扮演.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pearyj](https://clawhub.ai/user/pearyj)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to import SillyTavern/TavernAI character cards from local files, URLs, or online card libraries, then chat or roleplay with the imported character across OpenClaw-supported messaging platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported character cards are untrusted content that may influence identity, memory, and behavior when activated.

Mitigation: Inspect card contents before activation and prefer the non-persistent chat mode for new or unfamiliar cards.

Risk: Persistent roleplay modes can alter OpenClaw identity and memory files.

Mitigation: Review or clean ~/.openclaw/SOUL.md, ~/.openclaw/SOUL.md.backup, ~/.openclaw/MEMORY.md, and ~/.openclaw/characters after use.

Risk: URL imports can retrieve arbitrary remote card files.

Mitigation: Avoid arbitrary URLs and use trusted card sources where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pearyj/skills/cn)
- [Chub.ai](https://chub.ai)
- [AI Character Cards](https://aicharactercards.com)
- [Character Tavern](https://charactertavern.com)
- [CharaVault](https://charavault.net)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and JSON character-card data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and may persist imported character data under the OpenClaw user directory.]

## Skill Version(s):

0.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
