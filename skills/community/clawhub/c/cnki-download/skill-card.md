## Description: <br>
Searches CNKI, applies source/year filters or sorting, and guides batch PDF downloads through a Playwright and Microsoft Edge workflow with reusable local login state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lfp1979](https://clawhub.ai/user/lfp1979) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and researchers use this skill to search CNKI, configure filters or sorting, handle first-run login, and download a requested number of academic paper PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a CNKI entry URL and browser login state locally for reuse. <br>
Mitigation: Review or delete scripts/user_config.json and scripts/browser_data when saved URL or session reuse is not desired. <br>
Risk: An automated Edge session can access CNKI using an institution or personal login. <br>
Mitigation: Run only in a trusted workspace and avoid setting CNKI_USER_DATA_DIR to a shared browser profile unless session reuse is intentional. <br>


## Reference(s): <br>
- [Config JSON Schema](references/config-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/lfp1979/skills/cnki-download) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON config files and trigger a Playwright/Edge process that downloads PDFs to scripts/download/.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
