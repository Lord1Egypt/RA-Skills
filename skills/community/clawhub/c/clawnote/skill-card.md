## Description: <br>
Review-first Xiaohongshu/Rednote content ops for OpenClaw. Use when creating a repeatable workflow for topic research, draft generation, Feishu review, exact-title approval, structured publish packages, and optional approved publishing after explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and content operators use this skill to run a review-first Xiaohongshu/Rednote workflow in OpenClaw, from topic research and draft preparation through Feishu review and optional exact-title publishing after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live publishing or deletion could affect a real Xiaohongshu account if run with the wrong account, toolkit, or target title. <br>
Mitigation: Keep publishing and deletion confirmation-based, verify the local toolkit and login state, and require exact-title confirmation before any live action. <br>
Risk: The workflow writes local draft, memory, and publish package files that may contain unpublished content or account preferences. <br>
Mitigation: Use an intended local workspace, review generated files before sharing, and configure Feishu review identifiers through the user's own environment. <br>
Risk: Cron-driven use can create repeated draft activity if scheduled incorrectly. <br>
Mitigation: Verify cron setup manually and keep default operation review-first rather than unattended live publishing. <br>


## Reference(s): <br>
- [Clawnote on ClawHub](https://clawhub.ai/zhangifonly/clawnote) <br>
- [Safety](docs/SAFETY.md) <br>
- [Publish Assist](workspace-template/PUBLISH_ASSIST.md) <br>
- [Tools](workspace-template/TOOLS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON draft packages and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review-first draft and publish-assist artifacts; live publishing requires explicit approval and exact title confirmation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
