## Description:

Blog Editorial Calendar helps an agent manage a blog publishing queue by selecting topics from a balanced backlog, scheduling posts into configured cadence slots, syncing with CMS state, and delegating writing and publishing to companion skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, indie hackers, and content teams use this skill to run a recurring long-tail SEO publishing cadence, keep topic clusters and post formats balanced, and avoid duplicate work by reconciling a local backlog with live CMS state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive companion publishing workflows that create drafts or scheduled CMS posts.

Mitigation: Review config.json, connected CMS credentials, and requested /blog-editorial-calendar commands before allowing publishing actions.

Risk: Publishing state depends on local backlog and published-index files matching the CMS.

Mitigation: Run sync before publishing, review any ambiguous or missing-post diff entries, and keep the writer adapter's publish locks enabled.

Risk: An empty backlog can trigger a refill workflow through blog-topic-research.

Mitigation: Require review of proposed refill candidates before they are appended to the queue.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/automatelab/skills/blog-editorial-calendar)
- [Publisher Profile](https://clawhub.ai/user/automatelab)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell or command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local backlog and published-index state files and may invoke companion publishing skills when used by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
