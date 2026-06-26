## Description: <br>
Optical chemical structure recognition workflow for extracting molecule structures and names from images through SciMiner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chemists, researchers, and agents working with chemistry documents use this skill to submit chemistry images to SciMiner AlphaExtractor and receive extracted molecule structures, names, task status, and share URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chemistry images and related task results are sent to SciMiner, and successful tasks return share_url result pages. <br>
Mitigation: Submit only images and results that your organization allows to be processed by SciMiner and exposed through SciMiner result pages. <br>
Risk: The skill requires a SciMiner API key stored at ~/.config/sciminer/credentials.json. <br>
Mitigation: Keep the API key out of prompts, logs, and repository files; read it only from the credential file and send it as the documented authentication header. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sciminer/chemical-recognition) <br>
- [SciMiner AlphaExtractor API documentation](https://sciminer.tech/tool_api_files/AlphaExtractor_api_doc.md) <br>
- [SciMiner API key utility](https://sciminer.tech/utility) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown summary with JSON result excerpts and share_url links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SciMiner API key at ~/.config/sciminer/credentials.json and uploads chemistry images to SciMiner; long-running tasks are polled for up to 600 seconds.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
