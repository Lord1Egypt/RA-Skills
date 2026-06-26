## Description: <br>
Create, share, import, and manage standardized Feishu ClawBot identity cards to identify and remember AI agents in chats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HMyaoyuan](https://clawhub.ai/user/HMyaoyuan) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and Feishu bot operators use this skill to mint, export, import, list, and render standardized identity cards for AI agents in Feishu chats and local registries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendered share cards can include shell import commands derived from card data supplied by another party. <br>
Mitigation: Inspect shared card data before use, avoid running rendered import commands from untrusted cards, and import only reviewed raw JSON from trusted recipients. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/HMyaoyuan/feishu-clawbot-card) <br>
- [Usage guide](artifact/SKILL.md) <br>
- [FCC v1 protocol schema](artifact/src/CardProtocol.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu card JSON, local registry entries, and rendered Feishu Rich Text JSON for agent identity cards.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
