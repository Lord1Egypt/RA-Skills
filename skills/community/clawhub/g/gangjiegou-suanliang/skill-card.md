## Description:

Estimates steel-structure tonnage from existing geometry contracts; it does not read drawings or replace settlement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Steel estimators and structural engineering teams use this skill to turn an existing steel-geometry contract into a reviewable tonnage estimate, member ledger, and section summary. Drawing recognition is handled by a separate tool, and the result is not a final quantity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a contract integrity weakness that may affect acceptance of altered input.

Mitigation: Review contract provenance and hash-chain status before relying on a result, and use contracts from trusted sources.

Risk: The security review reports a mismatch between the stated no-drawing scope and a drawing-recognition workflow; its analysis is partial.

Mitigation: Review the workflow and unresolved references before installation, and confirm that drawing recognition stays within the documented boundary.

## Reference(s):

- [On-demand usage and estimation rules](artifact/references/on-demand.md)
- [Contract and bus reference](artifact/references/bus-contract.md)
- [ClawHub release page](https://clawhub.ai/lisong2003-lgtm/skills/gangjiegou-suanliang)

## Skill Output:

**Output Type(s):** [JSON, Markdown, CSV, Analysis]

**Output Format:** [JSON data, a Markdown review report, and CSV summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tonnage is presented as an estimate band of ±15%; final_quantity is false. Missing or unsupported evidence remains flagged for review.]

## Skill Version(s):

0.4.4 (source: frontmatter, changelog, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
