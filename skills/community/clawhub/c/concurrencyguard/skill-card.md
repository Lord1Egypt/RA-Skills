## Description: <br>
Race condition & concurrency safety analyzer -- detects unprotected shared state, missing locks, TOCTOU vulnerabilities, async/await pitfalls, thread-unsafe singletons, and deadlock-prone patterns across all languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan codebases for concurrency hazards, install pre-commit checks, and generate markdown reports that prioritize remediation work. Its findings should be treated as local heuristic analysis leads rather than definitive vulnerability proof. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git hook installation changes commit behavior and may block commits based on heuristic findings. <br>
Mitigation: Review the hook configuration before installation and keep an override or uninstall path available for false positives. <br>
Risk: Baseline files can suppress known findings and hide issues that still need review. <br>
Mitigation: Review baseline contents before accepting them and periodically re-audit suppressed findings. <br>
Risk: Race-condition findings are heuristic and can be false positives or incomplete. <br>
Mitigation: Use findings as review leads and verify them against the target code's actual synchronization and execution model. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suhteevah/concurrencyguard) <br>
- [ConcurrencyGuard website](https://concurrencyguard.pages.dev) <br>
- [Lefthook hook documentation](https://concurrencyguard.pages.dev/docs/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, markdown reports, git hook configuration, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local heuristic scanner; free tier is limited to five files per scan, with license-gated watch, CI, team report, and baseline modes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
