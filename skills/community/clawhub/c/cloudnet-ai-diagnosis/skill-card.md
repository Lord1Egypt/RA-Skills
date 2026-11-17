## Description:

Cloudnet AI Diagnostics helps troubleshoot poor wireless client experience, slow network adapters, and devices that cannot connect to WiFi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudnet-skills](https://clawhub.ai/user/cloudnet-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Network operations teams and support engineers use this skill to gather site and client details, query Cloudnet diagnostics, and return a focused WiFi troubleshooting summary, root cause analysis, and remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Cloudnet API key and sends site, terminal, and diagnostic data to the configured Cloudnet platform.

Mitigation: Use a least-privileged Cloudnet API key, configure the intended Cloudnet base URL, and avoid sharing unnecessary site or terminal identifiers.

Risk: The setup depends on a global npm installation of mcporter.

Mitigation: Verify the mcporter package and publisher before installation, and prefer pinned or controlled installation methods where possible.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cloudnet-skills/skills/cloudnet-ai-diagnosis)
- [Cloudnet management platform](https://oasis.h3c.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with diagnostic summary, root cause analysis, and remediation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npm, mcporter, and CLOUDNET_API_KEY to query the configured Cloudnet platform.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
