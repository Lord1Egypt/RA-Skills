## Description:

Fetches articles from WeChat, Xiaohongshu, Douban, and Zhihu, uploads article images to Aliyun OSS, extracts keywords with optional LLM support, and archives the result to Obsidian Markdown with optional Notion sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajayhao](https://clawhub.ai/user/ajayhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to turn supported social and article URLs, HTML, or MHTML captures into archived knowledge-base entries. It is suited for workflows that need Markdown notes, optional Notion records, OSS-hosted images, and generated tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted HTML or MHTML can contain image URLs that the runtime fetches and uploads to OSS before image URL validation is added.

Mitigation: Process only trusted article captures and URLs, and avoid untrusted HTML/MHTML inputs until image URL validation is available.

Risk: Article images are uploaded to a configured Aliyun OSS bucket, so image content leaves the local environment.

Mitigation: Use a dedicated least-privilege OSS bucket and credentials limited to the needed object operations.

Risk: When LLM keyword extraction is configured, article text is sent to the configured LLM endpoint and the endpoint is not forced to HTTPS by the skill.

Mitigation: Configure LLM_BASE_URL with HTTPS only, or leave LLM settings unset to use local keyword extraction.

Risk: The release has a suspicious security verdict and should be reviewed before deployment.

Mitigation: Prefer the pinned requirements.txt installation path and review the configured cloud accounts and input sources before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ajayhao/skills/article-fetcher)
- [Project Homepage](https://github.com/AjayHao/article-fetcher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown files with YAML frontmatter, optional Notion pages, terminal status text, and Python dictionary results when used as a module]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires environment configuration for Aliyun OSS; Obsidian, Notion, cookies, and LLM keyword extraction are optional configuration-dependent outputs.]

## Skill Version(s):

1.3.6 (source: server release evidence, metadata, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
