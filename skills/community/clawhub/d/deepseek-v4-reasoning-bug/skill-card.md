## Description: <br>
Helps diagnose DeepSeek V4-Pro tool-call failures caused by missing reasoning_content in multi-turn thinking-mode message replay, including trigger conditions, reproduction steps, a temporary workaround, and OpenClaw fix tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[17329971](https://clawhub.ai/user/17329971) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to recognize and troubleshoot DeepSeek V4-Pro thinking-mode HTTP 400 errors in OpenAI-compatible clients when multi-turn tool-call histories omit the reasoning_content field. It guides them toward checking request history, applying a minimal fallback, and verifying whether their client version already includes a fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The linked PR status and workaround may become outdated as DeepSeek or OpenClaw behavior changes. <br>
Mitigation: Verify the current DeepSeek API behavior, OpenClaw PR status, and client version before making production changes. <br>
Risk: Applying the workaround without reviewing message history could mask a different API, authentication, or client integration issue. <br>
Mitigation: Confirm the exact error message and the presence of multi-turn tool-call history before adding a reasoning_content fallback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/17329971/deepseek-v4-reasoning-bug) <br>
- [OpenClaw DeepSeek reasoning_content PR search](https://github.com/openclaw/openclaw/pulls?q=reasoning_content+deepseek) <br>
- [OpenClaw PR #71105](https://github.com/openclaw/openclaw/pull/71105) <br>
- [OpenClaw PR #71146](https://github.com/openclaw/openclaw/pull/71146) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown with diagnostic tables and Python request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable troubleshooting guidance; users should verify current DeepSeek and OpenClaw behavior before production changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
