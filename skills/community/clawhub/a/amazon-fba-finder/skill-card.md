## Description:

Amazon FBA Finder helps Amazon sellers evaluate product opportunities, market competition, supplier options, and FBA profit scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce operators use this skill to screen FBA product ideas, compare competitive signals, evaluate supplier fit, and estimate unit economics before making sourcing or launch decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides financial and product-launch recommendations that may be inaccurate, stale, or incomplete.

Mitigation: Treat recommendations as decision support; independently verify market data, FBA fees, policy constraints, and supplier terms before spending money.

Risk: The skill expects API keys and third-party dependencies.

Mitigation: Install in a virtual environment, pin or review dependencies before use, and keep real API keys in environment variables or private secret storage.

Risk: Product discovery and supplier search paths appear partially stubbed in the artifact.

Mitigation: Verify live data integrations and end-to-end behavior before relying on paid product claims or operational recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/skills/amazon-fba-finder)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [package.json](package.json)
- [clawhub.json](clawhub.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, configuration snippets, and structured analysis outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision-support outputs should be reviewed against current Amazon fees, marketplace policy, supplier data, and the user's own due diligence.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, clawhub.json, and artifact __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
