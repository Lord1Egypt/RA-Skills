## Description:

Create user-facing App Store release notes by collecting and summarizing all user-impacting changes since the last git tag (or a specified ref).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimillian](https://clawhub.ai/user/dimillian)

### License/Terms of Use:


## Use Case:

Developers and release managers use this skill to turn local git history into concise App Store release notes that focus on user-visible changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or option-like revision arguments could affect git command behavior in the helper script.

Mitigation: Use normal commit or tag references when invoking the script, and avoid untrusted revision values until revision validation and quoted git arguments are added.

Risk: Generated release notes could include changes that are not actually user-visible.

Mitigation: Validate each bullet against the selected git range and omit internal-only work, duplicates, and overly technical wording.

## Reference(s):

- [App Store Release Notes Guidelines](references/release-notes-guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/dimillian/skills/app-store-changelog)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown bullet list with optional title and supporting shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Release notes should be concise, user-facing, deduplicated, and tied back to real changes in the selected git range.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
