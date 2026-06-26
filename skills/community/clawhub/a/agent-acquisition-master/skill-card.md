## Description: <br>
Agent Acquisition Master helps an agent plan and operate client-acquisition workflows across cold email, LinkedIn outreach, organic content funnels, lead qualification, follow-up, and closing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and revenue teams use this skill to have an agent build prospect lists, draft outreach, manage follow-up cadences, create content funnels, qualify interested leads, and summarize acquisition performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run persistent outreach and follow-up workflows that contact prospects without enough human approval. <br>
Mitigation: Disable crons until reviewed and require manual approval or draft-only mode before any message is sent. <br>
Risk: The skill can read inbox replies, scrape prospect data, and forward lead information through Telegram or third-party enrichment services. <br>
Mitigation: Use dedicated accounts, restrict API keys and connected services, minimize shared data, and define retention and redaction rules for prospect and inbox data. <br>
Risk: Sales outreach can create legal, privacy, deliverability, or platform-compliance exposure. <br>
Mitigation: Review campaigns for applicable outreach laws and platform terms, honor opt-out requests immediately, and confirm compliance before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/agent-acquisition-master) <br>
- [Publisher profile](https://clawhub.ai/user/georges91560) <br>
- [Homepage from skill metadata](https://github.com/wesley-agent/wesley-acquisition-master) <br>
- [Gmail outreach target](https://gmail.com) <br>
- [LinkedIn prospecting target](https://linkedin.com) <br>
- [X/Twitter organic acquisition target](https://twitter.com) <br>
- [Reddit community acquisition target](https://reddit.com) <br>
- [Hunter.io optional email-finding target](https://hunter.io) <br>
- [Apollo.io optional lead-database target](https://apollo.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update acquisition files, outreach sequences, campaign reports, and operational logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
