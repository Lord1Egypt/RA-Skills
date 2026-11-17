## Description:

Automates academic-library download workflows for books, articles, DOIs, and URLs across supported library and publishing platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare academic-library download workflows by title, author, DOI, URL, or batch list. It is intended for use only where the user has authorized institutional access and permission to download the requested materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to configure institutional credentials for library access.

Mitigation: Use credentials only when institutional policy permits this workflow, and prefer an isolated environment with only the access needed for the specific task.

Risk: Server security evidence reports incomplete authentication behavior and an exploitable Playwright helper if used.

Mitigation: Review carefully before installing, avoid invoking or integrating the Playwright helper until the injection issue is fixed, and pin dependencies in an isolated environment.

Risk: Download behavior may require manual completion and may not reliably fetch requested content.

Mitigation: Treat output as workflow assistance, verify any downloaded or suggested material manually, and comply with applicable license and access terms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/anne-library-downloader)
- [Crossref Works API](https://api.crossref.org/works)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-style command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print platform detection, DOI lookup results, manual-download status, and setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
