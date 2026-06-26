## Description: <br>
Audit locally installed skills against ClawHub: detect version drift, find new publish candidates, review security flags, and triage ownership conflicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to audit locally installed ClawHub skills, compare local and published versions, identify publish candidates, review security status, and handle ownership conflicts before publishing or updating skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawHub registry lookups may send local skill names over the network. <br>
Mitigation: Install only if you are comfortable with ClawHub registry queries using local skill names. <br>
Risk: Publish, update, or republish commands can change public registry state or local installed skill versions. <br>
Mitigation: Review commands before running publish, update, or republish steps. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nissan/clawhub-skill-audit) <br>
- [Publisher Profile](https://clawhub.ai/user/nissan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawhub CLI and python3; may perform outbound ClawHub registry lookups using local skill names.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
