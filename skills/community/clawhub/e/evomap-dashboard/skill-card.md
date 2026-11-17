## Description:

Launch a local EvoMap Node Dashboard web viewer for viewing EvoMap node status, reputation, tasks, and assets with a Node ID and Node Secret.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppop0uuiu](https://clawhub.ai/user/ppop0uuiu)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and EvoMap node operators use this skill to launch or inspect a local dashboard for viewing node reputation, claimed tasks, and asset history through the EvoMap API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard ships with embedded EvoMap credentials.

Mitigation: Remove the embedded credentials, rotate the exposed secret, and require users to provide their own Node ID and Node Secret explicitly.

Risk: The local proxy is unauthenticated and the server binds broadly with permissive CORS.

Mitigation: Bind the dashboard to localhost, restrict CORS to the local dashboard origin, and add local authentication or other access controls before use.

Risk: The artifact includes publish.py, which can write to EvoMap and is unrelated to viewing dashboard data.

Mitigation: Delete or isolate publish.py from deployed packages and audit any publishing workflow separately.

Risk: Node Secrets entered into the dashboard grant sensitive account authority.

Mitigation: Treat Node Secrets as credentials, avoid sharing them, and run the dashboard only in trusted local environments after review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ppop0uuiu/skills/evomap-dashboard)
- [Project Repository Listed in Artifact Documentation](https://github.com/ppop0uuiu/evomap-dashboard)
- [EvoMap](https://evomap.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct an agent to run a local FastAPI dashboard and handle Node ID and Node Secret values as sensitive credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, skill.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
