## Description: <br>
Automates product search and add-to-cart, favorite, or interest-marker actions across Taobao, JD, Pinduoduo, and Xianyu through Brave Browser CDP, stopping before checkout or payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayf3](https://clawhub.ai/user/mayf3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate logged-in shopping-site browsing tasks that place items in carts, save favorites, or mark interest while leaving purchase decisions and payment to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify live carts, favorites, interest markers, and possibly chats in logged-in third-party accounts. <br>
Mitigation: Use only with accounts where those changes are acceptable, require confirmation before each live action, and prefer a dry-run or manual review step before changing an account. <br>
Risk: Browser automation against logged-in shopping sessions may expose session tokens or account state in command output, screenshots, or logs. <br>
Mitigation: Avoid sharing or logging session tokens, keep screenshots and page text captures limited to what is needed for verification, and review outputs before retaining or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mayf3/add-to-cart) <br>
- [Platform guides](references/platform-guides.md) <br>
- [Platform selectors](references/platform-selectors.md) <br>
- [Experience log](references/experience-log.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and browser automation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running Brave Browser CDP session and a compatible brave-browser-agent skill; outputs should be reviewed before live account changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
