## Description: <br>
Amazon Category Research helps Amazon sellers automate ASIN analysis, competitor research, and market intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuancheng888](https://clawhub.ai/user/yuancheng888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External Amazon sellers and operators use this skill to collect public or user-authorized Amazon, SellerSprite, and SIF data for category research, ASIN comparison, competitor analysis, and market assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill forces Feishu cloud document creation and local Markdown report storage, even when a user may not want cloud export or workspace backups. <br>
Mitigation: Install only when those outputs are acceptable, or modify the skill to require explicit confirmation and support chat-only or no-export workflows before use. <br>
Risk: The skill uses an OpenClaw browser profile and reads data visible through SellerSprite and SIF plugins. <br>
Mitigation: Use a dedicated browser profile, confirm plugin login state, and run the skill only for intended Amazon research tasks. <br>
Risk: The skill requests Feishu authorization and creates documents under the user's identity. <br>
Mitigation: Review requested authorization before granting access and revoke or narrow access if Feishu document creation is no longer needed. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [English README](README.en.md) <br>
- [Output Report Template](references/output-template.md) <br>
- [Negative Extraction Rules](references/negative-rules.md) <br>
- [DOM Selector Mapping](references/selectors.md) <br>
- [BSR Node ID Mapping](references/bsr-node-mapping.md) <br>
- [Input and Output Examples](references/examples.md) <br>
- [SellerSprite](https://www.sellersprite.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/yuancheng888/skills/amz-cat-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [Markdown reports, Feishu cloud documents, local Markdown backups, and short chat summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw browser profile, Amazon page access, SellerSprite and SIF plugin visibility for full data, and Feishu authorization for cloud document output.] <br>

## Skill Version(s): <br>
5.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
