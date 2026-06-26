## Description: <br>
Second-opinion consultation plus automatic skill-engineering escalation for reviews, rewrites, hardening, weak-model optimization, packaging, testing, and publish readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ciklopentan](https://clawhub.ai/user/ciklopentan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to add structured second-opinion review to skill and artifact work, including rewrite, hardening, weak-model optimization, packaging, validation, and publish-readiness checks. It is most useful when an agent needs explicit round structure, consultant visibility rules, patch discipline, and rollback-aware validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local skill or runtime files and paste artifact text to external model consultants when that mode is allowed. <br>
Mitigation: Use local-only or findings-only constraints for private code, and require exact pasted context only when disclosure is acceptable. <br>
Risk: The workflow can apply real patches during review. <br>
Mitigation: Review proposed changes, run validation before accepting patched state, and rely on the skill's rollback gate when validation fails. <br>
Risk: Broad second-opinion workflows can introduce incorrect or misleading guidance into a skill if outputs are accepted without review. <br>
Mitigation: Treat consultant findings as review inputs, keep the main agent responsible for synthesis, and scan the final skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ciklopentan/dual-thinking) <br>
- [Runtime contract](references/runtime-contract.md) <br>
- [Modes](references/modes.md) <br>
- [Weak-model guide](references/weak-model-guide.md) <br>
- [Verification evidence](references/verification-evidence.md) <br>
- [Reference scenarios](references/reference-scenarios.md) <br>
- [Reference test log](references/reference-test-log.md) <br>
- [Governance](GOVERNANCE.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured Markdown round blocks, review guidance, patch proposals, code edits, shell commands, and validation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SELF_POSITION, CONSULTANT_POSITION, SYNTHESIS, validation state, patch state, continuation state, and resume snippets.] <br>

## Skill Version(s): <br>
8.5.24 (source: evidence.release.version and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
