## Description: <br>
Manage secrets through the Bitwarden CLI for shell sessions, Secure Notes, vault listing, and machine setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevengonsalvez](https://clawhub.ai/user/stevengonsalvez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to load Bitwarden-stored secrets into shell sessions, create or update Secure Notes from environment files, list vault items, and set up Bitwarden CLI workflows on machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loading Secure Note contents with bwe or bwe_safe can execute shell content from Bitwarden notes. <br>
Mitigation: Use only Bitwarden notes and vaults you fully trust, prefer bwe_safe for shared or organization accounts, and review note contents before loading them. <br>
Risk: bwce can store every exported environment variable from the current shell in a Bitwarden Secure Note. <br>
Mitigation: Use bwce only when intentionally capturing the current environment and review exported variables first. <br>
Risk: Deletion helpers can remove vault items after resolving an item name. <br>
Mitigation: Manually confirm the target item identity before deletion and prefer limited Bitwarden accounts or collections. <br>


## Reference(s): <br>
- [Bitwarden CLI Documentation](https://bitwarden.com/help/cli/) <br>
- [ClawHub Skill Page](https://clawhub.ai/stevengonsalvez/bitwarden-bwe) <br>
- [CLI Reference](references/cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and sourceable shell functions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bitwarden CLI (bw) and jq; functions operate on Bitwarden vault items and shell environment variables.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
