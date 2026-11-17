## Description:

This skill helps generate and manage advertising creative content, including copy, marketing images, video materials, prompt optimization, result selection, and deduplication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeyeshield](https://clawhub.ai/user/jeyeshield)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and developers use this skill to create, inspect, cancel, select, rank, optimize, and deduplicate advertising creative generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled generation counts are not bounded, creating an availability risk.

Mitigation: Set a strict maximum generation count and enforce queue and concurrency limits before production use.

Risk: Cancellation does not stop scheduled work, so cancelled tasks may continue or emit completion events.

Mitigation: Make cancellation interrupt pending scheduled work and prevent completion events for cancelled tasks.

Risk: The release currently appears to use mock in-memory generation.

Mitigation: Validate production behavior and persistence requirements before using it for live advertising workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeyeshield/skills/ad-production-ai-generation)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON command responses with task identifiers, task status, generated result records, optimized prompts, suggestions, and short text messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation count, model, prompt, and optional task parameters are provided by the caller; no external binaries are required by the release metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
