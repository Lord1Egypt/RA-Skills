## Description:

Use the ClawdHub CLI to search, install, update, and publish agent skills from clawdhub.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jk50505k](https://clawhub.ai/user/jk50505k)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to run ClawdHub CLI commands for searching, installing, updating, listing, authenticating, and publishing ClawHub skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned global npm install can install a CLI version that differs from the reviewed release.

Mitigation: Prefer installing a specific reviewed `clawdhub` version and avoid elevated or global installs when possible.

Risk: Broad noninteractive update commands can change every installed skill without prompts.

Mitigation: Use `update --all --no-input --force` only in controlled settings where changing all installed skills is intentional.

## Reference(s):

- [Clawdhub Copy skill page](https://clawhub.ai/jk50505k/skills/clawdhub-copy)
- [ClawdHub registry](https://clawdhub.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may use the npm-installed clawdhub CLI, optional authentication, registry overrides, and working-directory or install-directory flags.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
