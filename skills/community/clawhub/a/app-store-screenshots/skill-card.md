## Description: <br>
App Store and Google Play screenshot creation with exact platform specs, gallery ordering, device mockups, and preview videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, product teams, and app marketers use this skill to plan and generate App Store and Google Play screenshot sets, device mockups, gallery ordering, captions, localization variants, and preview video prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quick start uses a curl-to-shell installer for a third-party CLI. <br>
Mitigation: Review the installer before running it, or use the documented manual checksum verification path. <br>
Risk: Prompts or uploaded images may include confidential app UI, customer data, secrets, or unreleased product details. <br>
Mitigation: Use only data approved for the target inference service and avoid submitting confidential or secret material. <br>
Risk: Generated screenshots and videos may misrepresent app behavior or include inaccurate platform requirements if used without review. <br>
Mitigation: Review outputs against the current app UI and store submission requirements before publishing. <br>


## Reference(s): <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>
- [ClawHub skill page](https://clawhub.ai/okaris/app-store-screenshots) <br>
- [Publisher profile](https://clawhub.ai/user/okaris) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and structured checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes platform dimensions, gallery ordering, caption guidance, preview video structure, localization advice, and infsh command examples.] <br>

## Skill Version(s): <br>
0.1.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
