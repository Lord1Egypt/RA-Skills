## Description:

ApplyTop is a CLI and Node client for the ApplyTop public API that lets agents search jobs and work with alerts, matches, saved jobs, CVs, ATS scoring, CV tailoring, and cover-letter generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shman2000](https://clawhub.ai/user/shman2000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to instruct an agent on ApplyTop CLI and Node client workflows for job search, alerts, matches, saved jobs, CV management, and paid AI resume actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run an external npm CLI that may not be pinned to a reviewed version.

Mitigation: Install only after reviewing the ApplyTop npm package and publisher, and prefer a pinned version that has been reviewed.

Risk: API keys, CV data, and account details may be handled by the CLI or saved on the local machine.

Mitigation: Use environment variables or saved credentials carefully, avoid passing real API keys on shared command lines, and clear or rotate saved credentials on shared machines.

Risk: Some commands consume paid ApplyTop AI credits and charge the key owner.

Mitigation: Check the account credit balance before running AI commands, and review commands that invoke CV tailoring, cover-letter generation, or ATS scoring.

Risk: Custom API URLs or insecure TLS options can send credentials or CV data to unintended endpoints.

Mitigation: Use the default ApplyTop production API unless you control the endpoint, and do not use --insecure outside controlled development environments.

## Reference(s):

- [ApplyTop website](https://applytop.com)
- [ApplyTop API key dashboard](https://applytop.com/dashboard/api-keys)
- [Server-resolved source repository](https://github.com/shman2000/applytop-agent)
- [ClawHub skill page](https://clawhub.ai/shman2000/skills/applytop-agent)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, JSON examples, and JavaScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on ApplyTop CLI and Node client usage; CLI commands described by the skill emit JSON.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
