## Description: <br>
Collects, filters, deduplicates, and classifies AI industry news, then generates Chinese titles, summaries, Excel tables, and Word briefings from configured company and source lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nighmat1220](https://clawhub.ai/user/Nighmat1220) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and operations teams use this skill to run a repeatable AI-news collection workflow from configured RSS and web sources, company lists, and time windows. It supports daily briefing workflows that need categorized company news, global AI-event highlights, and export-ready Excel and Word deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches configured RSS and web sources, so it may process untrusted or changing external content. <br>
Mitigation: Review configured sources, keep crawl scope limited to intended sites, and inspect generated results before relying on them. <br>
Risk: When Ark/Doubao summarization is enabled, article content and related company/category context may be sent to Volcengine Ark. <br>
Mitigation: Use ARK_API_KEY only through the environment, process only shareable content, and avoid confidential or regulated material. <br>
Risk: Generated summaries, classifications, or importance scores may be affected by source content, prompt injection, or model error. <br>
Mitigation: Review generated titles, summaries, and selected key events before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Nighmat1220/ai-news-workflow) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill metadata](artifact/skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, configuration] <br>
**Output Format:** [Excel workbooks (.xlsx), Word documents (.docx), logs, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Excel outputs under ./output/excel and Word briefings under ./output/word; optional Doubao summaries target about 80 Chinese characters.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
