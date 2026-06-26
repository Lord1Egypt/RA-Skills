## Description: <br>
Fast red-or-yellow chest-pain triage for overworked developers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoqing404](https://clawhub.ai/user/shaoqing404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and desk workers use this skill to triage chest pain, related discomfort, or exhaustion-aware health concerns. It helps distinguish emergency action now from urgent same-day medical review, while treating local fatigue and host context as supporting signals only. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles urgent health situations and is not a substitute for emergency services or professional medical care. <br>
Mitigation: Keep emergency guidance prominent, avoid reassurance, and escalate active chest-pain danger signs to emergency help now. <br>
Risk: Local Node scripts can inspect host context and nearby Git commit timing. <br>
Mitigation: Review before installing and run only where narrow local host and Git inspection is acceptable. <br>
Risk: The skill may store sensitive health-triage history under ~/.dont-deal. <br>
Mitigation: Use only on machines where local record retention is acceptable, and require explicit consent before saving user-provided background history. <br>


## Reference(s): <br>
- [Emergency thresholds](references/emergency-thresholds.md) <br>
- [Quick mode](references/quick-mode.md) <br>
- [Installation and activation](references/installation-and-activation.md) <br>
- [ClawHub release page](https://clawhub.ai/shaoqing404/dont-deal-triage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Short plain-language triage guidance, with optional JSON fields for urgency, reasoning summary, recommended action, and follow-up questions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quick-mode CLI output may be bilingual and may append local event history under ~/.dont-deal.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
