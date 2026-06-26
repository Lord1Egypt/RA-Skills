## Description: <br>
AIFS - HTTP File system helps agents store, retrieve, list, patch, delete, and summarize non-sensitive files through the AIFS.space cloud storage API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Deploydon](https://clawhub.ai/user/Deploydon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to persist non-sensitive notes, documents, and session data across sessions or sync cloud-backed files when they provide an AIFS.space API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Content is stored with an external cloud storage service. <br>
Mitigation: Use the skill only for non-sensitive content and avoid secrets, regulated data, or confidential material. <br>
Risk: Write, patch, and delete operations can change or remove remote files. <br>
Mitigation: Confirm the target path and requested action before overwriting, patching, or deleting files. <br>
Risk: Broad API keys increase the impact of mistakes or exposure. <br>
Mitigation: Use a least-privilege AIFS.space API key, keep it in environment or user configuration, and rotate it if exposed. <br>


## Reference(s): <br>
- [AIFS.space](https://aifs.space) <br>
- [ClawHub skill page](https://clawhub.ai/Deploydon/aifs-space) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AIFS_API_KEY and AIFS.space HTTP endpoints; confirm destructive write, patch, and delete operations before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
