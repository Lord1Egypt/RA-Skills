## Description:

Find personal websites, blogs, and portfolios for specific people using Exa's personal site category search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find and verify a person's personal website, blog, portfolio, or speaking page from Exa personal-site search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted names, affiliations, roles, handles, or locations could be inserted into shell command templates.

Mitigation: Pass search terms as structured Exa CLI arguments, or escape and reject shell metacharacters before execution.

Risk: The skill may read local product-marketing context files when present.

Mitigation: Review local context files before use and avoid including sensitive information that should not influence search behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-exa-personal-site-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with Exa CLI command examples and summarized search findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries include person name, site URL, site type, key content found, and visible last-updated information when available.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
