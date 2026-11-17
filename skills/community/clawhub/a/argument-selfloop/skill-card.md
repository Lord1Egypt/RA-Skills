## Description:

Maintains an argument ledger and premise consistency report for drafted sections to check paragraph argument moves, narrative linkage, and premise hygiene before merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and writing agents use this skill during prose drafting to self-check section-level argument continuity, premise stability, and paragraph roles before merging draft sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe output path handling can write reports outside the chosen workspace.

Mitigation: Run only in a controlled workspace, restrict outputs to expected workspace-local report paths, and review generated paths until output handling is fixed.

Risk: The bundled package contains unrelated pipeline files with broad routing hints.

Mitigation: Confirm whether the target OpenClaw environment activates bundled pipeline files, and remove or isolate unrelated workflows before production use.

Risk: The PASS result should not be treated as a real quality gate until the ledger schema is enforced and an argument-selfloop validator exists.

Mitigation: Manually review ARGUMENT_SELFLOOP_TODO.md, SECTION_ARGUMENT_SUMMARIES.jsonl, and ARGUMENT_SKELETON.md before relying on the skill's pass/fail status.

Risk: Server-resolved provenance is unavailable for this release.

Mitigation: Do not infer GitHub or upstream repository provenance from skill text; verify source history separately before enterprise deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/willoscar/skills/argument-selfloop)
- [Publisher profile](https://clawhub.ai/user/willoscar)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, Files, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSONL ledger records, section edits, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes argument reports under configured output paths; review path handling before use because scan evidence flags unsafe output handling.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
