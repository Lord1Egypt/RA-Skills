## Description:

Platform-specific AI search optimization -- audit and optimize for Google AI Overviews, ChatGPT, Perplexity, Gemini, and Bing Copilot individually.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, SEO practitioners, and GEO teams use this skill to audit a target site's readiness across major AI search platforms and produce a prioritized platform-specific optimization report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests unrestricted shell access that is not needed for the stated audit and reporting workflow.

Mitigation: Remove Bash access or constrain shell use to explicit, reviewed commands before deployment.

Risk: The skill can create or overwrite GEO-PLATFORM-OPTIMIZATION.md.

Mitigation: Require user confirmation before writing or replacing the report file.

Risk: Platform-specific SEO and GEO recommendations may be incomplete or become outdated as AI search systems change.

Mitigation: Review recommendations against current platform behavior and source evidence before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/geo-platform-optimizer)
- [Publisher profile](https://clawhub.ai/user/asale-ai)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces GEO-PLATFORM-OPTIMIZATION.md with per-platform scores, gaps, and prioritized action items.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
