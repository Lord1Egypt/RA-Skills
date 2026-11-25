## Description:

Structured code reviews with severity-ranked findings and deep multi-agent mode. Use when performing a code review, auditing code quality, or critiquing PRs, MRs, or diffs, including a diff or patch pasted inline, even when the review looks quick from reading it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review code changes, audits, and PR or MR diffs for specification gaps, correctness, security, reliability, and test integrity, then receive severity-ranked findings with an evidence-supported review verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some fixes may be applied without approval.

Mitigation: Keep the task within an explicit review scope and require human confirmation before applying fixes.

Risk: Review activity may include evaluation operations beyond the expected review purpose.

Mitigation: Check the requested scope and intended actions before starting, and avoid evaluation actions that are outside that scope.

Risk: One referenced file was only partly analyzed, leaving a gap in the medium-confidence security assessment.

Mitigation: Inspect the included reference material before enabling the skill in workflows that can modify code.

## Reference(s):

- [Skill workflow](SKILL.md)
- [Skill specification](SPEC.md)
- [Scope and mode selection](references/scope-and-mode-selection.md)
- [Scope resolution](references/scope-resolution.md)
- [Standard review process](references/standard-review-process.md)
- [Deep review](references/deep-review.md)
- [Severity and confidence](references/severity-and-confidence.md)
- [Action routing](references/action-routing.md)
- [Reviewer trust boundary](references/reviewer-trust-boundary.md)
- [Report and integration](references/report-and-integration.md)
- [Check categories](references/check-categories.md)
- [Security patterns](references/security-patterns.md)
- [Reliability patterns](references/reliability-patterns.md)
- [Source and boundary evidence](references/source-and-boundary-evidence.md)
- [Security test coverage](references/security-test-coverage.md)
- [Review judgment traps](references/review-judgment-traps.md)
- [Review traps catalog](references/review-traps-catalog.md)
- [Language profiles](references/language-profiles.md)
- [False-positive suppression](references/false-positive-suppression.md)
- [Pull request sizing](references/pr-sizing.md)
- [Composer review](references/composer-review.md)
- [External review subprocess](references/external-review-subprocess.md)
- [Composer schema](https://getcomposer.org/doc/04-schema.md)
- [Composer configuration](https://getcomposer.org/doc/06-config.md)
- [Composer repository priorities](https://getcomposer.org/doc/articles/repository-priorities.md)
- [CVSS 3.1 specification](https://www.first.org/cvss/v3.1/specification-document)
- [GitHub Actions cache access rules](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching#cache-access-for-low-trust-workflow-triggers)
- [Claude Code dynamic context injection](https://code.claude.com/docs/en/skills#inject-dynamic-context)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with evidence-backed, severity-ranked findings and a review verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope-specific findings, recommendations, coverage notes, and residual risks; caller-specified format takes precedence.]

## Skill Version(s):

5.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
