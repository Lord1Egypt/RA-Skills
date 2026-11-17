## Description:

Provides arXiv academic paper search, download, metadata export, and literature-summary workflows for agents conducting research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterkouss](https://clawhub.ai/user/peterkouss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research agents use this skill to query arXiv, download papers, transform metadata into citation formats, and generate paper summaries or literature overviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path handling can let crafted JSONL or metadata input write files outside the selected output directory.

Mitigation: Install and run in an isolated environment, avoid untrusted JSONL or metadata files until filenames and arXiv IDs are validated, constrain output paths, and review output directories before using overwrite behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peterkouss/skills/arxiv-search-master)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; generated artifacts may include JSON, PDF files, BibTeX, CSV, RIS, and summary JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes rate-limit controls, retry settings, output-directory options, and optional overwrite behavior.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
