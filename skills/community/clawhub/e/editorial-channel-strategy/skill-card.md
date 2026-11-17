## Description:

Load reusable publication-channel strategy for layout, packaging, and publication-fit decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Content authors and editorial agents use this skill to adapt final content structure, packaging, scanability, and publication-fit checks for WeChat public accounts or Xiaohongshu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the publication channel is missing or ambiguous, the agent could apply the wrong channel strategy.

Mitigation: Require the user or calling workflow to specify the active channel before final packaging or layout.

Risk: The WeChat guidance expects final articles to be staged in Obsidian with image embeds, which may not match every publishing workflow.

Mitigation: Review the staging expectation before use and adapt the final publication checklist to the user's actual toolchain.

## Reference(s):

- [WeChat Public Account Channel Strategy](references/channels/wechat-public-account.md)
- [Xiaohongshu Channel Strategy](references/channels/xiaohongshu.md)
- [Editorial Channel Strategy on ClawHub](https://clawhub.ai/chaoyang78/skills/editorial-channel-strategy)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance and channel-fit recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the publication channel to be specified before final packaging or layout work.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
