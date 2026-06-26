## Description: <br>
AI girlfriend selfie generator. Injects "NingYao" persona and generates images through ClawGirl API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueoriginai](https://clawhub.ai/user/blueoriginai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users install this OpenClaw skill to generate persona-based selfie or outfit-change images through the ClawGirl API from natural-language prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and a ClawGirl API key to clawgirl.date. <br>
Mitigation: Install only if you trust clawgirl.date with the API key and prompt content; set CLAWGIRL_API_KEY explicitly and avoid sensitive prompts. <br>
Risk: Generated images may remain in the local OpenClaw media directory. <br>
Mitigation: Periodically remove generated images from the media directory when local retention is not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blueoriginai/clawgirl-selfie) <br>
- [ClawGirl Website](https://clawgirl.date) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [Plain text status lines containing IMAGE_PATH, IMAGE_URL, DOWNLOAD_FAILED, or TEXT_RESPONSE_BASE64 values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved locally when download succeeds; text responses are base64-encoded UTF-8.] <br>

## Skill Version(s): <br>
0.0.24 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
