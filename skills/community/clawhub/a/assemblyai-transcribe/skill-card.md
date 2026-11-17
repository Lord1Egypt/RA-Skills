## Description:

Transcribe, diarize, translate, post-process, and structure audio/video with AssemblyAI into agent-friendly Markdown, JSON, subtitles, and workflow outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to run AssemblyAI-specific transcription workflows for local files or URLs, including speaker labels, speaker naming, translation, Speech Understanding, LLM Gateway extraction, and stable downstream transcript exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and sensitive media can be sent to custom configured endpoints.

Mitigation: Use only approved official AssemblyAI HTTPS endpoints and do not set custom base URL variables from untrusted contexts.

Risk: Confidential recordings and transcript content may be processed by external AssemblyAI services.

Mitigation: Do not process confidential recordings without approval, and choose the required regional endpoint before upload or LLM Gateway use.

Risk: The delete command can remove remote transcript data without stronger confirmation controls.

Mitigation: Confirm transcript IDs before deletion, prefer dry-run checks in automation, and treat deletion as irreversible.

Risk: AssemblyAI API keys may be exposed through prompts, logs, or command arguments.

Mitigation: Inject API keys through environment variables, keep them out of chat logs, and rotate credentials if exposure is suspected.

## Reference(s):

- [AssemblyAI documentation](https://www.assemblyai.com/docs)
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/assemblyai-transcribe)
- [Capabilities](references/capabilities.md)
- [Workflows and recipes](references/workflows.md)
- [Output formats](references/output-formats.md)
- [Speaker mapping](references/speaker-mapping.md)
- [LLM Gateway notes](references/llm-gateway.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Markdown, JSON, Text, Files]

**Output Format:** [Markdown transcripts, normalized agent JSON, raw JSON, plain text, SRT/VTT subtitles, and bundle manifests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write sidecar files and bundle manifests; long transcripts should use bundle or explicit output paths.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
