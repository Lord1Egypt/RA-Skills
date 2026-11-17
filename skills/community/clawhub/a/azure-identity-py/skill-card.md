## Description:

Azure Identity SDK for Python authentication guidance for DefaultAzureCredential, managed identity, service principals, and token caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegovind](https://clawhub.ai/user/thegovind)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for guidance on authenticating Python Azure SDK clients with Microsoft Entra ID across local development, CI/CD, and Azure-hosted workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could paste real Azure client secrets into prompts or source files while adapting the examples.

Mitigation: Use placeholder values in prompts and keep real tenant IDs, client IDs, and client secrets in approved secret stores or environment configuration.

Risk: The skill may trigger on generic credential or authentication questions outside Azure Identity for Python.

Mitigation: Confirm the task is about Azure Identity for Python before applying its credential guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thegovind/skills/azure-identity-py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is bundled; examples include placeholder Azure credential environment variables.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
