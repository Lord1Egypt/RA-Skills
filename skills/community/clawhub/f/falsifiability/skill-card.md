## Description: <br>
Helps agents turn empirical claims, strategies, experiments, and investment theses into testable statements with explicit falsification conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to evaluate empirical claims, design experiments, define measurable thresholds, and pre-commit to actions when evidence falsifies a claim. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may over-apply empirical testing to ethical, aesthetic, philosophical, or otherwise non-empirical claims. <br>
Mitigation: First classify whether the claim is empirical and stop or redirect when falsifiability does not apply. <br>
Risk: The skill may encourage extra questioning or test design when the cost of running a test exceeds the value of the knowledge. <br>
Mitigation: Check test value before proceeding and avoid recommending measurement work that is not worth the decision impact. <br>
Risk: Generated thresholds or action plans could become misleading if accepted without domain review. <br>
Mitigation: Treat outputs as structured guidance and have the user or domain owner confirm metrics, time windows, and actions before relying on them. <br>


## Reference(s): <br>
- [Sources - falsifiability](artifact/references/sources.md) <br>
- [Method in Action: Popper 1934 + Eddington 1919 Eclipse + Modern Applications](artifact/examples/popper-1934-eddington-1919-eclipse-modern-applications.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/deciqai/skills/falsifiability) <br>
- [Publisher Website](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured falsifiability analysis with claim, evidence basis, falsification threshold, observation plan, owner, action, and ad-hoc preservation risk.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
