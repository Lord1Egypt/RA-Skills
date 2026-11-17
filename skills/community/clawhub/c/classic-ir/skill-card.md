## Description:

Provides local lexical search over Markdown and text files with ranked results, optional query expansion, and ranking fusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gautham-ai-dev](https://clawhub.ai/user/gautham-ai-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users search local Markdown and text collections, expand queries, and combine ranked search results for first-pass retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Building an index or saving results can delete or overwrite an existing file at a user-chosen path.

Mitigation: Use dedicated index and output filenames in a safe working directory; confirm both paths before running.

Risk: Code files outside .md and .txt are not indexed despite the broader code-search description.

Mitigation: Check that the collection contains supported file types; use another search tool for other code files.

## Reference(s):

- [Classic IR on ClawHub](https://clawhub.ai/gautham-ai-dev/skills/classic-ir)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown command examples and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local, offline retrieval; indexing is limited to .md and .txt files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
