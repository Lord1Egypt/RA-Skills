## Description: <br>
Extracts and cleans text from structural CAD DXF files, including TSSD-style rebar symbol normalization, and returns complete drawing annotations as Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lialia691691-alt](https://clawhub.ai/user/lialia691691-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, estimators, and construction engineers use this skill to extract complete text annotations from DXF structural drawings and return them as a clean Markdown list for downstream quantity takeoff and feature matching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to silently install an unpinned Python dependency before execution. <br>
Mitigation: Require explicit approval before dependency installation, and prefer preinstalling or pinning ezdxf in a controlled environment. <br>
Risk: Generated Markdown may contain confidential project details from CAD drawings. <br>
Mitigation: Run the skill only on DXF files intended for processing and handle extracted Markdown as confidential when drawings contain private information. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lialia691691-alt/dxf-text-extractor) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Example extracted DXF report](artifact/分栏提取_总说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown list with extracted CAD text and concise operational guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves extracted drawing text without model summarization or omission.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
