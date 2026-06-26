## Description: <br>
识别汉字书法图片中的主要字体类型，并返回置信度和备选识别结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jfxia](https://clawhub.ai/user/jfxia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, calligraphy learners, researchers, and cultural-heritage reviewers can use this skill to classify the dominant calligraphy style in uploaded images or image URLs. Agents can use it to return a concise recognition result with confidence and alternate candidates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and image URLs may be sent to third-party services, including xjf123.dy.takin.cc and Hugging Face. <br>
Mitigation: Use only images that are approved for external processing, and avoid private manuscripts, proprietary scans, or sensitive documents. <br>
Risk: The implementation may return character recognition results in some paths rather than font classification results. <br>
Mitigation: Review returned fields before relying on the result, and disclose whether the output is a character label or a calligraphy font label. <br>
Risk: A broad Hugging Face token could be exposed if authenticated access is configured casually. <br>
Mitigation: Use a minimally scoped token only when authenticated Hugging Face access is intentional, and keep it in the HF_TOKEN environment variable rather than embedding it in prompts or files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jfxia/chinese-calligraphy-recognition) <br>
- [Hugging Face Space: jfxia/shufa](https://huggingface.co/spaces/jfxia/shufa) <br>
- [Hugging Face Space API endpoint](https://jfxia-shufa.hf.space/run/predict) <br>
- [Third-party mirror upload endpoint](https://xjf123.dy.takin.cc/upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and CLI text with JSON-compatible recognition fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recognition results may include a top label or character, confidence score, alternate candidates, and error text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
