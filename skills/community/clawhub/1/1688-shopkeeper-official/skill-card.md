## Description: <br>
1688-shopkeeper helps agents search 1688 products, inspect product and shop details, publish selected products to connected downstream stores, configure the 1688 access key, review opportunity and trend signals, and generate shop operation reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External commerce operators and their agents use this skill to source products from 1688, manage connected stores, publish selected listings to supported downstream platforms, and review market or shop-operation signals. Developers and operators can also use its CLI commands for structured search, product-detail retrieval, configuration, and report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a 1688 access key and can access linked shop operations. <br>
Mitigation: Treat the AK like a password, avoid pasting it into chat, rotate it if exposed, and review where OpenClaw stores it before installation. <br>
Risk: The publish command can create or distribute listings to connected downstream stores. <br>
Mitigation: Run a dry-run first and require explicit final confirmation of the exact shop and products before formal publishing. <br>
Risk: Product research, product-detail, and publish workflows may create local snapshot files containing sensitive commerce data. <br>
Mitigation: Review or clear local snapshot files when product research, shop data, or publish activity is sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-shopkeeper-official) <br>
- [1688 AI App](https://air.1688.com/kapp/1688-ai-app/pages/home?from=1688-shopkeeper) <br>
- [Search capability guide](artifact/references/capabilities/search.md) <br>
- [Publish capability guide](artifact/references/capabilities/publish.md) <br>
- [Shop daily report guide](artifact/references/capabilities/shop_daily.md) <br>
- [Data contracts](artifact/references/common/data-contracts.md) <br>
- [Error handling](artifact/references/common/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses containing a success flag, human-readable Markdown, and structured data; agents typically present the Markdown and may add concise analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands save local product, product-detail, or publish snapshots for later reference; publishing is a write operation that should be preceded by dry-run validation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact constant) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
