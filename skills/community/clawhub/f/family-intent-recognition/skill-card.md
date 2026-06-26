## Description: <br>
家庭消费意图识别 - 从家庭聊天文本中识别消费意图，输出结构化JSON <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhaichao87](https://clawhub.ai/user/wuhaichao87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to classify Chinese household chat messages for purchase intent, intent category, stage, strength, triggering keywords, and a short reason. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Flask API can expose household chat text if it is reachable beyond the local machine or used with broad CORS settings. <br>
Mitigation: Bind the API to localhost or otherwise restrict network access and CORS, and avoid sending sensitive family chat text to exposed services. <br>
Risk: The rule-based keyword classifier can misclassify ambiguous messages or miss intents outside its configured categories and keywords. <br>
Mitigation: Review classifications before using them for consequential decisions and tune the keyword lists with representative household chat examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhaichao87/family-intent-recognition) <br>
- [Publisher profile](https://clawhub.ai/user/wuhaichao87) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands] <br>
**Output Format:** [JSON object with intent fields; CLI and API examples are provided as shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The classifier returns has_intent, intent_category, intent_stage, intent_strength, up to five keywords, and reason.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
