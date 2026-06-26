## Description: <br>
All in One Video AI Editor helps agents upload MP4 or MOV files to Sparki, start AI video-editing projects for shorts, captions, resizing, highlights, vlogs, montages, and talking-head clips, and return a processed video download URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sparki-dev](https://clawhub.ai/user/sparki-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and content teams use this skill to automate agent-driven video editing workflows: upload local footage, submit natural-language editing direction and style tips to Sparki, and retrieve the completed download URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads user videos and sends SPARKI_API_KEY to agent-api-test.aicoding.live, which evidence.security flags as an unexplained non-Sparki test domain. <br>
Mitigation: Use only after verifying that endpoint is intended by Sparki, and avoid confidential, regulated, personal, or otherwise sensitive footage. <br>
Risk: The artifact encourages broad proactive use for video-editing requests, which could send files to a remote service before the user has evaluated privacy or data handling implications. <br>
Mitigation: Confirm user intent, file scope, and API-key context before running upload or edit scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sparki-dev/all-in-one-video-ai-editor) <br>
- [Publisher profile](https://clawhub.ai/user/sparki-dev) <br>
- [Sparki homepage](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; scripts return plain-text object keys, project status, or a download URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and SPARKI_API_KEY; uploads MP4/MOV files up to 3 GB to a remote service and result URLs expire after 24 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and README mention 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
