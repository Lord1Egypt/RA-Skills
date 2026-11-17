## Description:

Analyzes 1688 merchant shop health across traffic, inquiries, transactions, products, customers, advertising, and risk, then produces a Chinese summary, an HTML data report, and prioritized follow-up action options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 merchants and their agents use this skill to run multi-shop operating health checks, compare recent business performance, identify risks, and select concrete optimization actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install unpinned packages.

Mitigation: Preinstall reviewed dependencies in a trusted environment and avoid runtime package installation.

Risk: Merchant access keys may be stored or forwarded with weak safeguards.

Mitigation: Protect or avoid plaintext access-key storage, restrict file permissions, and rotate the merchant key if exposure is possible.

Risk: A misconfigured OpenClaw gateway URL could send requests to the wrong local gateway.

Mitigation: Verify OPENCLAW_GATEWAY_URL points to the intended local OpenClaw gateway before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/skills/1688-shop-health-check)
- [1688aiinfra Publisher Profile](https://clawhub.ai/user/1688aiinfra)
- [Analysis Methodology](references/analysis-methodology.md)
- [CLI Command Reference](references/cli-commands.md)
- [Interaction Specifications](references/interaction-specs.md)
- [Wiki Routing Rules](references/wiki-routing-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown summary, JSON CLI results, interactive action cards, and an HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports multi-shop batch diagnostics and seven selectable diagnosis dimensions.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
