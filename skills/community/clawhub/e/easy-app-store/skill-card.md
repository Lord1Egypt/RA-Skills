## Description:

Automates iOS App Store releases by inspecting projects, preparing builds, completing App Store Connect listings, submitting versions for review, and checking review or publication status through Easy WebBridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers use this skill to prepare and publish iOS apps through App Store Connect, including build uploads, listing and compliance details, review submissions, status checks, and rejection follow-up. It requires Easy WebBridge and a browser already signed in to App Store Connect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation instructions use an unpinned npx skills command, and the security scan could not fully assess all referenced content.

Mitigation: Inspect the package and referenced script and test before installation; use a pinned version or verified release when available, and review commands before running them with account privileges.

## Reference(s):

- [Easy WebBridge repository (runtime)](https://github.com/xxjrq/easy-webbridge)
- [EasyBR official download page](https://www.ebrower.com/down.html)
- [EasyBR GitHub release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Files]

**Output Format:** [Markdown status summary and guidance, with project-specific commands and release files as applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies with the iOS project and requested release stage; may include a built IPA and store assets.]

## Skill Version(s):

0.2.3 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
