## Description:

AutoGLM Open Link opens a supplied web page through the AutoGLM Open Link API and returns extracted page text for downstream summarization, extraction, or analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfujian](https://clawhub.ai/user/flyfujian)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent builders can use this skill to fetch readable text from a URL before summarizing, extracting facts, or analyzing page content. It is suited to public web pages where sending the URL and retrieved content through AutoGLM is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs are sent to AutoGLM's external service and may reveal private, intranet, pre-authenticated, or secret-bearing links.

Mitigation: Use the skill only with links that are acceptable to send to AutoGLM; avoid private intranet URLs, pre-authenticated URLs, and URLs containing secrets.

Risk: The skill automatically retrieves and uses a bearer token from a localhost service.

Mitigation: Install and run it only when the local token service is trusted and scoped for the intended AutoGLM use.

Risk: The artifact includes an exposed app signing key used to generate request headers.

Mitigation: The publisher should remove or rotate the exposed signing key before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyfujian/skills/autoglm-open-link)
- [AutoGLM Open Link API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/open-link)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [JSON response containing extracted page text, typically converted by the agent into prose or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local bearer-token service on 127.0.0.1:53699 and sends submitted links to the external AutoGLM service.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
