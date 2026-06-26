## Description: <br>
Manage linkding bookmarks - save URLs, search, tag, organize, and retrieve your personal bookmark collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daveonkels](https://clawhub.ai/user/daveonkels) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and Linkding users use this skill to save, search, tag, organize, archive, delete, and retrieve bookmarks from a configured Linkding instance through the clinkding CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change bookmark data in the configured Linkding instance. <br>
Mitigation: Install only after trusting the clinkding CLI source and review create, update, archive, delete, upload, and download actions before approving them. <br>
Risk: A Linkding API token is required for authenticated use. <br>
Mitigation: Protect the API token and prefer environment variables or configuration files with appropriate local access controls. <br>
Risk: Automatic URL summarization can expose private, internal, or token-bearing URLs to the summarization tool. <br>
Mitigation: Avoid automatic summarization for sensitive URLs unless sharing that URL with the summarization tool is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daveonkels/clinkding) <br>
- [clinkding GitHub repository](https://github.com/daveonkels/clinkding) <br>
- [clinkding releases](https://github.com/daveonkels/clinkding/releases) <br>
- [Linkding project](https://github.com/sissbruecker/linkding) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can request JSON or plain-text CLI output for scripting and agent parsing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
