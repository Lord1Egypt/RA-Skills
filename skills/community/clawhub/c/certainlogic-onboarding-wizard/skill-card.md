## Description: <br>
Guides new OpenClaw users by detecting their environment, recommending skills, and generating personalized setup, verification, checkup, or team onboarding materials without auto-installing or auto-configuring credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certainlogicai](https://clawhub.ai/user/certainlogicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and teams use this skill to scan a local OpenClaw environment, choose an onboarding goal, and receive a practical starter checklist with install commands and follow-up verification guidance. It is intended for developers, business users, researchers, productivity users, and beginners who want a guided path to a useful OpenClaw setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enumerates local OpenClaw skills and writes onboarding reports or checkup state under the OpenClaw workspace. <br>
Mitigation: Install and run it only where local skill inventory reporting is acceptable, and choose a controlled output directory when needed. <br>
Risk: Generated setup scripts contain install commands for recommended skills and may be run later by the user. <br>
Mitigation: Review any generated setup.sh and the referenced SKILL.md files before executing install commands. <br>
Risk: Recommended skills may request OAuth tokens, API keys, or account access after installation. <br>
Mitigation: Evaluate each recommended skill separately before granting credentials or account permissions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/certainlogicai/certainlogic-onboarding-wizard) <br>
- [Publisher profile](https://clawhub.ai/user/certainlogicai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional bash setup scripts and JSON checkup state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes onboarding, verification, and weekly checkup reports under the OpenClaw workspace by default; team exports can include a setup.sh and README in a user-selected directory.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
