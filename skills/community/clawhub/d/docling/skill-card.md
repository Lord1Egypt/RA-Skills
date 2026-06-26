## Description: <br>
Docling extracts and parses content from web pages, PDFs, DOCX, PPTX, and images into clean structured text through the docling CLI with optional GPU acceleration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Er3mit4](https://clawhub.ai/user/Er3mit4) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill when they already have a URL or local document and need Docling to produce clean text, Markdown, JSON, YAML, or HTML output instead of performing general web search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote-service options can send document contents to external endpoints. <br>
Mitigation: Avoid remote-service flags for private documents unless the endpoint and data handling are deliberately approved. <br>
Risk: External plugins can load third-party code during document processing. <br>
Mitigation: Use external plugin flags only with plugins from trusted sources and after reviewing their behavior. <br>
Risk: Docling writes output files to the current directory by default. <br>
Mitigation: Use a controlled temporary output directory and clean it up after reading the extracted content. <br>


## Reference(s): <br>
- [Docling CLI Reference](references/cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Docling output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the docling CLI; outputs are written to the current directory by default or to a controlled output directory when specified.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
