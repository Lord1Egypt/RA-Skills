## Description: <br>
Capture full-page screenshots of websites with lazy-load support by using Puppeteer to open, scroll, and save the requested page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifelooploop](https://clawhub.ai/user/lifelooploop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need visual documentation of a webpage, including long pages and lazy-loaded content. It is intended for user-requested public or otherwise appropriate URLs and saves the resulting screenshot locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The headless browser opens the URLs requested by the user and may disclose normal browsing metadata to the target site. <br>
Mitigation: Use the skill only for URLs the user intends to visit and capture; avoid sensitive internal, confidential, or authenticated pages. <br>
Risk: Screenshots can capture page contents locally, including information visible in the loaded page. <br>
Mitigation: Store screenshots only in intended workspace locations and review them before sharing or publishing. <br>
Risk: The requested output path may overwrite an existing local screenshot file. <br>
Mitigation: Choose explicit, non-conflicting output paths for each capture. <br>
Risk: The skill depends on npm and Puppeteer packages plus a headless browser runtime. <br>
Mitigation: Install dependencies only in an environment where these packages are acceptable and review dependency policy before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lifelooploop/full-webpage-screenshot) <br>
- [Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; script execution returns JSON and writes a PNG screenshot file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports viewport and wait timing configuration through environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
