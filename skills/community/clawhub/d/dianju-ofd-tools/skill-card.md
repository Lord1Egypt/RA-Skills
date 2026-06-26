## Description: <br>
Convert local PDF and OFD files to each other and extract text content from OFD files with temporary download links provided. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stmmer](https://clawhub.ai/user/stmmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to convert local PDF and OFD documents through a configured dianju-ofd-tools service and extract text from OFD files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files, temporary download links, logs, and APP_KEY credentials may be exposed to the configured conversion service. <br>
Mitigation: Verify the dianju-ofd-tools npm package and API endpoint operator, use a secured endpoint, and avoid processing confidential PDFs or OFDs unless the service and credential handling are trusted. <br>
Risk: Converted files or extracted content may be incomplete, invalid, or unavailable after temporary links expire. <br>
Mitigation: Check service errors, download converted files promptly, and verify generated file integrity before sharing or using outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stmmer/dianju-ofd-tools) <br>
- [Publisher profile](https://clawhub.ai/user/stmmer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; conversion calls return temporary URLs and extraction returns JSON arrays.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APP_ID, APP_KEY, and API_URL configuration and processes local PDF/OFD files through the configured conversion service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
