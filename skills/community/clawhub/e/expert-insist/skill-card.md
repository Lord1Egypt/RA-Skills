## Description: <br>
Expert Insist guides agents to give independent, reasoned advice by using a three-round validation process for opinion, recommendation, analysis, and correction-driven prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn-zhou-chn](https://clawhub.ai/user/shawn-zhou-chn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent builders use this skill to reduce sycophantic advice in opinion-based questions by requiring an initial stance, self-challenge, and re-derivation after corrections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation may apply the opinionated advisory style when a neutral factual answer is preferred. <br>
Mitigation: Use explicit instructions for neutral factual answers or disable the skill for factual, formatting, technical-operation, and code-writing tasks. <br>
Risk: The source guidance is primarily Chinese-language, which may not match every user's preferred response language. <br>
Mitigation: Set an explicit language preference when using the skill in multilingual settings. <br>
Risk: Opinionated advice can still be wrong or misleading when assumptions are incomplete. <br>
Mitigation: Require the agent to state key assumptions, challenge its own conclusion, and present unresolved competing views when the validation rounds do not converge. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shawn-zhou-chn/expert-insist) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown-formatted advisory text with reasoning chains and key assumptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask clarifying questions before final advice; no tools, files, API keys, or dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
