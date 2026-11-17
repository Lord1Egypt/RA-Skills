## Description:

Guides agents through Auto.dev automotive data tasks, including VIN decoding, vehicle listings, photos, specs, recalls, payments, interest rates, taxes, OEM build data, plate-to-VIN, CLI commands, MCP tools, and SDK methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryant22](https://clawhub.ai/user/bryant22)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to work with Auto.dev automotive data through MCP tools, CLI commands, SDK methods, or direct API calls. It supports vehicle lookup, listings search, VIN and plate workflows, pricing-aware API use, exports, and application scaffolding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated app or webhook examples can expose paid Auto.dev API usage if deployed without access controls.

Mitigation: Add authentication, authorization, rate limits, quotas, spend caps, strict input validation, and fail-closed secret checks before public deployment.

Risk: Install guidance includes unpinned npm and npx commands.

Mitigation: Pin and verify package versions before running global install or npx commands.

Risk: Direct API usage requires an Auto.dev API key and some endpoints process sensitive user inputs such as credit score, ZIP code, price, trade-in, and down-payment values.

Mitigation: Use OAuth-backed CLI or MCP flows when available, keep AUTODEV_API_KEY secret, request only required values, and avoid persisting or echoing sensitive inputs.

Risk: Plate-to-VIN lookup can identify a specific vehicle and may implicate privacy or misuse concerns.

Mitigation: Confirm the user has a legitimate purpose and do not run bulk plate lookups against plates the user did not supply.

Risk: Large or paid API batches can create unexpected charges.

Mitigation: Estimate cost before chains or batches, warn before high-cost endpoints, and ask for explicit confirmation when estimated cost exceeds the documented threshold.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bryant22/skills/auto-dev)
- [Auto.dev CLI, MCP, and SDK Documentation](https://docs.auto.dev/v2/cli-mcp-sdk)
- [Auto.dev API Documentation](https://docs.auto.dev/)
- [Auto.dev Pricing](https://auto.dev/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls, Files]

**Output Format:** [Markdown with inline commands, code blocks, tables, JSON or CSV export guidance, and generated project files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pricing-aware API guidance, plan requirements, export recommendations, and app scaffolding patterns]

## Skill Version(s):

1.1.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
