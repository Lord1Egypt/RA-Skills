## Description:

Batch pre-closing cost and inventory self-check for client folders; runs 14 local reconciliation checks and reports one result line per client with source file and line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Cost accountants in manufacturing, trading, fresh food, and engineering use this before monthly cost closing to review client cost and inventory workpapers for arithmetic errors, reconciliation issues, omitted materials, and unexecuted checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads cost and inventory directories supplied by the user, which may contain sensitive accounting material.

Mitigation: Run it only on directories intentionally selected for review and avoid providing unrelated client or confidential files.

Risk: A clean-looking result can be misunderstood if materials were missing, table headers were unrecognized, or checks were listed as not executed.

Mitigation: Review all entries marked 未执行, checks_not_run, and sub_checks_not_run before relying on the output.

Risk: The output is an arithmetic and reconciliation aid, not an audit opinion or substitute for professional judgment.

Mitigation: Have a qualified reviewer confirm accounting assumptions, valuation judgments, physical existence, and any downstream audit or filing decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cost-inventory-pack-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each executed finding is intended to cite the client name, source file, and line; insufficient or unrecognized materials are reported as not executed rather than treated as clean.]

## Skill Version(s):

1.0.34 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
