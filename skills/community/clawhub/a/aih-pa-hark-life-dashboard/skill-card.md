## Description:

Coordinates source-aware life dashboards and actionable drafts for subscriptions, travel changes, and personal expense review without claiming to be an official Hark product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and their assistants use this skill to organize subscription renewals, create a local life dashboard, track travel changes, and reconcile expenses. It provides reviewable files and action drafts, with external actions gated by explicit authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial, travel or identity information may be exposed during account connection or uploads.

Mitigation: Keep sensitive data in user-designated locations; do not request passwords, tokens, cookies, verification codes or full identity documents; review upload scope before approval.

Risk: A suggested cancellation, payment, deletion or public post may have unintended consequences.

Mitigation: Provide a reviewable draft or confirmation card first, and require explicit authorization for each external action.

Risk: Optional AI-HIVE use may incur charges or fail when tools or permissions are unavailable.

Mitigation: Confirm available tools, current pricing and a spending limit before use; deliver completed local work and disclose any unexecuted steps.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-hark-life-dashboard)
- [Hark Pro product introduction (comparison source)](https://hark.com/articles/introducing-hark-pro)
- [AI-HIVE user portal](https://ai-hive.iclip.cn/chat)
- [Skill output and verification contract](artifact/references/output-contract.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance, Files]

**Output Format:** [Reviewable drafts and Markdown guidance; optional CSV, iCalendar, HTML and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records source references, incomplete steps and review status; does not treat a draft as an executed external action.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
