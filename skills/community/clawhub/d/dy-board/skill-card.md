## Description:

Read-only Douyin data access for keyword and creator searches, creator posts, individual work details, comments, and hot lists, returning structured JSON for comparison and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content teams, marketers, and analysts use the skill to compare public Douyin posts and creators, track trending topics, review comments, and identify content patterns or audience needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, Douyin links, or content and creator IDs may be sent to the third-party Guaikei service.

Mitigation: Review the service's use for your workflow and send only the public query terms or identifiers needed; avoid including private or sensitive information.

Risk: The security scan covered only 32 of 54 components, and runtime permissions were not verified.

Mitigation: Review the required Node.js runtime and GUAIKEI_API_TOKEN access, and inspect the release before installing it in a sensitive environment.

## Reference(s):

- [Skill usage and safety guidance](artifact/SKILL.md)
- [Output contract](artifact/references/contract.md)
- [Command options](artifact/references/options.md)
- [Environment and FAQ](artifact/references/faq.md)
- [Guaikei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results, with concise Markdown summaries when presented to the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be empty; request limits vary by plan. The skill documentation says queries send the relevant search terms, links, or IDs to the Guaikei service.]

## Skill Version(s):

1.5.1 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
