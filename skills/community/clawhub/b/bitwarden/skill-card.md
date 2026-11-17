## Description:

Access and manage Bitwarden/Vaultwarden passwords securely using the rbw CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asleep123](https://clawhub.ai/user/asleep123)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and run rbw commands for Bitwarden or Vaultwarden vault setup, unlock, sync, search, retrieval, and item management from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unlocking a Bitwarden or Vaultwarden vault can expose passwords and item JSON to the agent session.

Mitigation: Use the skill only in trusted workspaces, and lock or clear rbw session state when finished.

Risk: Vault operations depend on rbw being configured, authenticated, unlocked, and synced before use.

Mitigation: Confirm rbw setup, complete login or 2FA prompts, and run rbw sync before retrieving details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/asleep123/skills/bitwarden)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces rbw command guidance that may expose vault item data to the agent session.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
