## Description: <br>
Surfaces the best ClawHub skills for developer-tooling agents, including CI/CD, testing, code review, and developer productivity recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicope](https://clawhub.ai/user/nicope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to discover, score, and prioritize ClawHub skills for developer-tooling needs such as CI/CD, testing, code review, Git workflows, and stack-specific productivity gaps. It produces a short ranked recommendation report for onboarding, weekly discovery, or targeted capability-gap reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mission files such as SOUL.md may contain confidential stack, workflow, or internal mission details. <br>
Mitigation: Review and redact sensitive mission details before sharing generated recommendation reports outside the intended workspace. <br>
Risk: Recommended third-party skills may be unsuitable or risky for a specific agent despite matching the requested developer-tooling category. <br>
Mitigation: Manually review each recommended skill's publisher, security status, and install command before installation. <br>


## Reference(s): <br>
- [Clawtrix Dev Intel on ClawHub](https://clawhub.ai/nicope/clawtrix-dev-intel) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with ranked recommendations, rationale, skipped candidates, and install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits recommendations to the top 3 skills.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
