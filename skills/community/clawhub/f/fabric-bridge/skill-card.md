## Description:

Fabric Bridge helps agents run Fabric AI patterns through the fabric-ai CLI for text transformation, analysis, writing improvement, content creation, code review, threat modeling, and structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koriyoshi2041](https://clawhub.ai/user/koriyoshi2041)

### License/Terms of Use:


## Use Case:

Developers, analysts, writers, and other external users use this skill to route text, files, images, URLs, and video-derived content through Fabric AI patterns for summarization, extraction, critique, writing, code review, and security analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fabric requests may send provided text, files, images, URLs, or video-derived content to external AI providers.

Mitigation: Redact sensitive data before use and prefer dry-run or approved local/private backends for confidential material.

Risk: Broad triggers could invoke Fabric patterns without an explicit privacy reminder.

Mitigation: Use the skill deliberately for Fabric requests and confirm the intended inputs before running commands that call external providers.

## Reference(s):

- [Fabric project homepage](https://github.com/danielmiessler/fabric)
- [Popular Fabric Patterns](references/popular-patterns.md)
- [Fabric Bridge on ClawHub](https://clawhub.ai/koriyoshi2041/skills/fabric-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and Fabric CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stream responses, write output files, copy results to the clipboard, or preview requests with dry-run mode depending on the Fabric CLI flags used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
