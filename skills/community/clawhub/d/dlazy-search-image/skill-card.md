## Description: <br>
Image search tool: queries Pixabay image API by keywords and returns image URLs and metadata for references, backgrounds, and design assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to run dLazy image searches and retrieve image URLs and metadata for references, backgrounds, and design assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and stores or accepts sensitive credentials. <br>
Mitigation: Use a scoped dLazy organization key, prefer per-invocation environment variables when appropriate, and rotate or revoke the key from the dLazy dashboard if it may have been exposed. <br>
Risk: The skill asks users to install and run a third-party CLI that sends search parameters through dLazy services. <br>
Mitigation: Review the dLazy CLI and service terms before installation, pin the CLI version where possible, and avoid sending sensitive prompts or file paths through the service unless approved for the workflow. <br>
Risk: The security review flags uncertainty about whether dLazy merely proxies Pixabay or independently processes requests. <br>
Mitigation: Clarify the service behavior before relying on this skill for sensitive or regulated image-search workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-search-image) <br>
- [Publisher profile](https://clawhub.ai/user/dlazyai) <br>
- [dLazy](https://dlazy.com) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, json, guidance] <br>
**Output Format:** [JSON responses from the dLazy CLI, with Markdown guidance for authentication, errors, and command usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include image URLs and metadata; async mode may return a task identifier for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
