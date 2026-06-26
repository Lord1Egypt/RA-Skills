## Description: <br>
4MP high-resolution raster image generation. Suitable for print-ready assets and large-scale use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call the dLazy Recraft V4 Pro image generation service from an agent workflow and receive high-resolution raster image results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release installs @dlazy/cli with the @latest tag, so the installed CLI can change over time. <br>
Mitigation: Install only if you trust dLazy and the current @dlazy/cli package; prefer a pinned CLI version where possible and review the linked source or package before global install. <br>
Risk: The skill requires a dLazy API key and sends prompts, parameters, and any referenced local media files to dLazy services. <br>
Mitigation: Use an appropriate dLazy account, avoid sending sensitive inputs unless approved for the use case, and rotate or revoke the API key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-recraft-v4-pro) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Files, Guidance] <br>
**Output Format:** [JSON result objects with generated image URLs and optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx, a dLazy API key, and network access to dLazy API and file endpoints.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
