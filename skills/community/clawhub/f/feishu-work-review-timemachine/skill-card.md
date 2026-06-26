## Description: <br>
Summarize a user's recent Feishu work into a concise weekly review or time-machine recap by reading Feishu docs, meeting notes, and related materials, then separating the user's real work from meeting noise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nihiue](https://clawhub.ai/user/Nihiue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team contributors use this skill to turn recent Feishu docs, meeting notes, and project materials into concise weekly or monthly work reviews focused on the user's actual ownership and contributions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read sensitive Feishu workspace materials while gathering evidence for a work review. <br>
Mitigation: Give the agent a clear date range and project scope, and limit source collection to relevant docs, meeting notes, and project materials. <br>
Risk: A generated Feishu document could contain incorrect, overstated, or sensitive content if created, updated, overwritten, or shared without review. <br>
Mitigation: Review the generated draft before allowing document creation, update, overwrite, or sharing. <br>
Risk: Meeting attendance or unsupported AI-generated meeting summaries could be mistaken for work ownership. <br>
Mitigation: Use ownership signals from document authorship, assigned action items, repeated project evidence, and the skill's softer wording rules when confidence is limited. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Nihiue/feishu-work-review-timemachine) <br>
- [Publisher profile](https://clawhub.ai/user/Nihiue) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Chinese Markdown or chat text, with optional Feishu document content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a Feishu document when the user explicitly requests it and permissions allow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
