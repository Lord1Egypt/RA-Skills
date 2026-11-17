## Description:

Command-line tool to search, filter, and download arXiv papers by ID, author, category, or keyword without requiring API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and technical users can use this skill to install and operate an arXiv command-line interface for searching papers, filtering results, and downloading selected papers from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned PyPI package can introduce supply-chain drift between reviews.

Mitigation: Install with pipx when possible and pin or review the PyPI package version when stricter supply-chain control is required.

Risk: Running installation commands with elevated privileges can expand the impact of a compromised dependency.

Mitigation: Avoid administrator privileges for installation unless the environment explicitly requires them.

Risk: Automated paper searches and downloads can exceed service expectations if used too aggressively.

Mitigation: Follow arXiv usage terms and rate limits when using generated commands.

## Reference(s):

- [arxiv-cli-tools PyPI project](https://pypi.org/project/arxiv-cli-tools/)
- [arxiv Python client](https://pypi.org/project/arxiv/)
- [ClawHub skill page](https://clawhub.ai/killgfat/skills/arxiv-cli-tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install commands, CLI usage examples, option explanations, and operational guidance.]

## Skill Version(s):

0.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
