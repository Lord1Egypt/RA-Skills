## Description: <br>
Intent detection protocol for Claude that identifies the real goal behind requests, surfaces hidden assumptions, and decides when to ask clarifying questions versus when to proceed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an agent clarify ambiguous or high-impact requests before taking action. It is intended to reduce rework by translating intent, listing assumptions, scoring ambiguity, and setting scope boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may add an extra clarification step before work begins. <br>
Mitigation: Use it for ambiguous, significant, or hard-to-reverse requests, and skip it for simple factual questions or single-step operations. <br>
Risk: An incorrect intent translation could steer the agent toward the wrong scope. <br>
Mitigation: Ask the user to confirm when the translated goal differs from the literal request, and limit clarification to the most important questions. <br>


## Reference(s): <br>
- [Clarity First on ClawHub](https://clawhub.ai/skills/clarity-first) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style clarity checks, assumption summaries, scope boundaries, and concise clarifying questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution or external API calls; output is conversational guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
