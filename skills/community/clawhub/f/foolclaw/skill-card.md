## Description:

FoolClaw is an OpenClaw prank skill that creates playful local desktop and browser pranks and can arm a quiet background operator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[treapgogo](https://clawhub.ai/user/treapgogo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use FoolClaw to run playful OpenClaw pranks such as desktop notes, browser taunts, video-link pranks, and light messaging pranks in environments they control. It is intended for consensual prank use where the operator controls affected devices, accounts, and channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Starting or arming the skill can schedule recurring background prank activity.

Mitigation: Use it only in controlled environments and confirm operators can disarm FoolClaw, inspect OpenClaw cron jobs, and reset generated state afterward.

Risk: Configured messaging channels may allow prank messages to be sent to other people without clear per-action consent.

Mitigation: Limit configured accounts and targets, require an explicit approved recipient before sending, and avoid user-identity assumptions unless the host capability clearly supports them.

Risk: Desktop files, browser pages, and video-link pranks can interrupt users or leave visible artifacts.

Mitigation: Run pranks only where visible disruption is acceptable, keep prank content obviously playful, and remove generated desktop or browser artifacts with the reset path when finished.

## Reference(s):

- [FoolClaw ClawHub Page](https://clawhub.ai/treapgogo/skills/foolclaw)
- [FoolClaw Project Homepage](https://github.com/TreapGoGo/fool-claw)
- [Local Pranks Catalog](references/local-pranks.md)
- [Friend Pranks Catalog](references/friend-pranks.md)
- [Social Media Pranks Catalog](references/social-media-pranks.md)
- [Creative Light Pranks Catalog](references/creative-pranks-light.md)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Markdown-style agent responses with inline shell commands; runtime actions may create text files, HTML pages, browser opens, and message drafts or sends.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node. OpenClaw cron, browser, and messaging capabilities affect background operator behavior and external prank paths.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
