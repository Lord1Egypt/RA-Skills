## Description: <br>
Turn meeting audio or a transcript plus optional images into a publish-ready WeChat Official Account article. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinhuadeng](https://clawhub.ai/user/jinhuadeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and developers use this skill to convert meeting audio, transcripts, notes, screenshots, and optional QR codes into a structured WeChat Official Account article workflow. It produces a brief, article JSON, WeChat-ready markdown, image placement notes, and an optional handoff plan for draft publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting audio, transcripts, images, and generated drafts may contain confidential or sensitive content. <br>
Mitigation: Process only content approved for this workflow, keep local artifacts controlled, and review drafts before sharing or publishing. <br>
Risk: Generated WeChat markdown may misrepresent unclear transcript sections or include material that should not be published. <br>
Mitigation: Mark uncertain source material, review the final article manually, and require explicit approval before any WeChat handoff. <br>
Risk: Optional transcription and WeChat publishing steps depend on separate workflows outside this skill. <br>
Mitigation: Verify the separate transcription and publishing workflows before use, and treat publishing as an explicit user-requested step. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Style Guide](references/style-guide.md) <br>
- [Transcription Handoff](references/transcription-handoff.md) <br>
- [Publish Handoff](references/publish-handoff.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local article drafts and handoff artifacts; review generated markdown before any WeChat publishing step.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
