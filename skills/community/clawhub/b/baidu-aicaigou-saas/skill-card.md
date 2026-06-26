## Description: <br>
百度爱采购 SaaS 通用运营技能，覆盖商品管理、素材管理、店铺运营、营销活动与数据查看等任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangmiemie99](https://clawhub.ai/user/yangmiemie99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Baidu AiCaigou merchants and operators use this skill to automate SaaS back-office workflows such as uploading product images, creating or editing product listings, and changing listing status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, edit, publish, unpublish, or batch-change live Baidu AiCaigou product listings. <br>
Mitigation: Require a clear preview and explicit user confirmation before create, edit, save, publish, up/down listing, overwrite, delete, or batch actions. <br>
Risk: The skill can upload local image files into a merchant account. <br>
Mitigation: Approve exact file paths before upload and confirm the target merchant account before starting browser automation. <br>
Risk: The skill may attempt to install Playwright CLI automatically when browser tooling is missing. <br>
Mitigation: Do not allow automatic package installation unless the user explicitly accepts the environment change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangmiemie99/baidu-aicaigou-saas) <br>
- [Material management workflow](artifact/capabilities/material-upload.md) <br>
- [Product management workflow](artifact/capabilities/product-management.md) <br>
- [Baidu AiCaigou material management](https://b2bwork.baidu.com/shop/material/index) <br>
- [Baidu AiCaigou product creation](https://b2bwork.baidu.com/product/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with step-by-step browser instructions and inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser automation steps, upload results, listing status, failure reasons, or manual fallback guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
