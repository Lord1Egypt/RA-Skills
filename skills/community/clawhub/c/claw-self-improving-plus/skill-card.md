## Description:

Turn raw mistakes, corrections, discoveries, and repeated decisions into structured learnings and promotion candidates while keeping human approval before long-term file edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timothysong0w0](https://clawhub.ai/user/timothysong0w0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture lessons from mistakes, corrections, discoveries, and decisions, score their reuse value, deduplicate related records, and draft reviewable promotion patches for durable agent memory or behavior files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated patch files can modify durable agent behavior or memory files after an editable approved flag is set.

Mitigation: Review each patch manually, keep patch files under user control, and run apply_approved_patches.py only after confirming the target file, anchor, and suggested entry.

Risk: Low-confidence or untrusted observations could be promoted into SOUL.md, AGENTS.md, TOOLS.md, or MEMORY.md and affect future agent behavior.

Mitigation: Use the scoring, duplicate review, and human approval steps to keep uncertain items in the raw learning store unless they are verified and worth retaining.

Risk: Patch application can write to long-term files and may fail when anchors or replacement text do not match the workspace.

Mitigation: Prefer --dry-run first, inspect conflict and existing-promotion reports, and apply only controlled patch files with validated allowed targets.

## Reference(s):

- [Learning Store Layout](references/learning-store-layout.md)
- [Scoring Rubric](references/scoring-rubric.md)
- [Promotion Targets](references/promotion-targets.md)
- [Phase 2 Roadmap](references/phase-2-roadmap.md)
- [Phase 3 Roadmap](references/phase-3-roadmap.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples; scripts produce JSON, JSONL, Markdown-style review output, and patch candidate files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewable learning records, merge groups, backlog rankings, patch candidates, conflict reports, and optional apply reports. Applying durable changes requires approved patch entries.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
