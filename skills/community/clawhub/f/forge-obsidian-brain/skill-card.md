## Description: <br>
CLI tool for managing an AI's Obsidian vault with note CRUD, bidirectional sync, capture commands, and intelligent resurface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukeaustin13](https://clawhub.ai/user/lukeaustin13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage local Obsidian knowledge bases, capture notes, search Markdown vault content, and sync selected OpenClaw memory entries with a vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the release as suspicious because file access and deletion safeguards are broader and weaker than expected. <br>
Mitigation: Review or patch path containment and delete confirmation before installing, and run the skill only against a dedicated non-sensitive vault. <br>
Risk: Sync can copy private notes between an Obsidian vault and persistent OpenClaw memory. <br>
Mitigation: Limit sync to notes intended for agent memory, review synced files, and avoid storing secrets or sensitive personal content in synced folders. <br>
Risk: The security guidance warns against running sync/test.js on real data. <br>
Mitigation: Use dry runs or disposable test vaults for validation, and avoid executing test sync scripts against production notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lukeaustin13/forge-obsidian-brain) <br>
- [Obsidian](https://obsidian.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, JSON command results, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local filesystem operations for Obsidian vaults and OpenClaw memory; no network access is claimed in the artifact.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
