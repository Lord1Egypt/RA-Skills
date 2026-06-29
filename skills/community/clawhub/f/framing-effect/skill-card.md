## Description: <br>
This skill helps agents audit framing effects by identifying loaded gain, loss, attribute, or goal frames, constructing equivalent alternatives, and checking whether the decision remains stable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to evaluate decisions, statistics, persuasive messages, and recommendations where wording may be steering choices. It guides the agent to restate the same facts in equivalent frames, compare decisions across frames, and produce a concise framing audit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persuasive framing guidance could be used to manipulate readers. <br>
Mitigation: Use the skill to present materially equivalent frames, clarify tradeoffs, and avoid exploiting a reader's bias. <br>
Risk: A reframing can become misleading if it omits material facts or is not logically equivalent. <br>
Mitigation: Check equivalence explicitly and preserve all material facts before comparing decisions across frames. <br>
Risk: Multi-frame analysis can add friction for trivial decisions. <br>
Mitigation: Apply the full audit when the stakes justify the analysis cost. <br>


## Reference(s): <br>
- [Sources - framing-effect](references/sources.md) <br>
- [Method in Action: Tversky and Kahneman's 1981 Asian Disease Study](examples/tversky-and-kahnemans-1981-asian-disease-study.md) <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/framing-effect) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown framing audit with concise analysis fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause for user input in coach mode before completing the audit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
