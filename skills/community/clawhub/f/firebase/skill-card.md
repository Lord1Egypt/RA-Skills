## Description: <br>
Firebase Management API integration with managed OAuth for managing Firebase projects, web apps, Android apps, iOS apps, and Google Analytics links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Firebase projects and apps through Maton-managed OAuth. It is useful for listing projects, creating or updating app registrations, retrieving app configuration, and linking Google Analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton can act on the connected Firebase account through the OAuth connection. <br>
Mitigation: Install only if you trust Maton with the connected Firebase projects, use the least-privileged connection available, and periodically review or revoke Maton OAuth connections you no longer need. <br>
Risk: Create, update, and delete operations can change Firebase projects and app registrations. <br>
Mitigation: Confirm the target resource and intended effect before executing write or delete actions, and specify the intended Maton connection when multiple Firebase connections exist. <br>


## Reference(s): <br>
- [Firebase Skill on ClawHub](https://clawhub.ai/byungkyu/firebase) <br>
- [Maton](https://maton.ai) <br>
- [Firebase Management API Overview](https://firebase.google.com/docs/projects/api/workflow_set-up-and-manage-project) <br>
- [Firebase Management REST API Reference](https://firebase.google.com/docs/reference/firebase-management/rest) <br>
- [Firebase Projects Resource](https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API paths, JSON examples, and inline shell, Python, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and a Firebase OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
