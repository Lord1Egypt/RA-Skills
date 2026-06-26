## Description: <br>
Generates Chinese-language company and industry research, diligence reports, interview question lists, competitive analysis, and listed-company financial analysis with separate workflows for investment-sensitive reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwz119](https://clawhub.ai/user/xwz119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, investors, and business researchers use this skill to structure China-focused company or industry research, produce interview questions, compare competitors, and prepare diligence-style Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Investment-related sections can produce concrete buy, sell, hold, or position-sizing guidance. <br>
Mitigation: Require explicit user confirmation before investment-related output and remove or disable action and sizing instructions unless a compliant financial-advice workflow governs the use. <br>
Risk: Research history may include confidential targets, requester names, internal links, portfolio details, or deal context. <br>
Mitigation: Make memory archival opt-in and redact confidential company, requester, link, portfolio, and deal details before retaining or sharing outputs. <br>
Risk: The security review recommends manual review before installation. <br>
Mitigation: Review and edit the skill before use, especially any investment-decision and memory-archival behavior. <br>


## Reference(s): <br>
- [Analysis Frameworks](references/analysis-frameworks.md) <br>
- [Due Diligence Framework](references/due-diligence-framework.md) <br>
- [Interview Guide](references/interview-guide.md) <br>
- [Risk Review Prompt](references/risk-review-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research reports, interview question lists, risk review summaries, and decision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source citations, research boundary statements, risk ratings, and optional investment-decision sections when explicitly requested.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
