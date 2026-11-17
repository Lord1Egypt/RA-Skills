## Description:

Fund Trading Clawhub helps agents use a simulated fund-trading CLI for account management, fund lookup, simulated subscription and redemption, asset review, and trade history checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weitom0902](https://clawhub.ai/user/weitom0902)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to interact with a fund simulation workflow that uses live fund net value and market data with virtual trading funds for learning, testing, and strategy practice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security evidence says the skill mishandles credentials and stores authentication material insecurely.

Mitigation: Use simulated or low-value credentials only, run the skill in an isolated environment, restrict access to local config files, and rotate any client secret that appears in logs or plaintext config.

Risk: The security guidance notes a contradiction between HTTPS configuration documentation and the code behavior.

Mitigation: Verify the exact package version and endpoint configuration before installation, and require HTTPS endpoints for any environment that is not local testing.

Risk: Users may mistake simulated trading for real-money trading because the skill uses live fund net values and market data.

Mitigation: Treat all transactions as virtual-fund simulations and confirm that no valuable production account or credential is connected before running trading commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weitom0902/skills/fund-trading)
- [PyPI package](https://pypi.org/project/fund-trading-skill/)
- [npm package](https://www.npmjs.com/package/fund-trading-skill)
- [Artifact homepage](https://github.com/weiqitong/fund-trading-skill)
- [Artifact support](https://github.com/weiqitong/fund-trading-skill/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include simulated account identifiers, OAuth token status, fund details, holdings, order records, and error messages from the configured API.]

## Skill Version(s):

1.0.2 (source: server release metadata, skill frontmatter, clawhub metadata, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
