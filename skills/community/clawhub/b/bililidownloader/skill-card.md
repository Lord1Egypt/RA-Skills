## Description: <br>
Download Bilibili videos after asking the user for the Bilibili URL, using a Python script that supports single-video and playlist downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caiyundc880518](https://clawhub.ai/user/caiyundc880518) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users ask an agent to collect a Bilibili URL, choose single-video or playlist mode when needed, and run a yt-dlp-based downloader that saves media locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may download the wrong video, format, or playlist scope if the URL or batch mode is unclear. <br>
Mitigation: Confirm the Bilibili URL, desired format, and whether playlist batch mode is intended before running the downloader. <br>
Risk: Downloads create local media files in the current working directory. <br>
Mitigation: Run the script from the intended directory and review created files after completion. <br>
Risk: Account-gated Bilibili content may require cookies. <br>
Mitigation: Avoid providing Bilibili cookies unless the user deliberately needs access to account-gated content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with shell commands and download status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads media files to the current working directory unless the script is run from another location.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
