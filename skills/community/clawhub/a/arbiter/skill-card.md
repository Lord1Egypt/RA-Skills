## Description: <br>
Push decisions to Arbiter Zebu for async human review when human input is needed on plans, architectural choices, or approvals before proceeding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5hanth](https://clawhub.ai/user/5hanth) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Arbiter to send structured decision plans to a human reviewer, track review status, and retrieve completed answers before continuing blocked work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted agent name may cause review files to be written outside the intended Arbiter queue directory. <br>
Mitigation: Use trusted agent and session identifiers only, and prefer a fixed release that sanitizes agent values and verifies writes remain under ~/.arbiter/queue/pending. <br>
Risk: Decision content is persisted in local queue files and may be visible to the Arbiter bot and human review channel. <br>
Mitigation: Do not include secrets, credentials, or sensitive internal data in decision titles, context, options, or answers. <br>
Risk: The skill depends on local Arbiter queue files and a running Arbiter Zebu workflow. <br>
Mitigation: Confirm the Arbiter Zebu bot and ~/.arbiter/queue directories are configured before relying on the skill for blocked work. <br>


## Reference(s): <br>
- [Arbiter ClawHub Release](https://clawhub.ai/5hanth/arbiter) <br>
- [Arbiter Zebu Bot](https://github.com/5hanth/arbiter-zebu) <br>
- [Arbiter Zebu Architecture](https://github.com/5hanth/arbiter-zebu/blob/main/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON CLI responses and Markdown queue files with shell-command usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes decision plans under ~/.arbiter/queue/pending and reads pending or completed queue files.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
