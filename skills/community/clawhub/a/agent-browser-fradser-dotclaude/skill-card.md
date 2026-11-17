## Description:

Browser automation command reference and usage patterns for web testing, form filling, screenshots, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsafe](https://clawhub.ai/user/jsafe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a browser automation reference for navigating pages, inspecting interactive elements, filling forms, capturing screenshots or PDFs, recording sessions, and extracting page data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to drive browser sessions, including sessions against real accounts or private sites.

Mitigation: Use test or low-privilege accounts where possible and review planned browser actions before running them against real services.

Risk: The skill documents saving and reusing authenticated browser state and inspecting cookies or storage.

Mitigation: Avoid saving authenticated state unless necessary; keep saved state files and recordings out of version control and delete them after use.

Risk: Browser recordings, screenshots, PDFs, cookies, and storage output can contain private or sensitive information.

Mitigation: Treat captured files and extracted browser data as sensitive artifacts and restrict where they are stored or shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jsafe/skills/agent-browser-fradser-dotclaude)
- [Publisher profile](https://clawhub.ai/user/jsafe)
- [Packaged skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command reference material, workflow examples, and usage patterns for agent-browser.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
