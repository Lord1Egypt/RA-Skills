## Description:

Navigate Baidu Search, Maps, Baike, Wenku, and Qianfan with region-aware routing, official-source checks, and China-specific guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and teams use this skill to route Baidu-related requests across search, maps, knowledge, cloud, and Qianfan workflows while keeping mainland-versus-global assumptions and source quality visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Baidu-related searches, page requests, and product checks may send query text to Baidu services.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid sending secrets, credentials, tokens, customer data, or sensitive account details in chat.

Risk: Account-specific actions in Baidu Maps Open Platform, Baidu AI Cloud, Qianfan, or other Baidu consoles can affect resources, keys, billing, or permissions.

Mitigation: Keep account-level execution manual and require explicit user approval before any login, console change, key operation, billing action, or resource modification.

Risk: The skill can keep local Baidu workflow notes under ~/baidu.

Mitigation: Store only durable routing preferences, source notes, decisions, and approved account labels; do not store passwords, cookies, access keys, billing exports, or raw customer data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/baidu)
- [Baidu skill homepage](https://clawic.com/skills/baidu)
- [Baidu Search](https://www.baidu.com)
- [Baidu Baike](https://baike.baidu.com)
- [Baidu Wenku](https://wenku.baidu.com)
- [Baidu Maps](https://map.baidu.com)
- [Baidu Maps Open Platform](https://lbsyun.baidu.com)
- [Baidu AI Cloud](https://cloud.baidu.com)
- [Qianfan](https://qianfan.cloud.baidu.com)
- [Baidu Ecosystem Map](artifact/ecosystem-map.md)
- [Mainland Versus Global](artifact/mainland-vs-global.md)
- [Source Validation Ladder](artifact/source-validation.md)
- [Qianfan and Baidu AI Cloud](artifact/qianfan-cloud.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional inline shell commands and local configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Baidu workflow notes under ~/baidu when the user approves durable memory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
