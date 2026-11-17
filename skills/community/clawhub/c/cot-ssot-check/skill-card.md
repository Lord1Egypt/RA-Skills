## Description:

SSOT Check helps agents audit documentation-heavy repositories for hand-copied facts, propose canonical `.ssot.yaml` manifests, and verify that copies still match.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find copied facts across documentation-heavy repositories, propose a `.ssot.yaml` manifest, and check whether known copies still match their canonical source. It is suited to pre-commit review and documentation audits where drifted numbers, prices, or claims should be surfaced before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A `.ssot.yaml` manifest can direct the agent to read sibling repositories or paths outside the current project.

Mitigation: Review manifests before check mode, especially entries containing `..`, and run the skill only in repositories and sibling clones the user has approved for scanning.

Risk: Untrusted manifests can broaden what the agent inspects during a drift audit.

Mitigation: Use trusted manifests or confine the agent to the intended repositories before running checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conorbronsdon/skills/cot-ssot-check)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Discovery prompt template](artifact/patterns/discovery-prompt.md)
- [Example discovery report](artifact/examples/cot-production-discovery/discovery-report.md)
- [Example proposed SSOT manifest](artifact/examples/cot-production-discovery/proposed-ssot.yaml)
- [Related standalone ssot-check CLI](https://github.com/conorbronsdon/ssot-check)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with YAML manifest proposals, regex patterns, shell command snippets, and proposed diffs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not auto-apply fixes; proposes edits and manifest changes for human approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
