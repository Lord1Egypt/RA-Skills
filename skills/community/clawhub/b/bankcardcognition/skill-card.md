## Description: <br>
对银行卡图片 OCR，返回卡号、银行与卡类型等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to recognize a bank card image and return card number, bank name, card type, and bank code through JisuAPI. It is intended for cases where the user is authorized to process the card image and needs a concise OCR result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided bank card images to JisuAPI for OCR, which is sensitive-data processing. <br>
Mitigation: Use it only for cards the user is authorized to process, disclose the external API use, and avoid retaining card photos or full card numbers longer than necessary. <br>
Risk: The JISU_API_KEY credential is required to call the provider API. <br>
Mitigation: Store the key in the environment, restrict access to it, and avoid logging or sharing the key in prompts, outputs, or artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/bankcardcognition) <br>
- [JisuAPI Bank Card Recognition Documentation](https://www.jisuapi.com/api/bankcardcognition/) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON result object or JSON error object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; accepts a local relative image path or base64 image content.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
