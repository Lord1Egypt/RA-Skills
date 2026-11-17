## Description:

AutoGLM Toolkit helps agents use Zhipu AI services for browser automation, deep research, web search, image generation, image search, and web page content extraction, with emphasis on Chinese internet tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ye4wzp](https://clawhub.ai/user/ye4wzp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate AutoGLM-backed browser automation, research, search, image, and page-reading tasks to an agent. It is most relevant for workflows that need Chinese web coverage or Zhipu AI services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous browser automation can perform state-changing actions on logged-in sites, especially if sensitive-action auto-approval is enabled.

Mitigation: Keep auto_approve disabled unless the operator deliberately accepts the risk, and supervise posting, purchases, account changes, document edits, and similar actions.

Risk: Search terms, URLs, page contents, image prompts, and API credentials may be shared with the AutoGLM service.

Mitigation: Avoid submitting secrets or sensitive user data unless the deployment has approved data-sharing and credential-handling controls.

Risk: The security review flagged broad authority with limited safety scoping.

Mitigation: Review and scan the skill before deployment, scope tasks narrowly, and require human interaction for login or captcha flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ye4wzp/skills/autoglm-toolkit)
- [Zhipu AI](https://zhipuai.cn)
- [AutoGLM API base endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown summaries, structured reports, API examples, page extracts, image links, and browser-task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include screenshots, source links, generated-image URLs, and intermediate research findings depending on the capability used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
