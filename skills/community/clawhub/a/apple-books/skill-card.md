## Description: <br>
Read your Apple Books library, highlights, notes, and reading progress directly from the local SQLite databases on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexissan](https://clawhub.ai/user/alexissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to inspect a local Apple Books library, including books, highlights, notes, collections, and reading progress, through read-only SQLite queries on macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private reading history, highlights, and notes to the host agent process. <br>
Mitigation: Install only in a trusted environment, request only the Apple Books information needed, and avoid sharing highlights or notes unless intentional. <br>
Risk: Full Disk Access may grant the host process broader local visibility than the skill itself uses. <br>
Mitigation: Grant Full Disk Access only to trusted agent processes and remove that access when it is no longer needed. <br>
Risk: Write operations against Apple Books databases may corrupt local data or cause iCloud sync issues. <br>
Mitigation: Use the skill's read-only query posture and do not run INSERT, UPDATE, or DELETE statements against Apple Books databases. <br>


## Reference(s): <br>
- [ClawHub Apple Books skill page](https://clawhub.ai/alexissan/apple-books) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only local SQLite query guidance for macOS Apple Books data.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
