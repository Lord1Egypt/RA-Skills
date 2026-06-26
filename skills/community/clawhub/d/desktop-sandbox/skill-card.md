## Description: <br>
Desktop Sandbox installs AtlasCore Desktop Sandbox so OpenClaw can run with a native desktop experience in an isolated environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasCore-tech](https://clawhub.ai/user/AtlasCore-tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to download and run the AtlasCore Desktop Sandbox installer from GitHub releases on supported desktop platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs native installer packages from GitHub releases. <br>
Mitigation: Install only from a trusted AtlasCore release, prefer a pinned version, and verify installer signatures or hashes where available before execution. <br>
Risk: The installer can make persistent system-level changes and may require administrator approval. <br>
Mitigation: Run it in an environment where persistent desktop software installation is intended, and review operating system prompts before approving installation. <br>
Risk: The scanner reported limited confirmation controls around installer execution. <br>
Mitigation: Require explicit user approval before invoking the installer command and document the expected platform-specific installation target. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AtlasCore-tech/desktop-sandbox) <br>
- [AtlasCore-tech publisher profile](https://clawhub.ai/user/AtlasCore-tech) <br>
- [AtlasCore Desktop Sandbox GitHub repository](https://github.com/AtlasCore-tech/desktop-sandbox-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and runs a native platform installer when invoked.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
