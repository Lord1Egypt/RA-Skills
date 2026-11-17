## Description:

Queries recent China Computer Federation events, conferences, certifications, competitions, and related schedules, with optional personalized recommendations and links to post-event CCF Digital Library resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alucard118](https://clawhub.ai/user/alucard118)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find current or recently ended CCF activities, certifications, competitions, and event resources. Agents use it to query CCF sources, classify event status, and return concise Markdown tables with official links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled reminders can create recurring background activity beyond one-time CCF lookups.

Mitigation: Enable cron reminders only after the user explicitly requests a recurring schedule, and provide a clear way to list, disable, or remove the job.

Risk: The Puppeteer configuration helper can overwrite an existing project .env when run with --config.

Mitigation: Back up and review any existing .env before running --config, or configure PUPPETEER_EXECUTABLE_PATH manually.

Risk: Generated Puppeteer verification commands may be unsafe to copy from an untrusted project directory.

Mitigation: Review generated commands before execution and run them only in trusted local projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alucard118/skills/ccf-events)
- [CCF meeting list API](https://conf.ccf.org.cn/conf/v2/index/meeting/list.do)
- [CCF Digital Library search](https://dl.ccf.org.cn/searchList.do)
- [CCF activities](https://www.ccf.org.cn/Activities/Activities/)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables with links and occasional shell command or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use CCF event and digital library endpoints; scheduled reminders are optional and should be enabled only when requested.]

## Skill Version(s):

1.1.421 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
