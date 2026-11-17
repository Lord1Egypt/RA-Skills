## Description:

Console Patrol helps agents scan web applications for browser console errors and warnings, with framework-specific diagnostics for React, Ant Design, and Element UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhzgao](https://clawhub.ai/user/zhzgao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to audit web app routes for console errors, warnings, and framework-specific issues, then report severity, location, and suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Route scanning can touch unintended pages or sensitive production data.

Mitigation: Run scans only against approved test routes or controlled environments, and avoid sensitive production data.

Risk: Screenshots may capture sensitive page content.

Mitigation: Use screenshot capture only when needed and review where generated files are stored.

Risk: The skill depends on installed browser automation tooling and package dependencies.

Mitigation: Install and run dependencies in a least-privileged sandbox, and pin or vet them before CI or shared-agent use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhzgao/skills/console-patrol)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports page counts, issue totals, severity counts, rule identifiers, affected locations, and suggested fixes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
