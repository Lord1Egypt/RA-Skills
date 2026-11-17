## Description:

A Chinese-language toy skill that simulates logging into space, selecting destinations, checking status, and logging out through Python examples and command-line usage.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[pandasun](https://clawhub.ai/user/pandasun)

### License/Terms of Use:


## Use Case:

Developers and agents can use this skill as a light example for generating or running a simulated Python command-line workflow with destination selection, status checks, logout behavior, and configuration samples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the simulated login, identity, orbit, and permission language for real authentication or operational space functionality.

Mitigation: Treat the skill as learning or entertainment material and verify separately before adapting any pattern for production authentication, authorization, or mission workflows.

Risk: The documentation and user-facing examples are primarily Chinese-language, which may make behavior and limitations harder to review for some teams.

Mitigation: Have a Chinese-literate reviewer inspect the docs, prompts, and command examples before deployment in a shared agent environment.

Risk: The examples mention configuration and environment variables, which could encourage users to add real secrets when extending the toy workflow.

Mitigation: Keep sample configuration free of real credentials and re-scan any modified version that adds API calls, persistence, or credential handling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pandasun/skills/e-crm-a)
- [NASA Official Website](https://www.nasa.gov)
- [SpaceX Official Website](https://www.spacex.com)
- [China Manned Space](http://www.cmse.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, configuration JSON, and JSON-like status dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are illustrative and simulation-oriented; they do not represent real space, authentication, or API operations.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact documentation lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
