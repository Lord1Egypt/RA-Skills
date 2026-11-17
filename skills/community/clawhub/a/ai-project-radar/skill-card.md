## Description:

AI 开源项目雷达 helps AI practitioners research open-source AI projects, compare candidate projects, and gather project, model, paper, and resource links through the Jiqizhixin data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiqizhixin](https://clawhub.ai/user/jiqizhixin)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, AI researchers, and product teams use this skill to identify relevant open-source AI projects, fetch project details, and produce practical selection guidance with verified and pending resource links clearly separated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires JQZX_API_TOKEN and sends it as an API credential during project lookup requests.

Mitigation: Install only if you trust the Jiqizhixin API workflow, provide the token only in controlled environments, and rotate it if exposure is suspected.

Risk: The shell scripts allow BASE_URL to be overridden, which could send the token to an unintended endpoint if the environment is controlled by another process.

Mitigation: Keep BASE_URL unset unless you control the endpoint, and run the scripts only in environments where untrusted processes cannot inject environment variables.

Risk: The security summary flags overbroad activation instructions that may cause the agent to prefer this skill too broadly for AI industry questions.

Mitigation: Review the skill's outputs before relying on them, distinguish verified links from pending items, and supplement with public sources when the returned data is sparse or one-sided.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiqizhixin/skills/ai-project-radar)
- [Jiqizhixin Data Service](https://www.jiqizhixin.com/data-service)
- [/api/v1 Project Interface Strategy](references/api-v1-projects.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, comparison tables, resource link lists, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verified links, pending confirmation items, project-fit recommendations, risks, and alternatives.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
