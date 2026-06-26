## Description: <br>
Execute Python code on Google Colab GPU runtimes, manage Google Drive persistence, and run GPU-heavy workflows such as ML experiments, inference, training, and F5-TTS voice synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isotrivial](https://clawhub.ai/user/isotrivial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run GPU-dependent Python workloads on Colab when local hardware is insufficient. It supports runtime management, Google Drive checkpoint transfer, and voice synthesis workflows that need remote GPU compute. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute code on remote Colab runtimes and consume Colab resources. <br>
Mitigation: Review scripts before execution, avoid untrusted generated code, and stop kept-alive runtimes when work is complete. <br>
Risk: The skill can read the local Colab OAuth token and inject it into remote runtime scripts for Drive access. <br>
Mitigation: Use token injection only with reviewed scripts, limit Drive access to the documented drive.file scope, and revoke or rotate exposed tokens. <br>
Risk: Voice samples or transcripts may be sent to remote services during TTS workflows. <br>
Mitigation: Avoid sensitive voice data, obtain appropriate consent for voice cloning, and review remote service use before running TTS commands. <br>
Risk: The skill installs Python dependencies into a local virtual environment during first use. <br>
Mitigation: Run it in an isolated environment and pin or review dependencies where repeatability or supply-chain control matters. <br>


## Reference(s): <br>
- [Colab Examples](references/examples.md) <br>
- [googlecolab/colab-mcp](https://github.com/googlecolab/colab-mcp) <br>
- [Google Drive API](https://console.developers.google.com/apis/api/drive.googleapis.com) <br>
- [Google Colab](https://colab.research.google.com) <br>
- [ElevenLabs Voices API](https://api.elevenlabs.io/v1/voices/{voice_id}) <br>
- [ClawHub Skill Page](https://clawhub.ai/isotrivial/colab) <br>
- [Publisher Profile](https://clawhub.ai/user/isotrivial) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, runtime output, and file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Colab execution output, Drive transfer results, runtime state, checkpoints, and audio files depending on the invoked workflow.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
