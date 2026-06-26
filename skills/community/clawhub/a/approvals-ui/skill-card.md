## Description: <br>
Web dashboard to approve OpenClaw device and channel pairings, manage connections, and access a live terminal from the browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dr1nnas](https://clawhub.ai/user/Dr1nnas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to run a local dashboard for reviewing device and channel pairing requests, approving or rejecting connections, viewing gateway state, and opening a browser-based terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release exposes powerful local administration, gateway-token visibility, and shell access. <br>
Mitigation: Run only on localhost, keep the dashboard behind strong authentication, and remove the browser terminal route and template unless terminal access is required. <br>
Risk: Default dashboard credentials, API password, and Flask secret-key placeholder can allow unauthorized access if unchanged. <br>
Mitigation: Change the dashboard username and password, set a strong SERVER_AUTH_PASSWORD, and provide a random FLASK_SECRET_KEY before first use. <br>
Risk: Debug mode and broad Socket.IO CORS settings increase exposure if the service is reachable beyond the local machine. <br>
Mitigation: Disable debug mode, keep the host bound to 127.0.0.1, and do not expose the service to a network without TLS, strong auth, and a reverse proxy. <br>
Risk: The app reads sensitive OpenClaw state files, including gateway tokens and pairing credentials. <br>
Mitigation: Limit filesystem and account access to trusted users and treat the dashboard as sensitive administrative tooling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dr1nnas/approvals-ui) <br>
- [Publisher profile](https://clawhub.ai/user/Dr1nnas) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown guidance with shell commands, configuration notes, and local web UI behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Flask routes and browser UI interactions for pairing approval, token viewing, and terminal access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
