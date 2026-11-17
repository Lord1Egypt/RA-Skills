## Description:

Deep Research (Gemini) lets agents run asynchronous Gemini deep research, ground queries on local files, preview costs, and return structured research output without depending on Gemini CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[24601](https://clawhub.ai/user/24601)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and AI agents use this skill to launch Gemini deep research jobs, optionally ground research in local files, estimate cost before upload, and save reports or JSON outputs for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository context uploads may include sensitive files because the file-upload safeguards do not consistently match the documented exclusion promise.

Mitigation: Use --dry-run before upload, prefer narrow directory context over direct sensitive-looking files, and restrict the agent's filesystem access.

Risk: Gemini file-search stores may remain after failures or non-blocking runs.

Mitigation: Manually check and delete Gemini file-search stores after failures or non-blocking research runs.

Risk: Exported HTML reports may contain untrusted content.

Mitigation: Treat exported HTML as untrusted unless it is sanitized or opened in a constrained environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/24601/skills/agent-deep-research)
- [Project Homepage](https://github.com/24601/agent-deep-research)
- [Online Documentation References](references/online_docs.md)
- [File Search MIME Type Guide](references/file_search_guide.md)
- [Gemini Deep Research API](https://ai.google.dev/gemini-api/docs/deep-research)
- [Gemini File Search API](https://ai.google.dev/gemini-api/docs/file-search)
- [Google GenAI Python SDK](https://googleapis.github.io/python-genai/)
- [uv Documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON status and metadata, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports, metadata, interaction records, and extracted source files to an output directory.]

## Skill Version(s):

2.1.3 (source: server release metadata; artifact frontmatter and changelog show 2.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
