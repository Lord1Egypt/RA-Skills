## Description: <br>
Agent Vision Scraper packages a Docker-based browser automation tool for agents to navigate websites, scrape data, and use vision to handle graphical CAPTCHA challenges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tedtalk](https://clawhub.ai/user/Tedtalk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers can use this skill to run browser-based web automation and data extraction tasks in a containerized environment. It is intended only for authorized workflows on systems the user owns or has explicit permission to test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates stealth web scraping, CAPTCHA handling, and credentialed login flows. <br>
Mitigation: Install and run it only for authorized testing or automation on systems you own or have explicit permission to test; do not use it to bypass third-party anti-bot protections or CAPTCHAs. <br>
Risk: Runtime configuration may expose credentials, API keys, screenshots, or browser sessions. <br>
Mitigation: Avoid passing real credentials in command arguments, restrict API keys, assume screenshots may leave the machine, and secure or disable VNC rather than exposing port 5900 without a password. <br>
Risk: The release evidence notes that the Dockerfile should be inspected or obtained before running the container. <br>
Mitigation: Review the container build inputs before execution and run the skill in an isolated environment with only the permissions required for the authorized task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Tedtalk/agent-vision-scraper) <br>
- [Artifact README](artifact/README.md) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Tedtalk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console text with shell commands, configuration snippets, and extracted task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit browser automation results, extracted data, status logs, and setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
