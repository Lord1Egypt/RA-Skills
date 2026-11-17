## Description:

AI Sting is an AI application security testing agent that analyzes user-described assistants, generates prompt-injection test cases, and provides defensive system-prompt patches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caizhongxian](https://clawhub.ai/user/caizhongxian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to test AI agents they own or are authorized to assess. It produces tailored prompt-injection, social-engineering, and logic-bypass probes plus defensive system-prompt language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated attack prompts could be used against systems without authorization.

Mitigation: Use the skill only for AI systems you own or have explicit permission to test, and do not apply outputs to third-party assistants or production systems without approval.

Risk: The artifact does not state clear authorization limits for red-team prompt generation.

Mitigation: Add or enforce an operating rule that generated probes must stay within an approved testing scope before relying on the skill.

## Reference(s):

- [ClawHub skill page: AI Sting](https://clawhub.ai/caizhongxian/skills/ai-sting)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured sections and quoted prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk analysis, three tailored attack prompts, and one to two defensive system-prompt patches.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
