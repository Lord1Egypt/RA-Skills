## Description:

Routes sections of an explanation to suitable formats and can produce an interactive, offline HTML page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dotpopo](https://clawhub.ai/user/dotpopo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can use the skill to explain concepts, processes, architectures, and comparisons in a format suited to each section, either in chat or as an offline interactive page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted project settings may run code or expose secrets.

Mitigation: Use the CLI only in trusted projects or a sandbox without unrelated credentials, and review user and project configuration before running it.

Risk: Local routing does not disable plugins.

Mitigation: Review plugin configuration and do not treat local routing as a plugin safety boundary.

Risk: Private material may be exposed through embedded files or agent-wide hooks.

Mitigation: Check embedded files before sharing private material and avoid agent-wide hooks until file boundaries, temporary-file handling, and log privacy are improved.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, HTML, JSON]

**Output Format:** [Markdown responses, standalone interactive HTML pages, or JSON intermediate representation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pages can include diagrams, tables, sliders, tabs, and step-by-step views.]

## Skill Version(s):

0.4.1 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
