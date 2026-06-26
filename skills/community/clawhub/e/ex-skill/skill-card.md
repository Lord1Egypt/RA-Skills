## Description: <br>
Ex Skill helps create digital persona skills from chat histories and user-provided relationship details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1808182171](https://clawhub.ai/user/1808182171) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to guide intake, analyze chat records, and generate persona skills that simulate a specific communication style. It supports ongoing updates through additional records, corrections, version history, and rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access local message databases and possible credential-like WeChat encryption keys. <br>
Mitigation: Use it only for accounts and conversations you are authorized to process, and avoid disabling system protections. <br>
Risk: Generated persona files and knowledge files may retain private chat content. <br>
Mitigation: Prefer manual redacted chat exports when possible and review generated files for private data before sharing or deployment. <br>
Risk: The skill simulates personal communication patterns from intimate relationship data. <br>
Mitigation: Treat generated personas as simulations, review outputs carefully, and avoid using them to mislead or impersonate real people. <br>


## Reference(s): <br>
- [Ex Skill on ClawHub](https://clawhub.ai/1808182171/ex-skill) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Product Requirements](artifact/docs/PRD.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, persona files, JSON metadata, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local persona skill directories, metadata, version files, and chat-derived knowledge files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
