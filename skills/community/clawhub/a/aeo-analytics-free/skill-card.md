## Description:

Tracks AI visibility by scanning target prompts to measure whether a brand is mentioned and cited by AI assistants, storing scan history, trend data, competitor mentions, and recommended next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

External users, marketers, and SEO/AEO practitioners use this skill to track whether AI assistants mention or cite a brand for target prompts, analyze visibility trends, and identify content opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracked prompts and brand queries may be sent to Gemini or web search providers.

Mitigation: Avoid scanning secrets, personal data, regulated data, or confidential client material.

Risk: API keys can be exposed when placed directly in command-line URLs or shell history.

Mitigation: Use safer credential handling such as environment variables, keychains, or secret managers, and avoid logging full request URLs.

Risk: Local scan history can accumulate brand prompts, response excerpts, cited URLs, and competitor analysis.

Mitigation: Store the analytics JSON where only intended users can access it and review retained data before sharing reports.

## Reference(s):

- [AEO Analytics Data Schema](references/data-schema.md)
- [Using Gemini API with Grounding for AEO Analytics](references/gemini-grounding.md)
- [ClawHub Skill Page](https://clawhub.ai/psyduckler/skills/aeo-analytics-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports, JSON scan history, and shell or API call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends scan results to a local per-domain JSON history file and may query Gemini API or web search providers with user-supplied brand prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
