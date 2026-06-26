## Description: <br>
Detect deepfakes in images or videos using the Scam.ai API. Guides the user through API key setup if needed, then analyzes uploaded files for face-swap/deepfake manipulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuchennnnnnn](https://clawhub.ai/user/yuchennnnnnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit a local image or video to Scam.ai and receive a concise deepfake detection verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected images or videos to Scam.ai for analysis. <br>
Mitigation: Use only media that is appropriate to share with Scam.ai and follow applicable data handling requirements before analysis. <br>
Risk: The skill stores a Scam.ai API key in a local dotfile. <br>
Mitigation: Prefer a DeepFake Detection-specific key, keep restrictive file permissions, and delete or rotate the key when it is no longer needed. <br>


## Reference(s): <br>
- [Scam.ai](https://scam.ai) <br>
- [Scam.ai Docs](https://scam.ai/docs) <br>
- [Scam.ai Face Swap Detection API](https://api.scam.ai/api/defence/faceswap/predict) <br>
- [Scam.ai Video Detection API](https://api.scam.ai/api/defence/video/detection) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and a concise verdict line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a local Scam.ai API key and submit user-selected media to Scam.ai for analysis.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
