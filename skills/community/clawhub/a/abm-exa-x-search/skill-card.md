## Description:

Search Twitter/X for tweets, discussions, and sentiment on topics, people, or brands using Exa's tweet category search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Twitter/X with Exa's tweet category, then summarize relevant tweets, sentiment patterns, notable voices, themes, trends, and actionable insights for a brand, person, product, or topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command templates can turn an untrusted search topic into local shell execution if followed literally.

Mitigation: Pass search topics as safe process arguments and avoid interpolating untrusted topics into shell strings.

Risk: The skill may read a local product-marketing context file and use that context in the search workflow.

Mitigation: Review local marketing context before use and avoid including sensitive or irrelevant information in files the skill reads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-exa-x-search)
- [ClawHub publisher profile](https://clawhub.ai/user/mariokarras)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tweet summaries, sentiment synthesis, actionable insights, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Exa CLI search and contents commands, dry-run commands, sentiment labels, key themes, notable voices, and conversation trend assessments.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
