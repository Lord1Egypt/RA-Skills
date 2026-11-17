## Description:

Coverify extracts commitment-bearing text kernels, compares them with Jaccard similarity, detects ghost-token leakage, and runs model-swap checks for transformation drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, auditors, and researchers use Coverify to check whether commitments in text survive transformation by extracting kernels, comparing Jaccard scores, reviewing ghost-token leakage, and running model-swap checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The verifier reads matching entries from a local audit ledger during hash verification.

Mitigation: Review the relevant ledger entries and avoid using sensitive local audit records unless that local access is acceptable.

Risk: Model-swap runs save local reports that may contain sensitive signal text or derived kernels.

Mitigation: Review saved reports under the local model-swap output directory and sanitize sensitive text before sharing results.

Risk: Security evidence notes some overclaiming and metadata gaps.

Mitigation: Treat conservation, ghost-token, and model-swap results as heuristic analysis that should be reviewed before operational decisions.

## Reference(s):

- [Coverify ClawHub Skill Page](https://clawhub.ai/sunrisesillneversee/skills/coverify)
- [Falsifiability Protocol](references/falsifiability.md)
- [Ghost Token Specification](references/ghost-token-spec.md)
- [Published Claim DOI](https://zenodo.org/records/18792459)
- [MOSES Project Site](https://mos2es.io)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Text]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text verifier reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local CLI output may include SHA-256 input hashes, Jaccard scores, cascade risk labels, ghost_pattern fingerprints, ledger lookup status, and saved model-swap report paths.]

## Skill Version(s):

0.4.3 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
