## Description: <br>
Formats references for journal submission, converts between common citation styles, generates bibliographies for manuscripts, and checks reference formatting consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and academic writers use this skill to format citation text, convert APA, MLA, Vancouver, BibTeX, and unstructured references into AMA-style output, and prepare reproducible bibliography formatting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation describes a broader 1000-style reference-management API than the packaged CLI demonstrably exposes. <br>
Mitigation: Treat the release as an offline AMA citation converter and validate expected citation-style behavior with representative samples before relying on it for submission workflows. <br>
Risk: The documented Python API examples reference interfaces that may not match the packaged implementation. <br>
Mitigation: Use the CLI entry point at scripts/main.py until the publisher aligns the Python API documentation with the implementation. <br>


## Reference(s): <br>
- [AMA Citation Style Guide](references/ama-guidelines.md) <br>
- [Example Citations for Testing](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/citation-formatter-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with citation text, command examples, and optional CLI-generated output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI accepts a single citation, an input file, an optional output path, an input format selector, and interactive mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
