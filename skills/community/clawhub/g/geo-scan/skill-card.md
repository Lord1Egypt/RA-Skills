## Description:

Audit the answer-engine readiness (ChatGPT, Perplexity, Claude, Gemini, AI Overviews) of one public website URL and produce a prioritised fix list. Use when someone gives a public site or page URL and asks whether AI engines can crawl, cite or quote it, or wants its robots.txt / snippet-permission / schema check or quotability score. Not for - private or intranet hosts, JS-rendered SPAs, SEO keyword research, writing content to beat competitors. English and German quotability scoring. No API key, no account, Python stdlib only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aureliusclaw](https://clawhub.ai/user/aureliusclaw)

### License/Terms of Use:

MIT

## Use Case:

Website owners and developers use the skill to assess how answer engines can crawl, parse, and quote a public page, then prioritize technical fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a possible CPU-stalling regular-expression issue; its analysis was partial.

Mitigation: Review the reported regex behavior and obtain a complete security review before installing.

Risk: ClawScan flags a private-network scanning option despite the documented public-only scope; its analysis was partial.

Mitigation: Use the public-only plugin mode and review the standalone private-scan option before enabling it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/aureliusclaw/skills/geo-scan)
- [Project homepage](https://github.com/AureliusClaw/geo-scan)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown or JSON audit report with evidence and prioritized actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A 0–100 technical readiness score with evidence; English and German quotability scoring. It does not establish whether an answer engine will cite a page.]

## Skill Version(s):

1.2.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
