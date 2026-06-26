## Description: <br>
Corpus Builder helps agents build Chinese-novel text corpora with scene-aware chunking, optional DashScope annotation, rule-based fallback, and ChromaDB vector storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and writing-tool agents use this skill to split source novels into reusable text chunks, annotate scenes and writing attributes, embed the chunks, and maintain local corpus files for later analysis or retrieval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated corpus files may contain original text and embeddings. <br>
Mitigation: Store generated corpus directories in a trusted location and review exported JSON or YAML before sharing. <br>
Risk: LLM annotation mode can send text chunks to DashScope. <br>
Mitigation: Unset DASHSCOPE_API_KEY to use the offline rule-based mode, or only use LLM mode with text approved for that service. <br>
Risk: Persistent shell configuration can expose API keys, and cleanup commands can remove local corpus data. <br>
Mitigation: Prefer a secret manager or temporary environment variable for DASHSCOPE_API_KEY, and verify any rm -rf target before running cleanup commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuzhihui886/corpus-builder) <br>
- [Annotation Schema](artifact/references/annotation-schema.md) <br>
- [Troubleshooting Guide](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and configuration examples; generated corpus artifacts are JSON, YAML, and ChromaDB files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run fully offline with rule-based annotation, or use DashScope when DASHSCOPE_API_KEY is set.] <br>

## Skill Version(s): <br>
1.1.2 (source: release metadata; artifact pyproject.toml and CHANGELOG report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
