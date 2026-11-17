## Description:

Automates separate logged-in Doubao browser profiles to generate and retrieve images and videos through a command-line workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to manage authorized Doubao browser sessions, submit image or video generation tasks, and download or recover resulting media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged-in browser profiles and recent conversations expose private account content.

Mitigation: Use a dedicated DOUBAO_HOME and authorized profiles without personal chats; restrict access to local profiles and downloads.

Risk: Browser and local process control can affect sessions or processes outside the intended task.

Mitigation: Limit automation to assigned profiles and ports, review commands, and stop only instances started for this workflow.

Risk: A linked payment flow and unpinned external installer may incur charges or introduce additional software.

Mitigation: Review any purchase or SkillPay step personally; do not run the external npm installer unless its separate tool is trusted.

Risk: Documented safety-filter workarounds may undermine platform safeguards.

Mitigation: Follow Doubao's usage policies and do not use prompt changes to evade content restrictions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lingyu9495-source/skills/doubao-account-pool)
- [Installation guide](INSTALL.md)
- [Image workflow](references/workflow-image.md)
- [Video workflow](references/workflow-video.md)
- [Stability and limits](references/stability-and-limits.md)
- [Known pitfalls](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Files]

**Output Format:** [Structured CLI status lines and locally saved image, video, and result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media and session state are stored locally; commands return brief status lines.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
