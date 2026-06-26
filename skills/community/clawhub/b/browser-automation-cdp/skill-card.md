## Description: <br>
Enables an agent to control a user's logged-in Edge or Chrome browser through Chrome DevTools Protocol for navigation, page interaction, JavaScript evaluation, DOM extraction, and screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hunling233](https://clawhub.ai/user/hunling233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when ordinary page fetching is insufficient, such as JavaScript-rendered pages, authenticated browser sessions, forms, scrolling workflows, screenshots, and DOM-based data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over logged-in browser sessions. <br>
Mitigation: Use a dedicated automation profile, sign in only to accounts needed for the task, close the debug-enabled browser afterward, and manually approve sensitive submissions, account changes, purchases, downloads, and private-page access. <br>
Risk: Session and cookie handling guidance is under-scoped and may expose private browser state. <br>
Mitigation: Avoid cookie-database workflows and limit automation to pages and accounts that are appropriate for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hunling233/browser-automation-cdp) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Browser Automation CLI Reference](artifact/REFERENCE.md) <br>
- [Browser Automation Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; browser operations may return JSON data, PNG screenshots, or base64 screenshot data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Edge or Chrome with remote debugging enabled and a local Node.js WebSocket dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
