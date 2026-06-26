## Description: <br>
Use the Browser Use cloud API to create cloud browser sessions, preserve optional browser profiles, and run autonomous browser tasks for Clawdbot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Makforce](https://clawhub.ai/user/Makforce) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to create Browser Use cloud browser sessions for Clawdbot, manage persisted profiles for authenticated workflows, and launch autonomous browser tasks through the Browser Use API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser profiles can persist cookies and authenticated sessions that may expose sensitive accounts if reused broadly. <br>
Mitigation: Use fresh or dedicated low-privilege profiles, avoid syncing broad local Chrome cookies, and delete profiles when finished. <br>
Risk: Task prompts and browser automation may send sensitive browsing context, secrets, or regulated data to a cloud browser service. <br>
Mitigation: Do not include secrets or regulated data in task prompts, and restrict tasks to data approved for Browser Use. <br>
Risk: Active cloud browser sessions may remain available or continue incurring cost if left running. <br>
Mitigation: Stop browser sessions when finished and verify session status through the Browser Use API. <br>


## Reference(s): <br>
- [Browser Use documentation](https://docs.browser-use.com) <br>
- [Browser Use Cloud API documentation](https://docs.cloud.browser-use.com) <br>
- [ClawHub skill page](https://clawhub.ai/Makforce/browser-use-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown instructions with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Browser Use session URLs, profile IDs, task IDs, and API responses when the agent follows the guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
