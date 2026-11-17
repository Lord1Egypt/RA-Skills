## Description:

Teaches ADA how to perform file downloads using the browser tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pbseiya](https://clawhub.ai/user/pbseiya)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to download files from webpages through the browser tool, including standard link or button downloads and JavaScript-triggered interactions. It guides the agent to save requested files to the configured downloads directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded files may originate from untrusted webpages.

Mitigation: Review the source site and filename before downloading, and do not open or execute downloaded files unless the origin is trusted.

Risk: JavaScript-triggered clicks can download an unintended file if the selector targets the wrong element.

Mitigation: Confirm the target selector or browser reference and destination path before triggering the download.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pbseiya/skills/browser-download)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openclaw CLI and a correctly configured relayPort; saves requested downloads under /mnt/storage/ada_projects/downloads/.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
