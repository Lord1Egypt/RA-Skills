## Description:

Validate, plan and explicitly dispatch provenance-linked ML experiments using the bundled Python runtime, with budget reservations and durable result bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and ML engineers use this skill to validate experiment specifications, produce execution plans, and dispatch authorized local, SSH, or RunPod experiments while preserving provenance and budget-governance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad credential exposure during experiment execution.

Mitigation: Install and run only in an isolated environment, use narrowly scoped temporary tokens, and avoid running untrusted experiment commands with credentials in the shell environment.

Risk: Unsafe results paths or sensitive generated bundles may expose operational data.

Mitigation: Review bundles before publishing and avoid --repo-dir publishing until results_prefix containment is fixed.

Risk: Untrusted experiment specs or source commits can trigger unauthorized compute or external writes.

Mitigation: Run only trusted specs and source commits, confirm authorization before execution, and preserve budget reservation and reconciliation checks.

## Reference(s):

- [README](README.md)
- [Security and privacy](SECURITY.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, and Python runtime guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local plans and result bundles; real execution may contact external services and consume compute.]

## Skill Version(s):

0.1.0 (source: changelog, pyproject.toml, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
