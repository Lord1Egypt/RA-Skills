## Description:

Local-generate and deploy the Audio2SRT project, a MLX Whisper audio transcription and translation Web GUI for Apple Silicon Macs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create a local Audio2SRT transcription and translation web application from bundled templates, install its Python and Node.js dependencies, and launch the local backend and frontend services. It is aimed at Apple Silicon Mac workflows that need local audio-to-SRT generation without cloning source code from a remote repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated backend exposes unauthenticated APIs that may be reachable beyond the local browser session.

Mitigation: Bind the backend to 127.0.0.1, restrict CORS to the frontend origin, and add a session token before use on a shared network.

Risk: The backend can process local audio file paths and uploaded files, which can consume local disk, memory, or compute resources.

Mitigation: Remove arbitrary file_path processing, cap upload sizes and job duration, and clean temporary files after processing.

Risk: Dependency and model downloads occur at install or startup time and are not pinned by lockfiles.

Mitigation: Review and pin Python and Node.js dependencies and verify model sources before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/audio2srtlocal)
- [Publisher profile](https://clawhub.ai/user/yun520-1)
- [Skill instructions](artifact/SKILL.md)
- [File mapping](artifact/references/file-mapping.md)
- [Startup script](artifact/references/start.sh)
- [Backend server template](artifact/references/transcribe_server.py)
- [Whisper model on ModelScope](https://www.modelscope.cn/models/mlx-community/whisper-large-v3-turbo-4bit)
- [Qwen translation model on ModelScope](https://www.modelscope.cn/models/mlx-community/Qwen2.5-3B-Instruct-4bit)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local React/Vite frontend, Python aiohttp backend, dependency files, and a startup script.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
