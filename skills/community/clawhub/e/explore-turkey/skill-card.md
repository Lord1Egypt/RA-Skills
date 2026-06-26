## Description: <br>
Book flights to Turkey, including Istanbul, Cappadocia, and Antalya routes, using flyai CLI results powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[palexu](https://clawhub.ai/user/palexu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to collect route parameters, run flyai flight searches, and return real-time Turkey flight options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install an unpinned global third-party npm CLI. <br>
Mitigation: Review the flyai CLI package before use, pin an approved version, and install it manually in a controlled environment. <br>
Risk: Travel search details are sent to the flyai/Fliggy service. <br>
Mitigation: Avoid entering sensitive travel details unless the service and data handling are acceptable for the deployment context. <br>
Risk: The release advertises broader travel capabilities than the artifact's flight-focused workflow supports. <br>
Mitigation: Use the skill for flight searches only unless additional workflows are validated separately. <br>


## Reference(s): <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown flight-search summary with comparison tables and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be derived from flyai CLI JSON and include Book links when results are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
