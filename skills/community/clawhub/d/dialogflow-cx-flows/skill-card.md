## Description:

Manage flows and pages in Google Dialogflow CX via the REST API for creating and organizing conversation paths within agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage Dialogflow CX flows and pages, including listing, creating, retrieving, updating, deleting, importing, exporting, validating, and training conversation flow resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide persistent Dialogflow CX configuration changes through POST, PATCH, DELETE, import, and load operations.

Mitigation: Use a test agent first, review proposed operations before execution, and apply changes only with credentials scoped to the intended project, location, and agent.

Risk: Broad Google credentials could allow unintended access beyond the target Dialogflow CX resources.

Mitigation: Provide least-privileged Google credentials and avoid sharing service account keys or bearer tokens in prompts, logs, or committed files.

Risk: Running the Python helper installs and executes external dependencies in the local environment.

Mitigation: Pin dependencies and run the helper in an isolated environment before using it in shared or sensitive workspaces.

## Reference(s):

- [Flows & Pages API Reference](references/flows.md)
- [ClawHub Skill Page](https://clawhub.ai/yash-kavaiya/skills/dialogflow-cx-flows)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, curl, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST endpoint patterns and a Python CLI helper for Dialogflow CX flow and page operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
