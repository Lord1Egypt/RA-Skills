## Description: <br>
Error Recovery - Strategies for handling failures gracefully <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide agents through common failure recovery patterns, including retry backoff, graceful degradation, circuit breakers, tool failure handling, session recovery, and model fallback decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example logging and recovery notes could expose secrets, tokens, private prompts, or sensitive error payloads if copied into a production agent unchanged. <br>
Mitigation: Review generated handling patterns before use, sanitize logged errors, and avoid persisting sensitive details in recovery memory or session notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanxiao-bot/error-recovery) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown with JavaScript examples and recovery tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no tool calls, credentials, or install commands are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
