## Description: <br>
Generate a Cartesian verification artifact before trusting a plan, claim, implementation, or release. Turn confidence into explicit checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[malleus35](https://clawhub.ai/user/malleus35) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, reviewers, and release stakeholders use this skill to classify important claims and turn doubts about plans, implementations, decisions, or releases into concrete verification checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the generated doubt list as an automatic approval decision or release blocker. <br>
Mitigation: Treat the output as a checklist for human verification and decision-making, consistent with the security guidance. <br>
Risk: A review can remain too vague to test if claims are not classified or doubts are not mapped to actions. <br>
Mitigation: Require each important claim to be classified and each serious doubt to include a concrete verification action. <br>


## Reference(s): <br>
- [Agora Doubt List on ClawHub](https://clawhub.ai/malleus35/agora-doubt-list) <br>
- [Publisher profile: malleus35](https://clawhub.ai/user/malleus35) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown checklist with claim classifications, doubts, verification actions, clarity gate, and release posture] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a human-review artifact; it does not approve or block a release automatically.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
