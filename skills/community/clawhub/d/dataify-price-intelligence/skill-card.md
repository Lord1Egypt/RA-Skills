## Description:

Compare product or service prices across multiple sellers, marketplaces, or official pricing pages and produce normalized price findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compare prices for a product or service across sellers, marketplaces, or official pricing pages and produce normalized, evidence-backed pricing findings for monitoring or decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Dataify as a third-party processor for pricing research and can retain raw results locally.

Mitigation: Use it only where third-party processing and local retention are acceptable, and review retained output before sharing it.

Risk: The evidence security summary flags unsafe API token handling.

Mitigation: Use low-privilege or short-lived API tokens where possible and rotate any token used with this release.

Risk: The release bundles non-price scraping or prospecting-related capabilities outside the stated price-only purpose.

Mitigation: Review bundled dependency skills before allowing broad or implicit invocation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-price-intelligence)
- [Publisher Profile](https://clawhub.ai/user/dataify-server)
- [Token Setup](_dependencies/skills/dataify-task-operations/references/token-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON reports and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May retain raw responses, hashes, state, and Markdown/JSON reports in the selected output directory.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
