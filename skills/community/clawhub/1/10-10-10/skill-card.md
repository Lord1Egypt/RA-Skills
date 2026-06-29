## Description: <br>
Guides agents through the 10-10-10 decision framework so users can compare immediate, medium-term, and long-term consequences before committing to an action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People making non-trivial personal, career, relationship, or business decisions under emotional pressure use this skill with an agent to consider 10-minute, 10-month, and 10-year perspectives and choose a concrete next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence personal, career, relationship, or business choices where poor guidance may have consequences. <br>
Mitigation: Use it as a coaching aid that supports user judgment; consult qualified professionals for legal, financial, medical, or safety-critical decisions. <br>
Risk: The framework may be applied to trivial or urgent decisions where extra deliberation is not useful. <br>
Mitigation: Use it for non-trivial decisions with medium- or long-term consequences, and stop when all three time horizons return low-stakes answers. <br>
Risk: Users may treat the three horizon answers as an automatic decision rather than decision input. <br>
Mitigation: End with a specific action, timeline, and early signal while keeping final synthesis with the user. <br>


## Reference(s): <br>
- [Primary sources](references/sources.md) <br>
- [Method in Action: Suzy Welch, 1990s; Jeff Bezos, 1994](examples/suzy-welch-1990s-jeff-bezos-1994.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown coaching prompts and a structured decision summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive coaching flow may stop at WAIT points until the user responds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
