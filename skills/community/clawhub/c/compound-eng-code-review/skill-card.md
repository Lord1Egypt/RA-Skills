## Description: <br>
Structured code reviews with severity-ranked findings and deep multi-agent mode for reviewing code, auditing code quality, or critiquing PRs, MRs, and diffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to perform structured code reviews, verify PR intent, identify correctness, security, reliability, performance, and test-coverage issues, and produce severity-ranked review feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use a local repository and authenticated GitHub context for review work. <br>
Mitigation: Confirm the target repository, PR, and requested action before allowing comments, labels, proof publishing, or test commands. <br>
Risk: Review findings and proposed commands may be incorrect or incomplete. <br>
Mitigation: Treat the output as review guidance, verify findings against the code and tests, and review commands before execution. <br>


## Reference(s): <br>
- [ia-code-review Specification](SPEC.md) <br>
- [Scope & comparison-range resolution](references/scope-resolution.md) <br>
- [Deep Review Process](references/deep-review.md) <br>
- [Severity Levels and Confidence Rubric](references/severity-and-confidence.md) <br>
- [What to Check - Review Category Checklists](references/check-categories.md) <br>
- [Language-Specific Review Profiles](references/language-profiles.md) <br>
- [Security Detection Patterns](references/security-patterns.md) <br>
- [Security Test Coverage Checklist](references/security-test-coverage.md) <br>
- [Reliability Patterns](references/reliability-patterns.md) <br>
- [False Positive Suppression](references/false-positive-suppression.md) <br>
- [Action Routing - 4-Tier Fix Classification](references/action-routing.md) <br>
- [PR sizing and large-diff strategy](references/pr-sizing.md) <br>
- [Driving a long-running external reviewer subprocess](references/external-review-subprocess.md) <br>
- [Review Traps Catalog](references/review-traps-catalog.md) <br>
- [ClawHub skill page](https://clawhub.ai/iliaal/compound-eng-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with severity-ranked findings and optional command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include severity, confidence score, file and line evidence, residual risks, and a merge-readiness verdict.] <br>

## Skill Version(s): <br>
4.1.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
