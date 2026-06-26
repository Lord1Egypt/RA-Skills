## Description: <br>
Experience Manager creates standard experience-package zip files from reusable agent practices, learns those packages into agent capabilities, and searches or publishes packages through Experience Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlx](https://clawhub.ai/user/zlx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to package, share, discover, and learn reusable OpenClaw agent experiences so practices can transfer across sessions and agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private OpenClaw memory and configuration while creating or learning experience packages. <br>
Mitigation: Install only where that local access is acceptable and review package contents before learning or publishing. <br>
Risk: Learning an untrusted local or remote package can permanently change agent behavior. <br>
Mitigation: Use dry-run first, avoid --yes for untrusted packages, and do not learn packages from unknown URLs. <br>
Risk: Using an agent-targeting option can modify another agent's persistent instructions. <br>
Mitigation: Use --agent only when you administer the target agent and have reviewed the planned changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zlx/experience-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown/text guidance with command examples, YAML experience metadata, reference Markdown files, and zip package files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or learn persistent experience packages under the user's OpenClaw experience directories.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
