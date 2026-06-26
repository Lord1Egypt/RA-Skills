## Description: <br>
Launches the bundled Ashen Era CLI build, plays one real run through the live prompts, and writes a first-person gameplay report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssochi](https://clawhub.ai/user/ssochi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and evaluators use this skill when they want an agent to run Ashen Era through the real CLI flow, capture what happened, and return a concrete first-person play report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local native game executable from bundled release archives. <br>
Mitigation: Install only from a trusted publisher and run it in an environment where local game execution is acceptable. <br>
Risk: The reviewed artifact set did not include the referenced release archives, so the actual game binary payload was not validated in this evidence package. <br>
Mitigation: Review or scan the release archives before use when binary provenance matters for your environment. <br>


## Reference(s): <br>
- [CLI Surface](references/cli-surface.md) <br>
- [Report Contract](references/report-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown narrative report with launch details and gameplay recap] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the selected executable target, launch command, class, seed, locale, final result, major decisions, combat actions, and retrospective for the completed run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
