## Description:

Turns a teacher-provided club activity script and authorized stills into separate short talking clips, one per still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and club advisors use this skill to plan and produce separate 2–15 second talking clips from their club activity script and stills they are authorized to use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package uses a shared, persistent Beatra device authorization with broad account access.

Mitigation: Review the requested scopes before approving, protect the local credential, and disconnect if that access is no longer acceptable.

Risk: The bundled client silently updates package files by default.

Mitigation: Review the automatic-update behavior and run `python3 scripts/mcp_client.py update --auto off` before use if unapproved changes are unacceptable.

Risk: Voice cloning and clip generation consume credits and may use a person's likeness or voice.

Mitigation: Confirm rights to the media and obtain separate approval for each priced clone, speech, and video stage.

## Reference(s):

- [ClawHub release](https://clawhub.ai/beatra-ai/skills/club-notice-talking)
- [Beatra skill homepage](https://beatra.ai/skills/club-notice-talking)
- [Activity-script talking workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [Markdown slot list and separate audio/video artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 2–8 separate clips, each 2–15 seconds; no stitching.]

## Skill Version(s):

0.2.0 (source: ClawHub release and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
