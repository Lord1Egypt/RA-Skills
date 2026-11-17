## Description:

Generates a business-opportunity skills report from ClawHub data, opens it in Chromium, and captures a full-page screenshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakliao](https://clawhub.ai/user/jakliao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users can use this skill to generate a categorized report of business-opportunity-related ClawHub skills and save a shareable full-page screenshot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted inputs may cause unintended system command execution or writes outside intended folders.

Mitigation: Run only in a restricted workspace with trusted arguments; validate slugs and filenames; replace shell-string execution with argument-array process calls.

Risk: Browser automation may expose sensitive sessions if it connects to a reused Chromium profile.

Mitigation: Use a clean ephemeral browser profile without sensitive sessions and close Chromium after capture.

Risk: Search-derived text is inserted into generated HTML.

Mitigation: Escape HTML output before rendering report content.

Risk: Dependency behavior may change across installs.

Mitigation: Install dependencies from an approved registry and update or pin them according to release policy.

## Reference(s):

- [Business Opportunity Screenshot on ClawHub](https://clawhub.ai/jakliao/skills/business-opportunity-screenshot)
- [Publisher profile: jakliao](https://clawhub.ai/user/jakliao)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code]

**Output Format:** [HTML report file, JPEG screenshot, and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script accepts an optional search query and output filename.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
