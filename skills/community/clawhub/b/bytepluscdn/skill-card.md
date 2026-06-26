## Description: <br>
Skill for BytePlus CDN domain and policy management, purge and prefetch, and log delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whitechenyingxi-maker](https://clawhub.ai/user/whitechenyingxi-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage BytePlus CDN domains, origin configuration, distribution policy templates, cache purge and prefetch, and offline or real-time log delivery through a local CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real operational changes to BytePlus CDN domains, cache state, policy templates, and log delivery. <br>
Mitigation: Use least-privilege dedicated credentials and verify domains, purge or preload targets, and log destinations before running commands. <br>
Risk: Credential material may be handled during setup or log delivery configuration. <br>
Mitigation: Do not print or paste service-account JSON in terminals or CI logs, and keep BytePlus API keys out of version control. <br>
Risk: Bulk targets such as all domains or large purge and preload lists can affect many CDN resources. <br>
Mitigation: Avoid using broad targets such as "all" unless intended, and confirm target lists before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/whitechenyingxi-maker/bytepluscdn) <br>
- [Skill Guide](artifact/SKILL.md) <br>
- [BytePlus CDN Scripts Documentation](artifact/reference/about.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and parameter prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide interactive collection of CDN command parameters and credential setup.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports v1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
