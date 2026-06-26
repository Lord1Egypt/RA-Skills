## Description: <br>
Command-line tool to search, filter, and download arXiv papers by ID, author, category, or keyword without requiring API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to produce arXiv search and download commands for finding papers by keyword, author, category, or paper ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the wrong or unpinned PyPI package can reduce reproducibility or introduce unintended third-party code. <br>
Mitigation: Prefer pipx for isolation, verify the PyPI package name before installing, and pin the package version when reproducibility matters. <br>
Risk: Automated arXiv downloads can exceed expected service usage if run too aggressively. <br>
Mitigation: Follow arXiv usage terms and rate limits, and use download options such as destination folders and skip-existing behavior to avoid unnecessary repeated downloads. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/killgfat/arxiv-cli-tools) <br>
- [arxiv-cli-tools on PyPI](https://pypi.org/project/arxiv-cli-tools/) <br>
- [arxiv Python Client](https://pypi.org/project/arxiv/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key required; users should follow arXiv usage terms and rate limits.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
