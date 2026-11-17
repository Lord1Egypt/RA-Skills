## Description:

Assistant Reliability Watchtower runs deterministic ARW probes, digests, scorecard validation, and delivery preamble checks for OpenClaw assistant workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wit-oc](https://clawhub.ai/user/wit-oc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reliability operators use this skill to run ARW smoke probes, generate digests, validate scorecard evidence, render delivery preambles, and inspect current probe and configuration coverage without reading the full repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper is repo-backed and delegates execution to a local ARW checkout.

Mitigation: Install and run it only against a trusted ARW repository path supplied with --repo-root or ARW_REPO_ROOT.

Risk: Immediate alerts or non-dry-run delivery settings can target real recipients or write to an unexpected artifact location.

Mitigation: Review expected_recipient, actual_recipient, out_dir, and related delivery evidence values before enabling immediate alerts or live delivery.

## Reference(s):

- [ARW RC1 release contract](references/release-contract.md)
- [ARW probe and signal catalog](references/probe-catalog.md)
- [ARW config contract](references/config-contract.md)
- [Example ARW configuration](assets/example-config.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; wrapper commands produce JSON and Markdown monitoring artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes monitoring artifacts under the configured ARW artifact directory, typically artifacts/arw/.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
