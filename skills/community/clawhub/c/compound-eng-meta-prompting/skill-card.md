## Description: <br>
Structured reasoning modifiers (/think, /verify, /adversarial, /edge, /confidence, /assumptions, etc.) to stress-test decisions, surface assumptions, or enumerate edge cases when validating an important design, architecture decision, or ambiguous plan before committing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to apply structured reasoning patterns for architecture decisions, ambiguous plans, code reviews, security-sensitive questions, and other situations where assumptions or edge cases should be made explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reasoning modifiers can change answer structure, verbosity, or confidence framing in ways that may not fit sensitive workflows. <br>
Mitigation: Use explicit commands in sensitive sessions, keep custom pattern definitions narrow, and review final answers for task fit before acting. <br>
Risk: Adversarial, edge-case, and premortem patterns may surface speculative failure modes that distract from the primary answer. <br>
Mitigation: Treat pattern output as decision-support guidance and keep the core answer prominent when applying the skill. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown text, with JSON code blocks when the /json pattern is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include pattern markers such as VERIFIED ANSWER, REVISED ANSWER, confidence tiers, comparison tables, assumptions, or edge-case lists.] <br>

## Skill Version(s): <br>
3.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
