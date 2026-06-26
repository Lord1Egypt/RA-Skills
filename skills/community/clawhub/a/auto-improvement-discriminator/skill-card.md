## Description: <br>
Scores and ranks improvement candidates using heuristic scoring, evaluator evidence, optional LLM judging, and multi-reviewer blind panels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to score generated improvement candidates, run blind panel review, apply optional LLM-as-judge semantic evaluation, and diagnose hold, reject, or accept-for-execution recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence an improvement pipeline by producing accept_for_execution, hold, or reject recommendations. <br>
Mitigation: Treat recommendations as advisory unless a separate gate enforces policy before execution. <br>
Risk: The interface module can execute local Python skill code when used with the real evaluator path. <br>
Mitigation: Evaluate only trusted skill files or run untrusted targets inside an appropriate sandbox. <br>
Risk: Claude or OpenAI judge backends may send candidate and target content to an external model provider. <br>
Mitigation: Use mock or local-only judging for sensitive content and configure API credentials deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanyasheng/auto-improvement-discriminator) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance, shell commands] <br>
**Output Format:** [JSON ranking artifacts with advisory notes; CLI usage is documented in Markdown with shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scored candidates, recommendations, blockers, panel reviews, LLM verdicts, and a summary count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; skill frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
