## Description: <br>
Helps agents look up academic items by title, author, DOI, URL, or list and generate download-oriented commands, metadata, and manual retrieval guidance for library sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neckr0ik](https://clawhub.ai/user/neckr0ik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare academic-library download workflows, extract or look up DOIs, identify supported library platforms, and produce shell commands or guidance for single-item and batch retrieval. Users should treat credentialed and automated download behavior as requiring review because the server security evidence marks the release as suspicious. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to prepare institutional library credentials while the server security summary says the implementation overstates automation and ships incomplete or unsafe helper behavior. <br>
Mitigation: Review before installing, avoid providing institutional credentials unless the author documents exactly how they are used, declares them in metadata, and ships the missing authentication components. <br>
Risk: Automated or batch downloads may conflict with library, publisher, or institutional rules. <br>
Mitigation: Check applicable library and institutional policies before attempting automated or batch downloads. <br>
Risk: URL-based workflows can expose users to untrusted academic or library-looking links. <br>
Mitigation: Use trusted URLs only and inspect the target platform before running download workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/neckr0ik/anne-library-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON-like command output with inline shell commands and environment variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference credentials, library URLs, DOI values, input lists, output directories, and manual follow-up steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
