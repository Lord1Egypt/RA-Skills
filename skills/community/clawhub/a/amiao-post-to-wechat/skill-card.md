## Description: <br>
Editor-first WeChat Official Account publishing skill that helps prepare and post Markdown, HTML, plain-text articles, and image-text posts to WeChat Official Account via API or browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmxccc](https://clawhub.ai/user/tmxccc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, editors, and developers use this skill to polish, package, and publish WeChat Official Account content while checking formatting, metadata, images, and publish readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WeChat account credentials to publish content externally. <br>
Mitigation: Use only WeChat accounts you control, inspect the runtime before providing credentials, and require explicit confirmation before publishing. <br>
Risk: Turbo or auto-submit paths may reduce or bypass final user confirmation. <br>
Mitigation: Avoid Turbo and auto-submit modes until the workflow is trusted; keep confirm-before-publish enabled for normal use. <br>
Risk: Credential files, token caches, saved drafts, and publish logs may expose account or content information if stored in shared locations. <br>
Mitigation: Keep .env files, token caches, saved drafts, and publish logs out of shared or synced directories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/skills/amiao-post-to-wechat) <br>
- [Release Page](https://clawhub.ai/tmxccc/amiao-post-to-wechat) <br>
- [Configuration Reference](references/config-reference.md) <br>
- [Editorial Rules](references/editorial-rules.md) <br>
- [FSM Workflow](references/fsm.md) <br>
- [Quality Scoring](references/quality-scoring.md) <br>
- [Scripts CLI Reference](references/scripts.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [WeChat Official Account](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and concise prose with command snippets, configuration guidance, and publishing summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pre-publish summaries, quality scores, metadata suggestions, publish logs, and WeChat draft identifiers when the runtime supports publishing.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata; artifact frontmatter says 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
