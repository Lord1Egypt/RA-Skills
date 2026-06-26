## Description: <br>
Loads reusable publication-channel strategy for layout, packaging, and publication-fit decisions for specific publication surfaces such as WeChat public accounts or Xiaohongshu, asking for the channel when it is missing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Editors, content strategists, and agents use this skill to adapt final content for a specified publication channel. It applies channel-specific rules for structure, packaging, scanability, visuals, and final checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Channel-specific guidance may be applied to the wrong publication surface if the channel is not confirmed first. <br>
Mitigation: Confirm the publication channel before final packaging and load the matching channel strategy reference. <br>
Risk: The WeChat reference includes a workflow-specific staging expectation for image embeds that may not match every publishing process. <br>
Mitigation: Review the channel reference files before use and confirm their publishing advice fits the local editorial workflow. <br>


## Reference(s): <br>
- [WeChat Public Account channel strategy](references/channels/wechat-public-account.md) <br>
- [Xiaohongshu channel strategy](references/channels/xiaohongshu.md) <br>
- [ClawHub skill release page](https://clawhub.ai/chaoyang78/editorial-channel-strategy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown or plain text editorial guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a publication channel before final packaging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
