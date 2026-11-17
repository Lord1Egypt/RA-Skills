## Description:

AI 情报车间 analyzes how AI is affecting a selected industry, first producing a sourced signal report and then, after user confirmation, producing WeChat, Xiaohongshu, and Douyin content materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxiao200141-del](https://clawhub.ai/user/zhangxiao200141-del)

### License/Terms of Use:

MIT

## Use Case:

Content creators and analysts use this skill to research AI impact signals for a selected industry, classify the signals by evidence strength and impact type, and turn the confirmed report into platform-specific Chinese publishing materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill browses the web for the requested industry or topic and may surface inaccurate, stale, or weakly verified sources.

Mitigation: Review source links, dates, and verification status before relying on the report or publishing generated content.

Risk: Generated career, labor-market, or industry-impact claims could be mistaken for professional advice.

Mitigation: Keep the skill's disclaimers, require user review of sensitive employment or company data, and avoid presenting forward-looking judgments as decisions or guarantees.

Risk: The skill saves confirmed Markdown outputs using the industry name in the output path.

Mitigation: Avoid path-like industry names such as ../ or absolute paths until filename sanitization is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangxiao200141-del/skills/ai-intel-workshop)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown reports, long-form articles, short-form scripts, publishing captions, cover-image prompts, and saved Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are staged: a sourced signal report is produced first, then user-confirmed platform content is generated and saved under an output directory by industry and date.]

## Skill Version(s):

3.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
