## Description:

Generates Mermaid diagrams from natural-language descriptions, including flowcharts, sequence diagrams, architecture diagrams, ER diagrams, class diagrams, and state diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, product managers, and automation teams use this skill to turn natural-language descriptions into compact Mermaid or ASCII diagrams for documentation, architecture review, database design, workflow clarification, and teaching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests read and command access while advertising broader data, file, API, network, and retrieval behavior than its Mermaid diagram purpose requires.

Mitigation: Review before installing and use it only for Mermaid diagram creation or explicitly requested PNG export; avoid unrelated data analysis, API calls, broad file processing, or network diagnostics unless intentionally approved.

Risk: PNG export uses command execution through Mermaid CLI.

Mitigation: Run only the documented Mermaid CLI command with trusted diagram inputs and avoid concatenating untrusted user input into shell arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/diagram-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown with Mermaid code blocks, optional ASCII sketches, and optional PNG files exported through Mermaid CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free version supports one diagram per session, Mermaid and ASCII output, and PNG export when Node.js and Mermaid CLI are available.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
