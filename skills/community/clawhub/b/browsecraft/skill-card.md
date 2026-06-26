## Description: <br>
Memory-oriented browser automation skill for repeatable web workflows, including login, extraction, bulk actions, form filling, screenshots, and checks across RoxyBrowser, Camoufox, and Chrome. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whjstc](https://clawhub.ai/user/whjstc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Browsecraft to run repeatable browser workflows through the browsecraft CLI, including page setup, stable interactions, extraction, screenshots, checks, and controlled bulk actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can act inside logged-in sessions and may perform high-impact web actions. <br>
Mitigation: Keep workflows scoped to user-approved tasks and confirm before purchases, deletions, submissions, public posts, or bulk changes. <br>
Risk: The skill depends on the external browsecraft-cli package and may connect to browser endpoints or use Roxy credentials. <br>
Mitigation: Install the CLI only from a trusted source, keep Roxy credentials local, avoid printing secrets, and connect only to trusted browser endpoints. <br>


## Reference(s): <br>
- [Browsecraft on ClawHub](https://clawhub.ai/whjstc/browsecraft) <br>
- [browsecraft-cli npm package](https://www.npmjs.com/package/browsecraft-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured objective, steps, result, failure reason, and next action.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browsecraft CLI commands and screenshot evidence when the workflow calls for them.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
