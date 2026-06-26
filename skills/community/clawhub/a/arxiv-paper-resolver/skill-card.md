## Description: <br>
arXiv Paper Resolver extracts arXiv paper structure, downloads PDFs, parses experimental HTML full text, and helps agents generate Chinese Markdown documents organized by the paper's own sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jin-liquor](https://clawhub.ai/user/jin-liquor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use this skill to resolve an arXiv ID or URL into local paper artifacts, section text, metadata, and a Chinese Markdown reading document suitable for agent-assisted paper review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads public arXiv content and writes paper files to the local filesystem. <br>
Mitigation: Install and run it in a virtual environment, and choose a non-sensitive output directory for generated paper artifacts. <br>
Risk: Paper text may be sent to an LLM or provider when the agent translates extracted sections. <br>
Mitigation: Translate only papers whose contents are acceptable to share with the selected model or provider. <br>
Risk: Python dependencies are specified as broad minimum versions. <br>
Mitigation: Pin or audit dependency versions before using the skill in controlled or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jin-liquor/arxiv-paper-resolver) <br>
- [README](artifact/README.md) <br>
- [Usage example](artifact/scripts/usage_example.md) <br>
- [arXiv](https://arxiv.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown with shell commands, generated text, JSON metadata, PDF files, and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local paper directories containing the downloaded PDF, metadata JSON, section structure text, raw section text files, and a Chinese Markdown document when the agent completes translation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
