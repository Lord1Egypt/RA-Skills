## Description:

Deep Research Forge helps agents structure evidence-led research, compare alternatives, synthesize findings, and produce research briefs, decision briefs, reusable research assets, or retrospectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxbin](https://clawhub.ai/user/fxbin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run structured research on products, companies, people, concepts, technologies, markets, policies, or cultural phenomena. It is intended for evidence led synthesis, decision support, competitive analysis, concept lineage, source tracking, optional parallel research, and research quality review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports under-disclosed local automation for persistent research state, skill iteration, file changes, and evaluator command execution.

Mitigation: Review requested actions before allowing local validation scripts, evaluator commands, file edits, VERSION updates, or .skill-iterations state changes.

Risk: The skill can ask for multi-agent execution or local validation scripts during research and retrospective workflows.

Mitigation: Use multi-agent execution and scripts only when explicitly requested, and inspect the proposed roles, commands, and file paths before running them.

Risk: Evidence-heavy research and decision support can still produce incorrect or misleading conclusions when sources are incomplete or conflicts are unresolved.

Mitigation: Require source traceability, confidence labels, contradiction handling, and human review before using outputs for high-stakes decisions.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/fxbin/skills/tree/main/deep-research-forge)
- [ClawHub skill page](https://clawhub.ai/fxbin/skills/deep-research-forge)
- [Publisher profile](https://clawhub.ai/user/fxbin)
- [Research protocol](references/research-protocol.md)
- [Research methodology atlas](references/research-methodology-atlas.md)
- [Source strategy](references/source-strategy.md)
- [Claim citation protocol](references/claim-citation-protocol.md)
- [Multi-agent protocol](references/multi-agent-protocol.md)
- [Quality gates](references/quality-gates.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands, code]

**Output Format:** [Markdown, structured text, JSON evidence ledgers, schemas, templates, and optional shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first research workflow with optional multi-agent planning, citation maps, quality scoring, and reusable research artifacts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
