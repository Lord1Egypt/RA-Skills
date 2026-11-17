## Description:

Helps setup, configure and manage Telerik NuGet feeds in your repo's nuget.config file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lancemccarthy](https://clawhub.ai/user/lancemccarthy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure a Telerik NuGet package source and credentials for .NET projects through nuget.config.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores the Telerik API key in a user-wide environment variable.

Mitigation: Review before installing; prefer a process-scoped environment variable, secure credential store, or a version with explicit opt-in and cleanup guidance for removing or rotating the key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lancemccarthy/skills/configure-telerik-nuget)
- [Publisher profile](https://clawhub.ai/user/lancemccarthy)
- [Project homepage](https://github.com/DevOpsExamples/.github)
- [Telerik API keys](https://www.telerik.com/account/downloads/api-keys)
- [Telerik NuGet feed](https://nuget.telerik.com/v3/index.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides a PowerShell helper function that can create or update nuget.config and set a Telerik API key environment variable.]

## Skill Version(s):

1.1.0 (source: frontmatter, release metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
