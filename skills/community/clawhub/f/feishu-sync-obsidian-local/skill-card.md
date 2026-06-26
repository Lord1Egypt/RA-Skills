## Description: <br>
Synchronizes Feishu Wiki documents into a local Obsidian PARA knowledge base through a gated four-step pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink-kai](https://clawhub.ai/user/ink-kai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Obsidian users and knowledge-base maintainers use this skill to plan, confirm, fetch, and write Feishu Wiki content into a local PARA-structured vault while preserving source metadata and avoiding duplicate document imports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local write helper is not safely confined to the intended vault. <br>
Mitigation: Set an explicit VAULT_DIR, inspect SYNC-RULES.md, run --dry-run first, confirm every planned destination path, and keep a vault backup before allowing writes. <br>
Risk: Persistence and automation behavior is unclear, including AGENTS.md additions and a weekly sync timer mentioned in the artifact. <br>
Mitigation: Do not enable AGENTS.md appends or scheduled sync unless persistent automatic synchronization is intended and reviewed. <br>
Risk: The skill requires Feishu access through agent-side OAuth-capable tools. <br>
Mitigation: Use least-privilege Feishu access and avoid placing access tokens or long-lived credentials in the skill files or vault. <br>


## Reference(s): <br>
- [SYNC-RULES.md template](artifact/assets/sync-rules-template.md) <br>
- [Sync quality review checklist](artifact/references/review-checklist.md) <br>
- [ClawHub skill page](https://clawhub.ai/ink-kai/feishu-sync-obsidian-local) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-based sync plan/write inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Markdown files into an Obsidian vault when the user confirms the plan and invokes the local sync helper.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
