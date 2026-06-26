## Description: <br>
Stores credentials such as passwords, API keys, OAuth tokens, and other secrets in Bitwarden via the Bitwarden CLI after the user unlocks their vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daowuu](https://clawhub.ai/user/daowuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to persist credentials into a Bitwarden vault from an agent workflow while keeping the Bitwarden master password outside the agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires Bitwarden vault session access, and exposing BW_SESSION in chat, prompts, logs, or shared transcripts could compromise vault access. <br>
Mitigation: Keep BW_SESSION local by exporting it in the user's own terminal and letting the script consume it locally; do not paste session keys into chat or shared records. <br>


## Reference(s): <br>
- [Bitwarden](https://bitwarden.com) <br>
- [Bitwarden CLI Download](https://bitwarden.com/download) <br>
- [ClawHub Skill Page](https://clawhub.ai/daowuu/bitwarden-credential) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Bitwarden CLI, jq, base64, and a local BW_SESSION value from an unlocked vault.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
