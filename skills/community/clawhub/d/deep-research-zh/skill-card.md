## Description: <br>
中文深度调研工具，用于通过 OpenClaw 原生搜索、抓取和并行会话工具执行多源调研，并生成中文 Markdown/PDF 研究报告与飞书交付。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mydearzsy](https://clawhub.ai/user/mydearzsy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, analysts, and developers use this skill to plan and run structured deep research workflows for literature reviews, competitive analysis, industry research, policy research, and other topics that require source triangulation and documented reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires online research behavior and can save reports locally before sending them through Feishu. <br>
Mitigation: Use it only for topics and data appropriate for online research, and require confirmation of destination, file path, and content before delivery for confidential, regulated, or internal topics. <br>
Risk: The artifact instructs automatic PDF delivery without a final user approval step. <br>
Mitigation: Add an operational review checkpoint before any Markdown or PDF report is sent, especially when the report contains sensitive, proprietary, or user-specific information. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mydearzsy/deep-research-zh) <br>
- [Publisher profile](https://clawhub.ai/user/mydearzsy) <br>
- [README](artifact/README.md) <br>
- [Quick reference](artifact/quickref.md) <br>
- [Example workflow](artifact/example.md) <br>
- [Markdown to PDF converter](artifact/scripts/md2pdf.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown research plan and report, optional PDF file, and concise delivery status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final reports are expected to use APA-style citations, confidence annotations, documented limitations, and a Chinese-friendly PDF conversion path when local tooling is available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
