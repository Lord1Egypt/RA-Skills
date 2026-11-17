## Description:

Automated software development agent using ChatDev 2.0 and GLM-5 that discovers topics from GitHub Trending, CVE databases, and security news, generates code with a 7-agent ChatDev team, tests automatically, self-corrects failures, and publishes to GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rebugui](https://clawhub.ai/user/rebugui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to automate project idea discovery, code generation, testing, self-correction, and publication for software tools and DevOps utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive model-generated code, shell commands, and publication workflows.

Mitigation: Run it only in a disposable container or VM, keep network egress restricted, and manually review commands, generated source, GitHub pushes, and release creation.

Risk: The skill uses GitHub, Notion, and model API credentials.

Mitigation: Use least-privilege tokens, exclude host credential files from the runtime environment, and avoid task queues writable by untrusted users.

## Reference(s):

- [Dev Factory ClawHub skill page](https://clawhub.ai/rebugui/skills/dev-factory)
- [ChatDev 2.0](https://github.com/OpenBMB/ChatDev)
- [NVD CVE API](https://services.nvd.nist.gov/rest/json/cves/2.0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, generated code, and status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project files, tests, repository metadata, Notion updates, and GitHub publication steps when configured with credentials.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
