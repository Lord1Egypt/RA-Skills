## Description:

Check whether a part fits a machine and where it is in stock, using the compatsy MCP servers for 3D printing and home espresso. Use for nozzle, hotend, build plate, filament, enclosure, tamper, puck screen, basket and portafilter fit and price questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elliot-rosen](https://clawhub.ai/user/elliot-rosen)

### License/Terms of Use:

MIT-0

## Use Case:

External users can check whether 3D printing or home espresso parts fit a specific machine and compare current stock and prices. The skill reports fit verdicts from the service and preserves unknown results with their missing fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Correction reports go to Compatsy and could contain personal or confidential information.

Mitigation: Keep personal and confidential information out of correction reports.

Risk: Purchase links are affiliate links and may earn Compatsy a commission.

Mitigation: Disclose the commission relationship when sharing a purchase link; the skill states the default link is the lowest in-stock price regardless of commission.

## Reference(s):

- [Compatsy](https://compatsy.com)
- [Compatsy 3D printing MCP](https://compatsy.com/3d-printing/mcp)
- [Compatsy home espresso MCP](https://compatsy.com/home-espresso/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Markdown product-fit and price guidance, optionally with a comparison table and purchase links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fit verdicts include the rule ID; unknown results include missing fields. Prices include merchant and verification time. Purchase links may be affiliate links.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
