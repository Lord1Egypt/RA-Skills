## Description: <br>
Agent Board helps agents create multi-panel storyboards by creating projects, uploading image and audio assets, drawing annotations, exporting PDFs, and generating share links through hosted REST or MCP-compatible interfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xartex](https://clawhub.ai/user/0xartex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Agent Board to build ordered storyboard, pre-visualization, shot breakdown, and animatic projects with panel metadata, visual or audio assets, annotations, PDF exports, and shareable views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Storyboard content, media files, and project metadata may be sent to the hosted AgentBoard service. <br>
Mitigation: Confirm the user is comfortable uploading sensitive client or unpublished material before creating or populating projects. <br>
Risk: The skill can create public or editable share links for storyboard projects. <br>
Mitigation: Ask for confirmation before creating share links, and prefer scoped permissions and limited TTL values when sharing is needed. <br>
Risk: The service may return x402 payment-required responses and supports payment-related retry behavior. <br>
Mitigation: Get explicit user approval before retrying requests with an X-Payment header or taking any purchase-related action. <br>


## Reference(s): <br>
- [AgentBoard hosted service](https://agentboard.fly.dev) <br>
- [ClawHub release page](https://clawhub.ai/0xartex/agentboard) <br>
- [Publisher profile](https://clawhub.ai/user/0xartex) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON, markdown, files] <br>
**Output Format:** [Markdown guidance with REST endpoints, JSON request and response examples, and operational notes for generated storyboard projects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create hosted storyboard projects, uploaded media assets, public or scoped share URLs, and exported PDF files through the AgentBoard service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
