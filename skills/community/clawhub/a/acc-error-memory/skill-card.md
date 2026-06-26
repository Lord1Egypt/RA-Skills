## Description: <br>
Error pattern tracking for AI agents. Detects corrections, escalates recurring mistakes, learns mitigations. The 'something's off' detector from the AI Brain series. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImpKind](https://clawhub.ai/user/ImpKind) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to detect user corrections or frustration in OpenClaw session transcripts, track recurring error patterns, and load learned mitigations at the start of later sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw session transcripts and creates persistent memory from conversation content. <br>
Mitigation: Install only for workspaces where transcript review and persistent memory are acceptable, and periodically inspect or delete the generated workspace memory files. <br>
Risk: Configured model commands can receive excerpts from user and assistant exchanges during screening or calibration. <br>
Mitigation: Use local or explicitly trusted ACC_MODELS commands, and avoid enabling recurring analysis for sensitive work. <br>


## Reference(s): <br>
- [ACC Error Memory on ClawHub](https://clawhub.ai/ImpKind/acc-error-memory) <br>
- [AI Brain Series on ClawHub](https://clawhub.ai/skills?tag=ai-brain) <br>
- [Hippocampus Skill](https://clawhub.ai/skills/hippocampus) <br>
- [Amygdala Memory Skill](https://clawhub.ai/skills/amygdala-memory) <br>
- [VTA Memory Skill](https://clawhub.ai/skills/vta-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON files] <br>
**Output Format:** [Markdown and terminal text with JSON state files and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent workspace memory files for error patterns, watermarks, calibration state, pending exchanges, and session-readable ACC_STATE.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
