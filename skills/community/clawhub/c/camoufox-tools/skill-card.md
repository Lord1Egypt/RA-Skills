## Description: <br>
Simplified CLI tools for Camoufox anti-detection browser automation that provide fox-open, fox-scrape, fox-eval, fox-close, and fox-bilibili-stats commands for web scraping and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdAstraAbyssoque](https://clawhub.ai/user/AdAstraAbyssoque) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation users use this skill to install and run simplified shell commands for Camoufox browser automation, page scraping, JavaScript evaluation, and Bilibili video statistic collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anti-detection browser automation can be misused for unauthorized scraping or activity that violates target site policies. <br>
Mitigation: Use the commands only on sites and accounts where automation is authorized, and confirm that the workflow complies with applicable site terms and organizational policy. <br>
Risk: fox-eval runs JavaScript in the current browser page and can expose data from sensitive logged-in sessions. <br>
Mitigation: Run only reviewed JavaScript snippets, avoid sensitive sessions, and close the browser after the task is complete. <br>
Risk: The installer persistently modifies the user's shell startup file to add the skill's bin directory to PATH. <br>
Mitigation: Review the shell profile change during installation and remove the PATH entry when uninstalling or disabling the skill. <br>


## Reference(s): <br>
- [Camoufox Tools on ClawHub](https://clawhub.ai/AdAstraAbyssoque/camoufox-tools) <br>
- [AdAstraAbyssoque publisher profile](https://clawhub.ai/user/AdAstraAbyssoque) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Install script](artifact/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires openclaw CLI, Camoufox, and the agent-browser extension; commands may open browser sessions, scrape page content, or evaluate JavaScript in the current page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
