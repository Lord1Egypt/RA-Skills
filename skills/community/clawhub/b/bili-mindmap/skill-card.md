## Description: <br>
Turns a Bilibili video URL or BV number into structured notes and an XMind mind map from subtitles, comments, AI summary, and transcript fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pzc163](https://clawhub.ai/user/pzc163) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect Bilibili video context and turn it into outline.md and an .xmind mind map for review, study, or note-taking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fallback transcription can send extracted video audio to external ASR services. <br>
Mitigation: Prefer local-only ASR, avoid sensitive or private videos, verify any Parakeet endpoint, and delete generated audio and context files when finished. <br>
Risk: The workflow stores collected metadata, comments, subtitles, transcripts, generated context, and output files locally. <br>
Mitigation: Run it only for videos whose contents are acceptable to store locally, and remove generated output directories after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pzc163/bili-mindmap) <br>
- [Host LLM Outline Spec](references/host-llm-outline-spec.md) <br>
- [Mindmap Outline Template](references/mindmap-outline-template.md) <br>
- [Third-Party Notices](THIRD_PARTY_NOTICES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown outline plus an XMind file, with shell commands and status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include outline.md, an .xmind file, and local context files; ASR fallback may create audio and transcript artifacts.] <br>

## Skill Version(s): <br>
0.2.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
