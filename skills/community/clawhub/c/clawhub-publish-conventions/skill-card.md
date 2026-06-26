## Description: <br>
ClawHub skill publishing conventions for file inclusion, metadata requirements, versioning, scanner false-positive defense, and publish iteration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[almohalhel1408](https://clawhub.ai/user/almohalhel1408) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare and update ClawHub releases with the expected packaging, metadata, versioning, scanner review, and publish-fix-republish practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker and clawhub publish command examples can modify local images or publish releases if run without review. <br>
Mitigation: Review and adapt command examples in a safe workspace before execution, and confirm the intended version and changelog before publishing. <br>
Risk: Publishing materials and subprocess examples can expose secrets if users copy real credentials or pass full environments into subprocesses. <br>
Mitigation: Keep secrets out of SKILL.md, README files, command examples, and subprocess environments; use whitelist-only subprocess environments for copied patterns. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/almohalhel1408/clawhub-publish-conventions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, Dockerfile, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; review command examples before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
