## Description: <br>
Enforce contextual permission boundaries for AI agents based on communication surface, constraining capabilities such as execution, file I/O, secrets, and messaging by channel trust level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adroidian](https://clawhub.ai/user/adroidian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure, validate, resolve, and audit channel-based trust levels so agent capabilities stay within the permission ceiling for each communication surface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides policy and audit guidance but does not enforce a technical sandbox by itself. <br>
Mitigation: Review the trust-channel YAML and permission matrix before deployment, and pair the policy with platform-level controls for secrets, tool execution, file access, and message sending. <br>
Risk: Incorrect channel mappings or permissive defaults could grant broader agent interaction than intended. <br>
Mitigation: Validate the configuration with scripts/validate_config.py and audit channel bindings with scripts/audit_channels.py before relying on the policy. <br>


## Reference(s): <br>
- [Chitin Moat Skill](SKILL.md) <br>
- [Example Configuration](references/example-config.yaml) <br>
- [Permission Matrix](references/permission-matrix.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/adroidian/chitin-moat) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/adroidian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local policy guidance and audit output; it is not a technical sandbox.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
