## Description:

Summarizes long-form books in the user's preferred language at a verified 20 percent compression ratio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyxyz22](https://clawhub.ai/user/dannyxyz22)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, researchers, and agents use this skill to produce substantial summaries of plain-text books or Project Gutenberg texts while checking that the final summary stays between 18 percent and 22 percent of the original word count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads book text supplied by the user, which may include private or copyrighted content.

Mitigation: Use only source texts the user is permitted to share with the agent, and avoid providing sensitive material unless the environment is approved for it.

Risk: The workflow writes generated batch and summary files during splitting, aggregation, and validation.

Mitigation: Run the helper scripts in an intended working directory and review generated files before relying on or sharing them.

Risk: Large books may consume many tokens because the skill can summarize in multiple batches until the requested compression rate is met.

Mitigation: Estimate book size before starting and use batching for long texts so cost and context use remain visible.

## Reference(s):

- [Book summarizer ClawHub release](https://clawhub.ai/dannyxyz22/skills/book-summarizer)
- [Publisher profile](https://clawhub.ai/user/dannyxyz22)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary text with optional shell commands for counting, splitting, aggregating, and validating book summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 20 percent compression with an 18 percent to 22 percent accepted range; large books may require multiple batches and many tokens.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
