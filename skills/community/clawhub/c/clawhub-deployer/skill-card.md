## Description: <br>
Publish a skill to ClawHub registry. Use when user asks to publish, release, or deploy a skill to ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to validate a skill folder, prepare text-only release files, run ClawHub login and publish commands, and verify the released skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide repository changes and external publishing without an explicit final review gate. <br>
Mitigation: Before running login or publish commands, manually confirm the folder, files, slug, version, owner, and publish destination, and remove secrets or private notes from the release folder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/clawhub-deployer) <br>
- [ClawHub registry](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of a clean publishing folder and publish command parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
