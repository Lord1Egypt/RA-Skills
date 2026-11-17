## Description:

FlagRelease pipeline orchestrator that runs LLM deployment, verification, and benchmarking stages for multi-chip GPU backends and produces a structured final report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbavon](https://clawhub.ai/user/wbavon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to coordinate a GPU-container FlagRelease pipeline for installing and validating the LLM stack, verifying target models, running benchmarks, and collecting PASS, PARTIAL, or FAIL diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates execution to unbundled sibling skills that cannot be fully reviewed from this package.

Mitigation: Review or pin the four referenced sibling SKILL.md files before use.

Risk: The skill has broad command, file, network, and agent authority in a GPU container workflow.

Mitigation: Run it in a disposable or test GPU container, avoid mounting secrets or sensitive host paths, and require explicit approval before package installation, downloads, mirror use, or service startup.

## Reference(s):

- [Pipeline State Schema](artifact/references/pipeline-state.md)
- [ClawHub Skill Page](https://clawhub.ai/wbavon/skills/flagrelease-entrance-flagos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command snippets and structured JSON-style status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports PASS, PARTIAL, or FAIL status with step diagnostics, error details, and performance tables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
