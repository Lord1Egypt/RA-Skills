## Description: <br>
AI-powered professional networking assistant. Generate personalized cold emails and outreach playbooks to accelerate career growth and business development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hotwheelsBo](https://clawhub.ai/user/hotwheelsBo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Professionals use this skill to generate reviewed cold email drafts and structured outreach playbooks from LinkedIn profile URLs and a specific networking objective. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's email address, LinkedIn profile URL, target LinkedIn profile URLs, outreach objectives, and generated outreach data to Articuler. <br>
Mitigation: Share only appropriate profile and outreach data, and confirm the user is comfortable sending that information to Articuler before use. <br>
Risk: The Articuler login flow returns a token used for later API calls. <br>
Mitigation: Treat the token as private and avoid placing it in logs, chat transcripts, shared files, or other persistent records. <br>
Risk: Generated outreach can be inaccurate, overly broad, or inappropriate for the recipient. <br>
Mitigation: Review the generated email or playbook before acting on it, and do not send messages automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hotwheelsBo/articuler) <br>
- [Articuler](https://www.articuler.ai) <br>
- [Articuler MCP server](https://www.articuler.ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with curl command examples, JSON response examples, cold email drafts, and outreach playbook summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an async job flow; generated emails are presented for user review and are not sent automatically.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
