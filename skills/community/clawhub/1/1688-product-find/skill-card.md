## Description: <br>
Finds 1688 products from text, image, or link inputs, including similar-product search, bulk purchasing comparison, hot-sale and cross-border sourcing, and filters for price, sales, material, and attributes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sourcing teams use this skill to search 1688 for products, find same or similar items from images or links, compare candidate suppliers, and prepare purchasing research from API-returned product data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 1688 AK and stores credentials locally. <br>
Mitigation: Use a dedicated or least-privileged AK, avoid sharing secrets in chat, and clear or rotate credentials when they are no longer needed. <br>
Risk: CLI output, logs, and returned product data may include sensitive sourcing or credential-adjacent information. <br>
Mitigation: Treat command output and logs as sensitive and avoid pasting them into shared channels without review. <br>
Risk: The artifact includes automatic telemetry for completed CLI subcommands. <br>
Mitigation: Review the telemetry behavior before installation and confirm it is acceptable for the intended environment. <br>
Risk: The skill can support purchasing research and comparison workflows but does not handle payment, ordering, logistics, or inventory management. <br>
Mitigation: Use it only for product discovery and supplier comparison; route transaction and fulfillment actions through approved purchasing systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/1688-product-find) <br>
- [Publisher Profile](https://clawhub.ai/user/1688aiinfra) <br>
- [AK Portal](https://clawhub.1688.com/) <br>
- [Capability: text_search](references/capabilities/text_search.md) <br>
- [Capability: image_search](references/capabilities/image_search.md) <br>
- [Capability: link_search](references/capabilities/link_search.md) <br>
- [Capability: compare](references/capabilities/compare.md) <br>
- [Capability: configure](references/capabilities/configure.md) <br>
- [Common Error Handling](references/common/error-handling.md) <br>
- [Skill Telemetry Notes](references/skill埋点说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output with a markdown field containing product tables, status messages, and follow-up guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search commands require a 1688 AK and may return product identifiers, prices, supplier names, image URLs, detail links, and comparison tables.] <br>

## Skill Version(s): <br>
1.7.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
