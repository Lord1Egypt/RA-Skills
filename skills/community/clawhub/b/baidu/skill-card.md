## Description: <br>
Navigate Baidu Search, Maps, Baike, Wenku, and Qianfan with region-aware routing, official-source checks, and China-specific guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and operators use this skill to route Baidu-related work across search, knowledge, maps, AI Cloud, and Qianfan surfaces while making region, language, source-quality, and approval assumptions explicit. <br>

### Deployment Geography for Use: <br>
Global, with explicit mainland China, Chinese-language, or cross-border assumptions stated for each non-trivial task. <br>

## Known Risks and Mitigations: <br>
Risk: Baidu queries and page requests can leave the local machine and may reveal research intent to Baidu-owned services. <br>
Mitigation: Avoid sending secrets or sensitive business data in queries; prefer official Baidu documentation for verification and use approved supporting sources only when needed. <br>
Risk: Optional local memory under ~/baidu/ could capture sensitive account, region, or project context if used carelessly. <br>
Mitigation: Store only durable non-secret preferences, source notes, approval boundaries, and decision records; do not store credentials, tokens, billing exports, or raw customer data. <br>
Risk: Account-level Baidu Maps, AI Cloud, Qianfan, key, resource, or billing actions can affect live services or costs. <br>
Mitigation: Require explicit user approval and correct account context before any console, key, cloud-resource, or billing action proceeds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/baidu) <br>
- [Skill homepage](https://clawic.com/skills/baidu) <br>
- [Baidu Search](https://www.baidu.com) <br>
- [Baidu Baike](https://baike.baidu.com) <br>
- [Baidu Wenku](https://wenku.baidu.com) <br>
- [Baidu Maps](https://map.baidu.com) <br>
- [Baidu Maps Open Platform](https://lbsyun.baidu.com) <br>
- [Baidu AI Cloud](https://cloud.baidu.com) <br>
- [Baidu Qianfan](https://qianfan.cloud.baidu.com) <br>
- [Baidu Ecosystem Map](artifact/ecosystem-map.md) <br>
- [Mainland Versus Global](artifact/mainland-vs-global.md) <br>
- [Source Validation Ladder](artifact/source-validation.md) <br>
- [Qianfan and Baidu AI Cloud](artifact/qianfan-cloud.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with occasional shell command blocks and local markdown file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain optional local markdown memory under ~/baidu/ when the user approves setup; does not require credentials for planning, research, or source verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
