## Description: <br>
AI Photos helps OpenClaw users turn local photo folders into a searchable AI photo album with plain-language search and a local gallery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoubingwu](https://clawhub.ai/user/zoubingwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to set up, reconnect, index, search, and browse a local AI photo album from folders they choose. It supports natural-language search, date filtering, metadata inspection, manual sync, and optional automatic indexing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs an external ai-photos CLI release. <br>
Mitigation: Install only when the external project is trusted, and prefer a pinned and verified CLI release before using it with personal photo folders. <br>
Risk: The skill processes local photo folders that may contain private or sensitive images and metadata. <br>
Mitigation: Choose only intended folders, review what will be indexed, and avoid sharing gallery access beyond the local machine unless the exposure is understood. <br>
Risk: Optional automatic indexing can make ongoing changes to the album workflow. <br>
Mitigation: Enable automatic indexing only after review, and inspect any HEARTBEAT.md changes before relying on scheduled updates. <br>


## Reference(s): <br>
- [AI Photos ClawHub listing](https://clawhub.ai/zoubingwu/ai-photos) <br>
- [ai-photos CLI repository](https://github.com/zoubingwu/openclaw-ai-photos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Concise agent responses with shell commands, JSONL record guidance, and configuration updates when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure a local album profile, import captioned photo records, and update HEARTBEAT.md only when automatic indexing is approved.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and skill frontmatter v2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
