## Description: <br>
Self-learn your decision patterns to safely build its own decision-making over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to make consequential branching decisions more safely by checking structured local decision memory, matching required components, and asking before high-impact choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps a local decision log that can influence future recommendations. <br>
Mitigation: Review the contents of ~/decide/ regularly and avoid saving secrets or third-party private data there. <br>
Risk: Setup may suggest edits to AGENTS or SOUL steering files. <br>
Mitigation: Approve only after checking the exact snippet; the skill instructions require explicit approval before writes. <br>
Risk: A stale or overbroad stored decision could cause an agent to reuse guidance in the wrong context. <br>
Mitigation: Require material component matching, check domain exceptions, and ask first for money, production, publishing, deletion, contracts, or long-term architecture decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/decide) <br>
- [Skill homepage](https://clawic.com/skills/decide) <br>
- [Setup guide](setup.md) <br>
- [Decision components](components.md) <br>
- [Confidence calibration](confidence.md) <br>
- [Exceptions and always-ask cases](exceptions.md) <br>
- [Memory template](memory-template.md) <br>
- [Migration guide](migration.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local decision-memory structure and asks for approval before suggested workspace steering edits.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
