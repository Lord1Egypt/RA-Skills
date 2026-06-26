## Description: <br>
Academic paper research workflow for searching, downloading, and analyzing arXiv papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjr-123456](https://clawhub.ai/user/yjr-123456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to find academic papers, retrieve PDFs or arXiv LaTeX source, and produce structured summaries from paper source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An embedded API key is present in the paper search helper. <br>
Mitigation: Remove the embedded key, require users to provide SEMANTIC_SCHOLAR_API_KEY, and rotate any exposed credential before use. <br>
Risk: Downloaded archives are extracted without path-safety checks. <br>
Mitigation: Run the skill in a constrained workspace, use trusted arXiv IDs, and add archive extraction checks that reject unsafe paths before deployment. <br>
Risk: Download and extraction helpers can write files to user-controlled or default local paths. <br>
Mitigation: Verify output directories before execution and restrict downloads and extracted source files to an approved workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yjr-123456/document-workflow) <br>
- [Output schema](artifact/references/output_schema.json) <br>
- [arXiv e-print source endpoint](https://arxiv.org/e-print/{id}) <br>
- [Semantic Scholar paper search API](https://api.semanticscholar.org/graph/v1/paper/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and structured JSON schemas or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts may write downloaded PDFs, extracted LaTeX source directories, or JSON output files when run.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
