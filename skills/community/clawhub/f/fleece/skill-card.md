## Description:

Credit card research and redemption CLI. Looks up rewards rates, annual fees, welcome bonuses, statement credits, transfer partners, point valuations, application rules, lounge access, and travel protections for Chase, Amex, Citi, Capital One, Bilt, and all major US issuers. Compare cards, analyze wallet gaps, estimate ROI, get recommendations, look up merchant category codes, and search award flights and hotels. Install with pip install fleece-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyuan99](https://clawhub.ai/user/chenyuan99)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use Fleece to research US credit cards, compare rewards and benefits, analyze wallet gaps and first-year value, and generate award travel search URLs. Research commands can use live Brave Search data, while some profile, MCC, and redemption URL workflows run offline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved spending profile and wallet details may be included in live research workflows and sent to external services.

Mitigation: Store only the minimum profile details needed, avoid highly personal goal or preference text, and review saved profile values before running live research commands.

Risk: API keys and the Streamlit interface can increase exposure if configured casually or made available to untrusted users.

Mitigation: Use an isolated virtual environment, provide BRAVE_API_KEY through a protected environment variable or .env file, and avoid exposing the Streamlit interface unless URL fetching and access controls are hardened.

## Reference(s):

- [Fleece on ClawHub](https://clawhub.ai/chenyuan99/skills/fleece)
- [Fleece CLI on PyPI](https://pypi.org/project/fleece-cli/)
- [Fleece website](https://getfleece.io/)
- [README](README.md)
- [Fleece design notes](docs/DESIGN.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research commands may require BRAVE_API_KEY; profile, MCC lookup, and PointsYeah URL generation workflows can run without a Brave API key.]

## Skill Version(s):

1.6.1 (source: server release metadata; artifact frontmatter reports 1.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
