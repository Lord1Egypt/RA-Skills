## Description: <br>
Transcribes and summarizes meetings through SkillBoss, letting agents choose among AI models for speed, cost, or quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to set up AI-powered meeting transcription and summarization through SkillBoss. It is intended for selecting a suitable model and producing meeting-note guidance or API calls for the task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to connect a broad external API platform using a sensitive API key. <br>
Mitigation: Review the remote SkillBoss setup before installing, use a scoped or spend-limited key when available, and monitor usage and costs. <br>
Risk: Meeting recordings or transcripts may contain confidential or regulated information that would be processed by external AI services. <br>
Mitigation: Require user confirmation before uploading meeting content and avoid confidential or regulated meetings unless external AI processing is approved. <br>
Risk: Model choice can affect cost because the skill supports paid model calls. <br>
Mitigation: Confirm model and cost expectations before running requests, prefer lower-cost models when appropriate, and monitor billing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alvisdunlop/alv-ai-meeting-notes) <br>
- [SkillBoss console](https://skillboss.co/console) <br>
- [SkillBoss products](https://skillboss.co/products) <br>
- [SkillBoss chat completions endpoint](https://api.skillboss.co/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown instructions with shell and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
