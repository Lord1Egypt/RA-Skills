## Description: <br>
Content Matrix Publisher helps agents discover trending topics, generate original social content, adapt it for Xiaohongshu and WeChat Official Accounts, and prepare or publish the resulting posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agent operators use this skill to turn one topic or source item into platform-specific Xiaohongshu notes and WeChat articles. It supports hot-topic discovery, content summarization, draft generation, image-assisted adaptation, optional publishing, and a final publishing report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured credentials, schedules, or webhook triggers can cause content to be posted to real social accounts. <br>
Mitigation: Keep dry-run or draft-only behavior enabled by default, disable scheduled and webhook triggers unless explicitly needed, and require manual approval before publication. <br>
Risk: Publishing integrations depend on platform credentials such as session cookies, app IDs, and secrets. <br>
Mitigation: Store credentials outside skill files, restrict access to them, and rotate or revoke them when they are no longer needed. <br>
Risk: Generated or adapted posts may violate platform rules, originality expectations, or sensitive-word policies. <br>
Mitigation: Review originality, sensitive terms, and platform compliance before any post goes live. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/content-matrix-publisher) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Workflow configuration](workflow.json) <br>
- [Xiaohongshu template](templates/xiaohongshu.md) <br>
- [WeChat template](templates/wechat.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON configuration, YAML configuration, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare drafts or publish to linked social accounts when publishing credentials and dependent skills are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, SKILL.md, workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
