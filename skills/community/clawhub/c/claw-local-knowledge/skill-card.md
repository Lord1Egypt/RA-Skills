## Description: <br>
Manages a local knowledge base by converting uploaded docx, pdf, xlsx, and pptx files to Markdown and retrieving stored content for agent responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[overdue-lin](https://clawhub.ai/user/overdue-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to ingest uploaded office documents into a local Markdown knowledge base and retrieve relevant stored knowledge during later tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded documents are converted into a persistent local knowledge base and may be reused in later retrieval. <br>
Mitigation: Avoid ingesting secrets or sensitive documents unless local retention is acceptable, and review stored Markdown files and index entries. <br>
Risk: Proactive retrieval setup can change future agent behavior through SOUL.md instructions. <br>
Mitigation: Review any SOUL.md change before enabling proactive retrieval. <br>
Risk: Original uploaded files may be deleted after conversion, which can make recovery difficult if conversion quality is poor. <br>
Mitigation: Keep separate copies of important originals until the converted Markdown and index entry have been reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/overdue-lin/claw-local-knowledge) <br>
- [Add knowledge workflow](references/add_knowledge.md) <br>
- [Retrieval workflow](references/retrieval_knowledge.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON index entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces converted Markdown knowledge files and updates a local JSON knowledge-base index.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
