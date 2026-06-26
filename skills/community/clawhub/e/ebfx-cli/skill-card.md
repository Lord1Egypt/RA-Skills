## Description: <br>
Helps agents use the ebfx CLI to query EBFX financial platform data, quotes, dashboard status, deal profit, education payment calculations, supported currencies, and payout methods from a terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renxqoo](https://clawhub.ai/user/renxqoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to access EBFX operational or financial information through the ebfx CLI, including authentication status, dashboard pending items, deal profit, education payment quotes, currency support, and payout methods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to access protected EBFX financial dashboard and profit data. <br>
Mitigation: Require clear EBFX-specific user intent before login, dashboard, or profit queries, and confirm sender binding and token status before protected commands. <br>
Risk: Sender IDs and token files can expose access to user-scoped EBFX data if the runtime environment is not controlled. <br>
Mitigation: Run the skill only where sender IDs and token files are access-controlled, and rely on the injected OPENCLAW_SENDER_ID unless an explicit override is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/renxqoo/ebfx-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline bash commands; the referenced CLI commands normally return JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Protected queries should be gated on sender binding and token status before running business commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
