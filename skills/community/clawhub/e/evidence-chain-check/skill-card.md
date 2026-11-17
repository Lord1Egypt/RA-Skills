## Description:

Checks the order of timestamps, consistency of subjects, and continuity of declared hash links in a supplied evidence chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and auditors can check a supplied chain of electronic evidence records for out-of-order timestamps, inconsistent subjects, and mismatched adjacent hash references. Results are preliminary consistency checks, not proof of authenticity or legal admissibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checks compare supplied hash references but do not establish tamper-proof evidence or legal admissibility.

Mitigation: Independently validate record hashes, required fields, and the evidence schema; obtain human legal or audit review before making consequential decisions.

Risk: The documented --input, --verify, and --mode options are not implemented by the bundled command-line tool.

Mitigation: Check the actual --help output and pass a JSON array with --chain; use --json when machine-readable results are needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/evidence-chain-check)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text by default; JSON with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports breaks, a completeness flag, and observed subjects; exit status 0 for no detected breaks, 1 for detected breaks, and 2 for missing or invalid command-line input.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; bundled SKILL.md says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
