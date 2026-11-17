## Description:

Set up Blossom Hire, create local work opportunities, and help employers and jobseekers move through Blossom work flows in plain language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbiwu](https://clawhub.ai/user/robbiwu)

### License/Terms of Use:

MIT-0

## Use Case:

External employers and jobseekers use this skill to register for Blossom Hire, post or manage local work opportunities, find work, apply, review candidates, and arrange PopIns through confirmed plain-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Blossom API key is permanent and grants account access if exposed.

Mitigation: Store the key only in secure credential storage, keep it out of source code, logs, plaintext configuration, and conversation history, and contact Blossom support to rotate or revoke exposed keys.

Risk: The skill handles personal and job data and can perform account actions after confirmation.

Mitigation: Send only the current confirmed Blossom-related instruction, avoid forwarding unrelated context or credentials, and require clear confirmation before creates, updates, deletions, applications, or scheduling.

Risk: Conversational responses alone may not prove that a marketplace mutation was saved.

Mitigation: Treat a write as complete only when the returned structured action shows successful execution for the intended target.

## Reference(s):

- [Blossom homepage](https://blossomai.org)
- [Blossom protocol API](https://hello.blossomai.org/api/v1/blossom/protocol)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions]

**Output Format:** [Markdown guidance with JSON and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires secure storage for the returned Blossom API key and confirmation before account-changing actions.]

## Skill Version(s):

2.0.2 (source: server release metadata; artifact frontmatter reports 4.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
