## Description: <br>
Helps agents place Markdown documentation and script files into the project's required docs/ and scripts/ directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to decide where Markdown documentation and scripts should be created in projects that follow the listed backend and frontend directory conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses strict, path-specific placement rules that may not match other repositories. <br>
Mitigation: Adapt the directory mapping or disable the skill outside repositories that use these exact conventions. <br>
Risk: The skill can steer documentation and script placement decisions broadly. <br>
Mitigation: Review proposed file paths before allowing an agent to create or move files. <br>


## Reference(s): <br>
- [Directory Mapping - Complete Reference](references/directory-mapping.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/urbantech/file-placement) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with directory mapping tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Path-specific rules for Markdown documentation and shell or Python scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
