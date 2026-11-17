## Description:

Execute code on Google Colab GPU runtimes (T4/L4/A100/H100) and manage persistent storage via Google Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isotrivial](https://clawhub.ai/user/isotrivial)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run GPU-backed experiments, model training, inference, text-to-speech generation, and Drive-backed checkpoint workflows on Google Colab when local hardware is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses reusable Google OAuth credentials for Colab and optional Drive access.

Mitigation: Use a dedicated Google account or project where practical, grant only the needed scopes, and revoke or rotate tokens after use.

Risk: Code and token-bearing scripts may be transmitted to Colab runtimes, and Drive workflows can move files into Google Drive.

Mitigation: Review scripts before execution, avoid embedding sensitive secrets in submitted code, and use Drive persistence only for files intended to leave the local machine.

Risk: Voice workflows can send voice identifiers, reference audio, text, or API credentials to ElevenLabs and Colab-backed TTS tooling.

Mitigation: Use non-sensitive voice data, avoid passing real API keys as command-line arguments, and confirm that voice data use is authorized.

## Reference(s):

- [Colab examples](references/examples.md)
- [Google Colab MCP](https://github.com/googlecolab/colab-mcp)
- [Google Drive API](https://console.developers.google.com/apis/api/drive.googleapis.com)
- [ClawHub skill page](https://clawhub.ai/isotrivial/skills/colab)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets; runtime commands may return text, JSON markers, base64 audio markers, or generated files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or transfer local files, Google Drive files, Colab runtime state, virtual environment dependencies, and audio outputs depending on the selected command.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
