## Description:

Generate, quote, monitor, retrieve, and cancel AI videos through the AI Video Maker API. Use when a user asks an agent to create text-to-video, image-to-video, frame-guided, or reference-guided video; estimate video cost before spending; check API setup or balance; resume an existing generation; or automate AI Video Maker workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[husu](https://clawhub.ai/user/husu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to check account setup, estimate video-generation costs, and create or manage AI video tasks through the AI Video Maker API. It guides the agent to obtain approval before paid generation and to return task status and the resulting video link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence because of privacy and permission-scope concerns, and the artifact review was incomplete.

Mitigation: Before installing, review how credentials, environment and shell access are used, and decide whether prompts or media may be sent to the external AI Video Maker service.

## Reference(s):

- [API Reference](references/api-reference.md)
- [Usage Examples](references/examples.md)
- [AI Video Maker service](https://aivideomaker.ai)
- [ClawHub skill listing](https://clawhub.ai/husu/skills/ai-video-maker)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Video links, Task status and cost details]

**Output Format:** [Markdown summaries and video URLs; workflow command output is JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video-generation requests can incur API credit charges; outputs include task identifiers and a video link with a 24-hour retention window.]

## Skill Version(s):

1.0.15 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
