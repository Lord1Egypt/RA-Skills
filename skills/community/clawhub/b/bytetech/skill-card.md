## Description:

ByteTech helps an agent fetch ByteTech technical article metadata, directory context, summaries, and optional body text through an authenticated browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiushibang](https://clawhub.ai/user/qiushibang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to collect ByteTech article metadata, API-derived context, and selected article content for review, summarization, or technical research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse a live Chrome login session to access authenticated ByteTech and Feishu content.

Mitigation: Use an isolated Chrome profile with only the required ByteTech and Feishu accounts, and require explicit confirmation before fetching full Feishu document bodies.

Risk: Under-scoped browser and network tooling can inspect or save authenticated request details beyond a narrow article summary task.

Mitigation: Restrict runs to specific article IDs, avoid broad article-discovery prompts, pin the MCP package version, and confirm before inspecting or saving network responses.

## Reference(s):

- [ByteTech API Reference](artifact/references/api-reference.md)
- [ByteTech skill page](https://clawhub.ai/qiushibang/skills/bytetech)
- [ByteTech](https://bytetech.info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON excerpts, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include article metadata, article links, author details, engagement metrics, directory context, summaries, and fetched body text when the user has authorized access.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
