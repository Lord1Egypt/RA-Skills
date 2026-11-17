## Description:

Runs a minimal test matrix for Alibaba Cloud Model Studio skills in this repo across image, video, audio, realtime speech, omni, visual reasoning, embedding, rerank, and editing capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to run one small validation request per Alibaba Cloud Model Studio sub-skill and record model, request, response, duration, and pass/fail evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses cloud credentials and can exercise media and voice-generation capabilities.

Mitigation: Use a least-privilege non-production API key in a disposable or low-privilege environment, and avoid sensitive prompts or personal media unless approved.

Risk: The reviewed artifact coordinates referenced Model Studio sub-skills that are not included in this artifact.

Mitigation: Review the referenced sub-skill instructions before use and run one bounded validation request first to confirm behavior.

Risk: Some tests may create remote artifacts or incur provider charges.

Mitigation: Confirm region, scope, and expected cost before execution, and record created artifacts for cleanup or review.

Risk: Saved evidence outputs may contain prompts, media details, response summaries, or environment information.

Mitigation: Keep evidence out of shared repositories and CI artifacts unless it has been reviewed and redacted.

## Reference(s):

- [Source list](references/sources.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown test report with command snippets and saved evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records capability, sub-skill, model, request summary, result summary, status, notes, and supporting artifacts under the configured output directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
