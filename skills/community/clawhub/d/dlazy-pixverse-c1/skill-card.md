## Description: <br>
PixVerse C1 video generation covers text-to-video, image-to-video, first/last-frame-to-video, and reference-to-video workflows through the dLazy CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and agents use this skill to invoke PixVerse C1 for short video generation from prompts and optional image inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and provided media files are sent to dLazy cloud services. <br>
Mitigation: Use only content approved for dLazy processing and avoid sensitive prompts or media unless permitted by your organization. <br>
Risk: The skill requires a dLazy API key that may be saved in local CLI configuration. <br>
Mitigation: Handle the API key as a secret, prefer per-invocation environment variables when appropriate, and rotate or revoke keys from the dLazy dashboard when needed. <br>
Risk: Using the skill installs or runs the external @dlazy/cli npm package. <br>
Mitigation: Install or run it only when you intend to use dLazy/PixVerse C1, and review the pinned package or source before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-pixverse-c1) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown guidance with bash commands; CLI responses are JSON with generated media URLs or async task status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key; prompts and media paths are sent to dLazy services, and local media inputs may be uploaded.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
