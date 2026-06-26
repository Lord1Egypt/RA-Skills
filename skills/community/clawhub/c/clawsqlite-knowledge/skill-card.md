## Description: <br>
Knowledge base skill that wraps the clawsqlite knowledge CLI for ingest/search/show. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ernestyu](https://clawhub.ai/user/ernestyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let agents ingest URLs or local notes into a SQLite-backed knowledge base, search it with FTS, vector, or hybrid retrieval, and show stored records. It can also call the underlying CLI to produce interest reports from the current knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs the third-party clawsqlite PyPI package. <br>
Mitigation: Install it only in environments that trust that package source and review dependency installation behavior before deployment. <br>
Risk: Fetched webpages, notes, and generated knowledge artifacts can be stored on disk. <br>
Mitigation: Use a dedicated knowledge root and avoid ingesting secrets, regulated data, private internal URLs, or confidential notes unless the storage location is trusted. <br>
Risk: Configured scraper, embedding, and small-LLM providers may receive or process ingested content or search text. <br>
Mitigation: Review provider configuration before use and run `clawsqlite knowledge doctor --json` to check paths, vector index, embedding, and small-LLM settings. <br>
Risk: Interest reports summarize stored knowledge and may expose sensitive themes or source material. <br>
Mitigation: Review `report_interest` output behavior and generated report locations before enabling reports in shared or production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ernestyu/clawsqlite-knowledge) <br>
- [clawsqlite homepage](https://github.com/ernestyu/clawsqlite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with optional Markdown report files and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns structured success or error data from the underlying clawsqlite knowledge CLI, including next-step hints when configuration or dependencies are missing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
