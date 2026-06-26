## Description: <br>
Search Pixabay for stock videos by keywords, filtering by type, category, and duration, returning video URLs and metadata for footage sourcing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to search for stock video assets through the dLazy CLI and return candidate footage URLs with metadata for sourcing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key that may be stored in local CLI configuration or supplied through an environment variable. <br>
Mitigation: Use organization-scoped keys, keep configuration files restricted to the current OS user, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Search requests are sent through the dLazy hosted API rather than directly to Pixabay. <br>
Mitigation: Avoid submitting sensitive search terms and install only if this third-party API routing is acceptable for the user or organization. <br>
Risk: Using a global CLI install leaves a persistent binary on the system. <br>
Mitigation: Use the documented npx invocation when a temporary, pinned CLI execution is preferred. <br>


## Reference(s): <br>
- [Dlazy Search Video on ClawHub](https://clawhub.ai/dlazyai/dlazy-search-video) <br>
- [dLazy CLI repository](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy](https://dlazy.com) <br>
- [dLazy API key management](https://dlazy.com/dashboard/organization/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON returned by the dLazy CLI, with Markdown guidance for setup and error handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns video URLs and metadata; async mode can return a generateId for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
