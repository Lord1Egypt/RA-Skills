## Description: <br>
Use this skill when users need outfit advice or shopping suggestions for clothing, shoes, accessories, or bags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasontujun](https://clawhub.ai/user/jasontujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to receive personalized outfit, accessory, and shopping recommendations based on their profile, current need, and feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store style-profile details and user feedback in USER.md. <br>
Mitigation: Use it only when profile retention is acceptable, and review or remove stored profile details when they are no longer needed. <br>
Risk: The skill can visit configured shopping sites to gather product names, prices, images, and links. <br>
Mitigation: Review configured shopping sites before use and keep browsing limited to expected product discovery. <br>
Risk: The skill can create or update Feishu documents with recommendations and product images. <br>
Mitigation: Review document contents and image uploads before sharing, especially when recommendations include user profile details. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown recommendations with item links, optional image references, and Feishu document updates when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce up to three outfit recommendations and update a remembered style profile from user feedback.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
