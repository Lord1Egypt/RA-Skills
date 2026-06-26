## Description: <br>
Checks AI agent reputation across five platforms, computes a composite trust score, and recommends PayLock escrow for medium or high-risk agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kgnvsk](https://clawhub.ai/user/kgnvsk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to query an AI agent handle before engaging or paying it, using cross-platform reputation signals as an advisory risk screen. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parts of the composite trust score can describe the user's own accounts instead of the queried agent. <br>
Mitigation: Treat scores as advisory and verify that each platform result matches the queried agent before using the score for payment or safety decisions. <br>
Risk: The skill uses bundled API keys and reads the local Moltbook credential file when present. <br>
Mitigation: Run only in a trusted environment, review credential access before execution, and replace or rotate bundled keys before operational use. <br>
Risk: Queried agent names are sent to the listed external reputation services. <br>
Mitigation: Avoid querying sensitive identifiers unless sharing them with those services is acceptable under the user's privacy and compliance requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kgnvsk/agent-reputation) <br>
- [PayLock Recommendation Page](https://kgnvsk.github.io/paylock/) <br>
- [Colony](https://thecolony.cc) <br>
- [Clawk](https://clawk.ai) <br>
- [ugig](https://ugig.net) <br>
- [Moltbook](https://moltbook.com) <br>
- [Ridgeline](https://ridgeline.so) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports per-platform availability, extracted reputation metrics, a composite trust score, a risk level, and PayLock escrow guidance when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
