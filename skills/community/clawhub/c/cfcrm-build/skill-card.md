## Description: <br>
Multi-version ContactFlowCRM planning skill that helps agents review CFCRM status, version plans, launch checklists, next actions, and roadmap summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vega6dev](https://clawhub.ai/user/vega6dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, builders, and project agents use this skill to plan ContactFlowCRM delivery across v1 through v5, inspect version-specific deliverables, run launch checklists, and decide the next build action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CFCRM progress may be stored in project memory when the host environment supports it, which can affect who can view or update roadmap status. <br>
Mitigation: Confirm the intended project memory location and access expectations before using checklist status updates. <br>
Risk: Generic roadmap or sprint discussions could activate CFCRM planning behavior unexpectedly. <br>
Mitigation: Use explicit /cfcrm-build commands when possible, and ask for confirmation before applying progress changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vega6dev/cfcrm-build) <br>
- [ContactFlowCRM](https://contactflowcrm.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with command-style responses, tables, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize roadmap status, version plans, checklists, next actions, and completion updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
