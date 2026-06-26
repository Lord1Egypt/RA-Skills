## Description: <br>
Imports SillyTavern-compatible TavernAI V2/V3 character cards for roleplay across OpenClaw-supported chat platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pearyj](https://clawhub.ai/user/pearyj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to import, manage, and activate community character cards for roleplay, companion-style chat, or temporary character preview sessions. It can modify persistent identity and memory files in play and soul modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported third-party character cards can persistently change the assistant's identity and memory. <br>
Mitigation: Prefer temporary chat mode for untrusted cards, inspect card prompts before play or soul mode, and restore SOUL.md or clean MEMORY.md before returning to normal or sensitive tasks. <br>
Risk: Arbitrary URL imports can bring in untrusted roleplay card content. <br>
Mitigation: Import cards only from trusted sources and review downloaded card content before using persistent play or soul modes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pearyj/cn) <br>
- [Chub.ai character cards](https://chub.ai) <br>
- [CharaVault character cards](https://charavault.net) <br>
- [AI Character Cards](https://aicharactercards.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON character-card data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and may write character data, SOUL.md, and MEMORY.md in the user's OpenClaw directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
