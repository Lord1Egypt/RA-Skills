## Description: <br>
Interact with the system clipboard (text only) using `xclip` from any OpenClaw session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to copy text or file contents to the local system clipboard and to read text from it during OpenClaw sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clipboard contents may be visible to operating system clipboard history or other local applications. <br>
Mitigation: Only copy or paste text and file contents that are appropriate to expose through the local clipboard. <br>
Risk: The skill depends on `xclip`, so clipboard operations will fail on systems where it is missing or unavailable. <br>
Mitigation: Install `xclip` before use and verify clipboard behavior in the target Linux environment. <br>


## Reference(s): <br>
- [ClawHub Clipboard skill page](https://clawhub.ai/Xejrax/clipboard) <br>
- [Publisher profile](https://clawhub.ai/user/Xejrax) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local `xclip` binary for clipboard operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
