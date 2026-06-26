## Description: <br>
根据用户的海报和平面设计需求，调用创客贴智能设计 API 生成设计缩略图并展示给用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitlmt](https://clawhub.ai/user/hitlmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and designers use this skill to turn poster, invitation, social image, product poster, and banner prompts into Chuangkit-generated design previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Design prompts are sent to Chuangkit's external service. <br>
Mitigation: Do not include secrets, private personal data, unreleased campaign details, or confidential business information in prompts. <br>
Risk: The workflow opens a preview URL returned by the external service. <br>
Mitigation: Review returned URLs before opening them when operating in sensitive environments. <br>


## Reference(s): <br>
- [Chuangkit intelligent design API endpoint](https://gw.chuangkit.com/openplatform/intelligentDesign/api/generate) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [On a successful response, the agent opens the first returned imageUrl in the user's default browser.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
