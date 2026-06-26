## Description: <br>
Inline assumption checker that challenges your agent's thinking before responding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommot2](https://clawhub.ai/user/tommot2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Cross Check to surface assumptions, blind spots, disagreements, and confidence notes before relying on a response. It is useful for complex decisions, long prompts where accuracy matters, and explicit requests for a second opinion or assumption challenge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Two-model verification can send the problem context and extracted assumptions to the configured verifier model or provider. <br>
Mitigation: Avoid 2-model mode for highly sensitive prompts unless that provider and model are acceptable for the context. <br>
Risk: Assumption checks and confidence notes can still be incomplete or misleading. <br>
Mitigation: Use the generated challenge notes as review guidance and independently verify high-impact conclusions before acting. <br>
Risk: Lite and deep modes increase token usage compared with a single response. <br>
Mitigation: Use lite mode for routine checks and reserve deep or 2-model mode for higher-risk decisions. <br>


## Reference(s): <br>
- [Cross Check ClawHub release page](https://clawhub.ai/tommot2/cross-check) <br>
- [Cross Check homepage listed in artifact](https://clawhub.ai/skills/cross-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown confidence notes and compact verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default confidence note, lite summaries capped at 8 lines, and deep summaries capped at 15 lines.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
