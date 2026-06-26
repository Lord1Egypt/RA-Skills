## Description: <br>
AI短剧内容基因检测。零依赖可用：AI直接分析版权疑似、年龄分级违规、小说魔改程度，输出结构化风险图谱。可选配 Python 环境启用三重相似度算法（n-gram / 编辑距离 / TF-IDF）提升精度。结果仅供内容审核参考，不构成法律意见。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaalenwow](https://clawhub.ai/user/aaalenwow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content reviewers, creators, and agents use this skill to screen short drama scripts, dialogue, or subtitles for suspected copyright similarity, age-rating concerns, and adaptation drift. It produces structured risk findings and remediation guidance for human review, not legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional AI-provider use may send script excerpts to configured OpenAI or Anthropic APIs during deep semantic confirmation. <br>
Mitigation: Use local mode for confidential or unpublished scripts, and enable provider API keys only when third-party AI processing is acceptable. <br>
Risk: The skill's compliance, copyright, and age-rating outputs are review aids and may contain false positives or false negatives. <br>
Mitigation: Use the generated findings as triage input and have high-risk content reviewed by qualified human reviewers or legal counsel. <br>


## Reference(s): <br>
- [Adaptation Analysis](references/adaptation_analysis.md) <br>
- [Age Rating Standards](references/age_rating_standards.md) <br>
- [Copyright Detection Guide](references/copyright_detection_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Structured JSON risk maps and Markdown compliance reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes risk levels, suspicious locations, age-rating suggestions, adaptation-deviation scores, and remediation recommendations.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
