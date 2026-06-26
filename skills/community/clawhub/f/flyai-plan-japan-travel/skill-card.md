## Description: <br>
Plan complete Japan trips with FlyAI CLI data for flights, hotels, attractions, visa questions, JR Pass context, and multi-city itineraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-planning agents use this skill to answer Japan travel requests and build CLI-sourced itineraries with booking links, prices, hotels, flights, attractions, and fallback guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct installation of an unpinned global CLI, including a sudo fallback. <br>
Mitigation: Review the CLI package before installation, install without sudo where possible, and pin or approve versions according to local policy. <br>
Risk: Travel planning prompts and internal logs may include sensitive personal travel details. <br>
Mitigation: Avoid entering passport numbers, payment details, or other sensitive personal data into prompts or CLI workflows. <br>
Risk: The security verdict is suspicious and requires review before installation. <br>
Mitigation: Use the skill only if the FlyAI CLI and Fliggy data flow are trusted for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/flyai-plan-japan-travel) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Fallbacks](artifact/references/fallbacks.md) <br>
- [Playbooks](artifact/references/playbooks.md) <br>
- [Runbook](artifact/references/runbook.md) <br>
- [Templates](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLI output as the required source for bookable travel items and prices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
