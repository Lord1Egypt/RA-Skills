## Description:

Transcribe, diarise, translate, post-process, and structure audio/video with AssemblyAI-oriented workflows, producing agent-friendly transcript outputs for downstream AI tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe local or remote audio/video, add speaker labels or names, translate and post-process transcripts, and package results for review or downstream automation. It is most relevant when AssemblyAI-specific transcription, Speech Understanding, LLM extraction, subtitle output, or normalized transcript JSON is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence says the documentation and runtime disagree about who receives sensitive audio, transcript text, prompts, schemas, and URLs.

Mitigation: Review before installing, avoid confidential or regulated recordings until the publisher aligns documentation and runtime behavior, and use only when sending selected data to SkillBoss API Hub and possibly downstream services is acceptable.

Risk: Security guidance flags endpoint overrides, uploads, and deletion behavior as areas needing explicit review.

Mitigation: Restrict endpoint overrides, require explicit confirmation for uploads and deletion, and keep API keys out of prompts and logs.

## Reference(s):

- [AssemblyAI Documentation](https://www.assemblyai.com/docs)
- [Capabilities](references/capabilities.md)
- [Workflow Recipes](references/workflows.md)
- [Output Formats](references/output-formats.md)
- [Speaker Mapping Reference](references/speaker-mapping.md)
- [LLM Gateway Notes](references/llm-gateway.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown transcripts, normalized agent JSON, raw JSON, plain text, paragraph and sentence exports, SRT/VTT subtitles, bundle manifests, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create multi-file transcript bundles and sidecar outputs for downstream agent workflows.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter metadata.version is 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
