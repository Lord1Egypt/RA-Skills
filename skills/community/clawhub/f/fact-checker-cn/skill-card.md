## Description: <br>
基于多源权威信息和视觉取证，客观拆解用户提交的文本或图片，验证信息真伪并识别谣言与误导。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuchang0812](https://clawhub.ai/user/liuchang0812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check public claims, rumors, news snippets, and images in Chinese by decomposing claims, gathering evidence, cross-checking sources, and reporting a clear truthfulness rating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can send claim details, image contents, or extracted text into web searches while gathering evidence. <br>
Mitigation: Avoid private or confidential material unless the user is comfortable with those details being used in search queries. <br>
Risk: Fact-checking current or developing events can produce incomplete conclusions when evidence is still emerging. <br>
Mitigation: Use the skill's evidence-insufficient rating, cite sources, and clearly label uncertainty when available information is limited. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuchang0812/fact-checker-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with claim breakdown, evidence, reasoning, verdict, and references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source links, uncertainty notes, visual-analysis observations, and a final rating of true, false, misleading, or unverified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
