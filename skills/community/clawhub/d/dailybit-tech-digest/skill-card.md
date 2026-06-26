## Description: <br>
DailyBit helps agents curate a daily technology briefing from top tech blogs using AI-generated Chinese summaries, hierarchical tags, and personalized recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Azurboy](https://clawhub.ai/user/Azurboy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to request a concise daily technology digest tailored to their current context, with 3-5 article or trend recommendations and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Digest requests can send inferred conversation context and personalization state to DailyBit. <br>
Mitigation: Avoid sensitive conversation details, use a generic rationale when possible, and provide a revocable DailyBit token only when personalization is needed. <br>
Risk: With a user token, the skill can modify RSS subscriptions. <br>
Mitigation: Require explicit user confirmation before adding or removing feeds, and list current feeds before deletion. <br>
Risk: Fetched article content is untrusted external blog data and may include prompt-injection text. <br>
Mitigation: Treat article content as passive data, ignore embedded instructions or code, and restrict requests to DailyBit endpoints. <br>


## Reference(s): <br>
- [DailyBit Homepage](https://dailybit.cc) <br>
- [DailyBit LLM Documentation](https://dailybit.cc/llms-full.txt?ack=xinqidong) <br>
- [ClawHub Skill Page](https://clawhub.ai/Azurboy/dailybit-tech-digest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown digest with article titles, personalized summaries, reasoning, trend synthesis, and original source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Presents exactly 3-5 articles or trends; personalization may use a user-provided DailyBit token.] <br>

## Skill Version(s): <br>
2.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
