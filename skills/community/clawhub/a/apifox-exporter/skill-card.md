## Description:

Apifox Exporter automates exporting OpenAPI JSON from Apifox and turns it into organized API documentation grouped by module.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzy05651666](https://clawhub.ai/user/zzy05651666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API teams use this skill to refresh Apifox API documentation by exporting a selected team/project and formatting the resulting OpenAPI data into a readable document. It also supports a fallback flow where the user supplies an exported Apifox JSON file for formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate an authenticated Apifox export and may export the wrong or sensitive project data if target selection is broad or ambiguous.

Mitigation: Use it only in accounts where exporting all visible Apifox project data is acceptable, and verify the selected team and project before export.

Risk: Saved browser profiles, downloaded source JSON, generated documents, and debug screenshots may retain sensitive API data locally.

Mitigation: Clear the saved chrome-profile, source JSON, generated desktop document, and debug screenshots after use when they contain sensitive information.

Risk: The fallback flow may process an unintended JSON file if the expected source location contains stale or incorrect Apifox exports.

Mitigation: Before using fallback mode, explicitly place the intended Apifox JSON at the expected source path and remove stale source files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zzy05651666/skills/apifox-exporter)
- [Publisher Profile](https://clawhub.ai/user/zzy05651666)
- [Apifox Web App](https://app.apifox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text API documentation with structured sections and JSON examples; agent responses may include Markdown instructions and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes formatted API documentation to the user's Desktop and stores the source OpenAPI JSON in the OpenClaw workspace.]

## Skill Version(s):

2.0.0 (source: server release evidence, skill.yaml, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
