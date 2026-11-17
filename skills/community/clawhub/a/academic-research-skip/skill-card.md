## Description:

Search academic papers and conduct literature reviews using the OpenAlex API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmyg11](https://clawhub.ai/user/mmyg11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research-support agents use this skill to search scholarly works by topic, author, or DOI; inspect citations and open-access metadata; and generate structured literature-review summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Academic search topics, author names, and DOIs are sent to OpenAlex; DOIs from deep-read requests may be sent to Unpaywall.

Mitigation: Avoid sensitive research queries when external API disclosure is not acceptable.

Risk: The literature-review workflow caches API responses under /tmp/litreview_cache, which may be unsuitable on shared or high-sensitivity systems.

Mitigation: Use the workflow on trusted systems and clear or isolate the cache when handling sensitive topics.

Risk: Generated reports include a publisher attribution link and may contain incomplete or misleading paper metadata from upstream services.

Mitigation: Review generated Markdown or JSON before publishing or relying on it.

## Reference(s):

- [OpenAlex API](https://api.openalex.org)
- [Unpaywall API](https://api.unpaywall.org)
- [Academic Research Skip on ClawHub](https://clawhub.ai/mmyg11/skills/academic-research-skip)
- [Topanga](https://topanga.ludwitt.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance]

**Output Format:** [Markdown, plain text, or JSON; literature reviews may be written to a Markdown or JSON file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include paper metadata such as title, authors, year, abstract when available, citation count, DOI, open-access URL, source, and OpenAlex ID.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
