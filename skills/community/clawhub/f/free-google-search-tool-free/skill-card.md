## Description:

谷歌搜索(免费版) helps agents run lightweight Google searches through browser automation, parse titles, URLs, and snippets, filter results, and export search outputs without requiring a Google API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation teams use this skill for quick Google search, SEO keyword checks, lightweight research collection, and result export through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser automation and local command execution for Google searches, with documented ability to write exported result files.

Mitigation: Install and run it in a dedicated workspace, and require agent confirmation before executing local commands or writing exported files.

Risk: The security evidence flags unsafe install guidance around piping a remote Bun installer script to the shell.

Mitigation: Prefer Node.js or a verified package-manager installation path, and review any remote installer before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/free-google-search-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Detailed reference](references/detail.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV files, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with command examples and structured search results exported as JSON, CSV, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write exported search result files when the agent runs the documented exporter.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
