## Description: <br>
Guides an agent through first-principles teardown of claims or decisions by separating bedrock facts from inherited assumptions and rebuilding the answer from what remains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to pressure-test expensive or hard-to-reverse decisions by decomposing claims into bedrock facts, inherited assumptions, and a reconstruction with confidence and open questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat generated citations, numbers, or bedrock claims as settled facts when making important decisions. <br>
Mitigation: Verify cited facts, numbers, and assumptions before relying on the teardown for material decisions. <br>
Risk: The method can add unnecessary analysis to routine, reversible decisions where convention is sufficient. <br>
Mitigation: Use the skill only for decisions that are expensive, hard to reverse, authority-driven, or explicitly requested from first principles. <br>


## Reference(s): <br>
- [Sources - first-principles](references/sources.md) <br>
- [Method in Action: Wright Brothers and the Lift Tables (1901)](examples/wright-brothers-1901.md) <br>
- [Stanford Encyclopedia of Philosophy: Aristotle's Logic](https://plato.stanford.edu/entries/aristotle-logic/) <br>
- [Encyclopaedia Britannica: Euclidean geometry](https://www.britannica.com/science/Euclidean-geometry) <br>
- [Smithsonian National Air and Space Museum: Wright Brothers and the Invention of the Aerial Age](https://airandspace.si.edu/explore/stories/wright-brothers-and-invention-aerial-age) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown teardown using Claim / Assumptions / Bedrock / Reconstruction / What changes / Confidence & open questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask follow-up questions in coach mode and uses explicit WAIT stops before advancing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
