## Description:

Double6 PPT CLI helps agents create, template-fill, inspect, verify, and repair editable native PPTX decks from Markdown, text, structured content, local authorized images, or existing presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[double6-ai](https://clawhub.ai/user/double6-ai)

### License/Terms of Use:

Apache License 2.0

## Use Case:

Developers and presentation-producing agents use this skill to build editable PPTX files, reuse existing PPTX templates, inspect deck structure, and perform bounded repair with verification receipts. It is intended for local user-provided content and does not parse PDF/DOCX input, search the web for images, create image-only slides, produce HTML slides, synthesize speech, or generate video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional OfficeCLI bootstrap path installs third-party dependencies under the user's account.

Mitigation: Run bootstrap only in a trusted environment and review or pin dependency integrity before using that install path.

Risk: The skill writes project and run files and may automate PowerPoint or LibreOffice.

Mitigation: Run it on user-authorized content in an appropriate workspace, review generated artifacts, and use the portable tier when native PowerPoint automation is unavailable or undesired.

## Reference(s):

- [Double6 PPT CLI on ClawHub](https://clawhub.ai/double6-ai/skills/double6-ppt-cli)
- [Double6 PPT CLI homepage](https://github.com/double6-ai/double6-skills/tree/main/skills/double6-ppt-cli)
- [Authoring contract](references/authoring-contract.md)
- [Delivery gates](references/delivery-gates.md)
- [Machine contracts](references/machine-contracts.md)
- [Repair policy](references/repair-policy.md)
- [Test report and verification tiers](references/test-report-and-verification-tiers.md)
- [PPT Master](https://github.com/hugohe3/ppt-master)
- [OfficeCLI](https://github.com/iOfficeAI/OfficeCLI)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON manifests, verification receipts, and PPTX file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write project and run files, bootstrap a pinned OfficeCLI runtime when authorized, and use PowerPoint or LibreOffice for verification depending on the selected tier.]

## Skill Version(s):

0.4.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
