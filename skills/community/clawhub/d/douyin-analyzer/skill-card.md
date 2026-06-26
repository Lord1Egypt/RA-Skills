## Description: <br>
内容分析模块。对转录文本进行语义分段、提取要点、生成总结。由 agent 直接完成，不依赖脚本。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[don068589](https://clawhub.ai/user/don068589) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and content workflow users use this skill to turn Whisper transcript text from Douyin videos into structured Markdown with corrected prose, semantic sections, key points, a summary, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke a local text-processing helper on transcript files, and the security guidance notes that users should be comfortable with local helper execution. <br>
Mitigation: Review the helper before execution, run it only on intended transcript inputs, and use direct agent review for sensitive repositories or content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown transcript structure, optional JSON from the helper script, and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled helper can preprocess text and produce JSON, but the skill directs the agent to perform higher-quality semantic analysis directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
