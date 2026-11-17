## Description:

Compares product prices across Chinese ecommerce platforms and helps agents produce price, promotion, shipping, review, shop reputation, and purchase recommendation analyses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[birdme007](https://clawhub.ai/user/birdme007)

### License/Terms of Use:


## Use Case:

External users and shopping research agents use this skill to compare ecommerce prices, monitor price changes, and generate purchase recommendations from product names or links. Developers may also use the bundled JD scraper and comparison references as a starting point for price-analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence marks the release suspicious because the documentation overclaims broad platform support while the concrete implementation is JD-focused.

Mitigation: Validate platform coverage before relying on results, and treat non-JD platform workflows as guidance unless matching implementation is supplied.

Risk: Security evidence notes anti-bot evasion guidance and risky unpinned dependency installation commands.

Mitigation: Use official or permitted APIs where possible, avoid unauthorized proxy, IP-rotation, or CAPTCHA-bypass workflows, and install pinned dependencies in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/birdme007/skills/ecommerce-price-comparison)
- [Platform API notes](references/platform_apis.md)
- [Comparison logic](references/comparison_logic.md)
- [Report template](assets/template_report.md)
- [JD scraper README](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include price comparison tables, ranking scores, product recommendations, and scraper usage guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
