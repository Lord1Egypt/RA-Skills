## Description: <br>
Organize completed projects into searchable archives with session transcript backup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaigegao1110](https://clawhub.ai/user/kaigegao1110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace agents use this skill when a project is complete and should be preserved as a searchable internal archive with sanitized session transcripts, deliverables, decisions, and reconstruction notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill archives local session transcripts for long-term retention. <br>
Mitigation: Use it only for completed projects that should be retained, confirm the selected transcript, and avoid storing unnecessary client contact details. <br>
Risk: Sensitive information may remain in transcript archives if sanitization is incomplete or skipped. <br>
Mitigation: Run the bundled sanitization step, review the sanitized output before committing, and keep archive data inside the internal workspace. <br>
Risk: Original session files can be deleted after archiving. <br>
Mitigation: Delete original session files only after explicit user approval and after verifying that the archive copy is correct. <br>


## Reference(s): <br>
- [Archive Project ClawHub page](https://clawhub.ai/kaigegao1110/archive-project) <br>
- [Archive Project homepage](https://github.com/KaigeGao1110/ArchiveProject) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown archive files, sanitized JSONL transcript files, directory structures, and git commit commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for internal workspace retention and include sanitized transcript backups before optional deletion of original session files.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata; artifact frontmatter lists 1.2.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
