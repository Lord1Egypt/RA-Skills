## Description: <br>
Provides a defensive prompt-injection checklist for AI agents that process external content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Byron-McKeeby](https://clawhub.ai/user/Byron-McKeeby) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit agent prompts, external-content handling, memory-write flows, and logging examples for prompt-injection defenses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example code blocks include file writes, URL fetching, and log paths that may be inappropriate in privileged environments. <br>
Mitigation: Require user approval before fetching URLs or writing files, and avoid privileged log paths unless they are necessary. <br>
Risk: The artifact includes a promotional external link that is not vetted security guidance. <br>
Mitigation: Treat the external promotional link cautiously and rely on reviewed internal security guidance for deployment decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklist items and example code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes defensive examples that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
