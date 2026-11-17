## Description:

将用户提供的 HTML/前端原型整理成一个可复用的网页应用 skill，默认输出为静态 HTML，并支持最终用户自行填写 API URL、API Key 和模型配置来运行图片重设计流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to package an existing HTML/front-end prototype as a reusable static web app for AI book-manuscript image redesign. The generated app lets end users upload manuscript images, configure an image generation API endpoint, and export deployable static files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-side API key handling can expose credentials.

Mitigation: Use test or low-privilege API keys for evaluation, and prefer a backend proxy or server-side environment variable injection before real deployment.

Risk: Uploaded manuscript images and generated results are sent to the configured external API endpoint.

Mitigation: Avoid unpublished or sensitive manuscript images unless the endpoint is trusted, and enforce HTTPS for API calls and polling.

Risk: External API responses may include untrusted URLs or messages.

Mitigation: Validate result URLs, keep polling same-origin or explicitly trusted, and render API messages as text rather than HTML.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/ai-book-image-redesign)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and generated static HTML/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a static HTML image-redesign web app, Vercel configuration, and setup/export shell scripts.]

## Skill Version(s):

1.0.100 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
