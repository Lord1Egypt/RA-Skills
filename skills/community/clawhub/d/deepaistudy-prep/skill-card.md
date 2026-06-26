## Description: <br>
基于教材 PDF 或图片 OCR 识别，AI 生成对应学科年级的互动 SVG 幻灯片与预习小测验课件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stoneyshum](https://clawhub.ai/user/stoneyshum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, students, and learning-support agents use this skill to turn textbook PDFs or page images into DeepAIStudy preview lessons with OCR text, interactive SVG slides, quiz questions, and knowledge-point summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Account passwords are stored plainly in the local configuration file. <br>
Mitigation: Use a dedicated or low-privilege account, restrict access to the local config file, and remove stored credentials after use. <br>
Risk: Local PDFs and images are uploaded to a remote AI-backed service for OCR and lesson generation. <br>
Mitigation: Verify the configured server is https://www.deepaistudy.com and avoid uploading sensitive, regulated, or confidential documents unless approved. <br>
Risk: The security verdict is suspicious because the package needs more safety guidance around credential handling and document upload. <br>
Mitigation: Install only from a trusted package source and review configuration, server destination, and generated outputs before classroom or production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stoneyshum/deepaistudy-prep) <br>
- [Publisher profile](https://clawhub.ai/user/stoneyshum) <br>
- [DeepAIStudy service](https://www.deepaistudy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and generated lesson assets such as OCR text, SVG slides, PNG slide images, quiz data, and knowledge-point lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads local PDFs or images to the configured DeepAIStudy server and may save generated SVG output when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
