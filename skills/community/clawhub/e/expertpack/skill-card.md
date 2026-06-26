## Description: <br>
ExpertPack guides agents through loading, creating, hydrating, and configuring structured knowledge packs for AI context and RAG workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianhearn](https://clawhub.ai/user/brianhearn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to consume or author ExpertPacks, configure RAG over pack content, and work with Obsidian-compatible knowledge vaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreviewed pack content may be indexed into RAG or shared unintentionally. <br>
Mitigation: Review pack content before adding it to RAG or sharing it, and only point memorySearch.extraPaths at directories intended for indexing. <br>
Risk: Time-bound knowledge in volatile pack files may become stale. <br>
Mitigation: Check volatile file staleness at session start and refresh only when the user initiates or approves the update. <br>


## Reference(s): <br>
- [ExpertPack homepage](https://expertpack.ai) <br>
- [Consumption Reference](references/consumption.md) <br>
- [Hydration Reference](references/hydration.md) <br>
- [ExpertPack Schemas Reference](references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with inline JSON, YAML, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No hidden execution or credential behavior found in server security evidence.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
