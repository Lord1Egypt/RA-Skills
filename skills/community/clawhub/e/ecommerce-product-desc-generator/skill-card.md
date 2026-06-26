## Description: <br>
批量生成多平台电商产品标题、卖点和详情描述，支持中文英文及 CSV 导入，提升跨境及本土化文案效率。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ecommerce sellers and operations teams use this skill to generate platform-tailored product titles, bullet points, and product descriptions for Amazon, Taobao, Pinduoduo, TikTok Shop, and Shopify, including batch CSV workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CSV input may include unintended product data or the wrong file. <br>
Mitigation: Point the CSV option only at files intended for product-copy generation. <br>
Risk: A selected output path may overwrite an existing file. <br>
Mitigation: Choose output paths deliberately and keep backups for important generated content. <br>
Risk: Running the optional test suite in shared or CI environments may use an unpinned pytest version. <br>
Mitigation: Pin or update pytest before running tests in shared automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/ecommerce-product-desc-generator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/shenghoo123-png) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, CSV, Files] <br>
**Output Format:** [Markdown, plain text, or CSV product-description content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read product rows from CSV and can write generated output to a user-selected file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
