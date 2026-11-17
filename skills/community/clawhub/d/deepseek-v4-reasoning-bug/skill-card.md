## Description:

Troubleshoots DeepSeek V4-Pro API 400 errors caused by missing reasoning_content in multi-turn tool-call histories, with trigger conditions, reproduction steps, a temporary workaround, and OpenClaw fix tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[17329971](https://clawhub.ai/user/17329971)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose DeepSeek V4-Pro thinking-mode failures in OpenAI-compatible clients when multi-turn tool calls return 400 errors. It helps them confirm the trigger pattern, apply a minimal reasoning_content fallback, and track related OpenClaw fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the reproduction snippet with real prompts, tool outputs, or production credentials could expose sensitive information to the DeepSeek API.

Mitigation: Use test prompts, test tool outputs, and non-production credentials when reproducing the error.

Risk: The troubleshooting guide is written in Chinese, which may increase the chance of misapplying the workaround for teams that cannot review it confidently.

Mitigation: Install and use it only when the operator can understand the guide or has it reviewed by someone who can.

## Reference(s):

- [OpenClaw DeepSeek reasoning_content PR search](https://github.com/openclaw/openclaw/pulls?q=reasoning_content+deepseek)
- [OpenClaw PR #71105](https://github.com/openclaw/openclaw/pull/71105)
- [OpenClaw PR #71146](https://github.com/openclaw/openclaw/pull/71146)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, API Calls, Configuration instructions]

**Output Format:** [Markdown with diagnostic steps and Python API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes troubleshooting criteria, workaround guidance, and links to OpenClaw fix tracking.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
