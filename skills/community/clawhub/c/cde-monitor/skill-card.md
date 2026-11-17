## Description:

Query CDE China drug review public data for breakthrough therapy announcements, priority review announcements, included lists by company or drug, in-review registration lookups by company or drug, and acceptance-number review status lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[changye](https://clawhub.ai/user/changye)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query live public China Center for Drug Evaluation listings for drug review announcements, included breakthrough or priority lists, in-review registrations, and acceptance-number review status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live browser automation uses under-disclosed automation-disguise settings and disables Chrome's sandbox while loading a public website.

Mitigation: Review before installing, run only in an isolated virtual environment under an unprivileged user, keep Chrome or Chromium patched, and avoid sensitive host mounts when containerized.

Risk: The Selenium dependency is not pinned to an exact reviewed version.

Mitigation: Pin Selenium to an exact reviewed version before production deployment.

Risk: The CDE page structure or network payloads can change, causing incomplete or unreliable query results.

Mitigation: Confirm important results against the public CDE site and rerun with a visible browser when parsing or query behavior appears inconsistent.

## Reference(s):

- [CDE homepage](https://www.cde.org.cn)
- [CDE information disclosure entry](https://www.cde.org.cn/main/xxgk/listpage/9f9c74c73e0f8f56a8bfbc646055026d)
- [CDE review task disclosure](https://www.cde.org.cn/main/xxgk/listpage/369ac7cfeb67c6000c33f85e6f374044)
- [Setup](references/setup.md)
- [Queries](references/queries.md)
- [Development Guide](references/development-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries and tables; underlying CLI output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the live CDE website, local Chrome or Chromium, and strict company, drug, or acceptance-number inputs.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
