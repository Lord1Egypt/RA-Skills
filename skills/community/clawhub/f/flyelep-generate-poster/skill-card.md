## Description: <br>
Uses the Flyelep API to generate e-commerce product main images and detail-page poster images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and e-commerce operators use this skill to prepare Flyelep API requests for product hero images and product detail posters across cross-border and Chinese marketplace formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product descriptions, reference image URLs, and the Flyelep API key are sent to Flyelep. <br>
Mitigation: Use only product assets and prompts that are acceptable to share with Flyelep, avoid confidential inputs, and rotate the API key if it appears in logs or shared chats. <br>
Risk: Image generation can be long-running or fail because of invalid credentials, service concurrency, queueing, or request timeouts. <br>
Mitigation: Use 300-600 second request timeouts, handle 401 and 500 responses, check for empty data, and retry later when the service is busy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/flyelepai/flyelep-generate-poster) <br>
- [Flyelep poster generation API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies, curl examples, and generated image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include semicolon-separated image URLs returned by Flyelep; image generation requests can require 300-600 second timeouts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
