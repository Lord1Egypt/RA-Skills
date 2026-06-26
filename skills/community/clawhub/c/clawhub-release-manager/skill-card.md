## Description: <br>
Safely release and publish skill updates to ClawHub with version bump discipline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okikesolutions](https://clawhub.ai/user/okikesolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to prepare and publish ClawHub skill releases with version bumping, lint/build checks, changelog notes, and release IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish ClawHub skill updates, so an agent could release an unintended version, changelog, or behavior change if the publish step is not reviewed. <br>
Mitigation: Before allowing publish, confirm `clawhub whoami`, the target skill folder, the version bump, changelog text, lint/build results, and release ID. <br>


## Reference(s): <br>
- [ClawHub Release Manager](https://clawhub.ai/okikesolutions/clawhub-release-manager) <br>
- [Release output template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown release summary with command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes release version, check status, publish result, routing or behavior changes, and a follow-up install/update command.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
