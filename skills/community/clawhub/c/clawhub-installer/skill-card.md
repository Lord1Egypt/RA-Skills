## Description:

Searches, filters, and installs the most appropriate ClawHub skills for the current task, including version-specific installation and post-install verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxiaofeng44](https://clawhub.ai/user/zhaoxiaofeng44)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill when a task requires finding and installing a suitable ClawHub skill, selecting from recommended candidates, optionally pinning a version, and verifying installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unreviewed third-party skill can change agent behavior in ways the user did not intend.

Mitigation: Check the publisher, exact version, permissions, and artifact contents before installation; pin a reviewed version for sensitive work.

Risk: Bulk updates can introduce changed skill behavior without per-skill review.

Mitigation: Avoid bulk updates unless each updated skill has been reviewed.

## Reference(s):

- [ClawHub Installer release page](https://clawhub.ai/zhaoxiaofeng44/skills/clawhub-installer)
- [ClawHub publisher profile: zhaoxiaofeng44](https://clawhub.ai/user/zhaoxiaofeng44)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends up to three candidate skills by default, then provides install and verification commands after user confirmation.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
