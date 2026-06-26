## Description: <br>
Publish agent skills to ClawHub marketplace. Search, install, update, and publish skills from clawhub.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to operate the ClawHub CLI for searching, installing, updating, and publishing agent skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the CLI from npm introduces package provenance risk. <br>
Mitigation: Verify the npm package provenance before installation. <br>
Risk: Forced bulk updates can change installed skills broadly. <br>
Mitigation: Avoid forced bulk updates unless the operator understands the impact. <br>
Risk: Publishing a skill directory can expose secrets or private files. <br>
Mitigation: Review skill directories for secrets and private files before publishing. <br>


## Reference(s): <br>
- [ClawHub marketplace](https://clawhub.com) <br>
- [ClawHub Publish Official release page](https://clawhub.ai/terrycarter1985/clawhub-publish-official) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume the ClawHub CLI is installed and authenticated when publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
