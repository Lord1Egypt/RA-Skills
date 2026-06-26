## Description: <br>
Config Review Flow guides agents through scoped configuration reviews with a complete item inventory, item-by-item confirmations, a workspace tracking file, and a final pre-apply confirmation gate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silronin](https://clawhub.ai/user/silronin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review configuration changes before applying them. It helps inventory settings, record decisions in a configuring/ file, and prevent real changes until final explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local configuration files and environment details during inventory. <br>
Mitigation: Install it only in workspaces where that inspection is appropriate, and review the final plan carefully before giving explicit permission to apply real configuration changes. <br>
Risk: Configuration recommendations or recorded decisions could be wrong or incomplete if sources are missing or conflicting. <br>
Mitigation: Require a source-backed inventory, mark unknowns explicitly, resolve conflicts before continuing, and use the mandatory final confirmation gate before applying changes. <br>


## Reference(s): <br>
- [Config Review Flow on ClawHub](https://clawhub.ai/silronin/config-review-flow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration guidance, shell commands] <br>
**Output Format:** [Markdown tracking file and conversational review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates a workspace configuring/ markdown file during review; no real configuration changes before final explicit apply confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
