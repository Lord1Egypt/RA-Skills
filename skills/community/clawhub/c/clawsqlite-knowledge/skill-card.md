## Description: <br>
Knowledge base skill that uses the published clawsqlite CLI for ingest, search, show, and maintenance workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ernestyu](https://clawhub.ai/user/ernestyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a configured clawsqlite knowledge instance through the official CLI, including ingest, search, record inspection, maintenance, and analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bootstrap step runs a shell installer that installs the clawsqlite Python package from PyPI. <br>
Mitigation: Install only in environments where running that bootstrap and installing the PyPI package are acceptable. <br>
Risk: Ingested URLs, notes, and documents become persistent knowledge-base content. <br>
Mitigation: Avoid secrets or sensitive documents unless the configured providers and storage locations in clawsqlite.toml are trusted. <br>


## Reference(s): <br>
- [clawsqlite homepage](https://github.com/ernestyu/clawsqlite) <br>
- [ClawHub skill page](https://clawhub.ai/ernestyu/skills/clawsqlite-knowledge) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with shell commands and JSON-producing CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI examples commonly request structured JSON output from clawsqlite.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata, SKILL.md frontmatter, manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
