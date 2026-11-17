## Description:

ClawSkill helps an agent install, verify, configure, and run RTC token mining with hardware attestation and wallet management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottcjn](https://clawhub.ai/user/scottcjn)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use ClawSkill to set up and control RTC mining workflows, including verification checks, wallet configuration, foreground mining, optional service startup, status checks, logs, and uninstall commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact is about running a token miner, but the security evidence says the reviewed artifact does not include the miner code it asks users to install.

Mitigation: Use a pinned and reviewed release with included source files before installation; inspect the package contents and run the available dry-run and verification commands first.

Risk: The miner profiles hardware, sends attestations to a network service, and creates wallet or configuration files under the user's account.

Mitigation: Proceed only with explicit user consent, disclose the hardware and wallet data involved, and run it under a user account where those files and network calls are acceptable.

Risk: The security evidence notes incomplete or inconsistent install and service disclosures, including auto-restart service creation when service mode is used.

Mitigation: Avoid service mode unless the operator has reviewed the service creation behavior and can remove or disable the service during uninstall.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottcjn/skills/clawskill)
- [Publisher profile](https://clawhub.ai/user/scottcjn)
- [RustChain source code listed by skill](https://github.com/Scottcjn/Rustchain)
- [PyPI package listed by skill](https://pypi.org/project/clawskill/)
- [npm package listed by skill](https://www.npmjs.com/package/clawskill)
- [RustChain homepage listed by package metadata](https://rustchain.org)
- [Block explorer listed by skill](https://bulbous-bouffant.metalseed.net/explorer)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-facing commands and setup guidance; no structured machine output is promised by the skill card.]

## Skill Version(s):

1.2.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
