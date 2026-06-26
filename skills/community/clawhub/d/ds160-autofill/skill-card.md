## Description: <br>
Automate filling of US nonimmigrant visa DS-160 forms using CDP for element location, CSV data source for user information, LLM assistance for complex cases (captcha, missing elements), and session persistence for resume capability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clulessboy](https://clawhub.ai/user/clulessboy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to help fill or resume a US DS-160 nonimmigrant visa application from CSV data while preserving progress between sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive visa, identity, travel, and recovery information. <br>
Mitigation: Keep the workspace private, review each page before continuing, and delete or protect ds160-user-info.csv and ds160-session.json after use. <br>
Risk: Screenshots or personal fields may be sent to external AI tools for captcha reading, translation, or troubleshooting. <br>
Mitigation: Use those AI-assisted paths only when you explicitly accept that disclosure. <br>
Risk: Generated security answers and automated browser form filling can create incorrect or hard-to-recover application state. <br>
Mitigation: Do not rely on generated security answers, verify the saved application details, and review the form before advancing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clulessboy/ds160-autofill) <br>
- [DS-160 application site](https://ceac.state.gov/genniv/) <br>
- [DS-160 element mappings](references/ds160-elements.yaml) <br>
- [DS-160 user data CSV template](references/ds160-user-info.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets, browser automation steps, CSV data, and JSON session state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces progress reports, prompts for missing data, and uses workspace files for DS-160 CSV data and session persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
