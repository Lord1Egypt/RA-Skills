## Description: <br>
Search and retrieve royalty-free media from Pexels (photos/videos), Pixabay (images/videos), Freesound (audio effects), and Jamendo (music/BGM). Use when the user needs to find stock photos, illustrations, vectors, videos, sound effects, or background music, download media, or query media libraries with filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darknoah](https://clawhub.ai/user/darknoah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use this skill to search media libraries and download royalty-free photos, videos, sound effects, and music for projects while managing provider attribution and licensing obligations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires API keys for media services. <br>
Mitigation: Provide keys through environment variables or a local config file, keep them out of prompts and shared files, and rotate keys if they are exposed. <br>
Risk: The security scan notes under-documented original-download behavior and broad URL-to-file download commands. <br>
Mitigation: Download only from provider search results or trusted provider URLs, avoid arbitrary or private-network URLs, and choose non-sensitive output folders. <br>
Risk: Downloaded media can carry provider-specific attribution, license, and original-file usage requirements. <br>
Mitigation: Review provider metadata and Freesound licensing before reuse, and include required attribution for Pexels, Pixabay, Freesound, and Jamendo assets. <br>


## Reference(s): <br>
- [API Reference](references/api_reference.md) <br>
- [Pexels API](https://www.pexels.com/api/) <br>
- [Pixabay API](https://pixabay.com/api/) <br>
- [Freesound API](https://freesound.org/apiv2/apply) <br>
- [Jamendo Developer Portal](https://devportal.jamendo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI scripts return JSON search results and downloaded media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires provider API keys and can write result JSON or downloaded media to user-specified output paths.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
