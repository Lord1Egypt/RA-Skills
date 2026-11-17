## Description:

Retrieves Douyin video details, comments, profiles, posts, search results, suggested terms, and share-link IDs through a credit-based AI Data Platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to collect Douyin content and account data for product research, creator analysis, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign with medium confidence, and some local references could not be resolved.

Mitigation: Before installing, check that the declared tool capabilities and file writes fit your needs, and review the skill scope and output paths.

Risk: Data collection calls consume platform credits, so batch work can incur costs.

Mitigation: Check the current balance and interface prices before a batch, estimate its total cost, and stop if the available balance is insufficient.

Risk: The CLI stores an API key in a local configuration file after login.

Mitigation: Keep the key private and do not share terminal output containing it through public channels.

## Reference(s):

- [AI Data Platform](https://zlh.aidata366.com)
- [ClawHub release page](https://clawhub.ai/cuiyunhai/skills/douyin-data)

## Skill Output:

**Output Type(s):** [JSON data, Files, Shell commands, Guidance]

**Output Format:** [JSON responses and saved files, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports paged results; large responses can be saved to files.]

## Skill Version(s):

1.0.9 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
