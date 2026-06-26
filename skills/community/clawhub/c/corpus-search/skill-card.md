## Description: <br>
Corpus Search is a local corpus retrieval skill that works with corpus-builder to run semantic search and metadata filtering by scene, emotion, pace, and quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and writing teams use this skill to search local fiction corpora for relevant passages by semantic query and filters such as scene type, emotion, pace, and quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python dependencies are specified with lower bounds rather than a lockfile. <br>
Mitigation: Install in a controlled environment and pin dependencies in a lockfile before deployment. <br>
Risk: The configured ChromaDB corpus path determines which local content can be searched. <br>
Mitigation: Verify configs/default_config.yml points only to approved corpus data before use. <br>
Risk: The embedding model may be downloaded when the search script initializes. <br>
Mitigation: Run in an environment where downloading and caching the configured embedding model is acceptable. <br>


## Reference(s): <br>
- [Corpus Search ClawHub Release](https://clawhub.ai/yuzhihui886/corpus-search) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Default Configuration](artifact/configs/default_config.yml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Console text or JSON search results, with optional exported result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default result limit is 10, maximum configured limit is 100, and result content previews are truncated to 500 characters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact SKILL.md lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
