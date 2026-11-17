## Description:

CCPA-Compliance is a local CCPA/CPRA compliance assistant that helps organizations assess privacy obligations, consumer rights handling, opt-out mechanisms, data sale or sharing practices, service provider controls, and compliance documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, privacy teams, and compliance staff use this skill to run CCPA/CPRA self-checks, review consumer rights and opt-out controls, evaluate data sale or sharing scenarios, and generate initial reports or templates. Its outputs are compliance guidance and should not be treated as legal advice.

### Deployment Geography for Use:

Global, for organizations assessing obligations related to California consumers under CCPA/CPRA.

## Known Risks and Mitigations:

Risk: The main command imports an adjacent compliance_core module outside the skill package.

Mitigation: Review and trust the adjacent compliance_core module before installation, or run the skill in an isolated controlled environment.

Risk: The skill provides compliance guidance that may be incomplete or unsuitable for a specific legal situation.

Mitigation: Use outputs as preliminary guidance only and have qualified legal counsel validate material CCPA/CPRA decisions.

Risk: The tools can write generated reports or templates to user-specified file paths.

Mitigation: Use explicit safe output locations and review generated files before sharing or relying on them.

## Reference(s):

- [CCPA/CPRA law summary](references/ccpa-law.md)
- [Security check guide](SECURITY_CHECK_GUIDE.md)
- [ClawHub skill page](https://clawhub.ai/wwumit/skills/ccpa-comliance)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, HTML, Guidance, Shell commands, Configuration]

**Output Format:** [CLI output and report files in text, JSON, Markdown, HTML, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports or templates to user-specified output paths; the main command depends on an adjacent compliance_core module.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
