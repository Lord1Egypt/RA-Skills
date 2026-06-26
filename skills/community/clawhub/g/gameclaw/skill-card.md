## Description: <br>
GameClaw helps users identify available terminal games, choose supported Linux or macOS release assets, and run downloaded CLI binaries from GitHub Releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Arcobalneo](https://clawhub.ai/user/Arcobalneo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this prompt-only skill to find GameClaw terminal games, select the correct supported platform package, and receive concise unpack and run instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may download and run a third-party game binary from GitHub. <br>
Mitigation: Confirm the repository, release asset name, and platform before running the binary. <br>
Risk: Users may request an unsupported platform or a missing release asset. <br>
Mitigation: Ask for the target platform when unknown, only claim linux-x86_64 and darwin-arm64 support, and state plainly when an asset is unavailable. <br>


## Reference(s): <br>
- [GameClaw on ClawHub](https://clawhub.ai/Arcobalneo/gameclaw) <br>
- [GameClaw GitHub repository](https://github.com/Arcobalneo/gameclaw) <br>
- [GameClaw latest releases](https://github.com/Arcobalneo/gameclaw/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only guidance; no local source files or runtime tools are required by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
