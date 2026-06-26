## Description: <br>
Automatically publish newly created local skills to ClawHub after the skill has been reviewed and committed, when the user has explicitly requested ongoing ClawHub publication for assistant-created skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G-Hanasq](https://clawhub.ai/user/G-Hanasq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to publish newly created, reviewed, and committed local skills to ClawHub through an authenticated local ClawHub session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish reviewed local skills to ClawHub using the active authenticated account. <br>
Mitigation: Confirm the active ClawHub account and review the referenced publish-flow script in the local environment before use. <br>
Risk: Publishing a vague draft or uncommitted skill could release incomplete guidance. <br>
Mitigation: Use only after the skill is coherent, reviewed, committed, and explicitly approved for ongoing ClawHub publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/G-Hanasq/auto-publish-created-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the skill, version, publish result, final URL when available, and verification status.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
