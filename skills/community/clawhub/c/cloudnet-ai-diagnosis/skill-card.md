## Description: <br>
Cloudnet AI Diagnostics helps troubleshoot poor wireless client experience, network lag, network adapter issues, and WiFi connection failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudnet-skills](https://clawhub.ai/user/cloudnet-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network operators, support engineers, and IT administrators use this skill to collect Cloudnet wireless diagnostics for a named site and client, then summarize root causes and actionable remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Cloudnet API key for authenticated diagnostics. <br>
Mitigation: Use a least-privilege API key where possible, avoid exposing it in chat or logs, and confirm how mcporter stores bearer tokens. <br>
Risk: Diagnostic results may include sensitive operational data such as MAC addresses, IP addresses, usernames, logs, and device telemetry. <br>
Mitigation: Treat diagnostic output as sensitive, share only what is needed for troubleshooting, and follow the organization's data handling rules. <br>
Risk: The workflow depends on npm, mcporter, and the Cloudnet endpoint. <br>
Mitigation: Install these components only from trusted sources and use the skill only when the Cloudnet endpoint is expected for the deployment. <br>


## Reference(s): <br>
- [Cloudnet AI Diagnostics on ClawHub](https://clawhub.ai/cloudnet-skills/cloudnet-ai-diagnosis) <br>
- [Cloudnet publisher profile](https://clawhub.ai/user/cloudnet-skills) <br>
- [Cloudnet default management endpoint](https://oasis.h3c.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown troubleshooting response with diagnostic summary, root-cause analysis, and recommended remediation steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mcporter command examples and Cloudnet diagnostic findings relevant to the user's wireless issue.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact frontmatter says 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
