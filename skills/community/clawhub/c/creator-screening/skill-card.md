## Description:

Screens and evaluates social media creators using configurable quality frameworks, Memories.ai video analysis, profile metadata, transcript evidence, and scoring criteria for creator reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx)

### License/Terms of Use:


## Use Case:

Marketing, partnerships, and creator operations teams use this skill to vet Instagram, TikTok, and YouTube creators before approval decisions. It gathers profile and video evidence, analyzes content, applies screening frameworks, and generates per-creator verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creator URLs, profile metadata, captions, and transcript or video-analysis requests may be sent to Memories.ai and optionally Apify.

Mitigation: Use the skill only with data that may be shared with those services, and use dedicated least-privilege API keys.

Risk: The Apify fallback has a credential-handling weakness according to the authoritative security guidance.

Mitigation: Avoid the Apify fallback until token handling is fixed, or review and replace that path before use.

Risk: The included CAC Crusher framework contains biased rejection criteria that can affect real creator approval decisions.

Mitigation: Review or replace the framework criteria before using the skill for production creator screening decisions.

## Reference(s):

- [Creator Screening on ClawHub](https://clawhub.ai/shawnshenopeninterx/skills/creator-screening)
- [Publisher profile](https://clawhub.ai/user/shawnshenopeninterx)
- [Memories.ai API tools](https://api-tools.memories.ai)
- [Memories.ai V2 API base URL](https://mavi-backend.memories.ai/serve/api/v2)
- [CAC Crusher creator screening framework](references/frameworks/cac-crusher.md)
- [Default creator screening framework](references/frameworks/default.md)
- [Framework template](references/frameworks/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON creator screening reports with supporting shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PASS/FAIL/FLAG section scores, profile statistics, transcript excerpts, visual quality notes, red flags, and final creator verdicts.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
