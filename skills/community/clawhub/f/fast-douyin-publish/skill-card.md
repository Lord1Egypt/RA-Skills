## Description: <br>
Fast Douyin Publish helps an agent upload videos to Douyin with QR-code login, title and tag handling, and local publishing logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeadLining](https://clawhub.ai/user/DeadLining) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and automation developers use this skill to publish prepared video files to a live Douyin account from an agent workflow, including titles, tags, and optional descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable login sessions locally and can post publicly to a live Douyin account. <br>
Mitigation: Install only from a trusted publisher, protect or delete saved cookies after use, avoid committing the config directory, and review the target account, video, title, tags, and description before running. <br>
Risk: Headless operation can publish content without an obvious final visual check. <br>
Mitigation: Run with a visible browser for first use or sensitive posts, and reserve headless mode for reviewed, repeatable workflows. <br>
Risk: The bundled account configuration includes unexplained credential fields for platforms outside the Douyin workflow. <br>
Mitigation: Remove unrelated platform entries from config/accounts.json before use and keep only the Douyin configuration required for the intended workflow. <br>


## Reference(s): <br>
- [Fast Douyin Publish on ClawHub](https://clawhub.ai/DeadLining/fast-douyin-publish) <br>
- [DeadLining publisher profile](https://clawhub.ai/user/DeadLining) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser automation instructions and publishing status; the publishing script may create local cookies, account configuration, debug screenshots, and publish logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
