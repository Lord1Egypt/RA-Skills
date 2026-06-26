## Description: <br>
Provides guidance for running a Flask frontend with a FastAPI backend, including route registration, API proxying, imports, cascading deletes, startup, and Docker Compose. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hunwenpinghao](https://clawhub.ai/user/hunwenpinghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when wiring a Flask frontend to a FastAPI backend and need practical guidance on routing, proxying API calls, startup scripts, and Docker Compose configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example services may expose network bindings or ports that are broader than a production deployment needs. <br>
Mitigation: Restrict host bindings, published ports, and firewall rules to the minimum required environment before deployment. <br>
Risk: Proxy snippets may omit production auth, cookie, header, timeout, and error-handling behavior. <br>
Mitigation: Review and adapt proxy behavior so authentication, session state, headers, status codes, and failures are preserved correctly. <br>
Risk: Deletion examples can remove related database records when used directly in an application. <br>
Mitigation: Protect destructive routes with access control, test cascade behavior, and maintain recovery or backup procedures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hunwenpinghao/fastapi-flask-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, Bash, and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; snippets require review before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
