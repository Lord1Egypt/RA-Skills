## Description:

Query flight, train, and hotel booking information via a backend AI assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanhua](https://clawhub.ai/user/xuanhua)

### License/Terms of Use:


## Use Case:

Travel users and assisting agents use this skill to answer natural-language questions about flights, trains, hotels, and travel planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends complete travel queries to a production HTTP backend by default.

Mitigation: Use only a trusted backend, prefer HTTPS, and choose a non-production environment unless production access is intentional.

Risk: Shell-style examples can expose users to command injection if user text is interpolated into a shell command.

Mitigation: Invoke the Python script with structured arguments and avoid constructing shell commands from untrusted user input.

Risk: Travel queries may contain sensitive personal or payment details.

Mitigation: Avoid entering sensitive personal or payment details unless the backend and handling process are approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuanhua/skills/amidyfortest)
- [ClawHub publisher profile](https://clawhub.ai/user/xuanhua)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text response with command-line invocation guidance and error messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streams response text from the configured travel service; output can be truncated when --max-chars is set.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
