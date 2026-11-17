## Description:

Guide a user through a compact two-step Chinese option flow for adult female portraits, generate two matched realistic images directly, then optionally create a video-ready character reference sheet from the first image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pddsa](https://clawhub.ai/user/pddsa)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn short Chinese portrait requests into guided choices, two realistic adult-female portrait images, and an optional character reference sheet for later video or motion-design preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a bundled Python usage gate that stores local counters and can block generation with an off-platform promotional unlock message.

Mitigation: Review the usage gate before installation and remove or clearly disclose quota, local state, and promotional contact behavior before normal use.

Risk: The skill is designed for adult female portrait generation and could be misused for underage or explicit requests.

Mitigation: Keep the documented refusal behavior for underage, school-age, sexualized youth, and explicit requests active in deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pddsa/skills/beauty-photo-generator)
- [Option Catalog](references/option_catalog.md)
- [Conversation Flows](references/conversation_flows.md)
- [Reference Sheet Prompt](references/reference_sheet_prompt.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Images, Shell commands]

**Output Format:** [Chinese conversational guidance with generated image outputs and JSON usage-gate responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces exactly two matched portrait images by default and can produce one optional character reference sheet.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
