## Description: <br>
AI会议纪要生成器Pro turns meeting recordings or transcripts into structured minutes with summaries, decisions, key conclusions, and action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, meeting organizers, and team leads use this skill to convert recordings or written transcripts into professional meeting minutes with decisions and follow-up tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting recordings and transcripts may contain confidential, regulated, or private information and may be sent to configured transcription and GPT providers. <br>
Mitigation: Use the skill only with participant and organizational approval, and avoid confidential or regulated content unless the configured providers are approved for that data. <br>
Risk: Generated minutes, decisions, and action items can omit context or misstate what was agreed in a meeting. <br>
Mitigation: Have a meeting owner review the generated minutes before sharing, assigning tasks, or using the output as an official record. <br>
Risk: The artifact documents Node commands but the release evidence advises reviewing or trusting a separately referenced Node implementation. <br>
Mitigation: Review the installed Node implementation and run it in an environment appropriate for the sensitivity of the meeting content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/ai-meeting-minutes-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Structured meeting minutes in Markdown; artifact documentation also describes Word and PDF output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include meeting metadata, summary, decisions, key conclusions, action items, and detailed notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
