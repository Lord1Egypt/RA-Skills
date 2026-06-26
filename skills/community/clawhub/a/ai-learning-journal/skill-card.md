## Description: <br>
Helps users maintain a bilingual AI learning journal, structure AI/LLM notes, review prior learning, create study plans, and generate Markdown summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengpeng9527](https://clawhub.ai/user/pengpeng9527) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to capture AI learning notes, organize prompt engineering and model/tool experiences, review learning history, and generate personalized AI study plans or summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad AI-learning triggers may convert casual AI-related comments into saved local Markdown notes. <br>
Mitigation: Tell the agent when a comment should not be journaled, and review generated entries before retaining them. <br>
Risk: Saved learning records can retain sensitive personal, client, or work details over time. <br>
Mitigation: Avoid placing secrets or sensitive information in entries, and periodically review or delete files in the records directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengpeng9527/ai-learning-journal) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Records index template](artifact/records/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance, Configuration] <br>
**Output Format:** [Markdown records, study plans, summaries, and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists AI learning records under the skill's records directory when used for journaling, planning, or summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
