## Description: <br>
A fully automated daily intelligence briefing system that searches AI/tech news, curates content, generates 3600px infographics and edge-tts voice narration, uploads to Feishu/Lark docs, and delivers scheduled briefings via cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiongwang11](https://clawhub.ai/user/xiongwang11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business users use this skill to automate daily AI/tech intelligence briefings, including news curation, infographic rendering, Chinese voice narration, Feishu/Lark document creation, and scheduled delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can upload generated briefing materials to Feishu/Lark and send them to configured recipients. <br>
Mitigation: Verify credentials, recipient IDs, document visibility, and delivery targets in a local or test run before enabling delivery. <br>
Risk: Cron automation can repeatedly distribute stale, incorrect, or incomplete briefings if a run fails or source content is poor. <br>
Mitigation: Keep delivery disabled until the checklist passes, review generated materials before unattended runs, and monitor scheduled executions. <br>
Risk: External search, text-to-speech, and collaboration services can return inaccurate results, fail, or change behavior. <br>
Mitigation: Review source summaries before distribution and keep output local until service behavior and generated content are verified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiongwang11/daily-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, CSS, and bash code blocks; generated briefing materials may include images, MP3 narration, and Feishu/Lark document links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create external service documents and scheduled delivery actions when credentials and recipients are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
