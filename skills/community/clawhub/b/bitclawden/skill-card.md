## Description: <br>
Look up, create, and edit credentials in Bitwarden vault via the bw CLI. Use when asked to store, retrieve, find, or manage passwords, secrets, or credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[typhonius](https://clawhub.ai/user/typhonius) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and local agents use this skill to manage Bitwarden vault items from a CLI session, including credential lookup, item creation, item edits, password generation, and vault sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on an unlocked Bitwarden vault and access sensitive credentials. <br>
Mitigation: Install only if the local agent runtime is trusted with the vault access available through the active Bitwarden session. <br>
Risk: BW_SESSION is a secret that can unlock vault operations if exposed. <br>
Mitigation: Keep BW_SESSION out of logs, chat, code, and committed files. <br>
Risk: Create, edit, and folder-move operations can change vault records. <br>
Mitigation: Review requested vault mutations before execution and sync the vault after approved changes. <br>
Risk: The built-in installer downloads the Bitwarden CLI with an unpinned curl command. <br>
Mitigation: Prefer installing or verifying the Bitwarden CLI directly before using the skill. <br>


## Reference(s): <br>
- [bitclawden on ClawHub](https://clawhub.ai/typhonius/bitclawden) <br>
- [Bitwarden CLI documentation](https://bitwarden.com/help/cli/) <br>
- [Bitwarden](https://bitwarden.com/) <br>
- [jq](https://jqlang.github.io/jq/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bw, jq, and BW_SESSION; lookup commands may reveal vault data, and create or edit commands can modify Bitwarden vault items.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
