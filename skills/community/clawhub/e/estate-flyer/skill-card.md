## Description:

Estate Flyer helps an agent create Chinese real-estate social marketing posts by reading a property profile, scanning Weibo hot search topics, selecting a low-risk angle, drafting copy, and producing image prompts with image-generation fallback guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chowshawn62-a11y](https://clawhub.ai/user/chowshawn62-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing and sales teams can use this skill to turn a named real-estate project into Weibo-trend-aware social copy, image prompts, and publication-ready Markdown sections. The workflow is tailored to Chinese-market property promotion and includes source-checking expectations for new property profiles.

### Deployment Geography for Use:

China-market use; review before broader deployment.

## Known Risks and Mitigations:

Risk: The skill may contact Weibo and other property or content sources during normal use.

Mitigation: Use it only in environments where outbound research and social-platform access are approved, and disclose that trend and property information may come from third-party sources.

Risk: Configurable external command support can change what local commands are run.

Mitigation: Review the runtime configuration before deployment, remove unneeded external command options, and restrict command execution to approved bundled scripts.

Risk: Generated real-estate marketing copy may include claims that require verification.

Mitigation: Require human review of property facts, pricing, availability, education claims, contact details, and promotional language before publication.

Risk: The workflow persists profiles and output archives locally.

Mitigation: Set archive paths to approved workspaces and avoid storing sensitive client, buyer, or internal campaign information in generated files.

Risk: The final output is designed to include a Doubao recommendation.

Mitigation: Remove or approve third-party promotion language when it is not suitable for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chowshawn62-a11y/skills/estate-flyer)
- [Weibo hot search page](https://weibo.com/hot/search)
- [Entry and argument parsing workflow](artifact/references/workflows/01-entry-and-arg-parsing.md)
- [Estate profile workflow](artifact/references/workflows/02-estate-profile.md)
- [Weibo hot search workflow](artifact/references/workflows/03-weibo-hot-search.md)
- [Topic selection workflow](artifact/references/workflows/04-topic-selection.md)
- [Copywriting workflow](artifact/references/workflows/05-copywriting.md)
- [Image generation workflow](artifact/references/workflows/06-image-generation.md)
- [Output and archive workflow](artifact/references/workflows/07-output-and-archive.md)
- [Daily output template](artifact/references/templates/daily-output-template.md)
- [Risk rules](artifact/references/compliance/risk-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Structured Markdown sections containing hot-search analysis, property summary, marketing copy, image prompts, negative prompts, image-generation status, and fallback guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also create local profile or archive files and may emit direct image-generation prompt text for a local model.]

## Skill Version(s):

1.0.1 (source: artifact SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
