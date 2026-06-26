## Description: <br>
Evaluates AI agents with cognitive diagnostic prompts, a scored behavioral rubric, and metacognitive correction guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fretelli](https://clawhub.ai/user/fretelli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and safety reviewers use this skill to probe target AI agents for authority bias, hallucination under false premises, and stereotype amplification, then summarize results in a structured diagnostic report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic prompts may elicit unsafe code requests, false-premise analysis, or biased content from a target agent. <br>
Mitigation: Run evaluations only in controlled, authorized settings and do not execute or reuse unsafe or biased target outputs. <br>
Risk: The skill is intended to pressure-test agent behavior and may be inappropriate for production or third-party systems without consent. <br>
Mitigation: Use consenting or sandboxed target agents and avoid production or third-party systems without authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fretelli/cognitive-behavior-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown diagnostic report with text prompts and scored rubric] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes 1-5 scoring across resistance to authority, fact grounding, and neutrality.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
