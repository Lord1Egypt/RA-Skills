## Description:

Helps sellers turn selected Douyin comment objections and authorized still images into short, spoken demo clips, one clip per still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers use this skill to plan responses to public Douyin objections, generate approved narration, and produce separate short talking demo clips from still images. It can use pasted comments when live comment lookup is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared local Beatra Device Token grants broad access to the connected account.

Mitigation: Authorize only if comfortable with this access; keep the token private and use the bundled disconnect workflow when removing access.

Risk: Approved lookups and media generation can consume Beatra credits.

Mitigation: Review live prices and confirm each paid stage before submitting; check the reported final charge.

Risk: The client sends limited installation telemetry and silently installs package updates by default.

Mitigation: Review these behaviors before installation and disable automatic updates with the documented update command if unwanted.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/douyin-comment-to-demo-clip)
- [Beatra skill page](https://beatra.ai/skills/douyin-comment-to-demo-clip)
- [Douyin comment-to-demo workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Video clips]

**Output Format:** [Markdown plans and task reports with separate audio and video artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 2–8 separate clips; video segments are 2–15 seconds and are not stitched together.]

## Skill Version(s):

0.1.8 (source: server-resolved ClawHub release and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
