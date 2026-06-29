## Description: <br>
Use this skill when a developer or desk worker reports chest pain, chest pressure, left arm or jaw discomfort, shortness of breath, unusual sweating, faintness, or asks for an exhaustion-aware health check that should consider local work patterns from git activity and current host context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoqing404](https://clawhub.ai/user/shaoqing404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and desk workers use this skill for conservative, local-first triage when chest discomfort, shortness of breath, faintness, unusual sweating, or exhaustion-aware health concerns require a quick emergency-versus-urgent-care recommendation. It is not a diagnosis tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake the triage flow for diagnosis or reassurance during potentially serious symptoms. <br>
Mitigation: State that the skill is not diagnostic, prioritize emergency red flags, and direct users toward emergency or same-day medical care when symptoms are concerning. <br>
Risk: Local work-pattern and host context can be sensitive and can only weakly inform fatigue risk. <br>
Mitigation: Keep inspection narrow, treat git-derived fatigue as context rather than proof, and store local health summaries only after explicit consent. <br>
Risk: This release references bundled scripts and reference files that are absent from the package. <br>
Mitigation: Use the remaining SKILL.md instructions as the available evidence and do not rely on missing local automation or reference documents until the package is updated. <br>


## Reference(s): <br>
- [Server-resolved source repository](https://github.com/shaoqing404/dont-deal/tree/main/skills/dont-deal-triage) <br>
- [ClawHub skill page](https://clawhub.ai/shaoqing404/skills/dont-deal-triage) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Concise triage guidance, optionally structured as JSON with urgency, reasoning_summary, recommended_action, and follow_up_questions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes short, action-oriented responses and one-question-at-a-time follow-up when symptoms are active.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
