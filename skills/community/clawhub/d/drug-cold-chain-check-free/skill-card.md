## Description:

Drug Cold Chain Record Check (Free) is a Chinese-language local checker that reviews drug cold-chain temperature and inventory ledgers for six consistency checks and cites source lines for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Quality managers and pharmacists at pharmacies, pharmaceutical distributors, and vaccination sites use this skill to check cold-chain temperature and inventory ledgers before monthly close, GSP self-inspection, or regulator-facing review. It focuses on the six declared local consistency checks and does not provide drug quality or regulatory certification decisions.

### Deployment Geography for Use:

Global; the workflow and examples are Chinese-language and reference China-oriented GSP review practices.

## Known Risks and Mitigations:

Risk: Users may treat ledger consistency findings as drug quality decisions, GSP certification outcomes, trace-code verification, or original instrument review.

Mitigation: Use the output only as a local ledger consistency check and route drug quality, certification, traceability, and source-instrument questions to qualified review processes.

Risk: The free edition omits checks including over-temperature handling closure, storage-condition matching, in-transit temperature analysis, batch tracing, and facility-by-product summaries.

Mitigation: Confirm the executed-checks and checks-not-run lists before relying on the report, and perform omitted checks separately when they matter.

Risk: Required ledger columns or recognizable table text may be missing, causing the checker to withhold conclusions.

Mitigation: Provide the table header and data rows together, preferably as tab-separated text or as a JSON object with a text field, and treat insufficient-input output as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/drug-cold-chain-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON report with cited source lines and lists of executed and omitted checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library code; returns insufficient-input status instead of a conclusion when required ledger material is missing.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
