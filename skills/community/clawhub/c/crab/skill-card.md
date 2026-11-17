## Description:

Crab Catch is a Web3 research skill that collects and organizes project data and potential risks from social media, websites, code, and on-chain sources, then produces a research report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notevende](https://clawhub.ai/user/notevende)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external Web3 researchers use this skill to investigate projects by cross-checking social, website, repository, and on-chain evidence and producing a concise risk-oriented report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill makes broad host, browser, API, credential, and persistence changes.

Mitigation: Review the skill before deployment and run it in a disposable or sandboxed environment where global package installation, browser automation, API calls, and local file writes are acceptable.

Risk: Research targets and prompts may be sent to the Crab service and upstream providers.

Mitigation: Avoid sensitive or private investigation targets unless the service and upstream data handling are acceptable for the use case.

Risk: The skill can store generated API credentials and reports under the user's home directory.

Mitigation: Rotate or delete ~/.config/crab/credentials.json and remove ~/.crab-catch/reports when the investigation is complete.

## Reference(s):

- [Crab ClawHub Skill Page](https://clawhub.ai/notevende/skills/crab)
- [Crab API Explorer Documentation](artifact/API_EXPLORER.md)
- [Crab Catch Architecture](artifact/ARCHITECTURE.md)
- [Crab Catch Report Template](artifact/REPORT_TEMPLATE.md)
- [Crab API Service](https://crab-skill.opsat.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research report with citations, tables, and concise risk findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local report files and uses signed API requests for Crab service calls.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact metadata lists 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
