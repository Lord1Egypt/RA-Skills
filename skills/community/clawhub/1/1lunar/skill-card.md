## Description: <br>
Helps users query Chinese lunar calendar dates by converting Gregorian dates to lunar year, month, day, zodiac, solar terms, and common holiday dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mysunsi](https://clawhub.ai/user/mysunsi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Chinese lunar calendar questions, including today's lunar date, Gregorian-to-lunar conversion, zodiac details, solar terms, and common festival dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and executes the chinese-lunar-calendar npm package, so dependency drift or package compromise could affect reproducibility or results. <br>
Mitigation: Pin or review the chinese-lunar-calendar package before use when stronger supply-chain assurance is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mysunsi/1lunar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash code blocks and plain-text date results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a disclosed npm dependency for lunar calendar conversion examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
