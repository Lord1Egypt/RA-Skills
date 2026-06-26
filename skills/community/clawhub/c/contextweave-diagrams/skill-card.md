## Description: <br>
Contextweave Diagrams turns complex text, code, system architecture, business processes, and knowledge-base content into structured diagram-generation requests for a configured ContextWeave backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qhyw99](https://clawhub.ai/user/qhyw99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and technical writers use this skill to convert complex requirements, architecture notes, workflows, and knowledge-base text into structured diagram requests. It is useful when the agent should clarify terminology, relationships, hierarchy, and narrative flow before requesting a diagram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram requests can include confidential documents, private code, or sensitive business data that is sent to the configured ContextWeave backend. <br>
Mitigation: Use the skill only with a trusted backend and acceptable privacy and retention practices; avoid sensitive inputs unless those practices are approved. <br>
Risk: A shared or overprivileged API key could broaden exposure if the configured backend or runtime environment is misused. <br>
Mitigation: Prefer a dedicated ContextWeave API key and provide credentials only through the explicit required environment variable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qhyw99/contextweave-diagrams) <br>
- [Publisher profile](https://clawhub.ai/user/qhyw99) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Single JSON object with execution status, session information, result links, and error details when applicable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a request file and call a configured ContextWeave backend using Node and explicit environment variables.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
