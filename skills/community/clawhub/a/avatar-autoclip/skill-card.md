## Description:

Turns an authorized portrait and script into a narrated avatar video with template-based editing, subtitles, and an optional cover image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to turn authorized portraits and narration into short avatar videos, or to assemble existing talking-head footage with templates and subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unapproved use of a person's likeness or voice, including voice cloning.

Mitigation: Obtain explicit consent for the portrait and voice; review any clone request as a sensitive voice-biometric action.

Risk: Public media URLs or exposed API keys may disclose private material or enable unauthorized spending.

Mitigation: Use short-lived private or signed media URLs, protect the API key, and avoid sharing private voice samples publicly.

Risk: Paid API usage may exceed the expected budget because budget safeguards are inconsistent.

Mitigation: Check current pricing and balance, preview requests with --dry-run, and monitor charges rather than relying on --budget as a hard cap.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/2253128/skills/avatar-autoclip)
- [API reference](references/api.md)
- [Usage and authorization guidance](references/通用说明.md)
- [A7W API and account portal](https://api.a7w.cn/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON task results]

**Output Format:** [Text and command examples with task results and generated-media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated videos are produced by an external paid API, not locally.]

## Skill Version(s):

1.0.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
