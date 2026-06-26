## Description: <br>
AI video production asset management system for creating, locking, versioning, planning, archiving, consistency-checking, and rework tracking for character, scene, prop, and shot assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlxeva](https://clawhub.ai/user/dlxeva) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to organize AI video production projects around locked character, scene, prop, shot, generation-record, consistency-check, and rework files. It helps maintain repeatable asset naming, project structure, and consistency checks across tools such as Runway, Kling, Pika, Sora, and Veo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The download helper can fetch arbitrary URLs and write files using unsafe local paths if provided crafted filenames. <br>
Mitigation: Use the helper only in a controlled project directory, avoid untrusted URLs and path-like filenames, and restrict URL schemes, internal hosts, file sizes, file types, overwrites, and destination paths before deployment. <br>


## Reference(s): <br>
- [Consistency Rules](references/consistency-rules.md) <br>
- [Project Templates](references/project-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file paths, project templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local project folders, markdown asset cards, generation logs, consistency checks, rework records, and downloaded media files when helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
