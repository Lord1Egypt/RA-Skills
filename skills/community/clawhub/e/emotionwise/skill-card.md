## Description: <br>
Analyze text for emotions and sarcasm using the EmotionWise API (28 labels, EN/ES). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timexicali](https://clawhub.ai/user/timexicali) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send text to EmotionWise for emotion detection, sarcasm detection, confidence scores, and short practical interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text is sent to the EmotionWise service for emotion and sarcasm analysis. <br>
Mitigation: Avoid submitting confidential, regulated, personal, or internal business text unless that processing is intended. <br>
Risk: The skill depends on a private EmotionWise API key. <br>
Mitigation: Keep the API key private and install the skill only when the publisher and EmotionWise service are trusted. <br>


## Reference(s): <br>
- [EmotionWise Homepage](https://emotionwise.ai) <br>
- [EmotionWise Emotion Detector API Endpoint](https://api.emotionwise.ai/api/v1/tools/emotion-detector) <br>
- [ClawHub Skill Page](https://clawhub.ai/timexicali/emotionwise) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown text with emotion labels, confidence scores, sarcasm status, and a short interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EMOTIONWISE_API_KEY and sends submitted text to the EmotionWise API.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
