## Description: <br>
Actionbook helps agents interact with websites through browser automation, web scraping, screenshots, form filling, UI testing, monitoring, and pre-verified page actions with tested selectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adcentury](https://clawhub.ai/user/adcentury) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and engineers use Actionbook to find page action manuals, retrieve selectors, and drive browser workflows such as navigation, form filling, screenshots, scraping, monitoring, and UI tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate broad browser actions across logged-in websites, including forms, messages, posts, settings, cookies, and JavaScript execution. <br>
Mitigation: Use dedicated low-privilege browser profiles and require explicit confirmation before submitting forms, sending messages, posting content, booking services, changing settings, modifying cookies, or running JavaScript. <br>
Risk: Persistent profiles and cookies can preserve access to authenticated accounts. <br>
Mitigation: Protect profile directories and tokens, avoid sensitive financial or personal accounts, and clear cookies or delete profiles when no longer needed. <br>
Risk: Stored selectors can become outdated as websites change. <br>
Mitigation: Validate selectors with current Actionbook output or a live browser snapshot before performing consequential actions. <br>


## Reference(s): <br>
- [Actionbook ClawHub Page](https://clawhub.ai/adcentury/actionbook) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Actionbook Command Reference](references/command-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples, selectors, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct browser actions that create screenshots or PDFs and may use persistent browser profiles when requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
