## Description: <br>
Provides a local Hebbian co-occurrence graph engine that records memory co-occurrences, calculates association weights, supports related-memory queries, and maintains a SQLite-backed association database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoisme007](https://clawhub.ai/user/whoisme007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building memory-enabled agents can use this skill to record which memories are retrieved together, rank related memories by decayed co-occurrence weight, inspect graph statistics, and clean stale association edges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The engine persists memory identifiers and association weights in a local SQLite database across runs. <br>
Mitigation: Set CO_OCCURRENCE_DB_PATH to an appropriately scoped location and clear, rotate, or isolate the database when retention is not intended. <br>
Risk: Untrusted or test memory identifiers can be recorded into a long-lived production memory graph. <br>
Mitigation: Avoid feeding untrusted or test identifiers into production graphs, and use separate database files for testing and production. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code examples and a Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configurable local SQLite database path and optional forgetting-curve integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
