## Description: <br>
AlphaShop Image helps agents call AlphaShop image-processing APIs for image translation, upscaling, object extraction, element detection and removal, cropping, virtual try-on, and model replacement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688AiInfra](https://clawhub.ai/user/1688AiInfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and commerce operators use this skill to prepare product imagery through AlphaShop services, including translation, enhancement, background or element editing, cropping, virtual try-on, and model-change workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends configured AlphaShop API credentials and submitted image URLs to AlphaShop's external service. <br>
Mitigation: Store keys in untracked secret configuration, monitor account usage, and submit only image URLs the user is authorized to share. <br>
Risk: Image-processing requests may include personal photos, OCR text, copyrighted material, watermarks, or other sensitive content. <br>
Mitigation: Confirm user authorization before submitting images, especially for personal, copyrighted, OCR, watermark-removal, or brand-related content. <br>
Risk: AlphaShop calls can fail when the account has insufficient balance or credits. <br>
Mitigation: Stop the workflow on balance or arrears errors and direct the user to replenish credits before continuing. <br>


## Reference(s): <br>
- [AlphaShop image API docs](references/api-docs.md) <br>
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management) <br>
- [AlphaShop API list and credits](https://www.alphashop.cn/seller-center/home/api-list) <br>
- [ClawHub skill page](https://clawhub.ai/1688AiInfra/alphashop-image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALPHASHOP_ACCESS_KEY and ALPHASHOP_SECRET_KEY; asynchronous workflows return task IDs that must be queried later.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
