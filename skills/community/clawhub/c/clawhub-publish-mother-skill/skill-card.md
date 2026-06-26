## Description: <br>
Workflow for publishing and updating OpenClaw skills on ClawHub using verified token authentication and validation checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare, authenticate, validate, publish, update, and troubleshoot OpenClaw skill releases on ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication troubleshooting may expose a live ClawHub token when environment details are printed. <br>
Mitigation: Review and mask token-related output before running or sharing troubleshooting logs. <br>
Risk: The artifact recommends stealth or residential-proxy login workflows that may create account-policy risk. <br>
Mitigation: Prefer official ClawHub token or browser authentication unless explicit authorization exists for alternate login tooling. <br>
Risk: Publishing commands can update or release skills under the authenticated account. <br>
Mitigation: Run validation and dry-run publish checks before executing an actual publish command. <br>


## Reference(s): <br>
- [ClawHub Publish Mother Skill](https://clawhub.ai/stefanferreira/clawhub-publish-mother-skill) <br>
- [Camo Fox for ClawHub Publishing](references/camo-fox.md) <br>
- [ClawHub Token Settings](https://clawhub.ai/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes validation, publish test, and authentication troubleshooting shell scripts.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
