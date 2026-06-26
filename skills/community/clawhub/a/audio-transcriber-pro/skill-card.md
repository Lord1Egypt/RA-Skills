## Description: <br>
Transform audio recordings into professional Markdown documentation with intelligent summaries using LLM integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to turn meeting, interview, lecture, or content audio into Markdown transcripts, summaries, meeting minutes, action items, and optional subtitle files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional LLM features can send sensitive transcript text to Claude CLI or GitHub Copilot under the user's existing accounts. <br>
Mitigation: Use transcript-only local Whisper mode for confidential, regulated, or client recordings, or disable external LLM calls before deployment. <br>
Risk: Runtime dependency installation can install transcription and terminal UI packages on the host. <br>
Mitigation: Review installation scripts and preinstall approved dependencies in a controlled environment before enabling automatic setup. <br>
Risk: Privacy expectations may be unclear because local transcription and optional external LLM processing are both documented. <br>
Mitigation: State the selected processing mode before use and require user confirmation before any LLM processing of transcript text. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>
- [Transcription Tools Comparison](references/tools-comparison.md) <br>
- [Claude CLI documentation](https://docs.anthropic.com/en/docs/claude-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with timestamped transcripts, metadata tables, summaries, action items, and optional subtitle or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create transcript and meeting-minutes files; optional LLM processing can generate summaries from transcript text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
