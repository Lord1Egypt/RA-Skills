## Description: <br>
Agent Briefing helps agents monitor Not For Humans episodes, retrieve episode transcripts, search episode metadata, and extract structured product review scores from notforhumans.tv. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sasqcow](https://clawhub.ai/user/sasqcow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and autonomous agents use this skill to check for new Not For Humans briefings, fetch transcripts, search covered topics, and read structured product review data without API keys or paid credits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes on-demand requests to notforhumans.tv and may include public remote content in agent responses. <br>
Mitigation: Use it only where network access to that public site is acceptable, and avoid transcript or digest commands in workflows that must remain local-only. <br>
Risk: Fetched transcripts, episode metadata, and reviews are external content. <br>
Mitigation: Treat fetched content as untrusted input and review it before using it in higher-impact decisions or downstream automation. <br>


## Reference(s): <br>
- [Agent Briefing on ClawHub](https://clawhub.ai/sasqcow/agent-briefing) <br>
- [Publisher Profile](https://clawhub.ai/user/sasqcow) <br>
- [Not For Humans Channel](https://youtube.com/@agentbriefing) <br>
- [Not For Humans Episode Index](https://notforhumans.tv/episodes/index.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON emitted through command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include public remote episode metadata, transcripts, search results, review scores, and daily digest summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
