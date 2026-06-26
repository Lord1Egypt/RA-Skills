## Description: <br>
Agent Browser CLI helps agents automate browser tasks such as check-ins, form filling, clicking, screenshots, and page-content capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Joshhuang123](https://clawhub.ai/user/Joshhuang123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when an agent needs to operate a browser through the agent-browser CLI for navigation, page inspection, clicking, form entry, screenshots, or scheduled check-in workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables browser automation that can click controls, fill forms, take screenshots, and interact with logged-in websites. <br>
Mitigation: Review pages before allowing clicks or submissions, avoid entering real credentials unless necessary, and be cautious with screenshots of logged-in pages. <br>
Risk: The skill may be used to create scheduled check-in scripts. <br>
Mitigation: Create scheduled scripts only intentionally, review their targets and actions, and close browser sessions when workflows finish. <br>
Risk: The artifact depends on installing the external agent-browser npm package globally. <br>
Mitigation: Install it only when the package source is trusted and the user accepts the risks of a global CLI dependency. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Joshhuang123/agent-browser-cli) <br>
- [Publisher profile](https://clawhub.ai/user/Joshhuang123) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on agent-browser CLI commands and browser automation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
