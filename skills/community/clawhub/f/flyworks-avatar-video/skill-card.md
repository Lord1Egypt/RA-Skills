## Description: <br>
Generate videos using Flyworks (a.k.a HiFly) Digital Humans. Create talking photo videos from images, use public avatars with TTS, or clone voices for custom audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linhui99](https://clawhub.ai/user/linhui99) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content creators use this skill to guide an agent through creating avatar videos, talking-photo videos, and cloned-voice TTS videos with Flyworks/HiFly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process face and voice media through a remote Flyworks/HiFly service. <br>
Mitigation: Only upload portraits and voice samples that the user owns or has explicit permission to use, and review the provider's retention, deletion, and acceptable-use terms before processing sensitive media. <br>
Risk: Generated avatar or cloned-voice media can be misused for impersonation or misleading content. <br>
Mitigation: Confirm consent for custom likeness and voice use, keep generated media aligned with the user's stated purpose, and review outputs before sharing. <br>
Risk: Flyworks/HiFly API tokens are sensitive credentials. <br>
Mitigation: Use a user-owned token when needed, store it in HIFLY_API_TOKEN, and avoid logging or committing tokens. <br>


## Reference(s): <br>
- [Authentication](references/authentication.md) <br>
- [Avatars](references/avatars.md) <br>
- [Voices](references/voices.md) <br>
- [Video Generation](references/video-generation.md) <br>
- [Flyworks](https://flyworks.ai) <br>
- [HiFly User Settings](https://hifly.cc/setting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and CLI output such as avatar IDs, voice IDs, task status, and video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, requests, network access to hfw-api.hifly.cc, and a Flyworks/HiFly token for unrestricted use] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
