## Description: <br>
Extracts Bilibili video metadata, danmaku, and comments, then turns engagement signals into concise content-operation analysis and title or topic suggestions. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, media planners, and creators use this skill to inspect public Bilibili video engagement, comments, and danmaku, then produce reusable content insights. It is framed by its own workflow as personal learning and research use, not commercial deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch, display, and locally retain raw public Bilibili comments or danmaku, including unsafe or unmoderated user-generated text. <br>
Mitigation: Delete bundled cache files before use, use no-cache operation when persistence is not needed, and review or filter raw comments before reusing them in reports. <br>
Risk: Bulk extraction can create platform compliance, rate-limit, or account-risk concerns. <br>
Mitigation: Avoid bulk scraping, keep request volume low, follow Bilibili terms and robots guidance, and use the documented delay and rate-limit controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/if530770/bilibili-video-extractor) <br>
- [Core Workflow](references/core-workflow.md) <br>
- [Analysis Framework](references/analysis-framework.md) <br>
- [Bilibili API Guide](references/bilibili-api-guide.md) <br>
- [Output Template](references/output-template.md) <br>
- [Competitor Analysis Template](references/competitor-analysis-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON extraction results, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include raw public comments and danmaku when extraction scripts are run; local cache files can persist extracted data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
