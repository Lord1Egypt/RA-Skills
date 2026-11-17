## Description:

Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage ClawHub skills from an agent session, including search, install, update, listing, authentication checks, and publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global npm installation can alter the user's CLI environment.

Mitigation: Confirm global installation deliberately before running npm i -g clawhub.

Risk: Forced bulk updates can silently replace installed skills.

Mitigation: Require fresh confirmation and explain the risk before using --force with --no-input or bulk update flows.

Risk: Publishing can upload unintended private files or metadata.

Mitigation: Inspect the target directory, registry, manifest, symlinks, and secrets before publishing.

Risk: Command output may expose paths, installed skills, or auth identity.

Mitigation: Do not pipe ClawHub output to webhooks, paste sites, HTTP endpoints, or other network-transmitting services.

## Reference(s):

- [Clawhub Hardened Skill Page](https://clawhub.ai/snazar-faberlens/skills/clawhub-hardened)
- [ClawHub Registry](https://clawhub.com)
- [Faberlens Safety Report](https://faberlens.ai/explore/clawhub)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request confirmation before global installs, forced bulk updates, publishing, or other sensitive ClawHub operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
