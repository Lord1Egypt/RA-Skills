## Description:

Add governance to experiment workflows - PIN-protected destructive ops, standardized metrics registry with thresholds, compare-scores ranking with gating, and competition rules audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamond2nv](https://clawhub.ai/user/diamond2nv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to add governance controls to experiment workflows, including PIN protection for destructive operations, standardized metric reporting, score comparison with gates, and competition-rule audit checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents or automation may bypass PIN safeguards for destructive experiment actions by using force-style command paths.

Mitigation: Require explicit human approval or scoped automation credentials for cancel, stop, delete, and PIN-clear actions; avoid blanket use of force flags on PIN-protected commands.

Risk: Credential or local-state exposure can occur if ClearML, Langfuse, dataset paths, or PIN hashes are stored in tracked configuration files.

Mitigation: Keep real credentials in local environment files or local config, store PIN hashes in the dedicated expflow state path, and review generated configuration before committing.

Risk: Unpinned tool launches can reuse older local tool environments or drift from the intended release.

Mitigation: Pin expflow-pde versions for uvx or tool-run workflows when reproducibility or supply-chain hygiene matters.

## Reference(s):

- [expflow homepage](https://github.com/diamond2nv/expflow)
- [ClawHub skill page](https://clawhub.ai/diamond2nv/skills/experiment-lifecycle-governance)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash, Python, YAML, and JSON-style examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe PIN-guarded experiment actions, ClearML metric reporting, comparison gates, audit commands, and local configuration patterns.]

## Skill Version(s):

0.7.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
