## Description:

Turn user-supplied drawing steps into one still per art demo page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Art teachers and lesson creators use this skill to turn user-supplied drawing steps into a labeled page plan and one classroom demonstration still per step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a reusable account credential shared with other Beatra tools, with permissions beyond image creation.

Mitigation: Prefer image-only authorization or an independently restricted account; revoke access in Beatra's console when finished, noting that removing one skill may leave the shared connection active.

Risk: User-selected media is uploaded to Beatra, and image generation can incur charges.

Mitigation: Upload only material suitable for Beatra and approve generation costs before creating images.

## Reference(s):

- [Art Demo Page on ClawHub](https://clawhub.ai/beatra-ai/skills/art-demo-set)
- [Beatra Art Demo Page](https://beatra.ai/skills/art-demo-set)
- [Art Demo Workflow](references/workflow.md)
- [Installation and Authentication](references/installation-and-auth.md)
- [Updates and Security](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Images, Text, Guidance]

**Output Format:** [A labeled page plan and one generated still image per approved art demo step]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation is performed only after the user approves the production details and cost.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
