## Description:

Searches arXiv papers by keyword, author, date, and category, then downloads PDFs, exports metadata, and generates summaries for literature review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterkouss](https://clawhub.ai/user/peterkouss)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to run literature searches, collect arXiv metadata, download papers, export citations, and summarize paper collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted JSON or JSONL inputs can cause JSON files to be written outside the chosen output directory.

Mitigation: Use trusted metadata and query files, run the skill in a scratch output directory, and review output paths before processing shared inputs.

Risk: Replacing existing downloaded or generated files may be unintended.

Mitigation: Keep the default skip-existing behavior and avoid --no-skip-existing unless replacement is intended.

Risk: Unpinned dependencies may change behavior across environments.

Mitigation: Pin dependencies in the execution environment before using the skill for repeatable workflows.

## Reference(s):

- [arXiv](https://arxiv.org/)
- [ClawHub skill page](https://clawhub.ai/peterkouss/skills/arxiv-master-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with CLI commands; runtime tools produce JSON, BibTeX, CSV, RIS, PDF, and summary JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to user-selected files and directories; supports rate limiting, retries, and logging.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
