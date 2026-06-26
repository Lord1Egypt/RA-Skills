## Description: <br>
普通话与十一种中文方言双向对照查询技能。支持哈尔滨话、河南话、湖南话、天津话、北京话、上海话、广东话、东营方言、重庆方言、闽南话、大连话与普通话的日常词汇对照。适用于AI方言对话、跨方言沟通、方言文化研究、文案本地化。含13333条词汇库。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esnowxu](https://clawhub.ai/user/esnowxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Mandarin-to-dialect and dialect-to-Mandarin vocabulary across eleven Chinese dialects for dialogue, localization, cultural research, and communication support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud-sharing and synchronization features may send contributed vocabulary and contributor metadata to a Feishu bitable when enabled. <br>
Mitigation: Install the cloud features only when needed, set cloud_share.enabled deliberately, and review the Feishu app and table credentials before use. <br>
Risk: Credential access is required for Feishu and MiniMax-backed workflows, and the security guidance calls out an API-key fallback for review. <br>
Mitigation: Use scoped credentials, audit or remove fallback credential access before installation, and avoid enabling enrichment or sync workflows without credential review. <br>
Risk: Automated AI enrichment and prompt-like dataset rows may introduce inaccurate or misleading dialect entries. <br>
Mitigation: Review generated entries, clean prompt-like rows, and treat dialect data as reference material rather than authoritative language guidance. <br>
Risk: The bundled queue submission script includes hardcoded recipient and queue defaults. <br>
Mitigation: Review and replace recipient, queue, and app identifiers before using any MQ-triggered synchronization workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/esnowxu/fangyan-map) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text output with configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local dialect query results and optional setup guidance for local database and cloud sync workflows.] <br>

## Skill Version(s): <br>
1.0.32 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
