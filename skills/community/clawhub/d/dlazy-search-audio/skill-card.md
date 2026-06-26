## Description: <br>
Searches royalty-free background music on Pixabay Music and returns track URLs and metadata for audio selection with dLazy API authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to search for background music candidates and retrieve track metadata through the dLazy CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key that may be stored in local CLI configuration. <br>
Mitigation: Treat the dLazy API key as a credential, restrict access to the local config, and rotate or revoke the key if exposure is suspected. <br>
Risk: Search queries, parameters, and provided media inputs may be sent to dLazy services for processing. <br>
Mitigation: Use the skill only for inputs appropriate for dLazy remote processing and avoid sending sensitive media or confidential search context. <br>
Risk: Installing the dLazy CLI globally can leave a persistent executable on the system. <br>
Mitigation: Use the npx invocation or a reviewed pinned CLI version when a persistent global install is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-search-audio) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires dLazy API authentication and may return asynchronous task identifiers for polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
