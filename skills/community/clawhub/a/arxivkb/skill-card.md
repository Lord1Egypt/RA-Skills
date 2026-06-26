## Description: <br>
Local arXiv paper manager with semantic search that crawls arXiv categories, downloads PDFs, chunks content, and indexes with FAISS and Ollama embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camopel](https://clawhub.ai/user/camopel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and technical users use this skill to build and query a local arXiv knowledge base by category, with PDF ingestion, chunking, embeddings, semantic search, paper lookup, statistics, and cleanup commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer changes the local Python environment by installing packages and pulling an Ollama embedding model. <br>
Mitigation: Install in an isolated environment when possible, review package installation behavior first, and confirm Ollama model downloads are acceptable. <br>
Risk: The installer may create a recurring daily ingest job through a user systemd timer on Linux or launchd plist on macOS. <br>
Mitigation: Inspect, disable, or remove the scheduled job after installation if manual-only operation is desired. <br>
Risk: The skill stores arXiv PDFs, extracted text, SQLite data, and FAISS indexes locally. <br>
Mitigation: Confirm the configured data directory before ingesting papers or running cleanup commands, and monitor disk usage for larger category sets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/camopel/arxivkb) <br>
- [Ollama](https://ollama.ai) <br>
- [arXiv category taxonomy](https://arxiv.org/category_taxonomy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local SQLite, FAISS, PDF, configuration, and background scheduler files when the installer or CLI commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
