## Description:

CLI to read Coda.io documents and pages. List docs, list pages, read content in markdown/json/html.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auniik](https://clawhub.ai/user/auniik)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to discover Coda documents, inspect page hierarchy, and read page content in markdown, JSON, or HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires global installation of an external npm CLI.

Mitigation: Review the coda-ai npm package before installation and install only from the expected package source.

Risk: The setup flow can leave a Coda API token in a plaintext .env file.

Mitigation: Use the narrowest practical Coda token, restrict file permissions, delete the .env file after authentication, and rotate the token if it may have been exposed.

Risk: Stored credentials remain available after authentication.

Mitigation: Use coda-ai logout when access is no longer needed and confirm stored credential files are owner-only.

## Reference(s):

- [ClawHub coda.io Skill Page](https://clawhub.ai/auniik/skills/coda-ai)
- [coda-ai npm Package](https://www.npmjs.com/package/coda-ai)
- [coda-ai README](https://github.com/auniik/coda-ai#readme)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, configuration]

**Output Format:** [Markdown, JSON, HTML, table output, toon-formatted text, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the coda-ai CLI and CODA_API_TOKEN; authentication can store credentials in ~/.coda-ai/config.json.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
