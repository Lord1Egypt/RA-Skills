## Description:

Downloads music from user-provided links by searching Bandcamp, Beatport, Amazon Music, Spotify, and YouTube for the best available source, preferring extended mixes and MP3 320k output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinnnnn](https://clawhub.ai/user/robinnnnn)

### License/Terms of Use:


## Use Case:

DJs, music curators, and agents assisting them use this skill to source tracks from user-provided links, return purchase links for paid sources, download from free sources, and clean MP3 filenames after download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use external downloader tools to retrieve music from online platforms.

Mitigation: Install downloader tools in an isolated environment and use the skill only for music the user is allowed to access.

Risk: The filename normalization script renames MP3 files in place.

Mitigation: Run normalization only on a dedicated download folder or a backup copy of the files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and download or purchase-link results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create MP3 files through external downloader tools and may rename local MP3 files in place during filename normalization.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
