## Description: <br>
Guides an agent through a dual-system decision process that separates fast intuition from deliberate analysis for consequential or unfamiliar choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to coach users, developers, and teams through high-stakes or unfamiliar decisions by identifying the initial intuitive answer, deciding whether deliberate review is needed, and applying structured checks such as alternatives, checklists, base rates, premortems, and calibration logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce decision advice that users may over-trust in medical, legal, financial, or other high-stakes contexts. <br>
Mitigation: Treat outputs as decision-support guidance, require human judgment, and consult qualified professionals for regulated or high-impact decisions. <br>
Risk: The framework may slow or overcomplicate genuinely routine, low-stakes, or time-critical decisions. <br>
Mitigation: Apply the skill only when the evidence-supported activation conditions are met: consequential, unfamiliar, pressured, depleted, or rapidly converging decisions. <br>


## Reference(s): <br>
- [Primary sources for dual-system thinking](artifact/references/sources.md) <br>
- [Method in Action: Kahneman 2011 and Tversky-Kahneman Research](artifact/examples/kahneman-2011-tversky-kahneman-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown decision-coaching template with structured prompts and a calibration log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable output; responses may include staged questions that stop for user input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
