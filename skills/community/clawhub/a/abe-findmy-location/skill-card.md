## Description:

Track a shared contact's location via Apple Find My with street-level accuracy. Returns address, city, and context (home/work/out) by reading map landmarks. Supports configurable known locations and SkillBoss API Hub vision fallback for unknown places.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve a shared Find My contact's approximate address, city, status, and home/work/out context from a macOS device with Find My access. It is most useful when an agent needs a structured location readout from an already-shared contact relationship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process the wrong shared contact.

Mitigation: Require explicit target verification before location lookup and confirm the selected contact before returning or uploading location data.

Risk: Full-screen Find My screenshots may expose sensitive location or account information.

Mitigation: Minimize screenshots to the required map region, delete temporary images after use, and avoid returning screenshot paths unless needed for review.

Risk: Screenshots may be uploaded to an external vision API when fallback analysis is used.

Mitigation: Ask for explicit consent before upload, disclose the external API use, and run without vision fallback when consent or SKILLBOSS_API_KEY is absent.

Risk: The Hammerspoon click helper can send UI clicks beyond the intended Find My flow.

Mitigation: Constrain the helper to the expected local endpoint and Find My window state, and disable it when reliable target selection cannot be confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-findmy-location)
- [peekaboo screen-reading CLI](https://github.com/steipete/peekaboo)
- [Hammerspoon](https://www.hammerspoon.org/)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Human-readable text or a JSON object containing contact, address, city, state, status, context, screenshot path, and vision fallback status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a local screenshot path and a needs_vision flag when external vision analysis was used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
