## Description:

Turns a user-supplied geography place table and authorized stills into a speakable place-fact clip for each still.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External educators use the skill to turn facts already printed in a geography place table, together with authorized still images, into short talking clips without inventing additional place facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra authorization grants broader account permissions than the geography-clip task requires.

Mitigation: Review the authorization prompt before approving, and revoke the device through the Beatra Console when access is no longer needed.

Risk: Selected images and voice samples receive external processing, and installation analytics are automatic.

Mitigation: Upload only material you are authorized to use, consider the external processing and analytics before installing, and avoid sensitive material.

Risk: Voice cloning, speech generation, and video generation are separate paid stages.

Mitigation: Review the live price and approve each paid stage and its complete segment count before submission.

## Reference(s):

- [Beatra skill page](https://beatra.ai/skills/geo-place-talking)
- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/geo-place-talking)
- [Place-talking workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Updates and security](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Text, Video]

**Output Format:** [Place-fact narration text and individual talking video clips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One clip per still; each clip is 2–15 seconds; the default pack contains three clips.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
