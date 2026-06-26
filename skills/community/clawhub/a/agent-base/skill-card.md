## Description: <br>
Guides agents through creating custom Node.js http.Agent subclasses with agent-base and choosing proxy-agent subclasses when appropriate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to produce TypeScript or JavaScript guidance and examples for custom HTTP connection handling, proxy routing, and agent-base connect() implementations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated proxy or custom Agent code may route traffic through unintended destinations or weaken TLS handling if used without review. <br>
Mitigation: Verify proxy destinations, TLS settings, routing rules, and package names before using generated code with production or corporate traffic. <br>
Risk: Suggested npm packages may add dependencies to an application. <br>
Mitigation: Confirm package names and dependency trust posture before installing packages or committing dependency changes. <br>


## Reference(s): <br>
- [Proxy Details and Subclass Selection](references/proxy-details.md) <br>
- [ClawHub skill page](https://clawhub.ai/openlark/agent-base) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with TypeScript or JavaScript examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated code and package recommendations should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
