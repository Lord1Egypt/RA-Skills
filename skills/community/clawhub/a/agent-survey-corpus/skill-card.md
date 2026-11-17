## Description:

Download a small corpus of open-access arXiv survey or review PDFs about LLM agents and extract text for style learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to create a local reference corpus of arXiv agent-survey PDFs and extracted text for studying survey structure, section sizing, comparison style, and evidence-backed writing patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence reports path handling weaknesses that can exceed the stated ref/ boundary when broader bundled tooling or untrusted inputs are used.

Mitigation: Review before installation, run only in an isolated workspace, and use trusted arXiv identifier files until path containment and arXiv ID validation are fixed.

Risk: The package bundles broader research-pipeline tooling in addition to the advertised arXiv PDF helper, and that tooling can create or modify many project files.

Mitigation: Limit normal use to the documented survey-corpus workflow and inspect planned file changes before running bundled pipeline machinery.

## Reference(s):

- [Agent Survey Corpus on ClawHub](https://clawhub.ai/willoscar/skills/agent-survey-corpus)
- [Publisher Profile](https://clawhub.ai/user/willoscar)
- [arXiv PDF endpoint](https://arxiv.org/pdf/)
- [arXiv API endpoint](https://export.arxiv.org/api/query?id_list={arxiv_id})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; generated local PDFs, text extracts, JSONL index records, and a Markdown style report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and network access to arXiv; PDF text extraction depends on readable PDF text and the configured page limit.]

## Skill Version(s):

1.0.0 (source: server release metadata; bundled SKILL.md frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
