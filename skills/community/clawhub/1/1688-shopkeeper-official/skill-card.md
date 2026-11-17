## Description:

1688-shopkeeper helps agents search 1688 products, inspect product details, manage bound downstream stores, publish products, configure a 1688 AK, review opportunity and trend data, and generate shop operation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators and their agents use this skill to find 1688 merchandise, evaluate product and trend data, publish selected goods to connected stores, and receive shop operation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a sensitive 1688 AK to query shop data and publish products to connected stores.

Mitigation: Use a scoped or revocable AK, protect the OpenClaw config file, and verify the gateway URL before configuration.

Risk: Publishing products can modify connected downstream stores.

Mitigation: Run the dry-run check first and require explicit operator confirmation before any publish action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-shopkeeper-official)
- [1688 AI app setup](https://air.1688.com/kapp/1688-ai-app/pages/home?from=1688-shopkeeper)
- [Capability reference: search](artifact/references/capabilities/search.md)
- [Capability reference: publish](artifact/references/capabilities/publish.md)
- [Common error handling](artifact/references/common/error-handling.md)
- [Data contracts](artifact/references/common/data-contracts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command output with a human-readable markdown field and structured data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and a configured ALI_1688_AK for authenticated 1688 API operations.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact constants)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
