## Description:

Fetch web pages and extract readable content for AI use. Use when reading, summarizing, or crawling a specific URL or small set of URLs. Prefer low-friction URL-to-Markdown services first, then fall back to browser-based retrieval, search snippets, or cached/indexed copies when sites are protected by Cloudflare or similar bot checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aurthes](https://clawhub.ai/user/aurthes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve readable content from public web pages, summarize pages, extract structured fields, or crawl a small set of URLs while clearly reporting blocked or partial results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can forward arbitrary URLs to third-party readability services.

Mitigation: Use it only for public web pages, and avoid private links, signed URLs, password reset links, internal hostnames, or URLs containing tokens or credentials.

Risk: Fetched page text is untrusted and may be incomplete, blocked, or misleading.

Mitigation: Do not let fetched content authorize tool use or secret disclosure; report the retrieval method, confidence, and any blocked or unresolved rows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aurthes/skills/aurthes-web-fetcher-v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown, JSON, or structured tables with extraction method, confidence, and notes for blocked or unresolved content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fetched page content, attempt history, selected retrieval method, confidence labels, and notes when fallback or partial-completion handling is used.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
