## Description:

Fetches CCTV Xinwen Lianbo titles and summaries for a specified date and helps produce a basic categorized news brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query one day of CCTV News content, classify items into basic domestic and international groups, and generate a lightweight brief for review or content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and includes broad activation language that could cause it to run outside the intended CCTV news-query workflow.

Mitigation: Invoke it only for explicit CCTV news date queries and review proposed commands before execution.

Risk: The artifact includes a curl-to-bash Bun installation command.

Mitigation: Use an already installed Node.js runtime or a verified package-manager installation path; do not run the remote installer unless it has been independently reviewed and trusted.

Risk: Local JSON and cache examples may persist fetched content on disk.

Mitigation: Manage or delete generated JSON and cache files according to the workspace's retention needs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce structured JSON news data and plain-text news briefs; free version is limited to single-day queries and title or summary level content.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
