## Description:

Generate music, sound effects, and ambience from text prompts through Luxin, returning WAV audio with a hosted URL and recoverable job details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgwilson](https://clawhub.ai/user/danielgwilson)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask an agent to create music, sound effects, or ambience from a text prompt. The skill returns hosted WAV audio with a recoverable job ID and cost receipt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feedback can include private task details, prompts, or diagnostic results.

Mitigation: Review and redact feedback before sending it.

Risk: Anyone who obtains a hosted audio link can access the audio.

Mitigation: Treat hosted audio links as shareable access and limit who receives them.

Risk: The supplied review did not verify the downloaded CLI or hosted service implementation.

Mitigation: Use reviewed, pinned package and skill revisions, isolate installation state, and set a spending limit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielgwilson/skills/ai-audio-generation)
- [Luxin homepage](https://luxin.sh)
- [Luxin agent guidance](https://luxin.sh/llms.txt)
- [Luxin skill contract](https://luxin.sh/skill.md)
- [Luxin full skill guidance](https://luxin.sh/skill-core.md)
- [Luxin CLI contract](https://luxin.sh/cli.md)
- [Luxin hosted API](https://api.luxin.sh)

## Skill Output:

**Output Type(s):** [Audio files, URLs, JSON]

**Output Format:** [WAV audio with a hosted media URL, job ID, and cost receipt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hosted media links have no signature or expiry; jobs can be re-fetched by ID.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
