## Description: <br>
Helps users find, compare, and select OpenClaw skills from the Clawhub marketplace based on task descriptions, domains, and desired outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earthwalking](https://clawhub.ai/user/earthwalking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to identify suitable OpenClaw or Clawhub skills, compare alternatives, and get practical usage or troubleshooting guidance for skill-based workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes exposed credentials or token-like material. <br>
Mitigation: Do not reuse included tokens or app secrets; rotate them if they are real before any installation or publication workflow. <br>
Risk: Publishing, upload, or account-linked commands appear in the artifact and may not fit the skill-search purpose. <br>
Mitigation: Treat those commands as examples only and avoid running them unless the credential, destination, and user confirmation are explicit. <br>
Risk: The skill is a broad recommendation guide and may produce unsuitable or incomplete skill matches. <br>
Mitigation: Verify recommendations against the current skill documentation and user requirements before deployment or task execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earthwalking/clawhub-skill-search) <br>
- [Clawhub skills marketplace](https://clawhub.ai/skills) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw skill creation documentation](https://docs.openclaw.ai/skills/creating) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with recommendation tables and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces skill recommendations, comparisons, quick-start guidance, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
