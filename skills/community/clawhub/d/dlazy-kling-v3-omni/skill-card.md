## Description: <br>
Versatile video generation with Kling v3 Omni. Supports multi-modal inputs to generate stunning dynamic videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to invoke dLazy's Kling v3 Omni video generation through the dLazy CLI, supplying prompts and optional image or video references to produce hosted media outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may store it in the local CLI configuration. <br>
Mitigation: Use DLAZY_API_KEY for per-run credentials when local persistence is undesirable, and rotate or revoke keys from dLazy when needed. <br>
Risk: Prompts and referenced media files are sent to dLazy's hosted API and media storage. <br>
Mitigation: Avoid passing private or sensitive prompts and media unless that upload is intended. <br>
Risk: The install command uses the latest @dlazy/cli package at execution time. <br>
Mitigation: Install only after reviewing the package and source links, or run with npx for on-demand use. <br>


## Reference(s): <br>
- [Dlazy Kling V3 Omni on ClawHub](https://clawhub.ai/dlazyai/dlazy-kling-v3-omni) <br>
- [dLazy CLI repository](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown instructions with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated results are returned as hosted media URLs; asynchronous requests may return a generateId for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
