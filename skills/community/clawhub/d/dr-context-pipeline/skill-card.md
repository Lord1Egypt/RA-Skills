## Description: <br>
Deterministic memory/context pipeline with semantic retrieval checks, compression/lint, safe fallback, and memory watchdog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate a deterministic memory/context pipeline for agent tasks. It standardizes routing, memory retrieval, context compression, validation, and runtime evidence across normal, debug, and audit modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to use local persistent memory as a context source, which can retain conversation details on disk. <br>
Mitigation: Install only when local memory is desired, and avoid memory commits or debug/audit modes when the conversation contains information that should not be retained. <br>
Risk: Setup can write or refresh local context_pipeline files and requires changes to AGENTS.md. <br>
Mitigation: Review the setup commands and resulting diffs before accepting the installation as the default context workflow. <br>
Risk: Semantic retrieval can be unavailable or degraded, which may reduce recall quality for tasks that depend on persistent memory. <br>
Mitigation: Run the documented memory watchdog with semantic checks before claiming semantic memory is healthy, and use explicit fallback or fail-closed behavior when required checks fail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniel-refahi-ikara/skills/dr-context-pipeline) <br>
- [Apply checklist](references/APPLY.md) <br>
- [Runtime evidence checklist](references/RUNTIME_CHECKLIST.md) <br>
- [Runtime artifact layout](references/RUNTIME_ARTIFACTS.md) <br>
- [Semantic memory assurance](references/SEMANTIC_MEMORY_ASSURANCE.md) <br>
- [Router configuration](references/router.yml) <br>
- [Retrieval Bundle schema](references/schemas/retrieval_bundle.schema.json) <br>
- [Context Pack schema](references/schemas/context_pack.schema.json) <br>
- [Receipt Ledger schema](references/schemas/receipt_ledger.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON schema/configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or validate local context_pipeline files and debug/audit JSON artifacts when the user requests those modes.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
