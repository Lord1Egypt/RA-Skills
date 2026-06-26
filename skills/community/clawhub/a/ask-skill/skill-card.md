## Description: <br>
Ask is a structured follow-up and deep analysis skill that turns ambiguous judgments into confidence-scored conclusions through triage, evidence scoring, optional web checks, Monte Carlo simulation, and critic review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gloryjack](https://clawhub.ai/user/gloryjack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use Ask to refine vague claims, forecasts, or research questions into direct conclusions with confidence scores, uncertainty notes, and risk points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves cross-session critique memory, which may retain analysis-derived weaknesses from sensitive topics. <br>
Mitigation: Before use on private, legal, financial, business, or personal topics, confirm whether /workspace/ask-memory.db can be disabled, inspected, or cleared. <br>
Risk: The skill can produce direct conclusions from evidence scoring, web checks, simulations, and critic review, so weak inputs may still lead to misleading guidance. <br>
Mitigation: Review the cited evidence, assumptions, confidence score, and stated uncertainty before acting on the output. <br>


## Reference(s): <br>
- [Ask on ClawHub](https://clawhub.ai/gloryjack/ask-skill) <br>
- [Publisher profile](https://clawhub.ai/user/gloryjack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with scored conclusions, uncertainty notes, and occasional code or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confidence scores and uncertainty labels; higher-depth forecast tasks may include Monte Carlo results.] <br>

## Skill Version(s): <br>
6.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
