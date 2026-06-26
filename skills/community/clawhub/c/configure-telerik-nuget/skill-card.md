## Description: <br>
Helps setup, configure and manage Telerik NuGet feeds in your repo's nuget.config file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LanceMcCarthy](https://clawhub.ai/user/LanceMcCarthy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Telerik NuGet package source access in a repository while keeping the Telerik API key in a user-level environment variable rather than hardcoding it in nuget.config. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Telerik API key in a user-level environment variable and configures nuget.config to reference it. <br>
Mitigation: Use a revocable Telerik API key, avoid sharing the environment value, and rotate the key if it may have been exposed. <br>
Risk: The skill edits or creates nuget.config in the selected repository path. <br>
Mitigation: Run it only against the intended repository and review nuget.config changes before committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LanceMcCarthy/configure-telerik-nuget) <br>
- [Publisher profile](https://clawhub.ai/user/LanceMcCarthy) <br>
- [Publisher homepage from clawdis metadata](https://github.com/DevOpsExamples/.github) <br>
- [Telerik API keys](https://www.telerik.com/account/downloads/api-keys) <br>
- [Telerik NuGet v3 feed](https://nuget.telerik.com/v3/index.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell code and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local environment variable updates and nuget.config edits.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
