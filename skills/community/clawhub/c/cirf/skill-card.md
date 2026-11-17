## Description:

Interactive crypto deep-research framework with human-AI collaboration for superior research outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kudodefi](https://clawhub.ai/user/kudodefi)

### License/Terms of Use:


## Use Case:

Developers, crypto researchers, and analysts use CIRF to run collaborative market, project, technology, tokenomics, sentiment, and content workflows. The skill guides an agent through structured research sessions that produce human-reviewed crypto research deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe workspace IDs or path-like project names could cause reads or writes outside the intended workspace folder.

Mitigation: Use simple workspace IDs with lowercase letters, numbers, and hyphens; add strict workspace ID validation, canonical path confinement, and confirmation before first writes.

Risk: The skill requires the agent to read local framework and workspace documents, use public web research, and write reports or workflow state locally.

Mitigation: Review the plain-text framework files before use, monitor generated files under workspaces/, and grant only the file and web access needed for the research session.

## Reference(s):

- [CIRF README](README.md)
- [Security & Permissions](SECURITY.md)
- [Framework Core Configuration](framework/core-config.yaml)
- [Research Methodology Guide](framework/guides/research-methodology.md)
- [Collaborative Research Guide](framework/guides/collaborative-research.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown research reports with YAML workspace and workflow configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local workspace files and research outputs under workspaces/ when activated by the user.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
