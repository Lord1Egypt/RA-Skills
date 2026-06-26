## Description: <br>
Search and download research papers from arXiv.org - Research skill for OpenClaw agents <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and research-focused agents use this skill to search arXiv, filter papers by category, retrieve paper metadata, and download selected PDFs for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external arxiv Python package. <br>
Mitigation: Install dependencies from trusted package indexes and review dependency provenance before use in controlled environments. <br>
Risk: Downloaded PDFs are files from the internet and are saved locally by default. <br>
Mitigation: Review downloaded PDFs with normal file-safety practices and change the download location when local storage policy requires it. <br>


## Reference(s): <br>
- [arXiv](https://arxiv.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python examples; command output is plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches rely on the external arxiv Python package, and downloads save PDFs under ~/Downloads/arxiv by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
