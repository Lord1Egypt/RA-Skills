## Description: <br>
Helps agents search 1688 products, inspect product and shop data, review trends and business opportunities, generate shop daily reports, and publish selected products to downstream shops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyongzhen](https://clawhub.ai/user/chenyongzhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and shop operators use this skill to source products from 1688, compare product and trend signals, manage bound shops, and publish listings to supported commerce platforms through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses 1688-linked shop credentials and may prompt users to provide an AK during setup. <br>
Mitigation: Use a secure secret mechanism instead of normal chat where possible, and rotate any AK that has already been pasted into chat. <br>
Risk: The publish capability can create live downstream listings. <br>
Mitigation: Review before installing and require explicit confirmation before every publish action. <br>
Risk: Local 1688-skill-data snapshots may retain product, shop, or publishing data. <br>
Mitigation: Periodically clean up local 1688-skill-data snapshots. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chenyongzhen/1688-shopkeeper-bak) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Search capability guide](artifact/references/capabilities/search.md) <br>
- [Product detail capability guide](artifact/references/capabilities/prod_detail.md) <br>
- [Publish capability guide](artifact/references/capabilities/publish.md) <br>
- [Shop daily report guide](artifact/references/capabilities/shop_daily.md) <br>
- [Common error handling](artifact/references/common/error-handling.md) <br>
- [1688 AI app](https://air.1688.com/kapp/1688-ai-app/pages/home?from=1688-shopkeeper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output containing a success flag, human-facing markdown, and structured data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent is expected to show the markdown field first and use structured data for follow-up analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
