## Description: <br>
Trains new or existing agents on studio conduct, identity customization, foundational skills, and optional advanced workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to onboard agents with conduct rules, persistent identity files, core collaboration and memory skills, and role-specific advanced training. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill teaches broad persistent changes to agent operating files. <br>
Mitigation: Require explicit confirmation for each file rewrite and keep backups before applying changes. <br>
Risk: The skill covers sensitive integrations and credential-backed tools. <br>
Mitigation: Redact credentials, keep backup paths allowlisted with secret scanning, and avoid sending private content to external services without clear consent. <br>
Risk: Browser and media workflows may expose active profiles, private content, or voice data. <br>
Mitigation: Avoid live Chrome profiles unless explicitly approved, and obtain consent before using private content or voice data with external services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/agent-teacher) <br>
- [Working Rules of Conduct](references/rules-of-conduct.md) <br>
- [Identity Customization](references/phase-0-identity.md) <br>
- [Foundation Curriculum](references/phase-1-foundation.md) <br>
- [Advanced Curriculum](references/phase-2-advanced.md) <br>
- [Artist Gstack Learning Guide](references/learning-from-gstack-artist.md) <br>
- [Designer Gstack Learning Guide](references/learning-from-gstack-designer.md) <br>
- [Producer Gstack Learning Guide](references/learning-from-gstack-producer.md) <br>
- [Programmer Gstack Learning Guide](references/learning-from-gstack-programmer.md) <br>
- [Gstack project](https://github.com/garrytan/gstack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to persistent agent operating files and commands for installing or configuring other skills.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
