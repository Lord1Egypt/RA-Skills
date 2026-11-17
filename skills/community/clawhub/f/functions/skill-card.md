## Description:

Guide Claude through deploying serverless browser automation using the official bb CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peytoncasper](https://clawhub.ai/user/peytoncasper)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, test, deploy, and invoke Browserbase Functions for cloud-hosted browser automation, including scheduled jobs, webhook endpoints, scraping flows, and authenticated workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes credential-handling guidance for Browserbase API keys and project IDs.

Mitigation: Review commands before execution, avoid printing .env values, keep .env out of version control, use the least-privileged Browserbase key available, and rotate keys that appear in logs or shared transcripts.

Risk: The skill recommends package execution and installation commands without pinning package versions.

Mitigation: Pin the Browserbase SDK package version before installing or running CLI commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peytoncasper/skills/functions)
- [Browserbase settings](https://browserbase.com/settings)
- [Browserbase Functions API invocation endpoint pattern](https://api.browserbase.com/v1/functions/FUNCTION_ID/invoke)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, TypeScript, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes CLI setup, environment-variable configuration, local testing, deployment, invocation, polling, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
