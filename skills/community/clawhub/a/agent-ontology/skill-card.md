## Description: <br>
Create, update, and query typed entities and relations like Person, Project, and Task in a verifiable knowledge graph with validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biociao](https://clawhub.ai/user/biociao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to maintain structured local memory as typed graph records, then create, query, relate, and validate entities such as people, projects, tasks, and dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Structured memory is saved locally in an append-only graph file and may persist sensitive information if users enter it. <br>
Mitigation: Store only intended non-secret information, and avoid passwords, API keys, tokens, or sensitive personal details unless local persistence is deliberate. <br>


## Reference(s): <br>
- [Ontology Schema Reference](references/schema.md) <br>
- [Query Reference](references/queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists user-created graph records to local append-only JSONL storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
