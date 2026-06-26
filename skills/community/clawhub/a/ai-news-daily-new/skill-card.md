## Description: <br>
Generates a structured AI news daily brief by searching approved sources from the last 24 hours, deduplicating coverage, classifying stories, and summarizing the most important developments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyieleven](https://clawhub.ai/user/wangyieleven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to produce concise AI industry daily briefs for product, strategy, research, and enterprise AI tracking. It is designed to return a high-signal Simplified Chinese digest with ranked stories, source links, impact notes, and takeaways. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled mode can write generated briefs to fixed Tencent Docs document targets. <br>
Mitigation: Review the configured document targets before installation, change or remove targets that are not yours, and use manual output or a dry run unless scheduled publishing is explicitly approved. <br>
Risk: The security review marks the release suspicious because of external document-writing behavior. <br>
Mitigation: Treat the skill as requiring review before use, confirm Tencent Docs access and intended publishing behavior, and monitor generated content before relying on automated posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyieleven/ai-news-daily-new) <br>
- [Supported sources](references/sources.md) <br>
- [Search rules](references/search-rules.md) <br>
- [Output template](references/output-template.md) <br>
- [Category taxonomy](references/category-taxonomy.md) <br>
- [Validation checklist](references/validation-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Structured Markdown daily brief, usually in Simplified Chinese, with ranked news items, source links, impact notes, and summary takeaways.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default scope is the last 24 hours. Scheduled use may append Markdown output to fixed Tencent Docs documents.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
