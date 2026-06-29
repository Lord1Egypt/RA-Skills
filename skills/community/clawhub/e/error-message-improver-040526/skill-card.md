## Description: <br>
Rewrite vague application, API, CLI, and support errors into diagnostic messages that explain what failed, why it likely failed, and the next safe action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product engineers, platform teams, support leads, technical writers, and SaaS operators use this skill to turn unclear errors into actionable user-facing messages, support notes, structured payloads, and review checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logs or original error text may contain secrets, stack traces, or internal implementation details that should not be exposed in user-facing messages. <br>
Mitigation: Remove secrets, irrelevant stack traces, and sensitive internals before producing or publishing rewritten error text. <br>
Risk: Broad invocation wording may cause the skill to be applied to general debugging or support prompts where a direct fix is expected instead of copy improvement. <br>
Mitigation: Use explicit invocation when error-message rewriting is desired and confirm the intended output before changing diagnostic guidance. <br>


## Reference(s): <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-040526) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown, structured text, or code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include before-and-after rewrites, structured error payloads, telemetry fields, support notes, and checklists.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
