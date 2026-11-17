## Description:

Corpus Builder builds Chinese-fiction corpora with scene-aware chunking, AI or rule-based annotation, embeddings, and ChromaDB vector storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and content engineers use this skill to turn directories of Chinese novel text into chunked, annotated, embedded corpora for later analysis or retrieval. It supports local rule-based annotation and optional DashScope-backed LLM annotation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional DashScope annotation can send source text to a cloud API when DASHSCOPE_API_KEY is set.

Mitigation: Set DASHSCOPE_API_KEY only when cloud annotation is intended; leave it unset for rule-based local annotation.

Risk: Troubleshooting steps include removal commands for local corpus or model-cache directories.

Mitigation: Verify and back up the exact target path before running deletion commands.

Risk: Production runs can change behavior if dependencies or embedding model revisions resolve differently over time.

Mitigation: Pin dependencies and the embedding model revision for production use.

Risk: Generated annotations, exports, checkpoints, and vector-store documents may contain original source text.

Mitigation: Store outputs in controlled local directories and review exported JSON or YAML before sharing.

## Reference(s):

- [README](README.md)
- [Annotation Schema](references/annotation-schema.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Usage Examples](examples/USAGE_EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are JSON, YAML, ChromaDB vector-store files, checkpoint files, and statistics files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include original source text, annotations, embeddings, and corpus metadata stored under the configured corpus directory.]

## Skill Version(s):

1.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
