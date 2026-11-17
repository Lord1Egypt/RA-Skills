## Description:

Generate audio replies using TTS for public URL reading, conversational spoken responses, and voice replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matrixy](https://clawhub.ai/user/matrixy)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill in Claude Code to turn concise assistant replies or public web page summaries into locally generated spoken audio on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied or fetched text may be interpolated into shell-style TTS commands without a safe argument boundary.

Mitigation: Pass TTS text as literal data through a safe command interface and review command construction before installing or using the skill.

Risk: URL reading can expose private, authenticated, signed, or network-internal content if validation is incomplete.

Mitigation: Use only public, non-sensitive http(s) URLs; validate redirects and resolved addresses; refuse private, local, credentialed, or sensitive links.

Risk: The skill runs uv locally and may download and execute the TTS package and model.

Mitigation: Install uv from a trusted source, review the local execution path, and use the skill only in environments where local TTS package execution is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matrixy/skills/audio-reply-skill)
- [Source homepage](https://github.com/MaTriXy/audio-reply-skill)
- [MLX Audio](https://github.com/Blaizzy/mlx-audio)
- [chatterbox-turbo-fp16 model](https://huggingface.co/mlx-community/chatterbox-turbo-fp16)
- [MLX](https://github.com/ml-explore/mlx)
- [uv package manager](https://github.com/astral-sh/uv)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Conversational text with local TTS shell commands and audio playback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Temporary audio files are expected to be cleaned up after playback; fetched text should be public and non-sensitive.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
