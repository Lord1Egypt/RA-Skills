## Description:

cn-med-oa helps agents search Weipu OA for Chinese medical literature, download available PDF full text, produce Vancouver or GB/T 7714 citation metadata, and verify Chinese citations with five-state results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsor1212](https://clawhub.ai/user/docsor1212)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and writing agents use this skill to retrieve open-access Chinese medical articles from Weipu OA and verify generated or supplied Chinese citations before using them in literature reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTPS certificate verification is disabled by default for network features.

Mitigation: Set CN_MED_OA_VERIFY_SSL=1 before using network features, or wait for the default to be fixed.

Risk: HTML verification reports may include unescaped citation or remote metadata values.

Mitigation: Treat generated HTML reports as untrusted and prefer JSON output until HTML escaping is added.

Risk: The optional PyMuPDF dependency expands the local execution surface when PDF checks are enabled.

Mitigation: Install PyMuPDF only in a virtual environment with a pinned, reviewed version.

Risk: The source platform can return weakly relevant results for broad or multi-term searches.

Mitigation: Use specific medical single-phrase queries, review relevance markers and disclosure text, and run citation verification before relying on results.

## Reference(s):

- [Weipu OA API Contract](references/weipu-oa-api-contract.md)
- [Weipu OA Platform](https://oa.cqvip.com)
- [ClawHub Skill Page](https://clawhub.ai/docsor1212/skills/cn-med-oa-pub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell and Python snippets; generated JSON manifests, PDF files, citation text, and HTML or JSON verification reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Weipu OA network requests, SQLite caching, retry backoff, rate limiting, a daily download quota, and optional PyMuPDF-based PDF checks.]

## Skill Version(s):

2.0.0 (source: release evidence, SKILL.md frontmatter, skillhub-meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
