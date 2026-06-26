## Description: <br>
Audio2srtlocal helps an agent generate and run a local Audio2SRT web app for Apple Silicon Macs that transcribes audio with MLX Whisper, translates SRT output, and launches a Python aiohttp backend with a Vite React frontend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create a local audio transcription and SRT translation project without cloning a remote source repository. It is intended for Apple Silicon macOS environments with Python and Node.js available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated backend exposes unauthenticated transcription APIs beyond the documented localhost-only use. <br>
Mitigation: Bind the backend to localhost or otherwise restrict network access before processing private audio. <br>
Risk: The setup writes a project directory, installs dependencies, downloads several gigabytes of models, and runs local web services. <br>
Mitigation: Run it on a trusted machine and network, preferably in a fresh empty target directory, and review the generated files before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yun520-1/audio2srtlocal) <br>
- [File mapping](references/file-mapping.md) <br>
- [Startup script](references/start.sh) <br>
- [Backend transcription server](references/transcribe_server.py) <br>
- [Frontend application](references/src/App.tsx) <br>
- [Whisper ModelScope model](https://www.modelscope.cn/models/mlx-community/whisper-large-v3-turbo-4bit) <br>
- [Qwen ModelScope model](https://www.modelscope.cn/models/mlx-community/Qwen2.5-3B-Instruct-4bit) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with generated project files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local project scaffolding for a Python backend, React frontend, model directory, dependency installation, and startup workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
