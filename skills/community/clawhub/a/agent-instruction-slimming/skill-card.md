## Description:

Reduce an agent instruction file (AGENTS.md, system prompt, rule file) without losing coverage: lever order (remove first, move second, reformat third, rewrite last), verbatim-subset edits with pointer lines, joint marker accounting, and tiering by frequency and reversibility. Use when a rule file has grown too large, when rules are being ignored, or before adding more rules. Tool-agnostic; includes marker counting and subset checking scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cengcengcai-creator](https://clawhub.ai/user/cengcengcai-creator)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to reduce oversized instruction files while checking that retained and relocated clauses preserve measurable structural coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan has medium confidence and is partial because a local path-like reference in SKILL.md could not be resolved.

Mitigation: Inspect the referenced path and confirm its target before relying on the related guidance.

Risk: The examples include approval wording that may need to match the user's local policy.

Mitigation: Review the approval wording against the applicable policy before reusing the example rules.

Risk: Marker counts describe instruction structure and do not establish that agent behavior improved.

Mitigation: Treat the counts as structural checks and use a separate before-and-after behavior probe when evaluating adherence.

## Reference(s):

- [Verbatim subset procedure](references/verbatim-subset.md)
- [Conditional marker counting script](scripts/cond_count.py)
- [Verbatim subset checking script](scripts/subset_check.py)
- [ClawHub skill page](https://clawhub.ai/cengcengcai-creator/skills/agent-instruction-slimming)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance and instruction files, Python scripts, and command-line verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Marker counts are structural proxies; behavior requires a separate before-and-after probe.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
