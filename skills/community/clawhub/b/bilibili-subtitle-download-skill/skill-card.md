## Description:

Downloads Bilibili video and course subtitles, splits transcript text into large chunks for LLM processing, and provides a prompt pattern for structured summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davincievans](https://clawhub.ai/user/davincievans)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to retrieve subtitles from Bilibili videos or course episodes and split them into text chunks for LLM-based summarization, key point extraction, and detailed content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Bilibili account authentication and stores reusable cookie or session files in plaintext.

Mitigation: Run it only in a private, non-shared workspace and treat generated cookie/session files as secrets.

Risk: Plaintext credential files may remain after subtitle extraction.

Mitigation: Delete ~/.openclaw/workspace/bilibili_cookie.txt and any bilibili_cheese_session.json file when finished.

Risk: Credential files and downloaded subtitle chunks could be exposed from synced or source-controlled directories.

Mitigation: Avoid running the skill from synced or source-controlled directories until credential storage and URL validation are improved.

## Reference(s):

- [Bilibili website](https://www.bilibili.com/)
- [Bilibili video metadata API](https://api.bilibili.com/x/web-interface/view)
- [Bilibili player subtitle API](https://api.bilibili.com/x/player/v2)
- [ClawHub skill page](https://clawhub.ai/davincievans/skills/bilibili-subtitle-download-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-reported chunk file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local subtitle chunk text files under bili_temp and may emit QR-code login status messages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
