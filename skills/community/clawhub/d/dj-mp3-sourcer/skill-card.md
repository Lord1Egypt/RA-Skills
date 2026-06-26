## Description: <br>
Downloads music from links by finding available sources across Bandcamp, Beatport, Amazon Music, Spotify, and YouTube, with MP3 320k output and a free-only mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robinnnnn](https://clawhub.ai/user/Robinnnnn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
DJs and music collectors use this skill to resolve single tracks or batch lists from mixed music links, surface paid purchase options, download free sources, and normalize downloaded MP3 filenames for music they have the right to access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The filename-normalization script can move MP3 files outside the chosen folder if track metadata contains path-like artist or title values. <br>
Mitigation: Sanitize artist and title values before normalization, reject slashes and '..', use a dry run where possible, and work in a disposable output folder. <br>
Risk: The skill can download or link to music from external platforms. <br>
Mitigation: Use it only for purchases, free releases, Creative Commons works, or music the user has the right to access, and follow copyright laws in the relevant jurisdiction. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file-handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce purchase links for paid sources and filename-normalization steps for downloaded MP3 files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
