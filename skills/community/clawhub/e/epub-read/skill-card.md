## Description: <br>
Task-mode-driven EPUB reading and analysis skill with overview, targeted reading, chunked full reading, extraction, complex-content inspection, and batch processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inf-lucas](https://clawhub.ai/user/inf-lucas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and other external users use this skill to parse EPUB files, inspect structure, read selected chapters or chunks, extract structured information, and manage long-book reading progress without loading an entire book by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves extracted book content and reading progress on disk. <br>
Mitigation: Keep output directories private and delete generated artifacts when they are no longer needed. <br>
Risk: EPUB inputs may contain copyrighted, confidential, or otherwise restricted content. <br>
Mitigation: Parse only EPUB files the user is allowed to process. <br>
Risk: Python dependencies and integration tests execute locally. <br>
Mitigation: Install dependencies in a virtual environment and run integration tests only with the default temporary path or a dedicated disposable directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inf-lucas/epub-read) <br>
- [README](README.md) <br>
- [Sample usage](examples/sample_usage.md) <br>
- [ClawHub release notes](docs/CLAWHUB_RELEASE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and references to generated JSON and Markdown artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference local parsed EPUB artifacts, including metadata, table of contents, chapter files, chunks, reading index, complex-content reports, and session state.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
