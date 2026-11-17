## Description:

Advanced log analysis for Docker containers using signal extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkrdiop](https://clawhub.ai/user/mkrdiop)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to extract high-signal Docker container log lines and summarize probable causes for failing containers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted container name could execute arbitrary local commands during Docker log extraction.

Mitigation: Before installing or running the skill, replace shell=True with a structured subprocess argument list and strictly validate container names.

Risk: Container logs are untrusted data and may contain misleading instructions or hostile content.

Mitigation: Treat extracted logs as diagnostic data only and verify suggested fixes before applying them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown diagnostic summary with inline shell commands and extracted log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script tails up to 1000 Docker log lines and returns up to 50 extracted context lines.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
