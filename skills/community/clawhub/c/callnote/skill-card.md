## Description: <br>
将医药/医疗行业电话会、策略会、专家会或业绩会的原始转写整理为高完整度、买方/卖方内部常用风格的标准化会议纪要，适用于术语纠错、Q&A重构、关键信息保留、低置信度内容与音频时间点标注。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzgztth-debug](https://clawhub.ai/user/lzgztth-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and investment-research teams use this skill to turn raw healthcare or medical-industry call transcripts into standardized Chinese meeting notes. It emphasizes complete information retention, cautious terminology correction, Q&A reconstruction, and timestamped marking of unclear or low-confidence content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input transcripts may contain confidential business information or protected health data. <br>
Mitigation: Use only transcripts you are authorized to process and keep patient-identifying details or secrets out of the workflow unless the required compliance controls are in place. <br>
Risk: Healthcare terminology, numbers, or names may be unclear in source transcripts. <br>
Mitigation: Preserve uncertainty labels and audio timestamps for low-confidence content instead of inventing or over-correcting details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lzgztth-debug/callnote) <br>
- [README.md](artifact/README.md) <br>
- [Example input](artifact/examples/input.md) <br>
- [Example output](artifact/examples/output.md) <br>
- [Call notes template](artifact/templates/call_notes_template.md) <br>
- [Invocation prompt template](artifact/templates/invocation_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Text] <br>
**Output Format:** [Structured Chinese Markdown meeting notes with summary, body notes, Q&A, and optional follow-up items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include uncertainty labels and audio timestamp markers for unclear terminology, numbers, names, or statements.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
