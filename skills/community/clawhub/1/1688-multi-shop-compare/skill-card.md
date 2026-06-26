## Description: <br>
1688 Multi Shop Compare analyzes bound 1688 shops across shop, category, and product levels to produce comparative rankings, product diagnostics, anomaly attribution, opportunity identification, and item-level recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External 1688 merchants and operations agents use this skill to compare multiple bound shops, diagnose performance differences, and identify concrete product-level actions. It is intended for multi-shop business analysis where the agent can access authorized 1688 shop credentials and operating data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires 1688 access keys and can access shop performance data and customer details. <br>
Mitigation: Install it only when the publisher and runtime are trusted, and keep the OpenClaw configuration file protected. <br>
Risk: Configuration may be written through an OpenClaw gateway endpoint. <br>
Mitigation: Use only a trusted gateway and do not set OPENCLAW_GATEWAY_URL to an untrusted endpoint. <br>
Risk: Generated reports may include sensitive shop, product, and customer business information. <br>
Mitigation: Review reports before sharing them outside the authorized business context. <br>
Risk: The workflow may hand off item-level optimization actions to downstream optimizer skills. <br>
Mitigation: Review any downstream optimizer skill separately before allowing listing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-multi-shop-compare) <br>
- [Publisher profile](https://clawhub.ai/user/1688aiinfra) <br>
- [Interaction specs](artifact/references/interaction-specs.md) <br>
- [Visualization rules](artifact/references/visualization-rules.md) <br>
- [Anti-patterns](artifact/references/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON command outputs and interactive card data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include shop comparisons, rankings, product diagnostics, anomaly actions, and configuration status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
