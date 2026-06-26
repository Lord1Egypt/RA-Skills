## Description: <br>
Run multi-agent Dream Cascade (hierarchical 3-tier synthesis) or Dream Swarm (parallel multi-domain search) workflows via the dr.eamer.dev orchestration API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukeslp](https://clawhub.ai/user/lukeslp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run multi-agent research and synthesis workflows through the dr.eamer.dev orchestration API when a task benefits from parallel search or hierarchical summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and task content are sent to the external dr.eamer.dev service. <br>
Mitigation: Use a dedicated or least-privileged API key and avoid submitting secrets, personal data, regulated information, or confidential business material unless the provider's data handling terms have been reviewed and accepted. <br>
Risk: Multi-agent research outputs can include incomplete or misleading synthesis. <br>
Mitigation: Review returned sources and synthesized answers before relying on them for decisions or downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lukeslp/geepers-orchestrate) <br>
- [Publisher profile](https://clawhub.ai/user/lukeslp) <br>
- [dr.eamer.dev orchestration API](https://api.dr.eamer.dev) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DREAMER_API_KEY and sends task prompts to the external dr.eamer.dev service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
