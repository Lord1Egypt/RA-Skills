## Description: <br>
Business module engineer skill for env config, cache usage, backend menu wiring, and module-level permission integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and module engineers use this skill to update Weline business-module environment configuration, cache wrappers, backend menu wiring, and module permissions while keeping changes scoped to the owning module. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect backend permission wiring could hide expected admin functionality or expose admin functionality to the wrong users. <br>
Mitigation: Review permission diffs with the owning module context and validate menu visibility and controller access outside production before release. <br>
Risk: Environment, setup, or cache changes could alter runtime behavior unexpectedly. <br>
Mitigation: Review proposed env/setup commands before execution and verify cache read, write, and invalidation behavior through the intended module flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiweline/business-config-cache-acl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and configuration changes plus validation commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include validation evidence and documentation notes when admin usage or configuration behavior changes.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
