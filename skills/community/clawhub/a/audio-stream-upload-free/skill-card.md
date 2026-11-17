## Description:

音频流上传免费版 helps agents guide users through creating an audio object, uploading a local audio file to a streaming API, and retrieving an HLS playback link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to prepare and run a basic three-step audio upload workflow for podcasts, voice content, or original music. It is intended for explicitly chosen local audio files and returns upload status, audio identifiers, and HLS playback links when the streaming API succeeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send local media files and streaming API credentials to a third-party service.

Mitigation: Use it only for explicit audio upload tasks, only with files the user intentionally chooses, and only when the user trusts the third-party streaming API.

Risk: API keys may be exposed if pasted into shell commands, logs, or generated scripts.

Mitigation: Store keys in environment variables or a secret manager and avoid echoing credentials in commands, logs, or shared output.

Risk: The trigger language is broader than the actual audio upload behavior and may be invoked for video processing, editing, conversion, or dubbing requests.

Mitigation: Limit use to audio upload and HLS link retrieval; choose a different workflow for general media processing or editing tasks.

Risk: The skill asks the agent to execute shell commands that read local files and perform network uploads.

Mitigation: Review proposed commands before execution, verify file paths and API endpoints, and avoid interpolating untrusted user input into shell commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python snippets plus expected API response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided audio file paths and streaming API credentials; may return operation status, audio IDs, and HLS links.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
