## Description:

Search and download research papers from arXiv.org for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search arXiv papers by query or category, inspect paper metadata, and download selected PDFs for research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party arxiv Python package.

Mitigation: Install the dependency in a virtual environment and review the package source and version before use.

Risk: The download command contacts arXiv and writes PDF files to the local Downloads/arxiv folder.

Mitigation: Run the skill in an approved environment and confirm the intended arXiv ID before downloading.

Risk: arXiv papers may be preprints that have not been peer reviewed.

Mitigation: Validate important claims against authoritative or peer-reviewed sources before relying on them.

## Reference(s):

- [arXiv](https://arxiv.org)
- [ClawHub Skill Page](https://clawhub.ai/nantes/skills/arxiv-research)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files]

**Output Format:** [Markdown text with inline shell commands and Python snippets; PDF files may be downloaded when the skill is invoked.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output includes titles, summaries, authors, publication dates, categories, PDF URLs, and arXiv IDs.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter; artifact _meta.json lists 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
