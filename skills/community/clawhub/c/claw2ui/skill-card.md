## Description: <br>
Generate interactive web pages such as dashboards, charts, tables, reports, and status pages from TypeScript DSL specs, then publish them to a public URL after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xsegfaulted](https://clawhub.ai/user/0xsegfaulted) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to turn data or page specifications into interactive web dashboards, reports, charts, and tables. It is intended for workflows where the user explicitly approves publishing the generated page to a public URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Published pages are accessible through a public URL and may expose sensitive data if included in page content. <br>
Mitigation: Review the exact content before publishing, exclude secrets, credentials, PII, internal endpoints, and regulated data, and use TTL for temporary or sensitive reports. <br>
Risk: The skill sends page content to a Claw2UI server API and stores connection credentials locally. <br>
Mitigation: Use only trusted Claw2UI servers, protect the local ~/.claw2ui.json token file, and self-host when public hosting is not appropriate. <br>
Risk: Self-hosted backup can upload page data and token metadata to a Hugging Face Dataset when backup variables are enabled. <br>
Mitigation: Enable backup only intentionally, keep backup datasets private, and avoid backing up sensitive page content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xsegfaulted/claw2ui) <br>
- [Claw2UI GitHub repository](https://github.com/0xsegfaulted/claw2ui) <br>
- [Claw2UI npm package](https://www.npmjs.com/package/claw2ui) <br>
- [Claw2UI Hugging Face Space](https://huggingface.co/spaces/0xsegfaulted/claw2ui) <br>
- [Self-hosting guide](ref/self-hosting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript DSL examples and shell commands; published pages return a public URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates temporary TypeScript spec files, writes Claw2UI connection configuration, and publishes only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
