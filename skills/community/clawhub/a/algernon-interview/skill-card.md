## Description: <br>
Mock technical interview mode for OpenAlgernon that simulates a senior AI engineering interviewer with adaptive difficulty, follow-up probes, and a full scored report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AntonioVFranco](https://clawhub.ai/user/AntonioVFranco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenAlgernon users use this skill to run mock technical interviews for a selected study material, practice concepts, application, trade-offs, and production reasoning, and receive a scored report with study recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the local OpenAlgernon study database to select interview topics. <br>
Mitigation: Run it only with study databases intended for interview practice. <br>
Risk: The skill writes a local interview memory summary under OpenAlgernon. <br>
Mitigation: Review or remove generated memory files if interview results contain sensitive content. <br>
Risk: When NOTION_CLI and NOTION_PAGE_ID are configured, the full interview report can be exported to Notion. <br>
Mitigation: Leave NOTION_PAGE_ID unset when external export is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AntonioVFranco/algernon-interview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Conversational prompts plus a Markdown interview report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read the local OpenAlgernon study database, write a local interview memory summary, and optionally append the full report to Notion when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
