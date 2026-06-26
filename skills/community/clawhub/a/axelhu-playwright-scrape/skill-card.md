## Description: <br>
Scrapes dynamic webpages using Playwright with system Chrome in simple or stealth mode, returning JSON with title, content, images, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to scrape JavaScript-rendered or login-gated webpages with Playwright and return structured page content for review or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GUI mode can reuse a logged-in Chrome profile through a persistent remote-debugging setup, giving the skill broad access to private browser sessions. <br>
Mitigation: Use an isolated Chrome profile or test account, approve each logged-in or sensitive URL before scraping, and close the debug Chrome instance after use. <br>
Risk: The documented Chrome wrapper and PATH change can make future Chrome launches inherit the remote-debugging behavior. <br>
Mitigation: Avoid the persistent wrapper and PATH change when possible; start a dedicated debug Chrome instance explicitly only for approved scraping tasks. <br>


## Reference(s): <br>
- [Skill usage documentation](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/axelhu-playwright-scrape) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, shell commands, guidance] <br>
**Output Format:** [JSON scrape result plus Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scrape JSON includes URL, mode, title, content capped at 15000 characters, image URLs, links, and load time.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata; artifact _meta.json reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
