## Description: <br>
Generate coherent transition videos using Jimeng's first and tail frame models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative automation users use this skill to generate transition videos from first and last frame images through the dLazy Jimeng I2V CLI. It is useful when an agent needs to pass prompts and frame inputs, then return generated media URLs or an asynchronous task identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a dLazy API key for authenticated requests. <br>
Mitigation: Use dLazy login or a scoped API key, keep credentials out of prompts and shared logs, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Local media files passed as inputs may be uploaded to dLazy service endpoints for generation. <br>
Mitigation: Only provide files that are approved for upload to dLazy, and avoid sensitive or private media unless the user has accepted that service flow. <br>
Risk: Execution depends on the external @dlazy/cli npm package. <br>
Mitigation: Review the package or source before installing, prefer the pinned version from the release metadata, and use npx for on-demand execution when a persistent global install is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-jimeng-i2v-first-tail) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [CLI command guidance and JSON results containing generated media URLs or asynchronous task status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key and npm or npx; local media inputs may be uploaded to dLazy service endpoints.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
