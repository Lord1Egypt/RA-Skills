## Description:

Conjecture-Prover guides agents through a Chinese-language workflow for decomposing conjectures, converting them to equivalent or reduced forms, validating intermediate claims, and packaging proof-style reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to structure conjecture-proof attempts, document reductions, separate verified claims from open gaps, and produce proof reports or supporting verification artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated mathematical claims or proof routes may be incomplete or misleading, especially where the artifact marks the key RH inequality as open.

Mitigation: Treat outputs as drafts and require expert review before relying on proofs, reductions, or validation results.

Risk: The skill presents broad cross-domain proof capabilities that are not backed by domain-specific implementations in the package evidence.

Mitigation: Use it as a workflow template and calibrate each result against the standards and evidence practices of the target domain.

## Reference(s):

- [Conjecture-Prover ClawHub page](https://clawhub.ai/wangjiaocheng/skills/conjecture-prover)
- [Conjecture-Prover catalog](artifact/references/conjecture-prover-catalog.md)
- [Conjecture-Prover requirements](artifact/references/conjecture-prover-requirements.md)
- [Conjecture-Prover exemplars](artifact/references/exemplars.md)
- [RH artifact overview](artifact/assets/RH_README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with optional code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proof status labels, reductions, validation notes, reports, and verifier scripts.]

## Skill Version(s):

1.0.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
