## Description: <br>
Evaluate whether a service qualifies as agent-native using the five hard criteria from the awesome-agent-native-services standard and the bonus URL Onboarding signal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoruilee](https://clawhub.ai/user/haoruilee) <br>

### License/Terms of Use: <br>
CC0-1.0 <br>


## Use Case: <br>
External users, developers, and maintainers use this skill to evaluate whether a service qualifies as agent-native, agent-adapted, or agent-builder. It guides evidence collection for the five hard criteria, URL Onboarding, bonus signals, classification, recommendation, confidence, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL onboarding checks may expose an agent to third-party service instructions that request registration, posting, claiming tasks, publishing data, or other actions. <br>
Mitigation: Keep onboarding checks to inspection and summary by default, and require explicit approval before the agent performs account, content, task, or publishing actions. <br>
Risk: The skill can produce an incorrect or misleading service classification if source evidence is incomplete or weak. <br>
Mitigation: Require source-backed evidence for each criterion and review the final recommendation before using it to publish or reject a service. <br>


## Reference(s): <br>
- [awesome-agent-native-services repository](https://github.com/haoruilee/awesome-agent-native-services) <br>
- [Moltbook URL Onboarding example](https://www.moltbook.com/skill.md) <br>
- [Ensue / autoresearch@home URL Onboarding example](https://raw.githubusercontent.com/mutable-state-inc/autoresearch-at-home/master/collab.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown evaluation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes URL Onboarding status, criterion-by-criterion results, bonus signals, classification, recommendation, confidence, reasoning, and next steps.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
