## Description:

Task-mode-driven EPUB reading and analysis skill with overview, targeted reading, chunked full reading, extraction, complex-content inspection, and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inf-lucas](https://clawhub.ai/user/inf-lucas)

### License/Terms of Use:

MIT

## Use Case:

Developers and readers use this skill to parse EPUB files, inspect book structure, read targeted sections or chunks, extract structured information, review complex content, and plan batch processing without loading long books into context all at once.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validation helper can delete a caller-supplied output directory.

Mitigation: Run validation only with isolated throwaway output directories and do not pass existing important folders to test_integration.py --output-dir.

Risk: Parsing EPUB files from unknown sources may expose the agent environment to untrusted file content and parser dependency behavior.

Mitigation: Process unknown EPUB files in a locked dependency environment and review the generated outputs before using them in downstream work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inf-lucas/skills/epub-read)
- [Publisher profile](https://clawhub.ai/user/inf-lucas)
- [README](artifact/README.md)
- [Sample usage](artifact/examples/sample_usage.md)
- [ClawHub release notes](artifact/docs/CLAWHUB_RELEASE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands and structured reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can reference parsed EPUB artifacts such as metadata, TOC, chapter files, chunk files, reading index, session state, and complex-content reports.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
