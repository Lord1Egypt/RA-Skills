## Description:

Local arXiv paper manager with semantic search that crawls arXiv categories, downloads PDFs, chunks content, and indexes results with FAISS and Ollama embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camopel](https://clawhub.ai/user/camopel)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and technical teams use this skill to build and query a local arXiv paper collection with category-based ingestion, PDF chunking, semantic search, and local embeddings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can create persistent daily ingestion jobs and change the local Python environment.

Mitigation: Review install.py before use, run it in a dedicated virtual environment, and disable systemd or launchd scheduling unless daily ingestion is intended.

Risk: Expiry commands can permanently delete stored papers, PDFs, and indexed chunks.

Mitigation: Run expiry with explicit day ranges and avoid the -y option unless deletion is intended.

Risk: Local paper downloads and embeddings can consume disk, memory, and background compute resources.

Mitigation: Limit enabled categories, use dry-run before ingestion, and monitor the configured data directory.

## Reference(s):

- [ClawHub arxivkb skill page](https://clawhub.ai/camopel/skills/arxivkb)
- [PrivateApp project](https://github.com/camopel/PrivateApp)
- [Ollama](https://ollama.ai)
- [arXiv category taxonomy](https://arxiv.org/category_taxonomy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line oriented text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+, Ollama, local disk storage, and the nomic-embed-text embedding model.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
