## Description: <br>
Convert static character images into vivid action videos with Jimeng Dream Actor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call dLazy's hosted Jimeng Dream Actor service from an agent workflow, sending prompts and image or video references to generate animated character media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced media are sent to dLazy's hosted service. <br>
Mitigation: Install only when this data sharing is acceptable for the user's workflow and avoid sending sensitive media or prompts without approval. <br>
Risk: The skill requires sensitive credentials and can persist an API key in local CLI configuration. <br>
Mitigation: Use DLAZY_API_KEY for less persistent credential storage when appropriate, and rotate or revoke the key from the dLazy dashboard if exposure is suspected. <br>
Risk: Global installation of @dlazy/cli adds third-party executable code to the user's environment. <br>
Mitigation: Review the @dlazy/cli package or source before global installation, or use npx for on-demand execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-jimeng-dream-actor) <br>
- [Publisher profile](https://clawhub.ai/user/dlazyai) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration guidance] <br>
**Output Format:** [CLI JSON responses with generated media URLs or async task status, plus concise setup and error-handling guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx, @dlazy/cli, and a dLazy API key. Prompts and referenced media may be sent to dLazy API and media storage endpoints.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
