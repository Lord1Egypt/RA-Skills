## Description: <br>
检测并去除中文文本中的AI写作痕迹。当用户说"去AI味"、"改得自然一点"、"太机器了"、"帮我润色"、"去掉AI感"时使用。支持文件输入或直接粘贴文本，输出改写后文本和对比报告。适用于论文、文案、公众号、社交媒体等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erongcao](https://clawhub.ai/user/erongcao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to detect Chinese AI-writing patterns, rewrite Chinese text in a more natural style, and compare AI-trace scores before and after rewriting. It supports pasted text, single-file input, and batch workflows for essays, marketing copy, public posts, and social media text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A chosen output path may overwrite an existing file. <br>
Mitigation: Use a new output filename or verify the path before running file-output commands. <br>
Risk: Rewriting can change tone, emphasis, or meaning in user-provided Chinese text. <br>
Mitigation: Review the rewritten result against the original before publishing or submitting it. <br>
Risk: Broad editing requests may trigger rewriting when the user only wanted a review. <br>
Mitigation: Use detection-only mode or confirm the intended action when the request is ambiguous. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/erongcao/erong-humanize-chinese) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown, with optional JSON detection reports and file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read pasted text or files; optional output paths write rewritten text to disk.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
