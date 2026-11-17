## Description:

DriftGuard Security Scanner+ is a local-first security drift scanner for repos, OpenClaw skills, and AI agent tools. Use to scan before trust, save trusted baselines, compare after updates, generate human review tickets, review file/hash drift, dependency drift, install-hook changes, symlink changes, prompt-injection signals, sensitive-path references, obfuscation, shell execution, network access, and risky capability diffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[david90232](https://clawhub.ai/user/david90232)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent administrators use this skill to scan local repos, installed skills, and AI agent tool folders before trust and to compare later updates against a reviewed baseline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports and baselines can include file names, hashes, manifests, and finding excerpts from scanned folders.

Mitigation: Scan only intended target folders and store generated reports and baselines in locations with suitable access controls.

Risk: Target-provided suppressions can hide findings if accepted before review.

Mitigation: Use reviewer-controlled config by default and enable target config only after reviewing the target-provided suppressions.

Risk: The scanner is heuristic and does not guarantee that a skill or repo is safe.

Mitigation: Use high or critical findings as manual review gates and combine DriftGuard output with human security review before trusting updates.

## Reference(s):

- [DriftGuard OpenClaw metadata page](https://clawhub.ai/david90232/driftguard/security/openclaw)
- [DriftGuard ClawHub skill page](https://clawhub.ai/david90232/skills/driftguard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text plus JSON reports, Markdown reports, trusted baseline JSON, and Markdown review tickets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes indicate low/no drift, medium risk or drift, and high or critical risk.]

## Skill Version(s):

0.3.1 (source: release evidence and scripts/version.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
