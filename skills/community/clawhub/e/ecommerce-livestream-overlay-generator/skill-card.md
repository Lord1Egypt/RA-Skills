## Description: <br>
Generates ecommerce livestream visual overlay packages from brand, product, promotion, and optional product-photo inputs, including backgrounds, title banners, host persona images, pricing cards, product shelves, benefits bars, green-screen cutouts, composite previews, and packaged local deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoyuji12138](https://clawhub.ai/user/gaoyuji12138) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, ecommerce operators, and livestream production teams use this skill to create ready-to-deliver overlay assets for Taobao, Douyin, PDD, Kuaishou, and similar commerce streams. Developers or agents may also use it to generate prompts, API calls, local image-processing code, shell commands, and packaged output files for a complete livestream visual set. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brand, promotion, and optional product-photo data may be sent to Volcano Engine for image generation. <br>
Mitigation: Use the skill only with data suitable for that service, review the provider privacy terms, and avoid uploading sensitive or proprietary product images unless approved. <br>
Risk: The skill writes generated images and packaged deliverables to local output locations. <br>
Mitigation: Confirm the target output folder before delivery and inspect generated files before sharing them externally. <br>
Risk: Release evidence reports capability-metadata mismatches involving purchase and crypto authority. <br>
Mitigation: Do not grant purchase, payment, cryptocurrency, or blockchain authority for this skill unless the publisher corrects the metadata and the release is rescanned. <br>
Risk: The skill requires a Volcano Engine API key. <br>
Mitigation: Use a scoped or revocable API key through VOLCENGINE_ARK_API_KEY and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaoyuji12138/ecommerce-livestream-overlay-generator) <br>
- [Volcano Engine Ark Console](https://console.volcengine.com/ark) <br>
- [Volcano Engine image generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>
- [Volcano Engine privacy policy](https://www.volcengine.com/docs/6369/71845) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, API Calls, Files] <br>
**Output Format:** [Markdown guidance with prompts, JSON API request examples, Python snippets, shell commands, and local image files such as PNG, JPG, and ZIP outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOLCENGINE_ARK_API_KEY plus python3 and pip3; outputs are saved locally and may include seven fixed image deliverables and a packaged archive when supported.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
