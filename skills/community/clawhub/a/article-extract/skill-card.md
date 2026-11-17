## Description:

Article Extract fetches web article pages, including WeChat, blogs, and news sites, and extracts readable plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caozeal](https://clawhub.ai/user/caozeal)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve an article URL and produce cleaned plain-text content for downstream reading, summarization, or archival workflows. It is oriented toward Chinese and WeChat article extraction but also describes support for blogs and news pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches arbitrary user-supplied URLs and may be exposed to server-side request forgery or private-network access if an agent supplies unsafe targets.

Mitigation: Restrict use to trusted URLs, require HTTP or HTTPS schemes, block localhost, private-network, metadata-service, and file targets, and consider an allowlist before deployment.

Risk: The skill advertises anti-scraping bypass behavior for Chinese and WeChat-oriented article extraction.

Mitigation: Use it only where fetching and extracting the target content is authorized and consistent with applicable site terms and organizational policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caozeal/skills/article-extract)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text emitted to stdout, with Markdown usage guidance and shell command examples in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The extraction script accepts a single URL argument and prints extracted article text; stderr is used for fetch status and errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
