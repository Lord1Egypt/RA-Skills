## Description:

One-click publishing helper for pushing skills to the ClawHub registry while handling acceptLicenseTerms and upload format issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bg1avd](https://clawhub.ai/user/bg1avd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to publish individual or batched ClawHub skills from local directories, using SKILL.md metadata and a local ClawHub token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload more files from a local skill directory than the user expects.

Mitigation: Run it only on clean skill directories and remove secrets, .env files, private keys, local configuration, symlinks, and unrelated files before publishing.

Risk: The skill uses the local ClawHub token to publish to clawhub.ai.

Mitigation: Confirm the target registry, slug, version, and selected account before execution, and rotate the token if unintended content is published.

Risk: The skill automatically includes acceptLicenseTerms when publishing.

Mitigation: Confirm the applicable ClawHub license terms and release license before running the publish command.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bg1avd/skills/clawhub-push-skill)
- [ClawHub registry](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish local skill files to clawhub.ai using the user's stored ClawHub token.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
