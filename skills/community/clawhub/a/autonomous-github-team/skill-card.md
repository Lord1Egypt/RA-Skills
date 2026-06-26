## Description: <br>
Autonomous GitHub Team coordinates 41 AI agents that monitor a GitHub repository, detect bugs, create fixes, open pull requests, and support release workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[captainsvbot](https://clawhub.ai/user/captainsvbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to run GitHub automation that detects issues, proposes fixes, opens pull requests, and coordinates release-related workflows for a target repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs external bash scripts that can modify a GitHub repository. <br>
Mitigation: Review the pinned external scripts before running and test first in an isolated fork or test repository. <br>
Risk: The required GH_TOKEN grants repository write, pull request, and issue permissions. <br>
Mitigation: Use a dedicated fine-grained PAT limited to one repository, keep config.env private, and avoid broad account or organization tokens. <br>
Risk: Automation may create changes that could reach main or production if review gates are weak. <br>
Mitigation: Require branch protection, pull request review, and explicit human approval before merging or releasing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/captainsvbot/autonomous-github-team) <br>
- [Publisher profile](https://clawhub.ai/user/captainsvbot) <br>
- [Autonomous GitHub Team install repository](https://github.com/captainsvbot/AutonomousGitHubTeam.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include repository-changing automation steps that require human review before merge or release.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
