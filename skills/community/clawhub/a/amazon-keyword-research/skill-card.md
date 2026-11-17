## Description:

Amazon keyword research and market opportunity analysis for sellers, including autocomplete suggestions, competitor landscape analysis, and market opportunity assessment across 12 Amazon marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers, marketplace researchers, and ecommerce operators use this skill to collect keyword ideas, compare competitor landscapes, assess seasonality, and decide which Amazon keywords or product niches merit further investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted keyword may cause unintended local code execution in the bundled shell script.

Mitigation: Use only trusted keyword inputs for this version, review the script before execution, and prefer a fixed release that passes keyword values to Python as arguments.

Risk: Installation and network behavior are under-scoped for a normal release.

Mitigation: Avoid global installation unless needed, pin the install source, and review the network endpoints before deployment.

Risk: Keyword research may transmit user-entered keywords to third-party services.

Mitigation: Do not enter sensitive or confidential keywords, and disclose that keyword values may be sent to Amazon autocomplete, Google Trends, and web search providers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/amazon-keyword-research)
- [Google Trends Explore](https://trends.google.com/trends/explore)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include long-tail keyword groups, competition metrics, seasonal trend notes, opportunity scoring, and recommendations.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
