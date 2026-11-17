## Description:

Flickr Claw helps agents use a user's local Flickr credentials to verify authorization, export recent-upload or album metadata, download images for local review, and update photo tags, titles, and descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users working with a Flickr account use this skill to run local auth checks, export album or recent-upload metadata, download images for visual review, and apply reviewed metadata updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flickr credentials and OAuth tokens are stored locally in plaintext under ~/.openclaw.

Mitigation: Protect ~/.openclaw from other users and backups, remove token files when no longer needed, and revoke or rotate Flickr tokens after use.

Risk: Write-capable authorization can change photo tags, titles, and descriptions.

Mitigation: Use read-only tokens for exports and downloads, mint write tokens only for reviewed metadata edits, and avoid delete permission.

Risk: The skill depends on locally installed Python packages.

Mitigation: Use a virtual environment and pin dependencies before running it in sensitive environments.

## Reference(s):

- [Flickr workflow](artifact/references/workflow.md)
- [Flickr Claw release page](https://clawhub.ai/stanestane/skills/flickr-claw)
- [Flickr REST API endpoint](https://api.flickr.com/services/rest)
- [Flickr OAuth authorization endpoint](https://www.flickr.com/services/oauth/authorize)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with command examples; CSV metadata exports and downloaded image files when commands are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Flickr API credentials and OAuth token files; write actions require write-capable Flickr authorization.]

## Skill Version(s):

1.5.0 (source: server evidence release.version and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
