## Description:

物业与不动产专家 routes pasted property and real-estate accounting tables to one of nine local checks and returns line-referenced, recalculable conclusions while withholding conclusions when required columns are missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Property managers, finance teams, and auditors use this skill to check pasted lease, rent, property-fee, utility, deposit, maintenance-fund, and public-income tables before settlement or review. It helps identify arithmetic mismatches, missing required columns, duplicate or invalid rows, and unexecuted checks that need separate review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release creates hidden local usage state and enforces a free-use limit before subscription.

Mitigation: Review and disclose the local usage counter and subscription behavior before deployment, or remove/approve the gating if hidden state is unacceptable.

Risk: Financial conclusions can be incomplete or misleading if source tables omit required columns, mix issue types, or use unsupported formats.

Mitigation: Require complete headers and source rows, review missing-input and unexecuted-check notices, and reconcile findings against contracts, ledgers, and qualified audit, legal, or tax review.

Risk: A clean result only means the executed checks passed, not that the full property, contract, tax, or audit question is resolved.

Mitigation: Treat results as spreadsheet-style consistency checks and keep human review for out-of-scope legal, tax, contract, and policy judgments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-property-pub)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill instructions](artifact/SKILL.md)
- [Expert manifest](artifact/scripts/engine/expert-manifest.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON check results from local Node.js execution, with Markdown usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include sub-skill routing, line-referenced findings, missing-column notices, and lists of checks that were not executed.]

## Skill Version(s):

1.0.10 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
