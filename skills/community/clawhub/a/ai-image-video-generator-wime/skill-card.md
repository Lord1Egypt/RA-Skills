## Description: <br>
WIME AI ecommerce image-processing skill for uploading local images or using image URLs to remove backgrounds and generate AI product photography. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxiaolong98](https://clawhub.ai/user/liuxiaolong98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call WIME OpenAPI workflows for ecommerce images, including upload, background removal, transparent-asset cropping, and AI product photography generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The WIME authentication helper can print a response containing the user's WIME access token when run directly. <br>
Mitigation: Do not run or share output from scripts/wime_auth.py unless the token is removed or masked; keep WIME_ACCESS_TOKEN in a secret environment variable. <br>
Risk: The skill uploads user-provided local images and may process public image URLs through WIME. <br>
Mitigation: Avoid sensitive, private, customer, or unreleased product images unless WIME's data handling is acceptable for the use case. <br>
Risk: Misconfigured WIME_BASE_URL could send requests to an unintended endpoint. <br>
Mitigation: Keep WIME_BASE_URL pointed at the intended WIME endpoint and review any override before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liuxiaolong98/ai-image-video-generator-wime) <br>
- [WIME Website](https://wime-ai.com/) <br>
- [Image Upload API](references/upload-image.md) <br>
- [Background Removal API](references/cutout.md) <br>
- [Product Photography API](references/photo-shoot.md) <br>
- [Asset and Task Query API](references/asset-query.md) <br>
- [Global Error Codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets plus WIME result URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WIME_ACCESS_TOKEN and may upload user-provided images or process public image URLs through WIME.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
