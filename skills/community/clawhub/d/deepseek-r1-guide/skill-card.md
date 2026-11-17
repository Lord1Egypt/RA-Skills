## Description:

DeepSeek AI development assistant for DeepSeek API integration, model selection, inference optimization, and local deployment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose DeepSeek models, integrate the DeepSeek API, draft Python, Node.js, and curl examples, and plan local deployment options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API examples send prompts and API keys to a third-party DeepSeek endpoint.

Mitigation: Avoid secrets and regulated data in prompts, store real API keys outside shell history, and review third-party provider terms before use.

Risk: Local deployment examples include package installation and model-serving commands.

Mitigation: Pin and verify packages such as `vllm`, run deployments in a virtual environment or container, and review commands before production use.

Risk: Pricing, model capabilities, and hardware guidance can become outdated.

Mitigation: Validate cost, model, and hardware recommendations against current DeepSeek and deployment documentation before relying on them.

## Reference(s):

- [DeepSeek API base URL](https://api.deepseek.com)
- [DeepSeek chat completions endpoint](https://api.deepseek.com/chat/completions)
- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/deepseek-r1-guide)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party API examples, model-selection guidance, local deployment commands, and cost-oriented recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
