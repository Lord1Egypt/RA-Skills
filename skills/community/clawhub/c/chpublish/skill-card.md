## Description: <br>
ClawHub 发布助手 helps agents publish or update local skill directories in the ClawHub marketplace by checking the target directory, release history, version, changelog, publish parameters, and result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare, publish, and verify ClawHub skill releases with confirmed slug, display name, version, changelog, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward publishing or updating a ClawHub skill with incorrect account, directory, slug, name, version, changelog, or tags. <br>
Mitigation: Confirm the logged-in ClawHub account, target directory, slug, display name, version, changelog, and tags before allowing any final publish command. <br>
Risk: Broad publish-related trigger phrases could start the publishing workflow when the user only intended to discuss publishing. <br>
Mitigation: Require explicit user confirmation of the target skill and release parameters before executing ClawHub CLI commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/chpublish) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides a step-by-step publishing flow and asks for confirmation before final publish parameters are used.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
