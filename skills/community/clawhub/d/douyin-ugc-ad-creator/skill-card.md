## Description:

Create a Douyin shopping video, Douyin UGC ad, or AI creator product pitch from a product photo, product details, and an on-camera direction. This AI UGC ad creator composes a vertical presenter frame with the product, shapes a conversational hook and spoken recommendation, and delivers a short Douyin product video for launches, creator-style reviews, demonstrations, unboxings, and paid social creative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants, creators, and marketing teams use this skill to prepare and produce short vertical Douyin product ads from an inspectable product photo, merchant-supplied details, and on-camera direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports broad shared Beatra account access beyond the ad-creation purpose.

Mitigation: Review the shared credential scope before connecting, keep the Device Token private, and limit access to the shared connection.

Risk: The security review reports recurring installation telemetry.

Mitigation: Review the documented registration fields and privacy terms before installation; defer use if that reporting is not acceptable.

Risk: The security review reports that uninstall actions could affect other skills through shared connection state.

Mitigation: Use the bundled uninstall flow, check its remaining-skill decision, and do not remove shared Beatra state manually.

## Reference(s):

- [Beatra skill page](https://beatra.ai/skills/douyin-ugc-ad-creator)
- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/douyin-ugc-ad-creator)
- [Douyin UGC ad workflow](references/workflow.md)
- [Installation registration](references/installation-registration.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [Updates and security](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Video, Audio, Text, Guidance]

**Output Format:** [Vertical product-ad video with spoken narration and aligned JSON, SRT, and VTT subtitles when available.]

**Output Parameters:** [One vertical 9:16 clip; the default spoken pitch is 8–12 seconds.]

**Other Properties Related to Output:** [Product claims are limited to merchant-supplied details; the skill presents paid preparation and video generation as separately confirmed stages.]

## Skill Version(s):

0.3.1 (source: server-resolved release evidence and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
