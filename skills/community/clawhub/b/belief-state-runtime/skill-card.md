## Description: <br>
LLM-driven epistemic reasoning engine that evaluates claims against evidence and outputs calibrated confidence with a structured belief state of VERIFIED, CONTESTED, or UNCERTAIN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hqzzdsda](https://clawhub.ai/user/hqzzdsda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to assess whether a claim is trustworthy, detect contradictions across evidence, and present a calibrated confidence result. It is useful when an agent has gathered evidence and needs a structured verification state before answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the host agent to use online search when verifying claims. <br>
Mitigation: Use it only in environments where online evidence gathering is acceptable, and review the sources used in the assessment. <br>
Risk: Confidence scores may be affected by biased, stale, incomplete, or adversarial evidence. <br>
Mitigation: Treat the score as advisory and require human review for sensitive or high-impact decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hqzzdsda/belief-state-runtime) <br>
- [Project homepage declared by artifact](https://github.com/hqzzdsda/belief-state-runtime) <br>
- [Belief State Runtime configurator](https://hqzzdsda.github.io/belief-state-runtime/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python usage snippets and JSON assessment results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a belief state, confidence score, confidence range, feature judgments, and summary text.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
