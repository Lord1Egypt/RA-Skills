## Description: <br>
FileChat RAG helps agents sync Google Drive folders into local vector indexes and answer or retrieve files using semantic search over document chunks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eladrave](https://clawhub.ai/user/eladrave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use FileChat RAG to let an agent index selected Google Drive folders, retrieve relevant document snippets, answer questions with file citations, and download requested files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recursively process selected Google Drive files and send document text, image contents, and search queries to Gemini or OpenAI. <br>
Mitigation: Use a dedicated Drive folder and dedicated API keys, and avoid regulated or highly sensitive files unless policy allows third-party AI processing. <br>
Risk: The skill keeps extracted text and embeddings in local vector_db files. <br>
Mitigation: Limit workspace access and delete generated vector_db files when the index is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eladrave/eladrave-filechat-rag) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [OpenAI embeddings API](https://api.openai.com/v1/embeddings) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, retrieved text snippets, filenames, file IDs, and optional media attachment paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Google Drive folder ID and Gemini or OpenAI API credentials; stores per-folder vector_db JSON files locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
