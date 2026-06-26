## Description: <br>
Provides a complete AI-run company setup playbook, including memory system, safety rails, payment integration, and multi-platform launch in 72 hours. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperzinou](https://clawhub.ai/user/casperzinou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders, builders, and operators use this skill to have an agent plan and assemble an AI-operated company launch, including product files, memory structure, payment setup, and launch checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive payment setup and purchase-related workflows. <br>
Mitigation: Require manual approval for every payment action and use test or least-privilege payment credentials until the workflow is reviewed. <br>
Risk: The skill may handle secrets while creating environment templates, memory files, and launch assets. <br>
Mitigation: Keep credentials out of memory files and generated documentation; provide secrets only through scoped environment variables or a secrets manager. <br>
Risk: The skill describes platform submissions, social posting, and companion-skill installation. <br>
Mitigation: Review each external submission, social post, and companion skill before enabling or publishing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/casperzinou/ai-company-builder) <br>
- [TalonForge store](https://www.talonforge.xyz/store) <br>
- [TalonForge GitHub profile](https://github.com/TalonForgeHQ) <br>
- [TalonForge X profile](https://x.com/TalonForgeHQ) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown instructions, generated project files, configuration templates, and launch checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve payment, credential, platform-submission, social-posting, and companion-skill installation steps that require human approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
