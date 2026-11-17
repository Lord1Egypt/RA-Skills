## Description: <br>
为待售船舶按船型、载重或容量、船龄及可选船旗匹配并评分真实求购买家。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linyihuang1992-ops](https://clawhub.ai/user/linyihuang1992-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ShippingClaw/OpenClaw users use this skill to match a seller's vessel against real buyer demand records by vessel type, capacity, age, and optional flag. It returns ranked buyer matches and buyer-demand details while filtering invalid records and avoiding paywalled or restricted contact data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Seller query details and user IDs can be submitted to a configured backend or queued locally when submission fails. <br>
Mitigation: Use a trusted backend URL, protect or clean the cache and outbox directory, and disclose/limit what seller data is submitted. <br>
Risk: The skill can use admin-level credentials when syncing demand records. <br>
Mitigation: Use a narrowly scoped service token instead of broad admin credentials and rotate it according to operational policy. <br>
Risk: The included FastAPI service can expose search and buyer-detail endpoints if bound broadly. <br>
Mitigation: Expose the service only behind appropriate access controls and avoid unauthenticated public deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linyihuang1992-ops/skills/find-buyer-for-vessel) <br>
- [Backend API reference](references/backend-api.md) <br>
- [Shipping Online purchase source](https://sp.sol.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown search summaries with linked result identifiers, JSON search/detail payloads, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cache status, manual-confirmation fields, demand-sync status, and public buyer-detail fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
