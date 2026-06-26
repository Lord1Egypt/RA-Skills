## Description: <br>
AnyGen: Download artifacts from a completed task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supertilico2001](https://clawhub.ai/user/supertilico2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents in downloading files or thumbnails from completed AnyGen tasks with the AnyGen CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an ANYGEN_API_KEY for AnyGen CLI access. <br>
Mitigation: Use a key with only the access needed for artifact downloads and avoid exposing it in prompts, logs, or shared shell history. <br>
Risk: The command writes downloaded task artifacts to a local output directory. <br>
Mitigation: Confirm the destination directory before running downloads and inspect downloaded files before opening or sharing them. <br>
Risk: The skill depends on the third-party @anygen/cli package. <br>
Mitigation: Install the CLI from a trusted package source and confirm the package is acceptable for the environment before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/supertilico2001/anygen-task-download) <br>
- [AnyGen shared skill](../anygen-shared/SKILL.md) <br>
- [AnyGen workflow generate skill](../anygen-workflow-generate/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides AnyGen CLI usage that returns JSON listing downloaded file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
