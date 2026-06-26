## Description: <br>
Fox Ontology provides a typed knowledge graph for structured agent memory, entity and relation management, constraint validation, and cross-skill state sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tihuaqin-commits](https://clawhub.ai/user/tihuaqin-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, query, relate, validate, and share structured local memory across skills using a typed ontology graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a persistent local knowledge graph that can retain sensitive personal, project, message, or credential-adjacent details. <br>
Mitigation: Store only information intended for workspace persistence, avoid raw secrets and unnecessary private content, and review memory/ontology/graph.jsonl before sharing or publishing the workspace. <br>
Risk: Append-only graph records mean delete operations can hide entities from the current graph without erasing prior log records. <br>
Mitigation: Treat the graph log as retained history and manually redact or rotate the storage file when permanent removal is required. <br>
Risk: Incorrect schema or relation updates can make the shared memory graph misleading for downstream skills. <br>
Mitigation: Run ontology validation after changes and review generated schema updates before relying on them for planning or cross-skill coordination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tihuaqin-commits/fox-ontology) <br>
- [Ontology schema reference](references/schema.md) <br>
- [Ontology query reference](references/queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON, YAML, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update append-only local ontology files under memory/ontology when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
