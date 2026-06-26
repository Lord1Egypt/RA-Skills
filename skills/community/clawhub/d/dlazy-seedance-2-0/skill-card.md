## Description: <br>
ByteDance's latest video generation model. Supports multi-modal reference (images, video, audio) to generate videos, as well as first/last frame and text-to-video modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to invoke dLazy's hosted Seedance 2.0 video generation workflow from an agent, using text prompts and optional image, video, audio, or frame references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key, which may be saved in local CLI configuration. <br>
Mitigation: Use a revocable dLazy API key, rotate it when needed, or pass it per invocation with DLAZY_API_KEY when persistent local storage is not desired. <br>
Risk: Local image, video, or audio inputs passed to the CLI may be uploaded to dLazy-hosted services for generation. <br>
Mitigation: Only provide media files intended for upload to dLazy and avoid sending sensitive or unauthorized content. <br>
Risk: The install command tracks the latest published @dlazy/cli package. <br>
Mitigation: Review the @dlazy/cli package or source before installation and pin a reviewed version when deployment policy requires deterministic dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-seedance-2-0) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [JSON responses and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media URLs are returned by the hosted dLazy service; asynchronous calls can return a task identifier for polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
