## Description:

轻量级联网搜索工具，支持 Bing 与 DuckDuckGo 双引擎自动路由，针对中文环境优化，适合个人日常信息检索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, researchers, and external users use this skill to run lightweight web searches, retrieve result summaries, and optionally fetch page text through an agent with browser and command execution capability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and file-read authority for package setup, browser setup, and search workflows.

Mitigation: Approve only commands that are necessary for dependency installation, browser setup, or the intended search task, and review commands before execution.

Risk: Full-text fetching may send sensitive queries or visit result pages that are not necessary for the task.

Mitigation: Avoid sensitive internal queries and keep full-text fetching disabled unless page content is required.

Risk: The artifact includes broad generic automation claims beyond the scoped web-search helper.

Mitigation: Treat file, API, and general command automation claims as out of scope unless each action is explicitly reviewed and approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/free-web-search-tool-free)
- [Publisher Profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and search-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-query searches return up to 10 results; optional full-text fetching covers up to 5 results with page text truncated at 8000 characters.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
