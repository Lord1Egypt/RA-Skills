## Description: <br>
Automatically publishes videos to Douyin by uploading a video file, filling title and description fields, and handling SMS verification when required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-j-j](https://clawhub.ai/user/mr-j-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and operators use this skill to automate video publishing workflows on Douyin Creator Center from a local environment with an existing logged-in browser profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in Douyin creator account and can publish content through that account. <br>
Mitigation: Use an isolated workspace or account, confirm the intended video and title before running, and install only if that level of account control is acceptable. <br>
Risk: An existing draft may be discarded during the upload flow. <br>
Mitigation: Check Douyin Creator Center for important drafts before running the publish command. <br>
Risk: Local browser profile and screenshot files may contain account or content details. <br>
Mitigation: Protect the working directory, avoid shared machines, and delete chrome_profile and screenshots when they are no longer needed. <br>


## Reference(s): <br>
- [Douyin Creator Center](https://creator.douyin.com/) <br>
- [ClawHub skill page](https://clawhub.ai/mr-j-j/douyin-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Playwright-driven browser automation script and writes local browser profile, SMS state, and screenshot files.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
