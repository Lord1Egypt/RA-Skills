## Description:

A MGC Blackbox based prompt suite that guides data analysts through credential handling, local script and workflow use, sealed collaboration, and knowledge management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT

## Use Case:

Data analysts and teams use the prompts and agent template to manage user-owned analysis scripts, workflows, credentials, and reusable knowledge with explicit authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's privacy promises conflict with its instructions, so confidential information could be exposed to an AI service.

Mitigation: Review the conflicting claims before use and treat knowledge retrieved by the agent as potentially visible to its AI service.

Risk: The skill recommends a direct API workaround when sandbox tools are blocked, which could bypass sandbox restrictions.

Mitigation: Preserve sandbox restrictions and run only trusted workflows with limited permissions.

Risk: After unsealing, workflows run with the invoking user's permissions and may access local files or networks.

Mitigation: Run only trusted workflows with limited permissions, and rotate or revoke credentials at their provider if compromised.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zkeviny/skills/data-analyst-secure-suite)
- [MGC Blackbox project (manifest link)](https://github.com/zkeviny/MGC-Blackbox)
- [MGC Blackbox issue tracker (manifest link)](https://github.com/zkeviny/MGC-Blackbox/issues)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Step-by-step instructions for user-authorized operations.]

## Skill Version(s):

1.4.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
