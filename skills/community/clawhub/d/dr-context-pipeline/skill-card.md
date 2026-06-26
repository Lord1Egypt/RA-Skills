## Description: <br>
DR Context Pipeline standardizes agent memory loading by routing messages, retrieving relevant snippets, compressing them into cited Context Packs, linting the result, and falling back safely when validation fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and validate a deterministic context-loading workflow for file-based memory. It supports routing, snippet retrieval, Context Pack compression, lint fallback, runtime evidence modes, and regression checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent workspace changes and make local memory retrieval part of normal agent behavior. <br>
Mitigation: Enable it only when that behavior is intended, and review the AGENTS.md patch, context_pipeline files, memory commit workflow, and debug or audit artifact paths before use. <br>
Risk: Local memory retrieval may expose secrets or sensitive account details stored in memory files. <br>
Mitigation: Do not store secrets or sensitive account details in memory files that the pipeline may retrieve. <br>
Risk: Debug and audit modes can persist runtime artifacts that summarize retrieved context and pipeline state. <br>
Mitigation: Use debug or audit modes only when the resulting artifacts are appropriate for the workspace, and review artifact paths before sharing or retaining them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniel-refahi-ikara/skills/dr-context-pipeline) <br>
- [Context Pipeline README](assets/context_pipeline/README.md) <br>
- [Runtime Evidence Checklist](references/RUNTIME_CHECKLIST.md) <br>
- [Runtime Artifacts](references/RUNTIME_ARTIFACTS.md) <br>
- [Router configuration](references/router.yml) <br>
- [Retrieval Bundle schema](references/schemas/retrieval_bundle.schema.json) <br>
- [Context Pack schema](references/schemas/context_pack.schema.json) <br>
- [Receipt Ledger schema](references/schemas/receipt_ledger.schema.json) <br>
- [Deterministic snippet IDs](references/deterministic_ids.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks, configuration files, schemas, and JSON runtime artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update context_pipeline files, AGENTS.md instructions, and debug or audit JSON artifacts when applied.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
