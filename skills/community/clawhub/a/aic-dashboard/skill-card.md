## Description: <br>
AI Commander Management Dashboard is a lightweight companion web UI for monitoring inbound emails received via the email-webhook skill and browser session status created by the browser-auth skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lksrz](https://clawhub.ai/user/lksrz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI Commander users use this skill to view recent inbound emails and browser session status from companion local skills in a token-protected dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can display sensitive email and session data through a local web server. <br>
Mitigation: Use a strong DASHBOARD_TOKEN and bind DASHBOARD_HOST to 127.0.0.1 unless remote access is intentional. <br>
Risk: The printed dashboard URL includes an access token that could grant access if shared. <br>
Mitigation: Avoid sharing terminal logs or screenshots containing the printed URL. <br>
Risk: The browser UI loads assets from external CDNs while viewing potentially sensitive mail. <br>
Mitigation: Consider replacing CDN-loaded UI assets before viewing sensitive mail. <br>


## Reference(s): <br>
- [AI Commander Dashboard on ClawHub](https://clawhub.ai/lksrz/aic-dashboard) <br>
- [email-webhook companion skill](https://clawhub.ai/lksrz/email-webhook) <br>
- [browser-auth companion skill](https://clawhub.ai/lksrz/browser-auth) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with shell commands and local web dashboard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Node.js web server that displays email and browser session data from local JSON files.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
