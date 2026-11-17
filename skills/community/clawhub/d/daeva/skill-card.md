## Description:

Daeva helps agents interact with local or remote GPU pods for AI inference tasks including transcription, image generation, OCR, vision analysis, pod lifecycle management, status checks, and GPU pod debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asmolebot](https://clawhub.ai/user/asmolebot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route AI inference jobs to Daeva-managed GPU pods and manage pod lifecycle, package installation, status, and troubleshooting through REST or MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-provided files or prompts to a local or remote Daeva service.

Mitigation: Use only trusted Daeva instances and confirm the resolved DAEVA_URL or DAEVA_PORT target before sending files or sensitive inputs.

Risk: Pod lifecycle actions can affect shared GPU infrastructure used by other agents or users.

Mitigation: Check pod and scheduler status before start, stop, activate, or swap actions, and avoid disruptive changes on shared instances unless authorized.

Risk: Installing pod packages from untrusted sources can introduce unsafe workloads or configuration.

Mitigation: Install only reviewed pod packages from trusted sources and inspect package manifests before registration or installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/asmolebot/skills/daeva)
- [Daeva Repository](https://github.com/asmolebot/daeva)
- [Publisher Profile](https://clawhub.ai/user/asmolebot)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoint guidance, environment variable setup, MCP configuration, and operational troubleshooting steps.]

## Skill Version(s):

0.2.6 (source: server release metadata; artifact frontmatter lists 0.2.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
