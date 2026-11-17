## Description:

Install a Chrome extension by ID or Chrome Web Store URL on this Mac.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanpwelliver-oss](https://clawhub.ai/user/ryanpwelliver-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install Chrome extensions by opening a Chrome Web Store page, applying a managed macOS Chrome policy, or loading an unpacked local extension during development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A managed-policy force install can add a Chrome extension without a user click and can persist until the policy is removed.

Mitigation: Prefer the Chrome Web Store method with user approval; use force install only for intentional administration and document how to remove the policy afterward.

Risk: Installing the wrong extension ID could grant browser permissions to an unintended extension.

Mitigation: Verify the exact extension ID, publisher, and requested permissions before running policy-based installation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryanpwelliver-oss/skills/chrome-extension-installer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides Chrome Web Store, macOS managed policy, and unpacked-extension installation guidance.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
